#!/usr/bin/env python3
"""Governed agentic loop runner for Atlante dei Concorsi.

The implementation is intentionally conservative. It can run a dry-run state
initialisation and one first-stage controlled implementation task. It does not
collect data, modify the golden dataset, infer relations or call external
sources.
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
REVIEW_CHECKLIST_DIR = DEFAULT_DOCS_DIR / "review-checklists"

ALLOWED_MODES = {"dry_run", "controlled_implementation"}
ALLOWED_CONTROLLED_TASKS = {"prepare-empty-review-checklist"}

ALLOWED_ACTIONS = [
    "read_repository",
    "read_issue_instruction",
    "write_loop_state",
    "write_execution_log",
    "run_validation",
    "report_blockers",
]

CONTROLLED_IMPLEMENTATION_ACTIONS = ALLOWED_ACTIONS + [
    "prepare_empty_review_checklist",
]

PROHIBITED_ACTIONS = [
    "large_scale_scraping",
    "unapproved_domain_expansion",
    "public_accusatory_language",
    "legal_conclusions",
    "raw_document_commit",
    "substantive_dataset_expansion_in_dry_run",
    "substantive_dataset_expansion_in_controlled_implementation",
    "relation_inference_without_human_review",
]

RESTRICTED_PATH_PREFIXES = (
    "data/golden-dataset/atlante-concorsi-universitari/procedures/",
    "data/golden-dataset/atlante-concorsi-universitari/source_registry/",
    "data/golden-dataset/atlante-concorsi-universitari/raw_documents/",
    "data/golden-dataset/atlante-concorsi-universitari/snapshots/",
)


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


def safe_procedure_id(procedure_id: str | None, issue_number: int | None) -> str:
    value = (procedure_id or f"ACU-REVIEW-{issue_number or 0:04d}").strip()
    allowed = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_")
    cleaned = "".join(char if char in allowed else "-" for char in value)
    return cleaned or f"ACU-REVIEW-{issue_number or 0:04d}"


def prepare_empty_review_checklist(issue_number: int | None, procedure_id: str | None) -> list[str]:
    REVIEW_CHECKLIST_DIR.mkdir(parents=True, exist_ok=True)
    clean_procedure_id = safe_procedure_id(procedure_id, issue_number)
    checklist_path = REVIEW_CHECKLIST_DIR / f"{clean_procedure_id}_checklist.md"

    content = f"""# Empty review checklist — {clean_procedure_id}

## Scope

This checklist is a neutral review scaffold. It contains no factual findings, no source extraction, no relation coding and no assessment of any person or procedure.

## Procedure metadata to be filled by a human reviewer

- Procedure ID:
- University:
- Department:
- Role/procedure type:
- Source page URL:
- Retrieval date:
- Reviewer:
- Review date:

## Source availability check

- Official call notice available:
- Committee appointment document available:
- Evaluation criteria / first minutes available:
- Admission or candidate list available:
- Final acts approval available:
- Source page snapshot available:
- Notes on missing or ambiguous documents:

## Evidence traceability check

- Every future coded field has a source document or URL:
- Every future excerpt is linked to a document:
- Multi-position source page ambiguity checked:
- Versioning/date ambiguity checked:
- Search path documented where evidence is unavailable:

## Methodological caution check

- No legal conclusion introduced:
- No reputational conclusion introduced:
- No relation inferred from weak name similarity:
- No relation inferred from same affiliation alone:
- No relation inferred from coauthorship alone:
- Human review required for ambiguous identity or relation evidence:

## Reviewer outcome

