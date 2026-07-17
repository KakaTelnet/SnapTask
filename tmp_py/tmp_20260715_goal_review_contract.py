"""Check the Snap Goal Review contract and persistent evaluation cases."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from tmp_20260717_goal_review_fixtures import FIXTURE_DIR, load_fixture_cases


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "snap-goal-review" / "SKILL.md"
RUBRIC = ROOT / "skills" / "snap-goal-review" / "references" / "review-rubric.md"
TASK_SKILL = ROOT / "skills" / "task-decompose" / "SKILL.md"
CASES = ROOT / "tests" / "goal-review-cases.json"
PLUGIN = ROOT / ".codex-plugin" / "plugin.json"
SKILL_CN = ROOT / "skills" / "snap-goal-review" / "skill_cn.md"
RUBRIC_CN = ROOT / "skills" / "snap-goal-review" / "references" / "review-rubric_cn.md"


def require(text: str, fragments: list[str], source: str) -> list[str]:
    """Return missing required fragments for one contract source."""
    return [f"{source}: missing {fragment!r}" for fragment in fragments if fragment not in text]


def main() -> int:
    """Validate required review behavior and evaluation coverage."""
    skill_text = SKILL.read_text(encoding="utf-8")
    rubric_text = RUBRIC.read_text(encoding="utf-8")
    task_text = TASK_SKILL.read_text(encoding="utf-8")
    skill_cn_text = SKILL_CN.read_text(encoding="utf-8")
    rubric_cn_text = RUBRIC_CN.read_text(encoding="utf-8")
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
    failures.extend(require(skill_cn_text, [
        "只审核，不重写",
        "8 个硬门槛",
        "10-12 分",
        "snap-goal-make",
        "Acceptance-to-evidence map",
        "Unfinished",
        "Unverifiable",
        "Blocked",
        "Out of scope",
        "Residual risks",
    ], "skill_cn.md"))
    failures.extend(require(rubric_cn_text, [
        "只有所有 8 个硬门槛都满足",
        "事实来源优先级",
        "取舍优先级",
        "没有新证据",
        "没有减少阻塞",
        "没有合理替代路径",
        "一一对应",
        "过度规定实现",
    ], "review-rubric_cn.md"))

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

    try:
        fixture_cases = load_fixture_cases()
    except (KeyError, OSError, TypeError, ValueError, json.JSONDecodeError) as error:
        fixture_cases = []
        failures.append(f"fixtures: {error}")

    fixture_ids = [str(case["id"]) for case in fixture_cases]
    fixture_paths = [Path(str(case["fixture_path"])) for case in fixture_cases]
    expected_files = set(FIXTURE_DIR.iterdir()) if FIXTURE_DIR.exists() else set()
    if len(fixture_cases) != 10:
        failures.append(f"fixtures: expected 10 cases, got {len(fixture_cases)}")
    if len(fixture_ids) != len(set(fixture_ids)):
        failures.append("fixtures: case ids must be unique")
    if set(fixture_paths) != expected_files:
        failures.append("fixtures: manifest paths do not exactly cover goal-fixtures/")
    fixture_statuses = Counter(str(case["expected_status"]) for case in fixture_cases)
    expected_distribution = Counter({
        "通过: Approved": 3,
        "修订: Revision Required": 5,
        "驳回: Rejected": 2,
    })
    if fixture_statuses != expected_distribution:
        failures.append(f"fixtures: unexpected status distribution {fixture_statuses}")
    suffixes = {path.suffix for path in fixture_paths}
    if suffixes != {".json", ".md", ".txt", ".yaml"}:
        failures.append(f"fixtures: format coverage differs: {suffixes}")
    if any(len(str(case["goal"])) < 80 for case in fixture_cases):
        failures.append("fixtures: extracted Goal payload is unexpectedly short")
    if any("测试元数据" in str(case["goal"]) for case in fixture_cases):
        failures.append("fixtures: extracted Goal contains test metadata")

    if failures:
        print("CONTRACT FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print(
        f"CONTRACT PASS: {len(cases)} evaluation cases; "
        f"FIXTURE PASS: {len(fixture_cases)} multi-format cases"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
