#!/usr/bin/env python3
"""Validate governed agentic-loop state files.

This validator intentionally uses only the Python standard library. It performs
structural checks equivalent to the repository state schema and adds project-
specific safety checks that are easier to express procedurally.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
STATE_DIR = ROOT / "reports" / "agentic-loop"
SCHEMA_PATH = ROOT / "schemas" / "agentic-loop" / "state.schema.json"

REQUIRED_TOP_LEVEL = {
    "loop_id",
    "issue_number",
    "mode",
    "status",
    "phase",
    "created_at_utc",
    "updated_at_utc",
    "allowed_actions",
    "prohibited_actions",
    "quality_score",
    "validation",
    "blocking_issues",
    "human_review_required",
    "next_action",
    "files_touched",
}

ALLOWED_MODES = {"dry_run", "controlled_implementation", "substantive_coding"}
ALLOWED_STATUSES = {"initialised", "running", "completed", "blocked", "failed"}
ALLOWED_VALIDATION_STATUSES = {"not_run", "passed", "failed", "blocked"}
REQUIRED_VALIDATION_KEYS = {"state_schema", "methodology", "golden_dataset"}

FORBIDDEN_WORDS = {
    "conflict_of_interest_confirmed",
    "suspicious",
    "rigged",
    "corruption_flag",
    "confirmed_conflict",
}

DRY_RUN_FORBIDDEN_PATH_PREFIXES = (
    "data/golden-dataset/atlante-concorsi-universitari/procedures/",
    "data/golden-dataset/atlante-concorsi-universitari/source_registry/",
    "data/golden-dataset/atlante-concorsi-universitari/raw_documents/",
    "data/golden-dataset/atlante-concorsi-universitari/snapshots/",
)


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def load_json(path: Path, errors: list[str]) -> dict[str, Any] | None:
    try:
        with path.open("r", encoding="utf-8") as handle:
            obj = json.load(handle)
    except json.JSONDecodeError as exc:
        fail(errors, f"Invalid JSON in {path}: {exc}")
        return None
    except OSError as exc:
        fail(errors, f"Cannot read {path}: {exc}")
        return None

    if not isinstance(obj, dict):
        fail(errors, f"State file must contain a JSON object: {path}")
        return None
    return obj


def validate_state(path: Path) -> list[str]:
    errors: list[str] = []
    state = load_json(path, errors)
    if state is None:
        return errors

    missing = sorted(REQUIRED_TOP_LEVEL - set(state))
    if missing:
        fail(errors, f"{path}: missing required fields: {', '.join(missing)}")

    extra = sorted(set(state) - (REQUIRED_TOP_LEVEL | {"last_commit", "last_pr", "notes"}))
    if extra:
        fail(errors, f"{path}: unknown fields: {', '.join(extra)}")

    loop_id = state.get("loop_id")
    if not isinstance(loop_id, str) or not re.fullmatch(r"ACU-LOOP-[0-9]{4}", loop_id):
        fail(errors, f"{path}: loop_id must match ACU-LOOP-0000 pattern")

    issue_number = state.get("issue_number")
    if issue_number is not None and (not isinstance(issue_number, int) or issue_number < 1):
        fail(errors, f"{path}: issue_number must be null or a positive integer")

    mode = state.get("mode")
    if mode not in ALLOWED_MODES:
        fail(errors, f"{path}: invalid mode: {mode}")

    status = state.get("status")
    if status not in ALLOWED_STATUSES:
        fail(errors, f"{path}: invalid status: {status}")

    quality_score = state.get("quality_score")
    if not isinstance(quality_score, int) or not 0 <= quality_score <= 100:
        fail(errors, f"{path}: quality_score must be an integer between 0 and 100")

    for key in ["allowed_actions", "prohibited_actions", "blocking_issues", "files_touched"]:
        value = state.get(key)
        if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
            fail(errors, f"{path}: {key} must be a list of strings")

    validation = state.get("validation")
    if not isinstance(validation, dict):
        fail(errors, f"{path}: validation must be an object")
    else:
        missing_validation = sorted(REQUIRED_VALIDATION_KEYS - set(validation))
        if missing_validation:
            fail(errors, f"{path}: missing validation keys: {', '.join(missing_validation)}")
        for key, result in validation.items():
            if key not in REQUIRED_VALIDATION_KEYS:
                fail(errors, f"{path}: unknown validation key: {key}")
                continue
            if not isinstance(result, dict):
                fail(errors, f"{path}: validation.{key} must be an object")
                continue
            result_status = result.get("status")
            if result_status not in ALLOWED_VALIDATION_STATUSES:
                fail(errors, f"{path}: validation.{key}.status invalid: {result_status}")
            if "command" not in result:
                fail(errors, f"{path}: validation.{key}.command missing")
            if "return_code" not in result:
                fail(errors, f"{path}: validation.{key}.return_code missing")

    human_review_required = state.get("human_review_required")
    if not isinstance(human_review_required, bool):
        fail(errors, f"{path}: human_review_required must be boolean")

    next_action = state.get("next_action")
    if not isinstance(next_action, str) or not next_action.strip():
        fail(errors, f"{path}: next_action must be a non-empty string")

    haystack = json.dumps(state, ensure_ascii=False).lower()
    for word in FORBIDDEN_WORDS:
        if word.lower() in haystack:
            fail(errors, f"{path}: forbidden governance term appears in state: {word}")

    files_touched = state.get("files_touched") or []
    if mode == "dry_run":
        for touched in files_touched:
            if touched.startswith(DRY_RUN_FORBIDDEN_PATH_PREFIXES):
                fail(errors, f"{path}: dry_run state touches substantive dataset path: {touched}")

    if status in {"completed", "blocked"} and not files_touched:
        fail(errors, f"{path}: completed/blocked state should record at least one touched file")

    return errors


def main() -> int:
    errors: list[str] = []

    if not SCHEMA_PATH.exists():
        errors.append(f"Missing schema file: {SCHEMA_PATH}")
    else:
        schema_errors: list[str] = []
        load_json(SCHEMA_PATH, schema_errors)
        errors.extend(schema_errors)

    if not STATE_DIR.exists():
        print("Agentic loop state validation report")
        print("-" * 38)
        print("WARN: reports/agentic-loop does not exist yet; no state files to validate.")
        print("Result: PASSED (0 state files)")
        return 0

    state_files = sorted(STATE_DIR.glob("*.json"))
    if not state_files:
        print("Agentic loop state validation report")
        print("-" * 38)
        print("WARN: no state JSON files found.")
        print("Result: PASSED (0 state files)")
        return 0

    for path in state_files:
        errors.extend(validate_state(path))

    print("Agentic loop state validation report")
    print("-" * 38)
    for error in errors:
        print(f"ERROR: {error}")

    if errors:
        print(f"\nResult: FAILED ({len(errors)} error(s), {len(state_files)} state file(s))")
        return 1

    print(f"Result: PASSED ({len(state_files)} state file(s))")
    return 0


if __name__ == "__main__":
    sys.exit(main())
