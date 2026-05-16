#!/usr/bin/env python3
"""Governed agentic loop runner for Atlante dei Concorsi.

The implementation is intentionally conservative. It supports dry-run state
initialisation and a small set of controlled implementation tasks. It does not
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
REVIEW_PACK_DIR = DEFAULT_DOCS_DIR / "procedure-review-packs"
SOURCE_INTAKE_DIR = DEFAULT_DOCS_DIR / "source-intake-packs"
COLLECTION_PLAN_DIR = DEFAULT_DOCS_DIR / "collection-plans"

ALLOWED_MODES = {"dry_run", "controlled_implementation"}
ALLOWED_CONTROLLED_TASKS = {
    "prepare-empty-review-checklist",
    "prepare-procedure-review-pack",
    "prepare-source-intake-pack",
    "prepare-collection-plan-from-intake",
}

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
    "prepare_procedure_review_pack",
    "prepare_source_intake_pack",
    "prepare_collection_plan_from_intake",
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


def normalise_optional_input(value: str | None) -> str | None:
    if value is None:
        return None
    cleaned = value.strip()
    while len(cleaned) >= 2 and cleaned[0] == cleaned[-1] and cleaned[0] in {"'", '"'}:
        cleaned = cleaned[1:-1].strip()
    return cleaned or None


def run_command(command: list[str]) -> dict[str, Any]:
    try:
        completed = subprocess.run(command, cwd=ROOT, check=False, capture_output=True, text=True)
    except OSError as exc:
        return {"status": "blocked", "command": " ".join(command), "return_code": None, "summary": f"Could not execute command: {exc}"}
    output = "\n".join(part for part in [completed.stdout.strip(), completed.stderr.strip()] if part)
    summary = output[-1200:] if output else "No output."
    return {"status": "passed" if completed.returncode == 0 else "failed", "command": " ".join(command), "return_code": completed.returncode, "summary": summary}


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


def read_local_pack_status(pack_dir: Path) -> dict[str, str]:
    status: dict[str, str] = {}
    if not pack_dir.exists():
        return status
    for path in sorted(pack_dir.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        filled_lines = [line for line in text.splitlines() if line.strip() and not line.strip().startswith("#")]
        status[path.name] = "present; human fields may still be empty" if filled_lines else "present but empty"
    return status


def write_files(base_dir: Path, files: dict[str, str]) -> list[str]:
    base_dir.mkdir(parents=True, exist_ok=True)
    touched: list[str] = []
    for filename, content in files.items():
        path = base_dir / filename
        path.write_text(content, encoding="utf-8")
        touched.append(str(path.relative_to(ROOT)))
    return touched


def prepare_empty_review_checklist(issue_number: int | None, procedure_id: str | None) -> list[str]:
    clean_procedure_id = safe_procedure_id(procedure_id, issue_number)
    return write_files(REVIEW_CHECKLIST_DIR, {f"{clean_procedure_id}_checklist.md": f"""# Empty review checklist — {clean_procedure_id}

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
"""})


def prepare_procedure_review_pack(issue_number: int | None, procedure_id: str | None) -> list[str]:
    clean_procedure_id = safe_procedure_id(procedure_id, issue_number)
    pack_dir = REVIEW_PACK_DIR / clean_procedure_id
    return write_files(pack_dir, {
        "README.md": f"""# Procedure review pack — {clean_procedure_id}

## Purpose

This folder is a neutral preparation pack for later human review.

It contains no factual findings, no source extraction, no candidate or committee information, no relation coding, no risk score, and no legal or reputational conclusion.

## Pack contents

- `source_inventory.md`: empty inventory for future source review.
- `coding_plan.md`: empty plan for future coding steps.
- `human_review_notes.md`: empty human-review notes.
- `handoff.md`: empty handoff template for the next authorised step.

## Current status

- Procedure/review identifier: `{clean_procedure_id}`
- Created by controlled implementation mode.
- Substantive coding: not started.
- Human review: pending.
""",
        "source_inventory.md": """# Source inventory

## Official source page

- URL:
- Retrieval date:
- Snapshot saved:
- Notes:

## Documents expected

- Call notice:
- Committee appointment:
- Evaluation criteria / first minutes:
- Admission or candidate list:
- Final acts approval:
- Other official documents:

## Ambiguity checks

- Multi-position source page:
- Version/date ambiguity:
- Missing documents:
- Search path still to document:
""",
        "coding_plan.md": """# Coding plan

## Pre-coding checks

- Procedure identifier confirmed:
- Source registry entry prepared:
- Documents linked to source URLs:
- Raw documents handled according to repository policy:
- Snapshot policy checked:

## Future coding sequence

1. Procedure metadata.
2. Document registry.
3. Profile requirements.
4. Evaluation criteria.
5. Committee members.
6. Candidates.
7. Committee-candidate relations only if evidence and approval permit.

## Stop gates

