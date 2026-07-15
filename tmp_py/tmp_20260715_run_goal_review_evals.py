"""Run fresh-context behavioral evaluations for snap-goal-review."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
from pathlib import Path


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
    parser.add_argument("--repeat", type=int, default=1)
    return parser.parse_args()


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
        review_case(codex, case, run_number)
        for case in cases
        for run_number in range(1, args.repeat + 1)
    ]
    for result in results:
        marker = "PASS" if result["passed"] else "FAIL"
        print(f"{marker} {result['id']}#{result['run']}: {result['first_line']}")
        for failure in result["failures"]:
            print(f"  - {failure}")

    failed = sum(not result["passed"] for result in results)
    print(f"EVAL SUMMARY: {len(results) - failed}/{len(results)} passed")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
