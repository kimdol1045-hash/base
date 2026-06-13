#!/usr/bin/env python3
"""Obsidian 자동 동기화 — YAML 스킬 → Obsidian 노트 + MOC + Graph RAG.md 생성."""

from __future__ import annotations

import argparse
import hashlib
import json
import logging
import os
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

import yaml

# packages/ 경로를 import 가능하도록 추가
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_PROJECT_ROOT))

logger = logging.getLogger(__name__)

SYNC_STATE_FILE = Path(__file__).resolve().parent.parent / ".obsidian-sync-state.json"


def _file_hash(path: Path) -> str:
    """Compute MD5 hash of file content."""
    return hashlib.md5(path.read_bytes()).hexdigest()


def _load_sync_state() -> dict:
    """Load sync state from JSON file."""
    if SYNC_STATE_FILE.exists():
        return json.loads(SYNC_STATE_FILE.read_text(encoding="utf-8"))
    return {}


def _save_sync_state(state: dict) -> None:
    """Save sync state to JSON file."""
    SYNC_STATE_FILE.write_text(
        json.dumps(state, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


# ─── Skill / Edge 로딩 (openai 의존성 없이 직접 로드) ───

def _content_hash(content: str) -> str:
    return hashlib.sha256(content.encode()).hexdigest()[:16]


def load_all_skills(skill_dir: str | None = None) -> list[dict[str, Any]]:
    """모든 YAML 스킬 파일 로드 (embeddings.py와 동일 로직, openai 미필요)."""
    base_dir = Path(skill_dir or "./skills")
    skills: list[dict[str, Any]] = []
    for yaml_path in sorted(base_dir.rglob("*.yaml")):
        try:
            with open(yaml_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
            if not data or "id" not in data:
                continue
            content = data.get("content", "")
            skills.append({
                "id": data["id"],
                "domain": data.get("domain", ""),
                "type": data.get("type", ""),
                "content": content,
                "tags": data.get("tags", []),
                "token_estimate": data.get("token_estimate", 400),
                "theory": data.get("theory", ""),
                "content_hash": _content_hash(content),
            })
        except Exception as e:
            logger.error("Failed to load %s: %s", yaml_path, e)
    logger.info("Loaded %d skills from %s", len(skills), base_dir)
    return skills


def _try_extract_all_edges() -> list[Any]:
    """extract_all_edges() 호출 시도. selector 의존성 없으면 빈 리스트 반환."""
    try:
        from packages.graph_rag.edge_extractor import extract_all_edges
        return extract_all_edges()
    except Exception as e:
        logger.warning("Edge extraction unavailable (continuing without edges): %s", e)
        return []


# ─── Brain Region 매핑 ───

BRAIN_REGIONS: dict[str, str] = {
    "development.backend": "BRAINSTEM",
    "development.database": "BRAINSTEM",
    "development.frontend": "CORTEX",
    "development.security": "CORTEX",
    "development.performance": "CORTEX",
    "development.ai": "CORTEX",
    "development.infra": "CEREBELLUM",
    "design": "CORTEX",
    "design.ux-psychology": "LIMBIC",
    "planning": "PREFRONTAL",
    "planning.business": "PREFRONTAL",
    "planning.project-mgmt": "PREFRONTAL",
    "marketing": "SENSORS",
    "marketing.persuasion": "LIMBIC",
    "marketing.seo": "SENSORS",
    "marketing.growth": "SENSORS",
    "analytics": "THALAMUS",
    "content": "WERNICKE",
    "qa": "CEREBELLUM",
    "meta": "PREFRONTAL",
}


def resolve_brain_region(domain: str) -> str:
    """도메인 문자열에서 brain region 결정. 가장 구체적인 매핑을 우선 사용."""
    if domain in BRAIN_REGIONS:
        return BRAIN_REGIONS[domain]
    # 상위 도메인으로 폴백 (e.g., "development.backend" → "development")
    parts = domain.split(".")
    while parts:
        candidate = ".".join(parts)
        if candidate in BRAIN_REGIONS:
            return BRAIN_REGIONS[candidate]
        parts.pop()
    return "UNKNOWN"


# ─── Edge 인덱스 빌드 ───

def build_edge_index(edges: list[Any]) -> dict[str, list[dict[str, str]]]:
    """skill_id → [{"target": ..., "type": ..., "weight": ...}] 양방향 인덱스."""
    index: dict[str, list[dict[str, str]]] = defaultdict(list)
    for edge in edges:
        index[edge.source_id].append({
            "target": edge.target_id,
            "type": edge.edge_type.value,
            "weight": str(edge.weight),
        })
        index[edge.target_id].append({
            "target": edge.source_id,
            "type": edge.edge_type.value,
            "weight": str(edge.weight),
        })
    return dict(index)


# ─── Skill → Obsidian Note ───

def render_skill_note(skill: dict[str, Any], brain_region: str,
                      connections: list[dict[str, str]]) -> str:
    """단일 스킬을 Obsidian 마크다운 노트로 렌더링."""
    # YAML frontmatter
    tags_str = ", ".join(f'"{t}"' for t in skill.get("tags", []))
    lines = [
        "---",
        f'id: "{skill["id"]}"',
        f'domain: "{skill.get("domain", "")}"',
        f'type: "{skill.get("type", "")}"',
        f"bloom_level: \"{skill.get('theory', '').split('#')[0].strip() or ''}\"",
        f"tags: [{tags_str}]",
        f'brain_region: "{brain_region}"',
        f"token_estimate: {skill.get('token_estimate', 400)}",
        "---",
        "",
        f"# {skill['id']}",
        "",
    ]

    # Theory (if present)
    theory = skill.get("theory", "")
    if theory:
        lines.append(f"> {theory}")
        lines.append("")

    # Content
    content = skill.get("content", "")
    if content:
        lines.append(content.rstrip())
        lines.append("")

    # Connections
    if connections:
        lines.append("## Connections")
        lines.append("")
        for conn in connections:
            lines.append(
                f"- [[{conn['target']}]] — {conn['type']} (weight: {conn['weight']})"
            )
        lines.append("")

    return "\n".join(lines)


# ─── MOC (Map of Content) ───

def render_moc(region: str, skill_ids: list[str]) -> str:
    """Brain region별 MOC 파일 생성."""
    lines = [
        "---",
        f'brain_region: "{region}"',
        f"skill_count: {len(skill_ids)}",
        "---",
        "",
        f"# {region} — Map of Content",
        "",
        f"Brain region **{region}** contains {len(skill_ids)} skills.",
        "",
        "## Skills",
        "",
    ]
    for sid in sorted(skill_ids):
        lines.append(f"- [[{sid}]]")
    lines.append("")
    return "\n".join(lines)


# ─── Master Graph RAG.md ───

def render_master(region_counts: dict[str, int], total: int) -> str:
    """Graph RAG.md 마스터 파일 생성."""
    lines = [
        "---",
        f"total_skills: {total}",
        "---",
        "",
        "# Graph RAG — Skill Brain Map",
        "",
        f"Total skills: **{total}**",
        "",
        "## Brain Regions",
        "",
        "| Region | Count | Link |",
        "|--------|-------|------|",
    ]
    for region in sorted(region_counts.keys()):
        count = region_counts[region]
        lines.append(f"| {region} | {count} | [[{region}]] |")
    lines.append("")
    return "\n".join(lines)


# ─── Orphan Detection ───

def detect_orphans(vault_dir: Path, known_ids: set[str]) -> list[str]:
    """vault에 존재하지만 현재 YAML에 없는 노트 파일 탐지."""
    orphans: list[str] = []
    if not vault_dir.exists():
        return orphans

    # MOC 및 마스터 파일은 제외
    skip_names = {"Graph RAG.md"}
    moc_regions = set(BRAIN_REGIONS.values()) | {"UNKNOWN"}
    skip_names.update(f"{r}.md" for r in moc_regions)

    for md_path in vault_dir.glob("*.md"):
        if md_path.name in skip_names:
            continue
        stem = md_path.stem
        if stem not in known_ids:
            orphans.append(stem)
    return sorted(orphans)


# ─── 파일 쓰기 헬퍼 ───

def write_file(path: Path, content: str, dry_run: bool) -> bool:
    """파일 쓰기. 내용이 같으면 스킵. 변경 여부 반환."""
    if path.exists():
        existing = path.read_text(encoding="utf-8")
        if existing == content:
            return False
    if not dry_run:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    return True


# ─── 메인 동기화 ───

def sync(
    vault_dir: Path,
    skill_dir: str,
    dry_run: bool = False,
    skill_id_filter: str | None = None,
    verbose: bool = False,
) -> None:
    """YAML 스킬을 Obsidian vault로 동기화."""
    # 스킬 로드
    skills = load_all_skills(skill_dir=skill_dir)
    if not skills:
        logger.warning("No skills found in %s", skill_dir)
        return

    # 엣지 로드 및 인덱스 빌드
    edges = _try_extract_all_edges()
    edge_index = build_edge_index(edges)

    # 필터링
    if skill_id_filter:
        skills = [s for s in skills if s["id"] == skill_id_filter]
        if not skills:
            logger.error("Skill '%s' not found", skill_id_filter)
            return

    # Brain region별 그룹핑
    region_skills: dict[str, list[str]] = defaultdict(list)
    known_ids: set[str] = set()

    created = 0
    updated = 0
    unchanged = 0

    for skill in skills:
        sid = skill["id"]
        known_ids.add(sid)
        domain = skill.get("domain", "")
        brain_region = resolve_brain_region(domain)
        region_skills[brain_region].append(sid)

        # 노트 렌더링
        connections = edge_index.get(sid, [])
        note_content = render_skill_note(skill, brain_region, connections)

        note_path = vault_dir / f"{sid}.md"
        is_new = not note_path.exists()
        changed = write_file(note_path, note_content, dry_run)

        if changed:
            if is_new:
                created += 1
            else:
                updated += 1
            if verbose:
                action = "CREATE" if is_new else "UPDATE"
                prefix = "[DRY-RUN] " if dry_run else ""
                logger.info("%s%s %s", prefix, action, note_path.name)
        else:
            unchanged += 1

    # MOC 파일 생성
    moc_changed = 0
    # 단일 스킬 모드에서도 전체 스킬로 MOC 생성하려면 전체 로드 필요
    if not skill_id_filter:
        for region, sids in region_skills.items():
            moc_content = render_moc(region, sids)
            moc_path = vault_dir / f"{region}.md"
            if write_file(moc_path, moc_content, dry_run):
                moc_changed += 1
                if verbose:
                    prefix = "[DRY-RUN] " if dry_run else ""
                    logger.info("%sMOC %s", prefix, moc_path.name)

        # 마스터 파일 생성
        region_counts = {r: len(sids) for r, sids in region_skills.items()}
        master_content = render_master(region_counts, len(skills))
        master_path = vault_dir / "Graph RAG.md"
        if write_file(master_path, master_content, dry_run):
            moc_changed += 1
            if verbose:
                prefix = "[DRY-RUN] " if dry_run else ""
                logger.info("%sMASTER Graph RAG.md", prefix)

    # Orphan 탐지
    # 전체 스킬의 known_ids가 필요하므로 필터 없이 다시 로드
    if not skill_id_filter:
        all_known = {s["id"] for s in load_all_skills(skill_dir=skill_dir)}
        orphans = detect_orphans(vault_dir, all_known)
    else:
        orphans = []

    # 결과 출력
    prefix = "[DRY-RUN] " if dry_run else ""
    print(f"\n{prefix}Sync complete:")
    print(f"  Skills: {created} created, {updated} updated, {unchanged} unchanged")
    print(f"  MOC/Master files: {moc_changed} written")
    if orphans:
        print(f"\n  Orphaned notes ({len(orphans)}):")
        for o in orphans:
            print(f"    - {o}.md")
    elif not skill_id_filter:
        print("  No orphaned notes found.")


def _parse_obsidian_to_skill(md_path: Path) -> dict | None:
    """Parse Obsidian markdown file back to skill YAML format."""
    text = md_path.read_text(encoding="utf-8")

    # Extract YAML frontmatter
    if not text.startswith("---"):
        return None

    parts = text.split("---", 2)
    if len(parts) < 3:
        return None

    try:
        frontmatter = yaml.safe_load(parts[1])
    except yaml.YAMLError:
        return None

    if not frontmatter or "id" not in frontmatter:
        return None

    # Extract content (everything after frontmatter)
    content = parts[2].strip()

    # Remove Obsidian-specific markers if present
    # e.g., "## 관련 스킬" section with [[wiki-links]]
    lines = content.split("\n")
    clean_lines = []
    skip_section = False
    for line in lines:
        if line.strip().startswith("## 관련 스킬") or line.strip().startswith("## Related"):
            skip_section = True
            continue
        if skip_section and line.startswith("## "):
            skip_section = False
        if not skip_section:
            # Remove wiki-link syntax [[...]]
            line = re.sub(r'\[\[([^\]]+)\]\]', r'\1', line)
            clean_lines.append(line)

    content = "\n".join(clean_lines).strip()

    skill = {
        "id": frontmatter["id"],
        "domain": frontmatter.get("domain", ""),
        "type": frontmatter.get("type", "rule"),
        "tags": frontmatter.get("tags", []),
        "content": content,
    }

    if "theory" in frontmatter:
        skill["theory"] = frontmatter["theory"]
    if "bloom_level" in frontmatter:
        skill["bloom_level"] = frontmatter["bloom_level"]

    return skill


def reverse_sync(
    obsidian_vault: Path,
    skills_dir: Path,
    dry_run: bool = False,
    force_obsidian: bool = False,
    sync_state_file: Path | None = None,
) -> dict:
    """Reverse sync: Obsidian → YAML.

    Returns:
        {"updated": int, "skipped": int, "conflicts": int, "errors": int}
    """
    state_file = sync_state_file or SYNC_STATE_FILE
    state = _load_sync_state() if state_file.exists() else {}

    updated = 0
    skipped = 0
    conflicts = 0
    errors = 0

    # Find all markdown files in vault
    for md_path in sorted(obsidian_vault.rglob("*.md")):
        try:
            skill = _parse_obsidian_to_skill(md_path)
            if not skill:
                continue

            skill_id = skill["id"]

            # Find corresponding YAML file
            parts = skill_id.split(".")
            yaml_path = skills_dir / "/".join(parts[:-1]) / f"{parts[-1]}.yaml"

            if not yaml_path.exists():
                if not dry_run:
                    # New skill from Obsidian
                    yaml_path.parent.mkdir(parents=True, exist_ok=True)
                    # Estimate tokens
                    content = skill.get("content", "")
                    korean_chars = sum(1 for c in content if "\uac00" <= c <= "\ud7a3")
                    ratio = korean_chars / len(content) if content else 0
                    skill["token_estimate"] = len(content) // 2 if ratio > 0.1 else len(content) // 4

                    with open(yaml_path, "w", encoding="utf-8") as f:
                        yaml.dump(skill, f, allow_unicode=True, default_flow_style=False)
                    print(f"  CREATED: {yaml_path.name} (from Obsidian)")
                else:
                    print(f"  [DRY-RUN] Would create: {yaml_path.name}")
                updated += 1
                continue

            # Check for conflicts
            md_key = str(md_path.relative_to(obsidian_vault))
            yaml_key = str(yaml_path)

            prev_md_hash = state.get(f"md:{md_key}", "")
            prev_yaml_hash = state.get(f"yaml:{yaml_key}", "")

            current_md_hash = _file_hash(md_path)
            current_yaml_hash = _file_hash(yaml_path)

            md_changed = current_md_hash != prev_md_hash
            yaml_changed = current_yaml_hash != prev_yaml_hash

            if md_changed and yaml_changed and not force_obsidian:
                print(f"  CONFLICT: {skill_id} (both modified, use --force-obsidian)")
                conflicts += 1
                continue

            if not md_changed:
                skipped += 1
                continue

            # Obsidian changed, update YAML
            if not dry_run:
                existing = yaml.safe_load(yaml_path.read_text(encoding="utf-8"))
                if existing:
                    # Preserve fields not in Obsidian
                    for key in ("token_estimate", "bloom_level"):
                        if key in existing and key not in skill:
                            skill[key] = existing[key]

                # Recalculate token estimate
                content = skill.get("content", "")
                korean_chars = sum(1 for c in content if "\uac00" <= c <= "\ud7a3")
                ratio = korean_chars / len(content) if content else 0
                skill["token_estimate"] = len(content) // 2 if ratio > 0.1 else len(content) // 4

                with open(yaml_path, "w", encoding="utf-8") as f:
                    yaml.dump(skill, f, allow_unicode=True, default_flow_style=False)

                # Update state
                state[f"md:{md_key}"] = current_md_hash
                state[f"yaml:{yaml_key}"] = _file_hash(yaml_path)

                print(f"  UPDATED: {skill_id} (Obsidian → YAML)")
            else:
                print(f"  [DRY-RUN] Would update: {skill_id}")
            updated += 1

        except Exception as e:
            print(f"  ERROR: {md_path.name}: {e}")
            errors += 1

    if not dry_run:
        _save_sync_state(state)

    return {"updated": updated, "skipped": skipped, "conflicts": conflicts, "errors": errors}


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Sync YAML skills to Obsidian vault as markdown notes."
    )
    parser.add_argument(
        "--vault-dir",
        type=str,
        default=os.environ.get("OBSIDIAN_VAULT_DIR", "../graph-rag-vault/"),
        help="Obsidian vault directory (default: OBSIDIAN_VAULT_DIR env or ../graph-rag-vault/)",
    )
    parser.add_argument(
        "--skill-dir",
        type=str,
        default="./skills",
        help="Skills YAML directory (default: ./skills)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would change without writing files",
    )
    parser.add_argument(
        "--skill-id",
        type=str,
        default=None,
        help="Sync a single skill only (e.g., dev.backend.api.role)",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Verbose output",
    )
    parser.add_argument(
        "--reverse",
        action="store_true",
        help="Reverse sync: Obsidian → YAML",
    )
    parser.add_argument(
        "--force-obsidian",
        action="store_true",
        help="On conflict, prefer Obsidian version",
    )
    parser.add_argument(
        "--force-yaml",
        action="store_true",
        help="On conflict, prefer YAML version",
    )
    parser.add_argument(
        "--sync-state-file",
        type=str,
        default=None,
        help="Path to sync state JSON file",
    )
    args = parser.parse_args()

    level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

    vault_dir = Path(args.vault_dir).resolve()
    print(f"Vault: {vault_dir}")
    print(f"Skills: {Path(args.skill_dir).resolve()}")

    if not vault_dir.exists() and not args.dry_run:
        vault_dir.mkdir(parents=True)
        print(f"Created vault directory: {vault_dir}")

    if args.reverse:
        skills_dir = Path(args.skill_dir).resolve()
        result = reverse_sync(
            obsidian_vault=vault_dir,
            skills_dir=skills_dir,
            dry_run=args.dry_run,
            force_obsidian=args.force_obsidian,
            sync_state_file=Path(args.sync_state_file) if args.sync_state_file else None,
        )
        print(f"\nReverse sync: {result}")
    else:
        sync(
            vault_dir=vault_dir,
            skill_dir=args.skill_dir,
            dry_run=args.dry_run,
            skill_id_filter=args.skill_id,
            verbose=args.verbose,
        )


if __name__ == "__main__":
    main()
