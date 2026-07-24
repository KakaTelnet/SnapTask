"""Check the Aim Review contract and persistent evaluation cases."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "aim-review" / "SKILL.md"
RUBRIC = ROOT / "skills" / "aim-review" / "references" / "aim-review-rubric.md"
CASES = ROOT / "tests" / "aim-review-cases.json"
AGENT = ROOT / "skills" / "aim-review" / "agents" / "openai.yaml"
MAKER_SKILL = ROOT / "skills" / "aim-make" / "SKILL.md"
GUIDE = ROOT / "AGENTS.md"


def require(text: str, fragments: list[str], source: str) -> list[str]:
    """Return missing required fragments for one contract source."""
    return [f"{source}: missing {item!r}" for item in fragments if item not in text]


def main() -> int:
    """Validate Reviewer contract, rubric, and evaluation coverage."""
    failures: list[str] = []

    if not SKILL.exists():
        failures.append("skill: missing skills/aim-review/SKILL.md")
        skill_text = ""
    else:
        skill_text = SKILL.read_text(encoding="utf-8")
    if not RUBRIC.exists():
        failures.append("rubric: missing references/aim-review-rubric.md")
        rubric_text = ""
    else:
        rubric_text = RUBRIC.read_text(encoding="utf-8")

    failures.extend(require(skill_text, [
        "name: aim-review",
        "Review Workflow",
        "Handoff Contract",
        "Judgment Rules",
        "Output Contract",
        "$aim-make",
        "$plan-make",
        "通过: Approved",
        "修订: Revision Required",
        "驳回: Rejected",
        "审核结果",
        "综合评分",
        "关键检查",
        "做得好的地方",
        "需要改进的地方",
        "下一步",
    ], "aim-review/SKILL.md"))

    failures.extend(require(rubric_text, [
        "Hard Gates",
        "Background clarity",
        "Target users identified",
        "Core value stated",
        "Boundaries explicit",
        "Success criteria observable",
        "已满足",
        "需要修订",
        "暂无法判断",
        "Scoring",
        "Direction clarity",
        "User relevance",
        "Scope discipline",
        "Success measurability",
        "Internal consistency",
        "Result Selection",
        "Finding Quality",
    ], "aim-review-rubric.md"))

    if not CASES.exists():
        failures.append("cases: missing tests/aim-review-cases.json")
    else:
        payload = json.loads(CASES.read_text(encoding="utf-8"))
        if payload.get("schema_version") != 1:
            failures.append("cases: schema_version must be 1")
        cases = payload.get("cases", [])
        if len(cases) < 5:
            failures.append(f"cases: need at least 5 cases, got {len(cases)}")
        ids = [c.get("id") for c in cases]
        if len(set(ids)) != len(ids):
            failures.append("cases: duplicate ids found")
        statuses = [c.get("expected_status") for c in cases]
        for required in ["通过: Approved", "修订: Revision Required", "驳回: Rejected"]:
            if required not in statuses:
                failures.append(f"cases: missing expected_status {required!r}")

    if not AGENT.exists():
        failures.append("agent: missing agents/openai.yaml")
    else:
        agent_text = AGENT.read_text(encoding="utf-8")
        failures.extend(require(agent_text, [
            "display_name",
            "short_description",
            "default_prompt",
            "$aim-review",
        ], "aim-review/agents/openai.yaml"))

    if failures:
        print("FAILURES:")
        for f in failures:
            print(f"  - {f}")
        return 1
    print("OK: aim-review contract valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
