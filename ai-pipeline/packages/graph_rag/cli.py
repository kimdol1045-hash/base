"""Graph RAG CLI — ingest, embed, status, reset, evolve 명령어."""

from __future__ import annotations

import argparse
import asyncio
import json
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-8s %(name)s — %(message)s",
)
logger = logging.getLogger("graph_rag.cli")


async def cmd_ingest(args: argparse.Namespace) -> None:
    """Neo4j에 스킬 노드 + 엣지 인제스트."""
    from .ingest import ingest_skills_to_neo4j
    from .neo4j_client import Neo4jClient

    async with Neo4jClient() as neo4j:
        result = await ingest_skills_to_neo4j(neo4j, args.skill_dir)

    print("\n✓ Neo4j ingest complete:")
    print(f"  Nodes: {result['nodes']}")
    print(f"  Edges: {json.dumps(result['edges'], indent=2)}")


async def cmd_embed(args: argparse.Namespace) -> None:
    """스킬 임베딩 → Qdrant 업서트."""
    from .ingest import ingest_skills_to_qdrant
    from .vector_client import VectorClient

    async with VectorClient() as vector:
        count = await ingest_skills_to_qdrant(vector, args.skill_dir)

    print(f"\n✓ Qdrant embed complete: {count} vectors")


async def cmd_status(args: argparse.Namespace) -> None:
    """Neo4j + Qdrant 상태 확인."""
    from .neo4j_client import Neo4jClient
    from .vector_client import VectorClient

    print("\n── Graph RAG Status ──")

    # Neo4j
    try:
        async with Neo4jClient() as neo4j:
            ok = await neo4j.verify_connection()
            if ok:
                counts = await neo4j.get_counts()
                print("  Neo4j: ✓ connected")
                print(f"    Nodes: {counts['nodes']}")
                print(f"    Edges: {json.dumps(counts['edges'], indent=6)}")
            else:
                print("  Neo4j: ✗ connection failed")
    except Exception as e:
        print(f"  Neo4j: ✗ {e}")

    # Qdrant
    try:
        async with VectorClient() as vector:
            ok = await vector.verify_connection()
            if ok:
                count = await vector.get_count()
                print("  Qdrant: ✓ connected")
                print(f"    Vectors: {count}")
            else:
                print("  Qdrant: ✗ connection failed")
    except Exception as e:
        print(f"  Qdrant: ✗ {e}")


async def cmd_reset(args: argparse.Namespace) -> None:
    """Neo4j + Qdrant 초기화."""
    if not args.confirm:
        print("⚠ This will DELETE all data. Use --confirm to proceed.")
        return

    from .neo4j_client import Neo4jClient
    from .schema import DELETE_ALL
    from .vector_client import VectorClient

    # Neo4j
    try:
        async with Neo4jClient() as neo4j:
            await neo4j.run_void(DELETE_ALL)
            print("✓ Neo4j: all data deleted")
    except Exception as e:
        print(f"✗ Neo4j reset failed: {e}")

    # Qdrant
    try:
        async with VectorClient() as vector:
            await vector.delete_collection()
            print("✓ Qdrant: collection deleted")
    except Exception as e:
        print(f"✗ Qdrant reset failed: {e}")


async def cmd_evolve(args: argparse.Namespace) -> None:
    """자가 발전 통계 + 감쇠 적용."""
    from .neo4j_client import Neo4jClient
    from .self_evolution import apply_decay, get_evolution_stats

    async with Neo4jClient() as neo4j:
        if args.decay:
            await apply_decay(neo4j)
            print("✓ Decay applied")

        stats = await get_evolution_stats(neo4j)
        print("\n── Evolution Stats ──")
        print("  Top executed skills:")
        for s in stats.get("top_executed", []):
            print(f"    {s['id']}: {s['count']} runs, {s['rate']:.2f} success rate")
        print(f"  Auto-created edges: {stats.get('auto_edges', 0)}")
        print(f"  Co-occurrence pairs tracked: {stats.get('co_occurrence_tracking', 0)}")
        print("  Weight distribution:")
        for w in stats.get("weight_distribution", []):
            print(f"    {w['type']}: avg={w['avgWeight']:.3f}, min={w['minWeight']:.3f}, max={w['maxWeight']:.3f}")


async def cmd_watch(args: argparse.Namespace) -> None:
    """스킬 디렉토리 감시 (파일 변경 → 자동 인제스트/삭제)."""
    from .watcher import start_watcher

    skill_dir = args.skill_dir or "./skills"
    observer = await start_watcher(skill_dir)
    print(f"\n✓ Watching {skill_dir} for changes (Ctrl+C to stop)")

    try:
        while True:
            await asyncio.sleep(1)
    except (KeyboardInterrupt, asyncio.CancelledError):
        observer.stop()
        observer.join()
        print("\n✓ Watcher stopped")


async def cmd_community(args: argparse.Namespace) -> None:
    """커뮤니티 탐지 실행."""
    from .community import detect_communities
    from .neo4j_client import Neo4jClient

    async with Neo4jClient() as neo4j:
        result = await detect_communities(neo4j)

    print("\n── Community Detection ──")
    print(f"  Communities: {result['community_count']}")
    print(f"  Modularity: {result.get('modularity', 0.0):.4f}")
    if result.get("fallback"):
        print("  (fallback: domain-based grouping)")
    for comm in result.get("communities", [])[:10]:
        domain = comm.get("domain", "")
        label = f" ({domain})" if domain else ""
        print(f"  Community {comm['community']}{label}: {comm['size']} skills")


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="graph_rag",
        description="Graph RAG CLI — Neo4j + Qdrant 기반 스킬 관리",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # ingest
    p_ingest = sub.add_parser("ingest", help="YAML → Neo4j 인제스트")
    p_ingest.add_argument("--skill-dir", default=None, help="스킬 디렉토리 경로")

    # embed
    p_embed = sub.add_parser("embed", help="스킬 임베딩 → Qdrant")
    p_embed.add_argument("--skill-dir", default=None, help="스킬 디렉토리 경로")

    # status
    sub.add_parser("status", help="Neo4j + Qdrant 상태 확인")

    # reset
    p_reset = sub.add_parser("reset", help="전체 데이터 초기화")
    p_reset.add_argument("--confirm", action="store_true", help="삭제 확인")

    # evolve
    p_evolve = sub.add_parser("evolve", help="자가 발전 통계 + 감쇠")
    p_evolve.add_argument("--decay", action="store_true", help="감쇠 적용")

    # watch
    p_watch = sub.add_parser("watch", help="스킬 디렉토리 감시 (자동 인제스트)")
    p_watch.add_argument("--skill-dir", default=None, help="스킬 디렉토리 경로")

    # community
    sub.add_parser("community", help="커뮤니티 탐지 실행")

    args = parser.parse_args()

    cmd_map = {
        "ingest": cmd_ingest,
        "embed": cmd_embed,
        "status": cmd_status,
        "reset": cmd_reset,
        "evolve": cmd_evolve,
        "watch": cmd_watch,
        "community": cmd_community,
    }

    asyncio.run(cmd_map[args.command](args))


if __name__ == "__main__":
    main()
