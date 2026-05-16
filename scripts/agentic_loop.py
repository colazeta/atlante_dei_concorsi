#!/usr/bin/env python3
"""Dry-run governed agentic loop runner for Atlante dei Concorsi.

The current implementation is intentionally conservative. It creates a
persistent loop state and execution log, then stops. It does not collect data,
modify the golden dataset, infer relations or call external sources.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_STATE_DIR = ROOT / "reports" / "agentic-loop"
DEFAULT_DOCS_DIR = ROOT / "docs" / "executions"

ALLOWED_ACTIONS = [
    "read_repository",
    "read_issue_instruction",
    "write_loop_state",
    "write_execution_log",
    "run_validation",
    "report_blockers",
]

PROHIBITED_ACTIONS = [
    "large_scale_scraping",
    "unapproved_domain_expansion",
    "public_accusatory_language",
    "legal_conclusions",
    "raw_document_commit",
    "substantive_dataset_expansion_in_dry_run",
    "relation_inference_without_human_review",
]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def run_command(command: list[str]) -> dict[str, Any]:
    try:
        completed = subprocess.run(
            command,
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
    except OSError as exc:
        return {
            "status": "blocked",
            "command": " ".join(command),
            "return_code": None,
            "summary": f"Could not execute command: {exc}",
        }

    output = "\n".join(part for part in [completed.stdout.strip(), completed.stderr.strip()] if part)
    summary = output[-1200:] if output else "No output."
    return {
        "status": "passed" if completed.returncode == 0 else "failed",
        "command": " ".join(command),
        "return_code": completed.returncode,
        "summary": summary,
    }


def compute_quality_score(validation: dict[str, dict[str, Any]], blocking_issues: list[str]) -> int:
    score = 40
    if validation["methodology"]["status"] == "passed":
        score += 20
    if validation["golden_dataset"]["status"] == "passed":
        score += 20
    if not blocking_issues:
        score += 20
    return min(score, 100)


def build_state(issue_number: int | None, state_dir: Path, docs_dir: Path, run_validators: bool) -> dict[str, Any]:
    state_dir.mkdir(parents=True, exist_ok=True)
    docs_dir.mkdir(parents=True, exist_ok=True)

    loop_id = f"ACU-LOOP-{issue_number:04d}" if issue_number else "ACU-LOOP-0000"
    now = utc_now()

    if run_validators:
        methodology = run_command([sys.executable, "scripts/validate_atlante_methodology.py"])
        golden = run_command([sys.executable, "scripts/validate_golden_dataset.py"])
    else:
        methodology = {
            "status": "not_run",
            "command": "python3 scripts/validate_atlante_methodology.py",
            "return_code": None,
            "summary": "Skipped by runner option.",
        }
        golden = {
            "status": "not_run",
            "command": "python3 scripts/validate_golden_dataset.py",
            "return_code": None,
            "summary": "Skipped by runner option.",
        }

    blocking_issues: list[str] = []
    if methodology["status"] == "failed":
        blocking_issues.append("Methodology validation failed; inspect validator output before continuing.")
    if golden["status"] == "failed":
        blocking_issues.append("Golden dataset validation failed; inspect validator output before continuing.")

    status = "blocked" if blocking_issues else "completed"
    next_action = (
        "Resolve validation blockers before enabling controlled implementation mode."
        if blocking_issues
        else "Open a reviewed issue for controlled implementation mode; keep substantive coding disabled by default."
    )

    validation = {
        "state_schema": {
            "status": "not_run",
            "command": "python3 scripts/validate_agentic_loop_state.py",
            "return_code": None,
            "summary": "State schema validation is run after this file is written.",
        },
        "methodology": methodology,
        "golden_dataset": golden,
    }

    files_touched = [
        f"reports/agentic-loop/{loop_id}_state.json",
        f"docs/executions/{loop_id}_execution.md",
    ]

    return {
        "loop_id": loop_id,
        "issue_number": issue_number,
        "mode": "dry_run",
        "status": status,
        "phase": "governed_foundation_dry_run",
        "created_at_utc": now,
        "updated_at_utc": now,
        "allowed_actions": ALLOWED_ACTIONS,
        "prohibited_actions": PROHIBITED_ACTIONS,
        "quality_score": compute_quality_score(validation, blocking_issues),
        "validation": validation,
        "blocking_issues": blocking_issues,
        "human_review_required": bool(blocking_issues),
        "next_action": next_action,
        "files_touched": files_touched,
        "last_commit": None,
        "last_pr": None,
        "notes": [
            "Dry-run foundation only: no source expansion, no data collection, no relation inference and no golden-dataset update.",
            "Substantive coding mode remains disabled unless explicitly approved through a reviewed issue.",
        ],
    }


def write_execution_log(state: dict[str, Any], docs_dir: Path) -> Path:
    log_path = docs_dir / f"{state['loop_id']}_execution.md"
    validation_lines = []
    for key, result in state["validation"].items():
        validation_lines.append(
            f"- `{key}`: {result['status']} "
            f"(command: `{result['command']}`, return code: `{result['return_code']}`)"
        )

    blockers = state["blocking_issues"] or ["None."]
    blockers_text = "\n".join(f"- {item}" for item in blockers)

    content = f"""# {state['loop_id']} — governed dry-run execution

