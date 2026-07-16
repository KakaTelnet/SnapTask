"""Run fresh-context behavioral evaluations for snap-goal-make."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CASES_PATH = ROOT / "tests" / "goal-make-cases.json"
OUTPUT_DIR = Path("/private/tmp/snap-goal-make-evals")
CANONICAL_HEADINGS = {
    "en": (
        "Goal Type",
        "Background and Value",
        "Goal",
        "Acceptance Criteria",
        "Completion Evidence",
        "Scope and Authority",
        "Constraints and Priorities",
        "Sources of Truth",
        "Assumptions and Unknowns",
        "Stop and Escalation Conditions",
        "Completion Report Requirements",
    ),
    "zh": (
        "Goal 类型",
        "背景与价值",
        "目标",
        "验收标准",
        "完成证据",
        "范围与权限",
        "约束与优先级",
        "事实来源",
        "假设与未知项",
        "停止与升级条件",
        "完成报告要求",
    ),
}
MAKER_JUDGMENT_PATTERNS = (
    r"(?im)^\s*(?:(?:overall|综合)\s*)?(?:score|评分)\s*[:：]?\s*\d+(?:\.\d+)?\s*/\s*\d+(?:\.\d+)?\s*$",
    r"(?im)^\s*(?:review result|审核结果)\s*[:：].*$",
    r"(?im)^\s*(?:[-*]\s*)?(?:(?:通过|修订|驳回)\s*[:：]\s*)?(?:Approved|Revision Required|Rejected)(?:\s*(?:[/|]|\(|（)\s*(?:通过|修订|驳回)\s*[)）]?)?\s*[。.!]?\s*$",
)


def parse_args() -> argparse.Namespace:
    """Parse evaluation, retained-output validation, and self-test modes."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--ids", help="Comma-separated case ids; default is all cases")
    parser.add_argument("--repeat", type=int, default=1)
    parser.add_argument(
        "--validate-existing",
        action="store_true",
        help="Validate retained output files without invoking Codex",
    )
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="Run focused response-validator tests without invoking Codex",
    )
    args = parser.parse_args()
    if args.repeat < 1:
        parser.error("--repeat must be at least 1")
    if args.validate_existing and args.self_test:
        parser.error("--validate-existing and --self-test cannot be combined")
    return args


def select_cases(args: argparse.Namespace) -> list[dict[str, object]]:
    """Load cases and apply an optional exact id filter."""
    payload = json.loads(CASES_PATH.read_text(encoding="utf-8"))
    cases = list(payload["cases"])
    if not args.ids:
        return cases
    selected = set(args.ids.split(","))
    filtered = [case for case in cases if case["id"] in selected]
    missing = selected - {case["id"] for case in filtered}
    if missing:
        raise SystemExit(f"unknown case ids: {sorted(missing)}")
    return filtered


def normalize_heading(line: str) -> str:
    """Accept common Markdown heading and bold heading formatting."""
    candidate = re.sub(r"^\s{0,3}#{1,6}\s+", "", line.strip())
    candidate = candidate.rstrip(":：").strip()
    if candidate.startswith("**") and candidate.endswith("**"):
        candidate = candidate[2:-2].strip()
    return candidate.rstrip(":：").strip()


def heading_counts(response: str, language: str) -> dict[str, int]:
    """Return exact canonical-heading counts without substring matching."""
    headings = CANONICAL_HEADINGS[language]
    counts = {heading: 0 for heading in headings}
    for line in response.splitlines():
        heading = normalize_heading(line)
        if heading in counts:
            counts[heading] += 1
    return counts


def validate_complete_goal(response: str, language: str) -> list[str]:
    """Require every canonical Goal heading exactly once."""
    failures: list[str] = []
    for heading, count in heading_counts(response, language).items():
        if count != 1:
            failures.append(f"canonical heading {heading!r} appears {count} times; expected exactly once")
    return failures


