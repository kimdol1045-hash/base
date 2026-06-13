"""Streamlit Dashboard — AI Pipeline Skill Explorer & Evolution Monitor.

Run: streamlit run apps/dashboard/app.py

Works in two modes:
  1. API mode: connects to the FastAPI server for live data
  2. Standalone mode: reads YAML files directly (fallback when API is down)
"""

from __future__ import annotations

import os
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

import streamlit as st

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

API_URL = os.environ.get("API_URL", "http://localhost:8000")
# Default skill directory relative to project root
_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
SKILL_DIR = os.environ.get("SKILL_DIR", str(_PROJECT_ROOT / "skills"))

st.set_page_config(page_title="AI Pipeline Dashboard", layout="wide")


# ---------------------------------------------------------------------------
# Data helpers — API with YAML fallback
# ---------------------------------------------------------------------------


def _api_available() -> bool:
    """Check if the FastAPI server is reachable."""
    import requests

    try:
        r = requests.get(f"{API_URL}/health", timeout=2)
        return r.status_code == 200
    except Exception:
        return False


@st.cache_data(ttl=60)
def _load_skills_from_yaml() -> list[dict[str, Any]]:
    """Direct YAML loading — standalone fallback."""
    import yaml

    skills: list[dict[str, Any]] = []
    base = Path(SKILL_DIR)
    if not base.exists():
        return skills
    for p in sorted(base.rglob("*.yaml")):
        try:
            with open(p, encoding="utf-8") as f:
                data = yaml.safe_load(f)
            if not data or "id" not in data:
                continue
            skills.append({
                "id": data["id"],
                "domain": data.get("domain", ""),
                "type": data.get("type", ""),
                "content": data.get("content", ""),
                "tags": data.get("tags", []),
                "token_estimate": data.get("token_estimate", 400),
                "theory": data.get("theory", ""),
                "bloom_level": data.get("bloom_level", ""),
            })
        except Exception:
            continue
    return skills


@st.cache_data(ttl=30)
def _fetch_skills_api(
    domain: str | None = None,
    type_: str | None = None,
    search: str | None = None,
) -> list[dict[str, Any]]:
    """Fetch skills from the API."""
    import requests

    params: dict[str, str] = {}
    if domain:
        params["domain"] = domain
    if type_:
        params["type"] = type_
    if search:
        params["search"] = search
    try:
        r = requests.get(f"{API_URL}/api/skills", params=params, timeout=5)
        r.raise_for_status()
        return r.json().get("skills", [])
    except Exception:
        return []


@st.cache_data(ttl=30)
def _fetch_skill_detail(skill_id: str) -> dict[str, Any] | None:
    import requests

    try:
        r = requests.get(f"{API_URL}/api/skills/{skill_id}", timeout=5)
        if r.status_code == 200:
            return r.json()
    except Exception:
        pass
    return None


@st.cache_data(ttl=30)
def _fetch_domains_api() -> list[dict[str, Any]]:
    import requests

    try:
        r = requests.get(f"{API_URL}/api/domains", timeout=5)
        r.raise_for_status()
        return r.json().get("domains", [])
    except Exception:
        return []


@st.cache_data(ttl=30)
def _fetch_stats_api() -> dict[str, Any]:
    import requests

    try:
        r = requests.get(f"{API_URL}/api/stats", timeout=5)
        r.raise_for_status()
        return r.json()
    except Exception:
        return {}


@st.cache_data(ttl=30)
def _fetch_evolution_stats() -> dict[str, Any]:
    import requests

    try:
        r = requests.get(f"{API_URL}/api/evolution/stats", timeout=5)
        if r.status_code == 200:
            return r.json()
    except Exception:
        pass
    return {}


def _post_decay() -> dict[str, Any]:
    import requests

    try:
        r = requests.post(f"{API_URL}/api/evolution/decay", timeout=10)
        return r.json()
    except Exception as e:
        return {"error": str(e)}


@st.cache_data(ttl=30)
def _fetch_usage_stats(top_n: int = 20) -> dict[str, Any]:
    import requests

    try:
        r = requests.get(f"{API_URL}/api/usage", params={"top_n": top_n}, timeout=5)
        if r.status_code == 200:
            return r.json()
    except Exception:
        pass
    return {}