- Review status:
- Required follow-up:
- Blocking issues:
- Approval to proceed to substantive coding:
"""
    checklist_path.write_text(content, encoding="utf-8")
    return [str(checklist_path.relative_to(ROOT))]


def build_validation(run_validators: bool) -> dict[str, dict[str, Any]]:
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

    return {
        "state_schema": {
            "status": "not_run",
            "command": "python3 scripts/validate_agentic_loop_state.py",
            "return_code": None,
            "summary": "State schema validation is run after this file is written.",
        },
        "methodology": methodology,
        "golden_dataset": golden,
    }


def build_state(
    issue_number: int | None,
    state_dir: Path,
    docs_dir: Path,
    run_validators: bool,
    mode: str,
    task: str | None,
    procedure_id: str | None,
) -> dict[str, Any]:
    state_dir.mkdir(parents=True, exist_ok=True)
    docs_dir.mkdir(parents=True, exist_ok=True)

    loop_id = f"ACU-LOOP-{issue_number:04d}" if issue_number else "ACU-LOOP-0000"
    now = utc_now()
    files_touched = [
        f"reports/agentic-loop/{loop_id}_state.json",
        f"docs/executions/{loop_id}_execution.md",
    ]
    blocking_issues: list[str] = []
    notes = [
        "No source expansion, no data collection, no relation inference and no golden-dataset update.",
        "Substantive coding mode remains disabled unless explicitly approved through a reviewed issue.",
    ]

    if mode not in ALLOWED_MODES:
        blocking_issues.append(f"Unsupported mode requested: {mode}")

    if mode == "controlled_implementation":
        if not task:
            blocking_issues.append("Controlled implementation mode requires --task.")
        elif task not in ALLOWED_CONTROLLED_TASKS:
            blocking_issues.append(f"Unknown or unauthorised controlled task: {task}")
        elif task == "prepare-empty-review-checklist":
            files_touched.extend(prepare_empty_review_checklist(issue_number, procedure_id))
            notes.append("Created a neutral empty review checklist for later human use.")
    elif task:
        blocking_issues.append("--task is only allowed with --mode controlled_implementation.")

    for touched in files_touched:
        if touched.startswith(RESTRICTED_PATH_PREFIXES):
            blocking_issues.append(f"Requested action touches a restricted path: {touched}")

    validation = build_validation(run_validators)
    if validation["methodology"]["status"] == "failed":
        blocking_issues.append("Methodology validation failed; inspect validator output before continuing.")
    if validation["golden_dataset"]["status"] == "failed":
        blocking_issues.append("Golden dataset validation failed; inspect validator output before continuing.")

    status = "blocked" if blocking_issues else "completed"
    if blocking_issues:
        next_action = "Resolve blocking issues before continuing."
    elif mode == "dry_run":
        next_action = "Open a reviewed issue for controlled implementation mode; keep substantive coding disabled by default."
    else:
        next_action = "Review the generated neutral checklist, then decide whether a later human-approved substantive coding task is appropriate."

    return {
        "loop_id": loop_id,
        "issue_number": issue_number,
        "mode": mode,
        "status": status,
        "phase": "governed_foundation_dry_run" if mode == "dry_run" else "controlled_implementation",
        "created_at_utc": now,
        "updated_at_utc": now,
        "allowed_actions": ALLOWED_ACTIONS if mode == "dry_run" else CONTROLLED_IMPLEMENTATION_ACTIONS,
        "prohibited_actions": PROHIBITED_ACTIONS,
        "quality_score": compute_quality_score(validation, blocking_issues),
        "validation": validation,
        "blocking_issues": blocking_issues,
        "human_review_required": bool(blocking_issues),
        "next_action": next_action,
        "files_touched": sorted(set(files_touched)),
        "last_commit": None,
        "last_pr": None,
        "notes": notes,
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

    content = f"""# {state['loop_id']} — governed agentic-loop execution

## Summary

- Issue: #{state['issue_number']}
- Mode: `{state['mode']}`
- Status: `{state['status']}`
- Phase: `{state['phase']}`
- Quality score: `{state['quality_score']}`
- Human review required: `{state['human_review_required']}`
- Updated at: `{state['updated_at_utc']}`

## Scope actually executed

This run wrote or updated governed loop artefacts only.

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
    parser = argparse.ArgumentParser(description="Run a governed agentic loop.")
    parser.add_argument("--issue-number", type=int, default=None)
    parser.add_argument("--state-dir", type=Path, default=DEFAULT_STATE_DIR)
    parser.add_argument("--docs-dir", type=Path, default=DEFAULT_DOCS_DIR)
    parser.add_argument("--skip-validators", action="store_true")
    parser.add_argument("--mode", choices=sorted(ALLOWED_MODES), default="dry_run")
    parser.add_argument("--task", default=None)
    parser.add_argument("--procedure-id", default=None)
    args = parser.parse_args()

    state = build_state(
        issue_number=args.issue_number,
        state_dir=args.state_dir,
        docs_dir=args.docs_dir,
        run_validators=not args.skip_validators,
        mode=args.mode,
        task=args.task,
        procedure_id=args.procedure_id,
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