- Identity ambiguity:
- Conflicting documents:
- Weak relation evidence:
- Sensitive interpretation:
- Human review required:
""",
        "human_review_notes.md": """# Human review notes

## Reviewer

- Name:
- Date:
- Scope reviewed:

## Notes

- Source availability:
- Methodological ambiguity:
- Coding uncertainty:
- Required follow-up:

## Decision

- Proceed:
- Repeat preparation:
- Stop:
- Reason:
""",
        "handoff.md": f"""# Handoff — {clean_procedure_id}

## Current state

A neutral procedure review pack has been prepared. No substantive coding has been performed.

## Files prepared

- README.md
- source_inventory.md
- coding_plan.md
- human_review_notes.md
- handoff.md

## Next authorised step

A human reviewer should complete the source inventory and decide whether substantive coding can be authorised under the repository governance rules.

## Non-actions confirmed

- No external source collection performed.
- No golden-dataset row changed.
- No relation inferred.
- No legal or reputational conclusion introduced.
""",
    })


def prepare_source_intake_pack(issue_number: int | None, procedure_id: str | None) -> list[str]:
    clean_procedure_id = safe_procedure_id(procedure_id, issue_number)
    pack_dir = SOURCE_INTAKE_DIR / clean_procedure_id
    return write_files(pack_dir, {
        "README.md": f"""# Source intake pack — {clean_procedure_id}

## Purpose

This folder is a neutral intake workspace for later human entry of official source URLs and retrieval notes.

It contains no downloaded material, no factual findings, no source extraction, no candidate or committee information, no relation coding, no risk score, and no legal or reputational conclusion.

## Pack contents

- `official_urls.md`: empty fields for official URLs and source-status notes.
- `document_expectations.md`: empty checklist of expected document categories.
- `retrieval_log.md`: empty log for future human retrieval activity.
- `source_risk_notes.md`: empty notes for source ambiguity and provenance risks.
- `handoff.md`: empty handoff template for the next authorised step.

## Current status

- Procedure/review identifier: `{clean_procedure_id}`
- Created by controlled implementation mode.
- External fetching: not performed.
- Substantive coding: not started.
- Human review: pending.
""",
        "official_urls.md": """# Official URLs

## Primary official source

- URL:
- Institution/domain:
- Page title:
- Retrieval date:
- Human reviewer:
- Notes:

## Secondary official pages

- URL:
- Institution/domain:
- Page title:
- Retrieval date:
- Notes:

## Exclusion notes

- Unofficial pages excluded:
- Search-engine snippets excluded:
- Mirrors or third-party copies excluded:
""",
        "document_expectations.md": """# Document expectations

## Expected official document categories

- Call notice:
- Committee appointment:
- Evaluation criteria / first minutes:
- Admission or candidate list:
- Final acts approval:
- Other official documents:

## Availability status to be filled later

- Complete:
- Partial:
- Missing:
- Not determinable:

## Ambiguity checks

- Shared multi-position page:
- Multiple versions of same document:
- Date/version inconsistency:
- Document title ambiguity:
- Procedure-code ambiguity:
""",
        "retrieval_log.md": """# Retrieval log

## Human retrieval events

| Date | Reviewer | Source URL | Action | Result | Notes |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |

## Repository handling

- Raw documents committed to repository:
- Raw documents excluded by policy:
- Snapshot path, if applicable:
- Hash manifest update required:
""",
        "source_risk_notes.md": """# Source risk notes

## Provenance risks

- Source is official:
- Source is institutional but ambiguous:
- Source is departmental rather than central:
- Source is a shared listing page:
- Source requires attribution to a specific position/procedure:

## Interpretation risks

- Missing document risk:
- Versioning risk:
- Identity ambiguity risk:
- Relation-evidence sensitivity:
- Human review required before coding:
""",
        "handoff.md": f"""# Handoff — {clean_procedure_id}

## Current state

A neutral source-intake pack has been prepared. No external source collection or substantive coding has been performed.

## Files prepared

- README.md
- official_urls.md
- document_expectations.md
- retrieval_log.md
- source_risk_notes.md
- handoff.md

## Next authorised step

A human reviewer should enter official URLs and retrieval notes, then decide whether document collection or coding can be authorised under the repository governance rules.

## Non-actions confirmed

- No web fetching performed.
- No document downloaded.
- No golden-dataset row changed.
- No relation inferred.
- No legal or reputational conclusion introduced.
""",
    })


def prepare_collection_plan_from_intake(issue_number: int | None, procedure_id: str | None) -> tuple[list[str], list[str]]:
    clean_procedure_id = safe_procedure_id(procedure_id, issue_number)
    intake_dir = SOURCE_INTAKE_DIR / clean_procedure_id
    if not intake_dir.exists():
        return [], [f"Missing source-intake pack: {intake_dir.relative_to(ROOT)}"]

    status = read_local_pack_status(intake_dir)
    status_lines = "\n".join(f"- `{name}`: {value}" for name, value in sorted(status.items())) or "- No intake files found."
    plan_dir = COLLECTION_PLAN_DIR / clean_procedure_id
    touched = write_files(plan_dir, {
        "README.md": f"""# Collection plan — {clean_procedure_id}

