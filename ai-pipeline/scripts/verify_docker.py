#!/usr/bin/env python3
"""Docker E2E 검증 스크립트 — 컨테이너 헬스 + API 기능 테스트."""

from __future__ import annotations

import sys
import time

import httpx

BASE_URL = "http://localhost:8000"
TIMEOUT = 30


def _check(name: str, passed: bool, detail: str = "") -> bool:
    status = "PASS" if passed else "FAIL"
    msg = f"[{status}] {name}"
    if detail:
        msg += f" — {detail}"
    print(msg)
    return passed


def check_health() -> bool:
    """1. /health → 200"""
    try:
        r = httpx.get(f"{BASE_URL}/health", timeout=TIMEOUT)
        return _check("Health check", r.status_code == 200, f"status={r.status_code}")
    except httpx.RequestError as e:
        return _check("Health check", False, str(e))


def check_stats() -> bool:
    """2. /api/stats → total_skills >= 500"""
    try:
        r = httpx.get(f"{BASE_URL}/api/stats", timeout=TIMEOUT)
        if r.status_code != 200:
            return _check("Stats", False, f"status={r.status_code}")
        data = r.json()
        total = data.get("total_skills", 0)
        return _check("Stats (skills >= 500)", total >= 500, f"total_skills={total}")
    except httpx.RequestError as e:
        return _check("Stats", False, str(e))


def check_domains() -> bool:
    """3. /api/domains → total_domains >= 20"""
    try:
        r = httpx.get(f"{BASE_URL}/api/domains", timeout=TIMEOUT)
        if r.status_code != 200:
            return _check("Domains", False, f"status={r.status_code}")
        data = r.json()
        total = data.get("total_domains", 0)
        return _check("Domains (>= 20)", total >= 20, f"total_domains={total}")
    except httpx.RequestError as e:
        return _check("Domains", False, str(e))


def check_evolution_health() -> bool:
    """4. /api/evolution/health → Neo4j 연결 확인"""
    try:
        r = httpx.get(f"{BASE_URL}/api/evolution/health", timeout=TIMEOUT)
        if r.status_code == 503:
            return _check("Evolution health", True, "Neo4j unavailable (optional)")
        data = r.json()
        connected = data.get("neo4j_connected", False)
        return _check("Evolution health", r.status_code == 200, f"neo4j={connected}")
    except httpx.RequestError as e:
        return _check("Evolution health", False, str(e))


def check_plan() -> bool:
    """5. POST /api/plan → 플랜 반환"""
    try:
        r = httpx.post(
            f"{BASE_URL}/api/plan",
            json={"input": "로그인 API 만들어줘"},
            timeout=TIMEOUT,
        )
        if r.status_code != 200:
            return _check("Plan API", False, f"status={r.status_code}")
        data = r.json()
        has_prompt = bool(data.get("system_prompt") or data.get("plans"))
        return _check("Plan API", has_prompt, f"mode={data.get('mode')}")
    except httpx.RequestError as e:
        return _check("Plan API", False, str(e))


def check_validate() -> bool:
    """6. POST /api/validate → PASS/FAIL"""
    try:
        plan_result = {
            "mode": "single",
            "session_id": "test",
            "post_checks": ["테스트 체크"],
            "skip_validation": True,
        }
        r = httpx.post(
            f"{BASE_URL}/api/validate",
            json={"output": "test output", "plan_result": plan_result},
            timeout=TIMEOUT,
        )
        if r.status_code != 200:
            return _check("Validate API", False, f"status={r.status_code}")
        data = r.json()
        status = data.get("status", "")
        return _check(
            "Validate API",
            status in ("PASS", "FAIL", "INCONCLUSIVE"),
            f"status={status}",
        )
    except httpx.RequestError as e:
        return _check("Validate API", False, str(e))


def main() -> int:
    print("=" * 60)
    print("AI Pipeline — Docker E2E 검증")
    print("=" * 60)
    print(f"Target: {BASE_URL}\n")

    # 서버 준비 대기
    print("Waiting for server...")
    for i in range(10):
        try:
            httpx.get(f"{BASE_URL}/health", timeout=5)
            break
        except httpx.RequestError:
            time.sleep(2)
    else:
        print("[FAIL] Server not responding after 20s")
        return 1

    print()

    results = [
        check_health(),
        check_stats(),
        check_domains(),
        check_evolution_health(),
        check_plan(),
        check_validate(),
    ]

    print()
    passed = sum(results)
    total = len(results)
    print(f"Results: {passed}/{total} passed")

    if all(results):
        print("\nAll checks PASSED!")
        return 0
    else:
        print("\nSome checks FAILED!")
        return 1


if __name__ == "__main__":
    sys.exit(main())
