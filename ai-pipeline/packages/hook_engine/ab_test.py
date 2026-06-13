"""A/B Test Framework — 스킬 조합 비교 테스트.

Usage:
    manager = ABTestManager()
    test_id = manager.create_test("auth-skills-v2", "development.backend",
                                   ["dev.backend.auth.role", "dev.backend.auth.jwt-auth"],
                                   ["dev.backend.auth.role", "dev.backend.auth.jwt-auth", "dev.backend.auth.verify"])
    variant = manager.get_variant(test_id)  # "A" or "B"
    # ... use variant's skills ...
    manager.record_result(test_id, variant, "PASS")
    results = manager.get_results(test_id)
"""

from __future__ import annotations

import json
import random
import threading
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"
AB_TESTS_FILE = DATA_DIR / "ab_tests.json"


@dataclass
class ABTestResult:
    """Result of a single A/B test evaluation."""
    variant: str  # "A" or "B"
    status: str  # "PASS", "FAIL", "INCONCLUSIVE"
    timestamp: str = ""

    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now(timezone.utc).isoformat()


@dataclass
class ABTest:
    """A/B test definition."""
    test_id: str
    name: str
    domain: str
    variant_a_skills: list[str]
    variant_b_skills: list[str]
    status: str = "active"  # active, completed, paused
    results: list[dict] = field(default_factory=list)
    created_at: str = ""

    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now(timezone.utc).isoformat()


class ABTestManager:
    """Manages A/B tests for skill combinations."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._tests: dict[str, ABTest] = {}
        self._load()

    def _load(self) -> None:
        """Load tests from JSON file."""
        if AB_TESTS_FILE.exists():
            try:
                data = json.loads(AB_TESTS_FILE.read_text(encoding="utf-8"))
                for t in data.get("tests", []):
                    test = ABTest(**{k: v for k, v in t.items() if k in ABTest.__dataclass_fields__})
                    self._tests[test.test_id] = test
            except (json.JSONDecodeError, OSError):
                pass

    def _save(self) -> None:
        """Save tests to JSON file."""
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        data = {"tests": [asdict(t) for t in self._tests.values()]}
        AB_TESTS_FILE.write_text(
            json.dumps(data, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    def create_test(
        self,
        name: str,
        domain: str,
        variant_a_skills: list[str],
        variant_b_skills: list[str],
    ) -> str:
        """Create a new A/B test. Returns test_id."""
        test_id = f"ab-{len(self._tests) + 1:03d}"
        test = ABTest(
            test_id=test_id,
            name=name,
            domain=domain,
            variant_a_skills=variant_a_skills,
            variant_b_skills=variant_b_skills,
        )
        with self._lock:
            self._tests[test_id] = test
            self._save()
        return test_id

    def get_variant(self, test_id: str) -> str:
        """Get a random variant for a test. Returns 'A' or 'B'."""
        with self._lock:
            test = self._tests.get(test_id)
            if not test or test.status != "active":
                return "A"  # default
        return random.choice(["A", "B"])

    def get_skills_for_variant(self, test_id: str, variant: str) -> list[str]:
        """Get skill IDs for a specific variant."""
        with self._lock:
            test = self._tests.get(test_id)
            if not test:
                return []
            if variant == "A":
                return list(test.variant_a_skills)
            return list(test.variant_b_skills)

    def record_result(self, test_id: str, variant: str, status: str) -> None:
        """Record a test result."""
        result = ABTestResult(variant=variant, status=status)
        with self._lock:
            test = self._tests.get(test_id)
            if test:
                test.results.append(asdict(result))
                self._save()

    def get_results(self, test_id: str) -> dict:
        """Get aggregated results for a test."""
        with self._lock:
            test = self._tests.get(test_id)
            if not test:
                return {"error": f"Test not found: {test_id}"}

            results_a = [r for r in test.results if r["variant"] == "A"]
            results_b = [r for r in test.results if r["variant"] == "B"]

            pass_a = sum(1 for r in results_a if r["status"] == "PASS")
            pass_b = sum(1 for r in results_b if r["status"] == "PASS")

            rate_a = pass_a / len(results_a) if results_a else 0
            rate_b = pass_b / len(results_b) if results_b else 0

            winner = "inconclusive"
            if len(results_a) >= 5 and len(results_b) >= 5:
                if rate_a > rate_b + 0.1:
                    winner = "A"
                elif rate_b > rate_a + 0.1:
                    winner = "B"
                else:
                    winner = "tie"

            return {
                "test_id": test_id,
                "name": test.name,
                "domain": test.domain,
                "status": test.status,
                "variant_a": {
                    "skills": test.variant_a_skills,
                    "sample_size": len(results_a),
                    "pass_rate": round(rate_a, 3),
                },
                "variant_b": {
                    "skills": test.variant_b_skills,
                    "sample_size": len(results_b),
                    "pass_rate": round(rate_b, 3),
                },
                "winner": winner,
            }

    def list_tests(self, status: str = "") -> list[dict]:
        """List all tests, optionally filtered by status."""
        with self._lock:
            tests = list(self._tests.values())
        if status:
            tests = [t for t in tests if t.status == status]
        return [
            {
                "test_id": t.test_id,
                "name": t.name,
                "domain": t.domain,
                "status": t.status,
                "sample_size": len(t.results),
            }
            for t in tests
        ]

    def get_active_test_for_domain(self, domain: str) -> ABTest | None:
        """Get active A/B test for a domain, if any."""
        with self._lock:
            for test in self._tests.values():
                if test.status == "active" and test.domain == domain:
                    return test
        return None


# Singleton
_manager: ABTestManager | None = None


def get_ab_manager() -> ABTestManager:
    """Get singleton ABTestManager."""
    global _manager
    if _manager is None:
        _manager = ABTestManager()
    return _manager
