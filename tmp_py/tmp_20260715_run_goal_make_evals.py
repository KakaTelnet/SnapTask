"""Run fresh-context behavioral evaluations for snap-goal-make."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CASES_PATH = ROOT / "tests" / "goal-make-cases.json"
OUTPUT_DIR = Path("/private/tmp/snap-goal-make-evals")


def parse_args() -> argparse.Namespace:
    """Parse optional case selection and repeat count."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--ids", help="Comma-separated case ids; default is all cases")
    parser.add_argument("--repeat", type=int, default=1)
    return parser.parse_args()


def run_case(codex: str, case: dict[str, object], run_number: int) -> dict[str, object]:
    """Run one isolated Maker turn and validate required and forbidden markers."""
    case_id = str(case["id"])
    output_path = OUTPUT_DIR / f"{case_id}-{run_number}.txt"
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
    completed = subprocess.run(
        command,
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=300,
        check=False,
    )
    response = output_path.read_text(encoding="utf-8") if output_path.exists() else ""
    response_folded = response.casefold()
    failures: list[str] = []
    if completed.returncode != 0:
        failures.append(f"codex exit {completed.returncode}")
    for marker in case["must_include"]:
        if str(marker).casefold() not in response_folded:
            failures.append(f"missing required marker {marker!r}")
    for alternatives in case.get("must_include_any", []):
        if not any(str(marker).casefold() in response_folded for marker in alternatives):
            failures.append(f"missing every alternative marker {alternatives!r}")
    for marker in case["must_exclude"]:
        if str(marker).casefold() in response_folded:
            failures.append(f"found forbidden marker {marker!r}")
    return {
        "id": case_id,
        "run": run_number,
        "passed": not failures,
        "failures": failures,
        "output": str(output_path),
    }


def main() -> int:
    """Run selected evaluations and print a compact summary."""
    args = parse_args()
    codex = shutil.which("codex")
    if codex is None:
        raise SystemExit("codex executable not found")
    payload = json.loads(CASES_PATH.read_text(encoding="utf-8"))
    cases = payload["cases"]
    if args.ids:
        selected = set(args.ids.split(","))
        cases = [case for case in cases if case["id"] in selected]
        missing = selected - {case["id"] for case in cases}
        if missing:
            raise SystemExit(f"unknown case ids: {sorted(missing)}")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    results = [
        run_case(codex, case, run_number)
        for case in cases
        for run_number in range(1, args.repeat + 1)
    ]
    for result in results:
        marker = "PASS" if result["passed"] else "FAIL"
        print(f"{marker} {result['id']}#{result['run']}: {result['output']}")
        for failure in result["failures"]:
            print(f"  - {failure}")
    failed = sum(not result["passed"] for result in results)
    print(f"EVAL SUMMARY: {len(results) - failed}/{len(results)} passed")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
