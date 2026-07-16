"""Check the Snap Goal Make contract and persistent evaluation cases."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "snap-goal-make" / "SKILL.md"
TEMPLATE = ROOT / "skills" / "snap-goal-make" / "references" / "goal-template.md"
CASES = ROOT / "tests" / "goal-make-cases.json"

AGENT = ROOT / "skills" / "snap-goal-make" / "agents" / "openai.yaml"
REVIEW_SKILL = ROOT / "skills" / "snap-goal-review" / "SKILL.md"
TASK_SKILL = ROOT / "skills" / "task-decompose" / "SKILL.md"
PLUGIN = ROOT / ".codex-plugin" / "plugin.json"
GUIDE = ROOT / "AGENTS.md"

def require(text: str, fragments: list[str], source: str) -> list[str]:
    """Return missing required fragments for one contract source."""
    return [f"{source}: missing {item!r}" for item in fragments if item not in text]


def main() -> int:
    """Validate Maker protocol, template, and evaluation coverage."""
    failures: list[str] = []
    if not SKILL.exists():
        failures.append("skill: missing skills/snap-goal-make/SKILL.md")
        skill_text = ""
    else:
        skill_text = SKILL.read_text(encoding="utf-8")
    if not TEMPLATE.exists():
        failures.append("template: missing references/goal-template.md")
        template_text = ""
    else:
        template_text = TEMPLATE.read_text(encoding="utf-8")

    failures.extend(require(skill_text, [
        "name: snap-goal-make",
        "Progressive Summary",
        "Authorized Context",
        "Outcome Goal",
        "Bounded Investigation Goal",
        "$snap-goal-review",
        "$task-decompose",
        "Unreviewed Draft",
        "complete Goal",
        "Do not score",
        "Do not create, require, or simulate a programmatic JSON review return.",
        "Consume snap-goal-review's existing human-readable contract.",
    ], "snap-goal-make/SKILL.md"))
    failures.extend(require(template_text, [
        "Goal Type",
        "Background and Value",
        "Acceptance Criteria",
        "Completion Evidence",
        "Scope and Authority",
        "Constraints and Priorities",
        "Sources of Truth",
        "Assumptions and Unknowns",
        "Stop and Escalation Conditions",
        "Completion Report Requirements",
        "Unfinished",
        "Unverifiable",
        "Blocked",
        "Out of scope",
        "Residual risks",
    ], "goal-template.md"))

    payload = json.loads(CASES.read_text(encoding="utf-8"))
    cases = payload["cases"]
    expected_ids = {
        "discovery-vague-outcome-zh",
        "context-aware-software-zh",
        "bounded-investigation-draft-zh",
        "labeled-low-risk-assumption-zh",
        "source-conflict-zh",
        "oversized-goal-zh",
        "existing-draft-gap-zh",
        "revision-complete-regeneration-zh",
        "rejected-redefine-zh",
        "approved-unchanged-handoff-zh",
        "unreviewed-draft-zh",
        "role-only-when-relevant-zh",
        "maker-never-judges-en",
        "flexible-compact-goal-zh",
    }
    observed_ids = {str(case["id"]) for case in cases}
    if observed_ids != expected_ids:
        failures.append(f"cases: ids differ: {sorted(observed_ids ^ expected_ids)}")
    for case in cases:
        for key in ("id", "mode", "language", "input", "must_include", "must_exclude"):
            if key not in case:
                failures.append(f"cases: {case.get('id', '<unknown>')} missing {key}")

    maker_case = next(
        (case for case in cases if case.get("id") == "maker-never-judges-en"),
        None,
    )
    if maker_case is not None:
        maker_input = str(maker_case["input"])
        for marker in (
            "human-readable review contract",
            "programmatic JSON review return",
        ):
            if marker not in maker_input:
                failures.append(f"cases: maker-never-judges-en missing marker {marker!r}")

    agent_text = AGENT.read_text(encoding="utf-8") if AGENT.exists() else ""
    review_text = REVIEW_SKILL.read_text(encoding="utf-8")
    task_text = TASK_SKILL.read_text(encoding="utf-8")
    plugin = json.loads(PLUGIN.read_text(encoding="utf-8"))
    guide_text = GUIDE.read_text(encoding="utf-8")
    failures.extend(require(agent_text, [
        'display_name: "Snap Goal Make"',
        "$snap-goal-make",
    ], "snap-goal-make/agents/openai.yaml"))
    failures.extend(require(review_text, [
        "return findings to `$snap-goal-make`",
    ], "snap-goal-review/SKILL.md"))
    if "`$snap-goal`" in review_text:
        failures.append("snap-goal-review/SKILL.md: obsolete $snap-goal handoff remains")
    failures.extend(require(task_text, [
        "return the Goal to `$snap-goal-make`",
    ], "task-decompose/SKILL.md"))
    if "`$snap-goal`" in task_text:
        failures.append("task-decompose/SKILL.md: obsolete $snap-goal handoff remains")
    if plugin.get("version") != "0.2.0":
        failures.append(f"plugin: expected version 0.2.0, got {plugin.get('version')!r}")
    plugin_text = json.dumps(plugin, ensure_ascii=False)
    failures.extend(require(plugin_text, [
        "Goal creation",
        "Create a Goal through guided conversation.",
    ], ".codex-plugin/plugin.json"))
    failures.extend(require(guide_text, [
        "skills/snap-goal-make/",
        "goal-make-cases.json",
    ], "AGENTS.md"))

    if failures:
        print("GOAL MAKE CONTRACT FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print(f"GOAL MAKE CONTRACT PASS: {len(cases)} evaluation cases")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
