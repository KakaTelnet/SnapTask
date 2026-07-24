"""Run aim-review live model evaluations against the regression case suite."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CASES_PATH = ROOT / "tests" / "aim-review-cases.json"
SKILL_PATH = ROOT / "skills" / "aim-review" / "SKILL.md"

DEFAULT_MODEL = os.environ.get("SNAPTASK_MODEL", "claude-sonnet-5")
CLI = os.environ.get("SNAPTASK_CLI", "claude")
TIMEOUT = int(os.environ.get("SNAPTASK_TIMEOUT", "300"))


def load_cases() -> list[dict]:
    payload = json.loads(CASES_PATH.read_text(encoding="utf-8"))
    return payload["cases"]


def run_prompt(prompt: str, model: str = DEFAULT_MODEL) -> tuple[str, str, int]:
    """Run a single prompt through the CLI. Returns (stdout, stderr, exit_code)."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
        f.write(prompt)
        prompt_file = f.name
    try:
        result = subprocess.run(
            [CLI, "-p", prompt, "--model", model, "--output-format", "text"],
            capture_output=True, text=True, timeout=TIMEOUT, cwd=str(ROOT),
        )
        return result.stdout, result.stderr, result.returncode
    finally:
        unlink_artifact(prompt_file)


def unlink_artifact(path: str) -> None:
    try:
        os.unlink(path)
    except OSError:
        pass


def validate_response(case: dict, output: str) -> list[str]:
    """Validate a single case response. Returns list of failure messages."""
    failures: list[str] = []
    expected = case["expected_status"]
    # The output must contain the expected bilingual verdict label
    if expected not in output:
        failures.append(f"expected_status: {expected!r} not found in output")
    # Must contain a score
    if not re.search(r"综合评分:\s*\d", output) and not re.search(r"Overall score:", output):
        failures.append("missing score line")
    # Must contain the key check table gates
    for gate in ["背景", "目标用户", "核心价值", "边界", "成功标准"]:
        if gate not in output:
            failures.append(f"missing gate check: {gate!r}")
    return failures


def build_review_prompt(case: dict) -> str:
    """Build a review prompt from a test case."""
    aim_text = case["aim"]
    return (
        f"Use $aim-review to assess this aim document.\n\n"
        f"--- AIM DOCUMENT ---\n{aim_text}\n--- END ---"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="aim-review live evals")
    parser.add_argument("--ids", nargs="*", help="Run specific case IDs")
    parser.add_argument("--repeat", type=int, default=1, help="Repeat each case N times")
    parser.add_argument("--list", action="store_true", help="List case IDs and exit")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Model to use")
    parser.add_argument("--self-test", action="store_true", help="Run a minimal smoke test")
    args = parser.parse_args()

    if args.repeat < 1:
        parser.error("--repeat must be at least 1")

    cases = load_cases()

    if args.list:
        for c in cases:
            print(f"{c['id']:50s}  expected={c['expected_status']:30s}  lang={c.get('language','')}")
        return 0

    if args.self_test:
        case = {"id": "self-test", "aim": "Background: test. Target users: devs. Core value: test. Not doing: nothing. Success criteria: test passes.", "expected_status": "通过: Approved"}
        print(f"Self-test: {case['id']}")
        stdout, stderr, rc = run_prompt(build_review_prompt(case), model=args.model)
        if rc != 0:
            print(f"  FAIL: CLI returned {rc}")
            print(f"  stderr: {stderr[:500]}")
            return 1
        print("  OK: model responded")
        return 0

    selected = [c for c in cases if not args.ids or c["id"] in args.ids]
    if not selected:
        print("No cases matched.")
        return 1

    passed = 0
    failed = 0
    for case in selected:
        for run_number in range(1, args.repeat + 1):
            label = f"{case['id']}" if args.repeat == 1 else f"{case['id']} run {run_number}/{args.repeat}"
            print(f"\n{'='*60}")
            print(f"Case: {label}")
            print(f"Expected: {case['expected_status']}")
            print(f"{'='*60}")

            prompt = build_review_prompt(case)
            start = time.time()
            stdout, stderr, rc = run_prompt(prompt, model=args.model)
            elapsed = time.time() - start

            if rc != 0:
                print(f"  FAIL: CLI returned {rc}")
                print(f"  stderr: {stderr[:500]}")
                failed += 1
                continue

            failures = validate_response(case, stdout)
            print(f"  Elapsed: {elapsed:.0f}s  Output length: {len(stdout)} chars")
            if failures:
                print(f"  FAIL ({len(failures)} issues):")
                for f in failures:
                    print(f"    - {f}")
                failed += 1
            else:
                print("  PASS")
                passed += 1

    print(f"\n{'='*60}")
    print(f"Results: {passed} passed, {failed} failed out of {passed + failed}")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
