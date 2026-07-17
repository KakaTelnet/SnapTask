"""Load multi-format Goal fixtures for contract and behavioral checks."""

from __future__ import annotations

import json
import textwrap
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "tests" / "goal-fixtures.json"
FIXTURE_DIR = ROOT / "tests" / "goal-fixtures"


def _section_payload(text: str, marker: str, source: Path) -> str:
    """Return the content after a fixture's declared review marker."""
    before, separator, after = text.partition(marker)
    if not separator or not before.strip():
        raise ValueError(f"{source}: missing review marker {marker!r}")
    return after.strip()


def _yaml_key_payload(text: str, key: str, source: Path) -> str:
    """Extract one top-level YAML mapping without requiring a YAML package."""
    marker = f"{key}:"
    lines = text.splitlines()
    try:
        start = lines.index(marker) + 1
    except ValueError as error:
        raise ValueError(f"{source}: missing YAML key {key!r}") from error

    payload_lines = lines[start:]
    if not payload_lines or any(line and not line.startswith("  ") for line in payload_lines):
        raise ValueError(f"{source}: {key!r} must be the final top-level mapping")
    return textwrap.dedent("\n".join(payload_lines)).strip()


def _extract_goal(text: str, payload: dict[str, str], source: Path) -> str:
    """Extract only the Goal input from one supported fixture format."""
    payload_type = payload.get("type")
    if payload_type == "section":
        return _section_payload(text, payload["marker"], source)
    if payload_type == "json_key":
        value = json.loads(text)[payload["key"]]
        return json.dumps(value, ensure_ascii=False, indent=2)
    if payload_type == "yaml_key":
        return _yaml_key_payload(text, payload["key"], source)
    raise ValueError(f"{source}: unsupported payload type {payload_type!r}")


def load_fixture_cases() -> list[dict[str, object]]:
    """Return normalized evaluation cases from the fixture manifest."""
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    if manifest.get("schema_version") != 1:
        raise ValueError(f"{MANIFEST_PATH}: unsupported schema_version")

    cases: list[dict[str, object]] = []
    for entry in manifest.get("cases", []):
        fixture_path = MANIFEST_PATH.parent / str(entry["path"])
        text = fixture_path.read_text(encoding="utf-8")
        goal = _extract_goal(text, dict(entry["payload"]), fixture_path)
        if not goal:
            raise ValueError(f"{fixture_path}: extracted Goal is empty")
        if str(entry["id"]) not in text:
            raise ValueError(f"{fixture_path}: embedded case id differs from manifest")
        if str(entry["expected_status"]) not in text:
            raise ValueError(f"{fixture_path}: embedded expected status differs from manifest")
        cases.append({**entry, "goal": goal, "fixture_path": str(fixture_path)})
    return cases
