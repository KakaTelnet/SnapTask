"""Check the Aim Make contract and persistent evaluation cases."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "aim-make" / "SKILL.md"
TEMPLATE = ROOT / "skills" / "aim-make" / "references" / "aim-template.md"
CASES = ROOT / "tests" / "aim-make-cases.json"
AGENT = ROOT / "skills" / "aim-make" / "agents" / "openai.yaml"
REVIEW_SKILL = ROOT / "skills" / "aim-review" / "SKILL.md"
PLAN_SKILL = ROOT / "skills" / "plan-make" / "SKILL.md"
GUIDE = ROOT / "AGENTS.md"


def require(text: str, fragments: list[str], source: str) -> list[str]:
    """Return missing required fragments for one contract source."""
    return [f"{source}: missing {item!r}" for item in fragments if item not in text]


def main() -> int:
    """Validate Maker protocol, template, and evaluation coverage."""
    failures: list[str] = []

    if not SKILL.exists():
        failures.append("skill: missing skills/aim-make/SKILL.md")
        skill_text = ""
    else:
        skill_text = SKILL.read_text(encoding="utf-8")
    if not TEMPLATE.exists():
        failures.append("template: missing references/aim-template.md")
        template_text = ""
    else:
        template_text = TEMPLATE.read_text(encoding="utf-8")

    failures.extend(require(skill_text, [
        "name: aim-make",
        "Core Boundary",
        "Progressive Summary",
        "Intake",
        "Discovery",
        "Draft",
        "$aim-review",
        "$plan-make",
        "complete aim",
        "Do not score",
        "every normative user decision in the complete aim",
        "The complete aim is the sole normative contract.",
        "背景",
        "目标用户",
        "核心价值",
        "不做的事",
        "成功标准",
        "Aim Draft",
        "Result Handling",
        "通过: Approved",
        "修订: Revision Required",
        "驳回: Rejected",
    ], "aim-make/SKILL.md"))

    failures.extend(require(template_text, [
        "背景",
        "目标用户",
        "核心价值",
        "不做的事",
        "成功标准",
    ], "aim-template.md"))

    if not CASES.exists():
        failures.append("cases: missing tests/aim-make-cases.json")
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
        modes = {c.get("mode") for c in cases}
        required_modes = {"discovery", "draft", "revision", "approved_handoff"}
        missing_modes = required_modes - modes
        if missing_modes:
            failures.append(f"cases: missing modes: {missing_modes}")

    if not AGENT.exists():
        failures.append("agent: missing agents/openai.yaml")
    else:
        agent_text = AGENT.read_text(encoding="utf-8")
        failures.extend(require(agent_text, [
            "display_name",
            "short_description",
            "default_prompt",
            "$aim-make",
            "$aim-review",
        ], "aim-make/agents/openai.yaml"))

    # PLAN_SKILL may not exist yet (future task) — skip if missing
    if PLAN_SKILL.exists():
        plan_text = PLAN_SKILL.read_text(encoding="utf-8")
        failures.extend(require(plan_text, [
            "$aim",
        ], "plan-make/SKILL.md"))

    if failures:
        print("FAILURES:")
        for f in failures:
            print(f"  - {f}")
        return 1
    print("OK: aim-make contract valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