## Purpose

This folder contains a neutral collection-planning scaffold derived only from local source-intake files.

It contains no web fetching, no downloaded material, no factual extraction, no candidate or committee information, no relation coding, no risk score, and no legal or reputational conclusion.

## Local intake files observed

{status_lines}

## Current status

- Procedure/review identifier: `{clean_procedure_id}`
- Created by controlled implementation mode.
- External fetching: not performed.
- Document download: not performed.
- Substantive coding: not started.
""",
        "collection_plan.md": """# Collection plan

## Manual collection sequence

1. Human reviewer confirms official source URLs in the intake pack.
2. Human reviewer checks whether each source is official and procedure-specific.
3. Human reviewer records retrieval date and source status.
4. Human reviewer decides whether document collection is authorised.
5. Human reviewer records any ambiguity before coding is considered.

## Fields still requiring human input

- Official source confirmation:
- Source-domain approval:
- Procedure-code matching:
- Retrieval method:
- Collection authorisation:

## Non-automated steps

- Web fetching:
- Document download:
- Source extraction:
- Golden-dataset update:
""",
        "document_handling_plan.md": """# Document handling plan

## Before collection

- Confirm repository policy for raw documents:
- Confirm whether snapshots are allowed:
- Confirm naming convention:
- Confirm hash-manifest requirement:
- Confirm no restricted material is included:

## After collection, if later authorised

- Store documents only in approved locations:
- Preserve original filenames where useful:
- Record source URL and retrieval date:
- Generate or update hash manifest:
- Do not code facts until a separate coding task is approved:
""",
        "approval_gates.md": """# Approval gates

## Gate 1 — Source perimeter

- All URLs are official:
- Source-domain expansion approved:
- Unofficial mirrors excluded:

## Gate 2 — Procedure specificity

- Source is tied to the intended procedure:
- Shared listing/page ambiguity resolved:
- Procedure code verified:

## Gate 3 — Collection authorisation

- Human reviewer authorises collection:
- Repository storage policy confirmed:
- Hashing/snapshot policy confirmed:

## Gate 4 — Coding authorisation

- Coding is separately approved:
- Ambiguities documented:
- Human-review requirement assessed:
""",
        "handoff.md": f"""# Handoff — {clean_procedure_id}

## Current state

A neutral collection plan has been prepared from local source-intake files only.

## Files prepared

- README.md
- collection_plan.md
- document_handling_plan.md
- approval_gates.md
- handoff.md

## Next authorised step

A human reviewer should complete approval gates before any later collection or coding task is considered.

## Non-actions confirmed

- No web fetching performed.
- No document downloaded.
- No golden-dataset row changed.
- No relation inferred.
- No legal or reputational conclusion introduced.
""",
    })
    return touched, []


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

    if mode == "controlled_implementation":
        if not task:
            blocking_issues.append("Controlled implementation mode requires --task.")
        elif task not in ALLOWED_CONTROLLED_TASKS:
            blocking_issues.append(f"Unknown or unauthorised controlled task: {task}")
        elif task == "prepare-empty-review-checklist":
            files_touched.extend(prepare_empty_review_checklist(issue_number, procedure_id))
            notes.append("Created a neutral empty review checklist for later human use.")
        elif task == "prepare-procedure-review-pack":
            files_touched.extend(prepare_procedure_review_pack(issue_number, procedure_id))
            notes.append("Created a neutral procedure review pack for later human use.")
        elif task == "prepare-source-intake-pack":
            files_touched.extend(prepare_source_intake_pack(issue_number, procedure_id))
            notes.append("Created a neutral source intake pack for later human use.")
        elif task == "prepare-collection-plan-from-intake":
            touched, task_blockers = prepare_collection_plan_from_intake(issue_number, procedure_id)
            files_touched.extend(touched)
            blocking_issues.extend(task_blockers)
            if not task_blockers:
                notes.append("Created a neutral collection plan from local source-intake files only.")
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
    elif task == "prepare-procedure-review-pack":
        next_action = "Review the generated procedure review pack, then decide whether a later human-approved substantive coding task is appropriate."
    elif task == "prepare-source-intake-pack":
        next_action = "Review the generated source-intake pack, then enter official URLs manually before any later collection or coding step."
    elif task == "prepare-collection-plan-from-intake":
        next_action = "Review the generated collection plan and complete approval gates before any later collection or coding step."
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
    state = build_state(args.issue_number, args.state_dir, args.docs_dir, not args.skip_validators, args.mode, normalise_optional_input(args.task), normalise_optional_input(args.procedure_id))
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
