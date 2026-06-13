#!/usr/bin/env python3
"""Graph RAG → Obsidian Vault 생성.

250개 Atomic Skill을 마크다운 파일로, 582개 엣지를 [[wikilink]]로 연결.

Usage:
    python tools/generate_obsidian_vault.py

Output:
    graph-rag-vault/
"""

from __future__ import annotations

import json
import logging
import shutil
import sys
from itertools import combinations
from pathlib import Path

import yaml

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
AI_PIPELINE = PROJECT_ROOT / "ai-pipeline"
SKILLS_DIR = AI_PIPELINE / "skills"
VAULT_DIR = PROJECT_ROOT / "graph-rag-vault"

# ─── Brain Region Mapping ───

REGION_MAP_PREFIX = [
    ("dev.backend.database", "BRAINSTEM"),
    ("dev.backend.auth", "BRAINSTEM"),
    ("dev.backend.patterns", "BRAINSTEM"),
    ("dev.backend", "BRAINSTEM"),
    ("dev.infra", "BRAINSTEM"),
    ("dev.frontend", "CORTEX"),
    ("dev.security", "CORTEX"),
    ("dev.performance", "CORTEX"),
    ("planning", "PREFRONTAL"),
    ("design", "LIMBIC"),
    ("marketing", "SENSORS"),
    ("analytics", "HIPPOCAMPUS"),
    ("content", "HIPPOCAMPUS"),
    ("qa", "EGO"),
    ("meta", "EGO"),
]

REGION_META = {
    "PREFRONTAL":  {"emoji": "🧠", "desc": "기획 / 메타인지 — Planning, Business, Project Mgmt"},
    "CORTEX":      {"emoji": "⚡", "desc": "실행 계층 — Frontend, Security, Performance"},
    "LIMBIC":      {"emoji": "💜", "desc": "감정 / UX — Design, UX Psychology"},
    "HIPPOCAMPUS": {"emoji": "🌿", "desc": "학습 / 분석 — Analytics, Content"},
    "BRAINSTEM":   {"emoji": "🔴", "desc": "핵심 인프라 — Backend, Database, Infra"},
    "SENSORS":     {"emoji": "📡", "desc": "입력 / 마케팅 — Marketing, Persuasion"},
    "EGO":         {"emoji": "🔵", "desc": "품질 / 자아 — QA, Meta-cognition"},
}


def get_brain_region(skill_id: str) -> str:
    for prefix, region in REGION_MAP_PREFIX:
        if skill_id.startswith(prefix):
            return region
    return "CORTEX"


# ─── Skill Type / Domain Inference ───

TYPE_SUFFIXES = {"role": "role", "verify": "verify", "stack": "stack"}


def infer_type(skill_id: str) -> str:
    last = skill_id.rsplit(".", 1)[-1] if "." in skill_id else skill_id
    return TYPE_SUFFIXES.get(last, "middle")


def get_domain(skill_id: str) -> str:
    parts = skill_id.split(".")
    return ".".join(parts[:2]) if len(parts) >= 2 else parts[0]


# ─── Load Data ───

def load_skill_dicts() -> tuple[dict, dict]:
    sys.path.insert(0, str(AI_PIPELINE))
    try:
        from packages.hook_engine.selector import BASE_SKILLS, KEYWORD_SKILLS
        return BASE_SKILLS, KEYWORD_SKILLS
    except Exception as e:
        logger.error("Import failed: %s", e)
        sys.exit(1)