# ---------------------------------------------------------------------------
# Derived data helpers for standalone mode
# ---------------------------------------------------------------------------


def _domains_from_skills(skills: list[dict]) -> list[dict]:
    counts: dict[str, int] = defaultdict(int)
    for s in skills:
        counts[s.get("domain", "unknown")] += 1
    return [{"domain": k, "count": v} for k, v in sorted(counts.items())]


def _stats_from_skills(skills: list[dict]) -> dict[str, Any]:
    domains: set[str] = set()
    types: set[str] = set()
    total_tokens = 0
    for s in skills:
        domains.add(s.get("domain", ""))
        types.add(s.get("type", ""))
        total_tokens += s.get("token_estimate", 0)
    return {
        "total_skills": len(skills),
        "total_domains": len(domains),
        "total_types": len(types),
        "total_token_estimate": total_tokens,
        "domains": sorted(domains),
        "types": sorted(types),
    }


# ---------------------------------------------------------------------------
# UI
# ---------------------------------------------------------------------------


def main() -> None:
    use_api = _api_available()

    # Always load YAML as fallback
    all_skills_yaml = _load_skills_from_yaml()

    # If API says available but returns no data, fall back to YAML
    if use_api:
        test_skills = _fetch_skills_api()
        if not test_skills:
            use_api = False

    mode_label = "API" if use_api else "Standalone (YAML)"

    st.title("AI Pipeline Dashboard")
    st.caption(f"Data source: **{mode_label}** | Skills: **{len(all_skills_yaml)}**")

    tab_skills, tab_domains, tab_evolution, tab_usage, tab_history, tab_cost, tab_metrics = st.tabs(
        ["Skills", "Domain Tree", "Evolution", "Usage", "History", "Cost", "Metrics"]
    )

    # ======================================================================
    # Tab 1: Skills
    # ======================================================================
    with tab_skills:
        st.subheader("Skill Explorer")

        # Filters
        col_search, col_domain, col_type = st.columns([2, 1, 1])

        # Build domain/type option lists
        if use_api:
            stats = _fetch_stats_api()
            domain_options = [""] + stats.get("domains", [])
            type_options = [""] + stats.get("types", [])
        else:

            domain_options = [""] + sorted({s.get("domain", "") for s in all_skills_yaml})
            type_options = [""] + sorted({s.get("type", "") for s in all_skills_yaml})

        with col_search:
            search_q = st.text_input("Search", placeholder="keyword or skill ID...")
        with col_domain:
            sel_domain = st.selectbox("Domain", domain_options, format_func=lambda x: x or "All")
        with col_type:
            sel_type = st.selectbox("Type", type_options, format_func=lambda x: x or "All")

        # Fetch
        if use_api:
            skills = _fetch_skills_api(
                domain=sel_domain or None,
                type_=sel_type or None,
                search=search_q or None,
            )
        else:

            skills = all_skills_yaml
            if sel_domain:
                skills = [s for s in skills if s.get("domain") == sel_domain]
            if sel_type:
                skills = [s for s in skills if s.get("type") == sel_type]
            if search_q:
                q = search_q.lower()
                skills = [
                    s for s in skills
                    if q in s.get("id", "").lower()
                    or q in s.get("content", "").lower()
                    or q in " ".join(s.get("tags", [])).lower()
                ]

        st.write(f"**{len(skills)}** skills found")

        if skills:
            import pandas as pd

            df = pd.DataFrame(skills)
            display_cols = [
                c for c in ["id", "domain", "type", "bloom_level", "tags", "token_estimate"]
                if c in df.columns
            ]
            st.dataframe(df[display_cols], use_container_width=True, hide_index=True)

            # Expandable detail
            selected_id = st.selectbox(
                "Select skill to view details",
                [""] + [s["id"] for s in skills],
                format_func=lambda x: x or "(select a skill)",
            )
            if selected_id:
                if use_api:
                    detail = _fetch_skill_detail(selected_id)
                else:
                    detail = next((s for s in skills if s["id"] == selected_id), None)
                if detail:
                    with st.expander(f"Detail: {selected_id}", expanded=True):
                        st.json(detail)

    # ======================================================================
    # Tab 2: Domain Tree
    # ======================================================================
    with tab_domains:
        st.subheader("Domain Skill Distribution")

        if use_api:
            domain_data = _fetch_domains_api()
        else:

            domain_data = _domains_from_skills(all_skills_yaml)

        if domain_data:
            import plotly.express as px

            labels = [d["domain"] for d in domain_data]
            counts = [d["count"] for d in domain_data]

            fig = px.bar(
                x=labels,
                y=counts,
                labels={"x": "Domain", "y": "Skill Count"},
                title="Skills per Domain",
            )
            fig.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)

            # Summary metrics
            total = sum(counts)
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Skills", total)
            col2.metric("Domains", len(labels))
            col3.metric("Avg per Domain", f"{total / len(labels):.1f}" if labels else "0")
        else:
            st.info("No domain data available.")

    # ======================================================================
    # Tab 3: Evolution
    # ======================================================================
    with tab_evolution:
        st.subheader("Self-Evolution Monitor")

        if not use_api:
            st.warning(
                "Evolution data requires the API server with Neo4j. "
                "Start the server and set API_URL to enable this tab."
            )
        else:
            evo = _fetch_evolution_stats()
            if evo and "error" not in evo:
                # Top 10 by execution count
                top = evo.get("top_executed", [])
                if top:
                    st.markdown("#### Top 10 Skills by Execution Count")
                    import pandas as pd

                    df_top = pd.DataFrame(top)
                    st.dataframe(df_top, use_container_width=True, hide_index=True)

                # Weight distribution
                weights = evo.get("weight_distribution", [])
                if weights:
                    st.markdown("#### Edge Weight Distribution")
                    import plotly.express as px

                    df_w = pd.DataFrame(weights)
                    if not df_w.empty and "type" in df_w.columns:
                        fig = px.bar(
                            df_w,
                            x="type",
                            y="avgWeight",
                            error_y=df_w["maxWeight"] - df_w["avgWeight"]
                            if "maxWeight" in df_w.columns
                            else None,
                            title="Average Edge Weight by Type",
                        )
                        st.plotly_chart(fig, use_container_width=True)

                st.markdown(
                    f"**Auto CO_OCCURS edges:** {evo.get('auto_edges', 0)} | "
                    f"**Tracked pairs:** {evo.get('co_occurrence_tracking', 0)}"
                )

                # Manual decay
                st.markdown("---")
                if st.button("Run Manual Decay"):
                    result = _post_decay()
                    if "error" in result:
                        st.error(f"Decay failed: {result['error']}")
                    else:
                        st.success(
                            f"Decay applied (factor: {result.get('decay_factor', '?')})"
                        )
                        st.cache_data.clear()
            else:
                err = evo.get("error", "Unknown error")
                st.warning(f"Could not load evolution stats: {err}")

    # ======================================================================
    # Tab 4: Usage
    # ======================================================================
    with tab_usage:
        st.subheader("Skill Usage Statistics")

        if not use_api:
            st.warning(
                "Usage data requires the API server. "
                "Start the server and set API_URL to enable this tab."
            )
        else:
            usage = _fetch_usage_stats(top_n=30)
            if usage and usage.get("total_calls", 0) > 0:
                col1, col2 = st.columns(2)
                col1.metric("Total API Calls", usage.get("total_calls", 0))
                col2.metric("Unique Skills Used", usage.get("unique_skills_used", 0))

                # Top skills bar chart
                top_skills = usage.get("top_skills", [])
                if top_skills:
                    st.markdown("#### Most Used Skills")
                    import pandas as pd
                    import plotly.express as px

                    df = pd.DataFrame(top_skills)
                    fig = px.bar(
                        df,
                        x="skill_id",
                        y="count",
                        labels={"skill_id": "Skill", "count": "Usage Count"},
                        title="Top Skills by Usage",
                    )
                    fig.update_layout(xaxis_tickangle=-45)
                    st.plotly_chart(fig, use_container_width=True)

                # Least used
                least = usage.get("least_used", [])
                if least:
                    st.markdown("#### Least Used Skills")
                    df_least = pd.DataFrame(least)
                    st.dataframe(df_least, use_container_width=True, hide_index=True)
            else:
                st.info(
                    "No usage data yet. Usage is tracked when skills are assembled "
                    "via `assemble_prompt` or `prepare_plan` tools."
                )

    # ======================================================================
    # Tab 5: History
    # ======================================================================
    with tab_history:
        st.subheader("Pipeline Execution History")
        st.info(
            "Pipeline run history is not yet persisted. "
            "This tab will show recent pipeline executions once "
            "a history store (e.g. SQLite or Redis) is configured."
        )

        # Show general stats as placeholder
        if use_api:
            stats = _fetch_stats_api()
        else:

            stats = _stats_from_skills(all_skills_yaml)

        if stats:
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total Skills", stats.get("total_skills", 0))
            col2.metric("Domains", stats.get("total_domains", 0))
            col3.metric("Types", stats.get("total_types", 0))
            col4.metric("Total Tokens", f"{stats.get('total_token_estimate', 0):,}")

    # ======================================================================
    # Tab 6: Cost
    # ======================================================================
    with tab_cost:
        st.header("API 비용 추적")

        # Fetch cost data
        try:
            if use_api:
                import requests

                resp = requests.get(f"{API_URL}/api/costs", timeout=5)
                cost_data = resp.json() if resp.ok else {}
            else:
                try:
                    from packages.skill_store.server import get_cost_stats

                    cost_data = get_cost_stats()
                except Exception:
                    cost_data = {}
        except Exception:
            cost_data = {}

        if cost_data:
            col1, col2 = st.columns(2)
            with col1:
                st.metric("총 비용 (USD)", f"${cost_data.get('total_cost_usd', 0):.4f}")
            with col2:
                st.metric("총 요청 수", cost_data.get('total_requests', 0))

            # Per-model breakdown
            per_model = cost_data.get("per_model", {})
            if per_model:
                st.subheader("모델별 비용")
                import pandas as pd

                model_rows = []
                for model, model_stats in per_model.items():
                    model_rows.append({
                        "모델": model,
                        "요청 수": model_stats["requests"],
                        "비용 (USD)": f"${model_stats['cost_usd']:.4f}",
                        "입력 토큰": model_stats["input_tokens"],
                        "출력 토큰": model_stats["output_tokens"],
                    })
                st.dataframe(pd.DataFrame(model_rows), use_container_width=True)

            # Recent records
            recent = cost_data.get("recent_records", [])
            if recent:
                st.subheader("최근 기록")
                import pandas as pd

                st.dataframe(pd.DataFrame(recent[-10:]), use_container_width=True)
        else:
            st.info("비용 데이터가 없습니다.")

    # ======================================================================
    # Tab 7: Metrics
    # ======================================================================
    with tab_metrics:
        st.header("시스템 메트릭")

        try:
            if use_api:
                import requests

                resp = requests.get(f"{API_URL}/metrics", timeout=5)
                metrics_text = resp.text if resp.ok else ""
            else:
                metrics_text = ""
        except Exception:
            metrics_text = ""

        if metrics_text:
            # Parse Prometheus format
            lines = [l for l in metrics_text.split("\n") if l and not l.startswith("#")]

            st.subheader("주요 메트릭")
            for line in lines[:20]:
                parts = line.split(" ")
                if len(parts) == 2:
                    st.text(f"  {parts[0]}: {parts[1]}")
        else:
            st.info("메트릭 서버에 연결되지 않았습니다. FastAPI 서버를 시작하세요.")

        # Skill stats (always available)
        st.subheader("스킬 통계")
        if use_api:
            skill_stats = _fetch_stats_api()
        else:
            skill_stats = _stats_from_skills(all_skills_yaml)

        if skill_stats:
            col1, col2, col3 = st.columns(3)
            col1.metric("총 스킬 수", skill_stats.get("total_skills", 0))
            col2.metric("도메인 수", skill_stats.get("total_domains", 0))
            col3.metric("타입 수", skill_stats.get("total_types", 0))


if __name__ == "__main__":
    main()
