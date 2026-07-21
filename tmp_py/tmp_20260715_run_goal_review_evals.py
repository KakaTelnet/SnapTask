"""Run fresh-context behavioral evaluations for snap-goal-review."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
from pathlib import Path

from tmp_20260717_goal_review_fixtures import load_fixture_cases


ROOT = Path(__file__).resolve().parents[1]
CASES_PATH = ROOT / "tests" / "goal-review-cases.json"
OUTPUT_DIR = Path("/private/tmp/snap-goal-review-evals")
REQUIRED_SECTIONS = (
    ("score", re.compile(r"(?im)^\**\s*(综合评分|overall score|comprehensive score)\s*:")),
    ("judgment", re.compile(r"(?im)^\**\s*(总体判断|overall judgment)\s*:")),
    ("strengths", re.compile(r"(?im)^\**\s*(做得好的地方|strengths|what works well)\s*:")),
    ("checks", re.compile(r"(?im)^\**\s*(关键检查|key checks)\s*:")),
    ("evidence map", re.compile(r"(?im)^\**\s*acceptance-to-evidence map\s*:")),
    (
        "findings",
        re.compile(
            r"(?im)^\**\s*(需要改进的地方|issues to improve|needs improvement|"
            r"what needs improvement|areas needing improvement)\s*:"
        ),
    ),
    (
        "unknowns",
        re.compile(r"(?im)^\**\s*(假设与未知项|assumptions and unknowns)\s*:"),
    ),
    (
        "remaining work",
        re.compile(r"(?im)^\**\s*remaining work and risks\s*:"),
    ),
    ("next action", re.compile(r"(?im)^\**\s*(下一步|next step)\s*:")),
)
REVISION_HEADING = re.compile(
    r"(?im)^(?:#{1,3}\s*)?\**\s*(?:separate\s+)?"
    r"(reference revision|reference goal revision|单独参考修订|参考修订|修订后的\s*goal)"
)


def parse_args() -> argparse.Namespace:
    """Parse optional case selection and repeat count."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--ids", help="Comma-separated case ids; default is all cases")
    parser.add_argument("--repeat", type=int)
    parser.add_argument(
        "--fixtures",
        action="store_true",
        help="Use tests/goal-fixtures.json instead of compact evaluation cases",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List selected cases after loading them without invoking a model",
    )
    return parser.parse_args()


def resolve_repeat(fixtures: bool, requested: int | None) -> int:
    """Return the requested run count or the stable default for the selected corpus."""
    repeat = requested if requested is not None else (3 if fixtures else 1)
    if repeat < 1:
        raise ValueError("--repeat must be at least 1")
    return repeat


def summarize_consensus(
    results: list[dict[str, object]],
) -> dict[str, dict[str, int | bool]]:
    """Aggregate isolated runs by case using a strict-majority pass threshold."""
    summary: dict[str, dict[str, int | bool]] = {}
    for result in results:
        case_id = str(result["id"])
        case_summary = summary.setdefault(
            case_id,
            {"passed_runs": 0, "total_runs": 0, "required_passes": 0, "passed": False},
        )
        case_summary["total_runs"] = int(case_summary["total_runs"]) + 1
        if bool(result["passed"]):
            case_summary["passed_runs"] = int(case_summary["passed_runs"]) + 1

    for case_summary in summary.values():
        required_passes = int(case_summary["total_runs"]) // 2 + 1
        case_summary["required_passes"] = required_passes
        case_summary["passed"] = int(case_summary["passed_runs"]) >= required_passes
    return summary


def language_instruction(language: str) -> str:
    """Return a deterministic response-language instruction."""
    if language == "en":
        return "Respond in English while preserving the exact bilingual verdict labels."
    return "Respond in Chinese while preserving the exact bilingual verdict labels."


def review_case(codex: str, case: dict[str, object], run_number: int) -> dict[str, object]:
    """Run one isolated review and validate its external contract."""
    case_id = str(case["id"])
    output_path = OUTPUT_DIR / f"{case_id}-{run_number}.txt"
    prompt = (
        "First read and follow skills/snap-goal-review/SKILL.md and every reference it "
        "requires. Do not inspect unrelated repository files. Review only and do not "
        "rewrite unless the request explicitly asks for a separate reference revision. "
        f"{language_instruction(str(case['language']))}\n\n"
        f"Goal under review:\n{case['goal']}"
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
    completed = subprocess.run(
        command,
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=240,
        check=False,
    )
    response = output_path.read_text(encoding="utf-8") if output_path.exists() else ""
    failures: list[str] = []
    expected_status = str(case["expected_status"])
    first_line = response.strip().splitlines()[0] if response.strip() else ""

    if completed.returncode != 0:
        failures.append(f"codex exit {completed.returncode}")
    if expected_status not in first_line:
        failures.append(f"first line {first_line!r} does not contain {expected_status!r}")
    for section_name, pattern in REQUIRED_SECTIONS:
        if pattern.search(response) is None:
            failures.append(f"missing semantic section {section_name!r}")

    has_revision = bool(REVISION_HEADING.search(response))
    if bool(case["allow_reference_revision"]) != has_revision:
        failures.append(
            f"reference revision expected={case['allow_reference_revision']} observed={has_revision}"
        )

    return {
        "id": case_id,
        "run": run_number,
        "passed": not failures,
        "failures": failures,
        "first_line": first_line,
        "output": str(output_path),
    }


def main() -> int:
    """Run selected evaluations and print a compact summary."""
    args = parse_args()
    try:
        repeat = resolve_repeat(args.fixtures, args.repeat)
    except ValueError as error:
        raise SystemExit(str(error)) from error
    if args.fixtures:
        cases = load_fixture_cases()
    else:
        payload = json.loads(CASES_PATH.read_text(encoding="utf-8"))
        cases = payload["cases"]
    if args.ids:
        selected = set(args.ids.split(","))
        cases = [case for case in cases if case["id"] in selected]
        missing = selected - {case["id"] for case in cases}
        if missing:
            raise SystemExit(f"unknown case ids: {sorted(missing)}")

    if args.list:
        for case in cases:
            print(f"{case['id']}: {case['expected_status']}")
        print(f"CASE SUMMARY: {len(cases)} loaded")
        return 0

    codex = shutil.which("codex")
    if codex is None:
        raise SystemExit("codex executable not found")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    results = [
        review_case(codex, case, run_number)
        for case in cases
        for run_number in range(1, repeat + 1)
    ]
    for result in results:
        marker = "PASS" if result["passed"] else "FAIL"
        print(f"{marker} {result['id']}#{result['run']}: {result['first_line']}")
        for failure in result["failures"]:
            print(f"  - {failure}")

    failed_runs = sum(not result["passed"] for result in results)
    print(f"RUN SUMMARY: {len(results) - failed_runs}/{len(results)} passed")

    consensus = summarize_consensus(results)
    for case_id, case_summary in consensus.items():
        marker = "PASS" if case_summary["passed"] else "FAIL"
        print(
            f"{marker} CONSENSUS {case_id}: "
            f"{case_summary['passed_runs']}/{case_summary['total_runs']} runs passed "
            f"({case_summary['required_passes']} required)"
        )
    failed_cases = sum(not bool(item["passed"]) for item in consensus.values())
    print(
        f"EVAL SUMMARY: {len(consensus) - failed_cases}/{len(consensus)} cases "
        "passed by consensus"
    )
    return 1 if failed_cases else 0


if __name__ == "__main__":
    raise SystemExit(main())
