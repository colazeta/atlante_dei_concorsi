#!/usr/bin/env python3
"""Governed agentic loop runner for Atlante dei Concorsi.

This runner is intentionally conservative. It supports dry-run state
initialisation and controlled implementation tasks that create or read only
local governance artefacts. It does not fetch web pages, download documents,
modify the golden dataset, infer relations, or produce legal/reputational
assessments.
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
REVIEW_PACK_DIR = DEFAULT_DOCS_DIR / "procedure-review-packs"
SOURCE_INTAKE_DIR = DEFAULT_DOCS_DIR / "source-intake-packs"
COLLECTION_PLAN_DIR = DEFAULT_DOCS_DIR / "collection-plans"
GATE_DECISION_DIR = DEFAULT_DOCS_DIR / "gate-decisions"

ALLOWED_MODES = {"dry_run", "controlled_implementation"}
ALLOWED_CONTROLLED_TASKS = {
    "prepare-empty-review-checklist",
    "prepare-procedure-review-pack",
    "prepare-source-intake-pack",
    "prepare-collection-plan-from-intake",
    "evaluate-collection-approval-gates",
}

ALLOWED_ACTIONS = [
    "read_repository",
    "read_issue_instruction",
    "write_loop_state",
    "write_execution_log",
    "run_validation",
    "report_blockers",
]
CONTROLLED_IMPLEMENTATION_ACTIONS = ALLOWED_ACTIONS + [task.replace("-", "_") for task in sorted(ALLOWED_CONTROLLED_TASKS)]

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


def normalise_optional_input(value: str | None) -> str | None:
    if value is None:
        return None
    cleaned = value.strip()
    while len(cleaned) >= 2 and cleaned[0] == cleaned[-1] and cleaned[0] in {"'", '"'}:
        cleaned = cleaned[1:-1].strip()
    return cleaned or None


def safe_procedure_id(procedure_id: str | None, issue_number: int | None) -> str:
    value = (procedure_id or f"ACU-REVIEW-{issue_number or 0:04d}").strip()
    allowed = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_")
    cleaned = "".join(char if char in allowed else "-" for char in value)
    return cleaned or f"ACU-REVIEW-{issue_number or 0:04d}"


def write_files(base_dir: Path, files: dict[str, str]) -> list[str]:
    base_dir.mkdir(parents=True, exist_ok=True)
    touched: list[str] = []
    for filename, content in files.items():
        path = base_dir / filename
        path.write_text(content, encoding="utf-8")
        touched.append(str(path.relative_to(ROOT)))
    return touched


def run_command(command: list[str]) -> dict[str, Any]:
    try:
        completed = subprocess.run(command, cwd=ROOT, check=False, capture_output=True, text=True)
    except OSError as exc:
        return {"status": "blocked", "command": " ".join(command), "return_code": None, "summary": f"Could not execute command: {exc}"}
    output = "\n".join(part for part in [completed.stdout.strip(), completed.stderr.strip()] if part)
    return {
        "status": "passed" if completed.returncode == 0 else "failed",
        "command": " ".join(command),
        "return_code": completed.returncode,
        "summary": (output[-1200:] if output else "No output."),
    }


def build_validation(run_validators: bool) -> dict[str, dict[str, Any]]:
    if run_validators:
        methodology = run_command([sys.executable, "scripts/validate_atlante_methodology.py"])
        golden = run_command([sys.executable, "scripts/validate_golden_dataset.py"])
    else:
        methodology = {"status": "not_run", "command": "python3 scripts/validate_atlante_methodology.py", "return_code": None, "summary": "Skipped by runner option."}
        golden = {"status": "not_run", "command": "python3 scripts/validate_golden_dataset.py", "return_code": None, "summary": "Skipped by runner option."}
    return {
        "state_schema": {"status": "not_run", "command": "python3 scripts/validate_agentic_loop_state.py", "return_code": None, "summary": "State schema validation is run after this file is written."},
        "methodology": methodology,
        "golden_dataset": golden,
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


def prepare_empty_review_checklist(issue_number: int | None, procedure_id: str | None) -> list[str]:
    pid = safe_procedure_id(procedure_id, issue_number)
    return write_files(REVIEW_CHECKLIST_DIR, {f"{pid}_checklist.md": f"""# Empty review checklist — {pid}