def extract_edges(
    base_skills: dict[str, list[str]],
    keyword_skills: dict[str, list[str]],
    valid_nodes: set[str],
) -> list[dict]:
    edges: list[dict] = []

    for _domain, skill_ids in base_skills.items():
        roles = [s for s in skill_ids if infer_type(s) == "role"]
        verifies = [s for s in skill_ids if infer_type(s) == "verify"]
        middles = [s for s in skill_ids if s not in roles and s not in verifies]

        for r in roles:
            for m in middles:
                edges.append({"source": r, "target": m, "type": "REQUIRES", "weight": 0.90})
        for r in roles:
            for v in verifies:
                edges.append({"source": r, "target": v, "type": "REQUIRES", "weight": 0.85})
        for m in middles:
            for v in verifies:
                edges.append({"source": m, "target": v, "type": "FEEDS", "weight": 0.80})
        for i in range(len(middles) - 1):
            edges.append({"source": middles[i], "target": middles[i + 1], "type": "FEEDS", "weight": 0.70})

    seen: set[tuple[str, str]] = set()
    for _kw, skill_ids in keyword_skills.items():
        for a, b in combinations(skill_ids, 2):
            pair = (min(a, b), max(a, b))
            if pair in seen:
                continue
            seen.add(pair)
            da, db = get_domain(a), get_domain(b)
            if da == db:
                edges.append({"source": a, "target": b, "type": "CO_CREATES", "weight": 0.60})
            else:
                edges.append({"source": a, "target": b, "type": "FEEDS", "weight": 0.50})

    edge_map: dict[tuple, dict] = {}
    for e in edges:
        key = (e["source"], e["target"], e["type"])
        if key not in edge_map or e["weight"] > edge_map[key]["weight"]:
            edge_map[key] = e

    return [e for e in edge_map.values() if e["source"] in valid_nodes and e["target"] in valid_nodes]


def load_yaml_metadata() -> dict[str, dict]:
    meta: dict[str, dict] = {}
    for yaml_path in sorted(SKILLS_DIR.rglob("*.yaml")):
        try:
            data = yaml.safe_load(yaml_path.read_text(encoding="utf-8"))
            if not data or "id" not in data:
                continue
            sid = data["id"]
            meta[sid] = {
                "id": sid,
                "domain": data.get("domain", ""),
                "type": data.get("type", ""),
                "tags": data.get("tags", []),
                "token_estimate": data.get("token_estimate", 400),
                "theory": data.get("theory", ""),
                "content": data.get("content", ""),
            }
        except Exception as e:
            logger.warning("Failed to load %s: %s", yaml_path, e)
    return meta


# ─── Obsidian Vault Generation ───

def build_adjacency(edges: list[dict]) -> dict[str, list[dict]]:
    """Build adjacency: skill_id → [{target, type, weight, direction}]."""
    adj: dict[str, list[dict]] = {}
    for e in edges:
        adj.setdefault(e["source"], []).append({
            "peer": e["target"], "type": e["type"], "weight": e["weight"], "dir": "out",
        })
        adj.setdefault(e["target"], []).append({
            "peer": e["source"], "type": e["type"], "weight": e["weight"], "dir": "in",
        })
    return adj


def generate_skill_note(node: dict, adj: dict[str, list[dict]]) -> str:
    """Generate markdown for a single skill note."""
    sid = node["id"]
    region = node["region"]
    region_info = REGION_META.get(region, {})
    tags_yaml = ", ".join(node.get("tags", []))
    connections = adj.get(sid, [])

    # Frontmatter
    lines = [
        "---",
        f'id: "{sid}"',
        f'domain: "{node["domain"]}"',
        f'type: "{node["type"]}"',
        f"region: {region}",
        f"token_estimate: {node.get('token_estimate', 400)}",
    ]
    if node.get("theory"):
        lines.append(f'theory: "{node["theory"]}"')
    if node.get("tags"):
        lines.append(f"tags: [{tags_yaml}]")
    lines.append("---")
    lines.append("")

    # Title
    lines.append(f"# {sid}")
    lines.append("")

    # Metadata table
    lines.append(f"> **Region**: {region_info.get('emoji', '')} [[{region}]]  ")
    lines.append(f"> **Domain**: `{node['domain']}`  ")
    lines.append(f"> **Type**: `{node['type']}`  ")
    if node.get("theory"):
        lines.append(f"> **Theory**: {node['theory']}  ")
    lines.append(f"> **Tokens**: {node.get('token_estimate', 400)}")
    lines.append("")

    # Skill content
    content = node.get("content", "").strip()
    if content:
        lines.append("## Content")
        lines.append("")
        lines.append(content)
        lines.append("")

    if not connections:
        return "\n".join(lines)

    # Group connections by type
    by_type: dict[str, list[dict]] = {}
    for c in connections:
        by_type.setdefault(c["type"], []).append(c)

    lines.append("## Connections")
    lines.append("")

    type_arrows = {"REQUIRES": "→", "FEEDS": "→", "CO_CREATES": "↔", "CO_OCCURS": "↔"}
    type_order = ["REQUIRES", "FEEDS", "CO_CREATES", "CO_OCCURS"]

    for etype in type_order:
        conns = by_type.get(etype, [])
        if not conns:
            continue
        arrow = type_arrows.get(etype, "→")
        lines.append(f"### {etype} ({len(conns)})")
        lines.append("")
        for c in sorted(conns, key=lambda x: x["peer"]):
            dir_symbol = "→" if c["dir"] == "out" else "←"
            lines.append(f"- {dir_symbol} [[{c['peer']}]] `w={c['weight']}`")
        lines.append("")

    return "\n".join(lines)