def validate_handoff_goal(response: str, case: dict[str, object]) -> list[str]:
    """Require an unchanged complete Goal as the entire pre-handoff block."""
    goal_text = str(case["goal_text"]).strip()
    marker = "审核结果与证据要求:"
    failures: list[str] = []
    if marker not in response:
        return [f"missing handoff marker {marker!r}"]
    pre_handoff, _ = response.split(marker, 1)
    if pre_handoff.strip() != goal_text:
        failures.append("pre-handoff Goal block is not exactly goal_text")
    if response.count(goal_text) != 1:
        failures.append("goal_text must appear exactly once in the handoff")
    failures.extend(validate_complete_goal(pre_handoff.strip(), str(case["language"])))
    failures.extend(validate_complete_goal(response, str(case["language"])))
    return failures


def validate_response(response: str, case: dict[str, object]) -> list[str]:
    """Validate one Maker response using structured case flags."""
    response_folded = response.casefold()
    failures: list[str] = []
    for marker in case["must_include"]:
        if str(marker).casefold() not in response_folded:
            failures.append(f"missing required marker {marker!r}")
    for alternatives in case.get("must_include_any", []):
        if not any(str(marker).casefold() in response_folded for marker in alternatives):
            failures.append(f"missing every alternative marker {alternatives!r}")
    for pattern in case.get("must_match", []):
        if re.search(str(pattern), response, re.IGNORECASE | re.MULTILINE) is None:
            failures.append(f"missing required semantic pattern {pattern!r}")
    for marker in case["must_exclude"]:
        if str(marker).casefold() in response_folded:
            failures.append(f"found forbidden marker {marker!r}")
    if case.get("requires_complete_goal"):
        failures.extend(validate_complete_goal(response, str(case["language"])))
    if case.get("requires_exact_handoff_goal"):
        failures.extend(validate_handoff_goal(response, case))
    if case.get("reject_maker_judgment"):
        for pattern in MAKER_JUDGMENT_PATTERNS:
            if re.search(pattern, response) is not None:
                failures.append(f"found forbidden Maker judgment pattern {pattern!r}")
    return failures


def concise_diagnostic(value: object) -> str:
    """Return at most 4,000 characters of process diagnostics."""
    if isinstance(value, bytes):
        value = value.decode("utf-8", errors="replace")
    return str(value or "")[-4000:]


def unlink_artifact(path: Path) -> None:
    """Remove a deterministic artifact before a fresh live evaluation."""
    if path.exists():
        path.unlink()


def run_case(codex: str, case: dict[str, object], run_number: int) -> dict[str, object]:
    """Run one isolated Maker turn and keep timeout/stderr evidence per case."""
    case_id = str(case["id"])
    output_path = OUTPUT_DIR / f"{case_id}-{run_number}.txt"
    stderr_path = OUTPUT_DIR / f"{case_id}-{run_number}.stderr.txt"
    unlink_artifact(output_path)
    unlink_artifact(stderr_path)
    goal_text = str(case.get("goal_text", ""))
    prompt = (
        "First read and follow skills/snap-goal-make/SKILL.md and every reference it "
        "requires. Read only repository files authorized by the user input. Treat the "
        "following as the current turn of a Goal-making conversation. Do not perform "
        "independent Goal review.\n\n"
        f"Expected conversation entry: {case['mode']}\n"
        f"Response language: {case['language']}\n"
        f"Current confirmed Goal when supplied:\n{goal_text}\n\n"
        f"User input:\n{case['input']}"
    )
    command = [
        codex,
        "exec",
        "--ephemeral",
        "--ignore-user-config",
        "--sandbox",
        "read-only",
        "--color",
        "never",
        "--cd",
        str(ROOT),
        "--output-last-message",
        str(output_path),
        prompt,
    ]
    failures: list[str] = []
    try:
        completed = subprocess.run(
            command,
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=300,
            check=False,
        )
    except subprocess.TimeoutExpired as error:
        stderr_path.write_text(
            f"timeout after 300 seconds\n{concise_diagnostic(error.stderr)}",
            encoding="utf-8",
        )
        failures.append("codex timeout after 300 seconds")
    else:
        stderr_path.write_text(
            f"exit {completed.returncode}\n{concise_diagnostic(completed.stderr)}",
            encoding="utf-8",
        )
        if completed.returncode != 0:
            failures.append(f"codex exit {completed.returncode}")
    response = output_path.read_text(encoding="utf-8") if output_path.exists() else ""
    failures.extend(validate_response(response, case))
    return {
        "id": case_id,
        "run": run_number,
        "passed": not failures,
        "failures": failures,
        "output": str(output_path),
        "stderr": str(stderr_path),
    }