## Summary

- Issue: #{state['issue_number']}
- Mode: `{state['mode']}`
- Status: `{state['status']}`
- Phase: `{state['phase']}`
- Quality score: `{state['quality_score']}`
- Human review required: `{state['human_review_required']}`
- Updated at: `{state['updated_at_utc']}`

## Scope actually executed

This run only initialised the governed loop state, wrote this execution log and optionally ran repository validators.

It did not collect external sources, update real golden-dataset records, infer relations, publish findings, or modify source taxonomies.

## Validation

{chr(10).join(validation_lines)}

## Blocking issues

{blockers_text}

## Files touched

{chr(10).join(f'- `{item}`' for item in state['files_touched'])}

## Next action

{state['next_action']}
"""
    log_path.write_text(content, encoding="utf-8")
    return log_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Run a governed dry-run agentic loop.")
    parser.add_argument("--issue-number", type=int, default=None)
    parser.add_argument("--state-dir", type=Path, default=DEFAULT_STATE_DIR)
    parser.add_argument("--docs-dir", type=Path, default=DEFAULT_DOCS_DIR)
    parser.add_argument("--skip-validators", action="store_true")
    args = parser.parse_args()

    state = build_state(
        issue_number=args.issue_number,
        state_dir=args.state_dir,
        docs_dir=args.docs_dir,
        run_validators=not args.skip_validators,
    )

    state_path = args.state_dir / f"{state['loop_id']}_state.json"
    state_path.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    log_path = write_execution_log(state, args.docs_dir)

    state_validation = run_command([sys.executable, "scripts/validate_agentic_loop_state.py"])
    state["validation"]["state_schema"] = state_validation
    state["quality_score"] = compute_quality_score(state["validation"], state["blocking_issues"])
    if state_validation["status"] == "failed" and "Agentic loop state validation failed" not in state["blocking_issues"]:
        state["blocking_issues"].append("Agentic loop state validation failed; inspect validator output before continuing.")
        state["status"] = "failed"
        state["human_review_required"] = True
        state["next_action"] = "Fix state schema validation before continuing."
    state["updated_at_utc"] = utc_now()

    state_path.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    write_execution_log(state, args.docs_dir)

    print(f"Wrote state: {state_path.relative_to(ROOT)}")
    print(f"Wrote log: {log_path.relative_to(ROOT)}")
    print(f"Status: {state['status']}")
    print(f"Quality score: {state['quality_score']}")
    if state["blocking_issues"]:
        print("Blocking issues:")
        for issue in state["blocking_issues"]:
            print(f"- {issue}")

    return 0 if state["status"] in {"completed", "blocked"} else 1


if __name__ == "__main__":
    sys.exit(main())