## Scope

This checklist is a neutral review scaffold. It contains no factual findings, source extraction, relation coding or assessment of any person or procedure.

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

## Reviewer outcome

- Review status:
- Required follow-up:
- Blocking issues:
- Approval to proceed to substantive coding:
"""})


def prepare_procedure_review_pack(issue_number: int | None, procedure_id: str | None) -> list[str]:
    pid = safe_procedure_id(procedure_id, issue_number)
    return write_files(REVIEW_PACK_DIR / pid, {
        "README.md": f"# Procedure review pack — {pid}\n\nNeutral preparation pack for later human review. No substantive coding has been performed.\n",
        "source_inventory.md": "# Source inventory\n\n- Official source page URL:\n- Retrieval date:\n- Snapshot saved:\n- Missing or ambiguous documents:\n",
        "coding_plan.md": "# Coding plan\n\n1. Procedure metadata.\n2. Document registry.\n3. Profile requirements.\n4. Evaluation criteria.\n5. Committee members.\n6. Candidates.\n7. Relations only if evidence and approval permit.\n",
        "human_review_notes.md": "# Human review notes\n\n- Reviewer:\n- Date:\n- Notes:\n- Decision:\n",
        "handoff.md": f"# Handoff — {pid}\n\nNo external source collection, golden-dataset change, relation inference or legal/reputational conclusion introduced.\n",
    })


def prepare_source_intake_pack(issue_number: int | None, procedure_id: str | None) -> list[str]:
    pid = safe_procedure_id(procedure_id, issue_number)
    return write_files(SOURCE_INTAKE_DIR / pid, {
        "README.md": f"# Source intake pack — {pid}\n\nNeutral intake workspace for later human entry of official source URLs and retrieval notes. No external fetching performed.\n",
        "official_urls.md": "# Official URLs\n\n## Primary official source\n\n- URL:\n- Institution/domain:\n- Page title:\n- Retrieval date:\n- Human reviewer:\n- Notes:\n\n## Secondary official pages\n\n- URL:\n- Institution/domain:\n- Page title:\n- Retrieval date:\n- Notes:\n",
        "document_expectations.md": "# Document expectations\n\n- Call notice:\n- Committee appointment:\n- Evaluation criteria / first minutes:\n- Admission or candidate list:\n- Final acts approval:\n- Other official documents:\n",
        "retrieval_log.md": "# Retrieval log\n\n| Date | Reviewer | Source URL | Action | Result | Notes |\n| --- | --- | --- | --- | --- | --- |\n|  |  |  |  |  |  |\n",
        "source_risk_notes.md": "# Source risk notes\n\n- Source is official:\n- Source is institutional but ambiguous:\n- Source is a shared listing page:\n- Human review required before coding:\n",
        "handoff.md": f"# Handoff — {pid}\n\nA human reviewer should enter official URLs and retrieval notes before any later collection or coding step.\n",
    })


def read_local_pack_status(pack_dir: Path) -> str:
    if not pack_dir.exists():
        return "- No intake files found."
    lines = [f"- `{path.name}`: present; human fields may still be empty" for path in sorted(pack_dir.glob("*.md"))]
    return "\n".join(lines) if lines else "- No intake files found."


def prepare_collection_plan_from_intake(issue_number: int | None, procedure_id: str | None) -> tuple[list[str], list[str]]:
    pid = safe_procedure_id(procedure_id, issue_number)
    intake_dir = SOURCE_INTAKE_DIR / pid
    if not intake_dir.exists():
        return [], [f"Missing source-intake pack: {intake_dir.relative_to(ROOT)}"]
    status_lines = read_local_pack_status(intake_dir)
    return write_files(COLLECTION_PLAN_DIR / pid, {
        "README.md": f"# Collection plan — {pid}\n\nNeutral collection-planning scaffold derived only from local source-intake files.\n\n## Local intake files observed\n\n{status_lines}\n",
        "collection_plan.md": "# Collection plan\n\n1. Human reviewer confirms official source URLs.\n2. Human reviewer checks source/procedure specificity.\n3. Human reviewer records retrieval date and source status.\n4. Human reviewer decides whether document collection is authorised.\n",
        "document_handling_plan.md": "# Document handling plan\n\n- Confirm repository policy for raw documents:\n- Confirm snapshot policy:\n- Confirm naming convention:\n- Confirm hash-manifest requirement:\n",
        "approval_gates.md": "# Approval gates\n\n## Gate 1 — Source perimeter\n\n- All URLs are official:\n- Source-domain expansion approved:\n- Unofficial mirrors excluded:\n\n## Gate 2 — Procedure specificity\n\n- Source is tied to the intended procedure:\n- Shared listing/page ambiguity resolved:\n- Procedure code verified:\n\n## Gate 3 — Collection authorisation\n\n- Human reviewer authorises collection:\n- Repository storage policy confirmed:\n- Hashing/snapshot policy confirmed:\n\n## Gate 4 — Coding authorisation\n\n- Coding is separately approved:\n- Ambiguities documented:\n- Human-review requirement assessed:\n",
        "handoff.md": f"# Handoff — {pid}\n\nA human reviewer should complete approval gates before any later collection or coding task is considered.\n",
    }), []


def approval_gate_completion(path: Path) -> tuple[str, list[str]]:
    if not path.exists():
        return "blocked", [f"Missing approval-gate file: {path.relative_to(ROOT)}"]
    missing = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        stripped = raw.strip()
        if stripped.startswith("- ") and stripped.endswith(":"):
            missing.append(stripped[2:-1])
    if missing:
        return "needs_human_input", missing
    return "ready_for_manual_collection", []


def evaluate_collection_approval_gates(issue_number: int | None, procedure_id: str | None) -> tuple[list[str], list[str]]:
    pid = safe_procedure_id(procedure_id, issue_number)
    plan_dir = COLLECTION_PLAN_DIR / pid
    if not plan_dir.exists():
        return [], [f"Missing collection-plan pack: {plan_dir.relative_to(ROOT)}"]
    decision, missing = approval_gate_completion(plan_dir / "approval_gates.md")
    missing_text = "\n".join(f"- {item}" for item in missing) if missing else "- None detected in the local approval-gate file."
    return write_files(GATE_DECISION_DIR / pid, {
        "README.md": f"# Gate decision — {pid}\n\nNeutral human-in-the-loop gate decision derived only from local collection-plan files.\n\n- Decision state: `{decision}`\n- External fetching: not performed.\n- Document download: not performed.\n- Substantive coding: not started.\n",
        "gate_decision.md": f"# Gate decision\n\n## Decision state\n\n`{decision}`\n\n## Basis\n\nThis decision is based only on whether local approval-gate fields appear complete. It is not a substantive assessment of any procedure, person, document or institution.\n\n## Missing or incomplete local gate inputs\n\n{missing_text}\n",
        "missing_inputs.md": f"# Missing inputs\n\n{missing_text}\n",
        "handoff.md": f"# Handoff — {pid}\n\n## Current state\n\nA neutral approval-gate decision has been created from local collection-plan files only.\n\n## Next step\n\nIf the decision is `needs_human_input`, a human reviewer should complete approval gates before any manual collection step is considered.\n\n## Non-actions confirmed\n\n- No web fetching performed.\n- No document downloaded.\n- No golden-dataset row changed.\n- No relation inferred.\n- No legal or reputational conclusion introduced.\n",
    }), []


def run_task(issue_number: int | None, mode: str, task: str | None, procedure_id: str | None) -> tuple[list[str], list[str], list[str]]:
    if mode == "dry_run":
        return [], [], []
    if not task:
        return [], ["Controlled implementation mode requires --task."], []
    if task not in ALLOWED_CONTROLLED_TASKS:
        return [], [f"Unknown or unauthorised controlled task: {task}"], []
    if task == "prepare-empty-review-checklist":
        return prepare_empty_review_checklist(issue_number, procedure_id), [], ["Created a neutral empty review checklist for later human use."]
    if task == "prepare-procedure-review-pack":
        return prepare_procedure_review_pack(issue_number, procedure_id), [], ["Created a neutral procedure review pack for later human use."]
    if task == "prepare-source-intake-pack":
        return prepare_source_intake_pack(issue_number, procedure_id), [], ["Created a neutral source intake pack for later human use."]
    if task == "prepare-collection-plan-from-intake":
        touched, blockers = prepare_collection_plan_from_intake(issue_number, procedure_id)
        return touched, blockers, [] if blockers else ["Created a neutral collection plan from local source-intake files only."]
    if task == "evaluate-collection-approval-gates":
        touched, blockers = evaluate_collection_approval_gates(issue_number, procedure_id)
        return touched, blockers, [] if blockers else ["Created a neutral approval-gate decision from local collection-plan files only."]
    return [], [f"Unhandled task: {task}"], []


def next_action_for(mode: str, task: str | None, blocking_issues: list[str]) -> str:
    if blocking_issues:
        return "Resolve blocking issues before continuing."
    if mode == "dry_run":
        return "Open a reviewed issue for controlled implementation mode; keep substantive coding disabled by default."
    if task == "prepare-source-intake-pack":
        return "Review the generated source-intake pack, then enter official URLs manually before any later collection or coding step."
    if task == "prepare-collection-plan-from-intake":
        return "Review the generated collection plan and complete approval gates before any later collection or coding step."
    if task == "evaluate-collection-approval-gates":
        return "Review the generated gate decision; if human input is still needed, complete approval gates before any later collection step."
    return "Review the generated neutral artefacts, then decide whether a later human-approved task is appropriate."


def build_state(issue_number: int | None, state_dir: Path, docs_dir: Path, run_validators: bool, mode: str, task: str | None, procedure_id: str | None) -> dict[str, Any]:
    task = normalise_optional_input(task)
    procedure_id = normalise_optional_input(procedure_id)
    state_dir.mkdir(parents=True, exist_ok=True)
    docs_dir.mkdir(parents=True, exist_ok=True)
    loop_id = f"ACU-LOOP-{issue_number:04d}" if issue_number else "ACU-LOOP-0000"
    now = utc_now()
    files_touched = [f"reports/agentic-loop/{loop_id}_state.json", f"docs/executions/{loop_id}_execution.md"]
    blocking_issues: list[str] = []
    notes = [
        "No source expansion, no data collection, no relation inference and no golden-dataset update.",
        "Substantive coding mode remains disabled unless explicitly approved through a reviewed issue.",
    ]
    if mode not in ALLOWED_MODES:
        blocking_issues.append(f"Unsupported mode requested: {mode}")
    elif mode == "controlled_implementation":
        touched, task_blockers, task_notes = run_task(issue_number, mode, task, procedure_id)
        files_touched.extend(touched)
        blocking_issues.extend(task_blockers)
        notes.extend(task_notes)
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
        "next_action": next_action_for(mode, task, blocking_issues),
        "files_touched": sorted(set(files_touched)),
        "last_commit": None,
        "last_pr": None,
        "notes": notes,
    }


def write_execution_log(state: dict[str, Any], docs_dir: Path) -> Path:
    log_path = docs_dir / f"{state['loop_id']}_execution.md"
    validation_lines = [f"- `{key}`: {result['status']} (command: `{result['command']}`, return code: `{result['return_code']}`)" for key, result in state["validation"].items()]
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
    state = build_state(args.issue_number, args.state_dir, args.docs_dir, not args.skip_validators, args.mode, args.task, args.procedure_id)
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