def generate_region_moc(region: str, region_nodes: list[dict]) -> str:
    """Generate MOC (Map of Content) for a brain region."""
    info = REGION_META.get(region, {})
    lines = [
        "---",
        f"tags: [region, {region.lower()}]",
        "---",
        "",
        f"# {info.get('emoji', '')} {region}",
        "",
        f"> {info.get('desc', '')}",
        "",
        f"**{len(region_nodes)} skills**",
        "",
    ]

    # Group by domain
    by_domain: dict[str, list[dict]] = {}
    for n in region_nodes:
        d = n["domain"] or get_domain(n["id"])
        by_domain.setdefault(d, []).append(n)

    for domain in sorted(by_domain.keys()):
        dns = by_domain[domain]
        lines.append(f"## {domain}")
        lines.append("")
        for n in sorted(dns, key=lambda x: x["id"]):
            type_badge = {"role": "🎭", "verify": "✅", "stack": "📚"}.get(n["type"], "📄")
            lines.append(f"- {type_badge} [[{n['id']}]]")
        lines.append("")

    return "\n".join(lines)


def generate_root_moc(nodes: list[dict], edges: list[dict]) -> str:
    """Generate root MOC with stats and region links."""
    region_counts: dict[str, int] = {}
    for n in nodes:
        region_counts[n["region"]] = region_counts.get(n["region"], 0) + 1

    edge_type_counts: dict[str, int] = {}
    for e in edges:
        edge_type_counts[e["type"]] = edge_type_counts.get(e["type"], 0) + 1

    lines = [
        "---",
        "tags: [MOC, graph-rag]",
        "---",
        "",
        "# 🧠 Graph RAG Knowledge Graph",
        "",
        f"> **{len(nodes)}** Neurons · **{len(edges)}** Synapses · **7** Brain Regions",
        "",
        "## Brain Regions",
        "",
    ]

    for region in ["PREFRONTAL", "CORTEX", "SENSORS", "LIMBIC", "HIPPOCAMPUS", "BRAINSTEM", "EGO"]:
        info = REGION_META.get(region, {})
        count = region_counts.get(region, 0)
        lines.append(f"- {info.get('emoji', '')} [[{region}]] — {count} skills — {info.get('desc', '')}")

    lines.append("")
    lines.append("## Edge Types")
    lines.append("")
    for etype, count in sorted(edge_type_counts.items()):
        lines.append(f"- **{etype}**: {count}")

    lines.append("")
    return "\n".join(lines)


