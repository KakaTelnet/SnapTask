"""Check the Snap Goal Review contract and persistent evaluation cases."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "snap-goal-review" / "SKILL.md"
RUBRIC = ROOT / "skills" / "snap-goal-review" / "references" / "review-rubric.md"
TASK_SKILL = ROOT / "skills" / "task-decompose" / "SKILL.md"
CASES = ROOT / "tests" / "goal-review-cases.json"
PLUGIN = ROOT / ".codex-plugin" / "plugin.json"


def require(text: str, fragments: list[str], source: str) -> list[str]:
    """Return missing required fragments for one contract source."""
    return [f"{source}: missing {fragment!r}" for fragment in fragments if fragment not in text]


def main() -> int:
    """Validate required review behavior and evaluation coverage."""
    skill_text = SKILL.read_text(encoding="utf-8")
    rubric_text = RUBRIC.read_text(encoding="utf-8")
    task_text = TASK_SKILL.read_text(encoding="utf-8")
    payload = json.loads(CASES.read_text(encoding="utf-8"))
    cases = payload["cases"]

    failures: list[str] = []
    failures.extend(require(skill_text, [
        "effort-only",
        "bounded investigation",
        "Handoff Contract",
        "$snap-goal",
        "task-decompose",
        "Acceptance-to-evidence map",
        "Unfinished",
        "Unverifiable",
        "Blocked",
        "Out of scope",
        "Residual risks",
    ], "SKILL.md"))
    failures.extend(require(rubric_text, [
        "Remaining-work visibility",
        "Source-of-truth priority",
        "Trade-off priority",
        "no new evidence",
        "no reduced blocker",
        "no reasonable alternative",
        "one-to-one",
        "Over-prescription",
    ], "review-rubric.md"))
    failures.extend(require(task_text, [
        "Goal Handoff",
        "通过: Approved",
        "修订: Revision Required",
        "驳回: Rejected",
    ], "task-decompose/SKILL.md"))

    if not PLUGIN.exists():
        failures.append("plugin: missing .codex-plugin/plugin.json")
    else:
        plugin = json.loads(PLUGIN.read_text(encoding="utf-8"))
        if plugin.get("name") != "snaptask":
            failures.append(f"plugin: unexpected name {plugin.get('name')!r}")
        if plugin.get("skills") != "./skills/":
            failures.append(f"plugin: unexpected skills path {plugin.get('skills')!r}")

    statuses = {case["expected_status"] for case in cases}
    languages = {case["language"] for case in cases}
    expected = {"\u901a\u8fc7: Approved", "\u4fee\u8ba2: Revision Required", "\u9a73\u56de: Rejected"}
    if statuses != expected:
        failures.append(f"cases: statuses differ: {statuses}")
    if not {"zh", "en", "mixed"}.issubset(languages):
        failures.append(f"cases: language coverage incomplete: {languages}")
    if len(cases) < 10:
        failures.append(f"cases: expected at least 10, got {len(cases)}")
    if not any(case["allow_reference_revision"] for case in cases):
        failures.append("cases: missing explicit reference-revision scenario")
    if not any("pressure" in case["id"] for case in cases):
        failures.append("cases: missing approval-pressure scenario")

    if failures:
        print("CONTRACT FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print(f"CONTRACT PASS: {len(cases)} evaluation cases")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