def validate_existing(
    cases: list[dict[str, object]],
    repeat: int,
) -> list[dict[str, object]]:
    """Revalidate exactly the selected retained case/run outputs."""
    results: list[dict[str, object]] = []
    for case in cases:
        case_id = str(case["id"])
        for run_number in range(1, repeat + 1):
            output_path = OUTPUT_DIR / f"{case_id}-{run_number}.txt"
            failures = (
                validate_response(output_path.read_text(encoding="utf-8"), case)
                if output_path.exists()
                else [f"missing retained output {output_path.name!r}"]
            )
            results.append({
                "id": case_id,
                "run": run_number,
                "passed": not failures,
                "failures": failures,
                "output": str(output_path),
            })
    return results


def run_self_tests() -> int:
    """Exercise complete-Goal, handoff, and Maker-verdict validator failures."""
    complete_goal = "\n\n".join(
        f"{heading}:\ncontent" for heading in CANONICAL_HEADINGS["en"]
    )
    complete_case = {
        "language": "en",
        "must_include": [],
        "must_exclude": [],
        "requires_complete_goal": True,
        "reject_maker_judgment": True,
    }
    checks = [
        ("accepts complete Goal", complete_goal, complete_case, True),
        ("rejects missing canonical heading", complete_goal.replace("Goal:\ncontent\n\n", ""), complete_case, False),
        ("rejects score verdict", f"{complete_goal}\n\nScore: 9/10", complete_case, False),
        ("rejects non-decimal score verdict", f"{complete_goal}\n\nOverall score: 9/12", complete_case, False),
        ("rejects review-result verdict", f"{complete_goal}\n\nReview result: Approved", complete_case, False),
    ]
    handoff_case = next(
        case for case in select_cases(argparse.Namespace(ids=None))
        if case["id"] == "approved-unchanged-handoff-zh"
    )
    handoff_goal = str(handoff_case["goal_text"])
    handoff_response = (
        f"{handoff_goal}\n\n审核结果与证据要求:\n通过: Approved。\n\n"
        "下一步:\n- 交给 $task-decompose。"
    )
    checks.extend([
        ("accepts exact handoff Goal", handoff_response, handoff_case, True),
        ("rejects second Goal block", f"{handoff_response}\n\n目标:\n重复", handoff_case, False),
    ])
    failures: list[str] = []
    for name, response, case, expected_pass in checks:
        passed = not validate_response(response, case)
        if passed != expected_pass:
            failures.append(name)
    if failures:
        print("VALIDATOR SELF-TEST FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print(f"VALIDATOR SELF-TEST PASS: {len(checks)} checks")
    return 0


def print_results(results: list[dict[str, object]], label: str) -> int:
    """Print a compact result summary and return a shell-compatible status."""
    for result in results:
        marker = "PASS" if result["passed"] else "FAIL"
        print(f"{marker} {result['id']}#{result['run']}: {result['output']}")
        for failure in result["failures"]:
            print(f"  - {failure}")
    failed = sum(not result["passed"] for result in results)
    print(f"{label}: {len(results) - failed}/{len(results)} passed")
    return 1 if failed else 0


def main() -> int:
    """Run selected evaluations or validate retained output artifacts."""
    args = parse_args()
    if args.self_test:
        return run_self_tests()
    cases = select_cases(args)
    if args.validate_existing:
        return print_results(validate_existing(cases, args.repeat), "RETAINED SUMMARY")
    codex = shutil.which("codex")
    if codex is None:
        raise SystemExit("codex executable not found")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    results = [
        run_case(codex, case, run_number)
        for case in cases
        for run_number in range(1, args.repeat + 1)
    ]
    return print_results(results, "EVAL SUMMARY")


if __name__ == "__main__":
    raise SystemExit(main())