def write_obsidian_config():
    """Write minimal .obsidian config with graph color groups."""
    obsidian_dir = VAULT_DIR / ".obsidian"
    obsidian_dir.mkdir(parents=True, exist_ok=True)

    # Graph color groups matching brain regions
    graph_config = {
        "collapse-filter": False,
        "search": "",
        "showTags": False,
        "showAttachments": False,
        "showOrphans": True,
        "collapse-color-groups": False,
        "colorGroups": [
            {"query": "path:BRAINSTEM", "color": {"a": 1, "rgb": 16736619}},   # #ff6b6b
            {"query": "path:CORTEX", "color": {"a": 1, "rgb": 5164484}},       # #4ecdc4
            {"query": "path:PREFRONTAL", "color": {"a": 1, "rgb": 10656766}},  # #a29bfe
            {"query": "path:LIMBIC", "color": {"a": 1, "rgb": 16612776}},      # #fd79a8
            {"query": "path:SENSORS", "color": {"a": 1, "rgb": 16771751}},     # #ffeaa7
            {"query": "path:HIPPOCAMPUS", "color": {"a": 1, "rgb": 5632964}},  # #55efc4
            {"query": "path:EGO", "color": {"a": 1, "rgb": 7649279}},          # #74b9ff
        ],
        "collapse-display": False,
        "showArrow": True,
        "textFadeMultiplier": 0,
        "nodeSizeMultiplier": 1,
        "lineSizeMultiplier": 1,
        "collapse-forces": False,
        "centerStrength": 0.5,
        "repelStrength": 10,
        "linkStrength": 1,
        "linkDistance": 100,
        "scale": 1,
        "close": False,
    }

    (obsidian_dir / "graph.json").write_text(
        json.dumps(graph_config, indent=2), encoding="utf-8"
    )

    # App config — dark theme
    app_config = {
        "theme": "obsidian",
        "baseFontSize": 15,
    }
    (obsidian_dir / "app.json").write_text(
        json.dumps(app_config, indent=2), encoding="utf-8"
    )


# ─── Main ───

def main():
    logger.info("Loading skill dictionaries...")
    base_skills, keyword_skills = load_skill_dicts()

    all_ids: set[str] = set()
    for ids in base_skills.values():
        all_ids.update(ids)
    for ids in keyword_skills.values():
        all_ids.update(ids)

    yaml_meta = load_yaml_metadata()
    all_ids.update(yaml_meta.keys())
    logger.info("Total skills: %d", len(all_ids))

    # Build nodes
    nodes: list[dict] = []
    for sid in sorted(all_ids):
        meta = yaml_meta.get(sid, {})
        nodes.append({
            "id": sid,
            "domain": meta.get("domain", ""),
            "type": meta.get("type", "") or infer_type(sid),
            "tags": meta.get("tags", []),
            "token_estimate": meta.get("token_estimate", 400),
            "theory": meta.get("theory", ""),
            "content": meta.get("content", ""),
            "region": get_brain_region(sid),
        })

    # Extract edges
    edges = extract_edges(base_skills, keyword_skills, all_ids)
    adj = build_adjacency(edges)
    logger.info("Edges: %d", len(edges))

    # Clean & create vault
    if VAULT_DIR.exists():
        shutil.rmtree(VAULT_DIR)
    VAULT_DIR.mkdir(parents=True)

    # Group nodes by region
    by_region: dict[str, list[dict]] = {}
    for n in nodes:
        by_region.setdefault(n["region"], []).append(n)

    # Write skill notes (one per skill, in region folders)
    for region, region_nodes in by_region.items():
        region_dir = VAULT_DIR / region
        region_dir.mkdir(exist_ok=True)

        for node in region_nodes:
            note = generate_skill_note(node, adj)
            filepath = region_dir / f"{node['id']}.md"
            filepath.write_text(note, encoding="utf-8")

        # Region MOC
        moc = generate_region_moc(region, region_nodes)
        (VAULT_DIR / f"{region}.md").write_text(moc, encoding="utf-8")
        logger.info("  %s: %d skills", region, len(region_nodes))

    # Root MOC
    root_moc = generate_root_moc(nodes, edges)
    (VAULT_DIR / "Graph RAG.md").write_text(root_moc, encoding="utf-8")

    # Obsidian config
    write_obsidian_config()

    logger.info("Vault generated: %s", VAULT_DIR)
    logger.info("  %d notes, %d edges as [[wikilinks]]", len(nodes), len(edges))
    logger.info("Open in Obsidian: File → Open Vault → %s", VAULT_DIR)


if __name__ == "__main__":
    main()
