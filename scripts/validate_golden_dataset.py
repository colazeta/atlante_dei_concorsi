#!/usr/bin/env python3
"""Validate golden dataset workspace for Atlante Concorsi Universitari."""

from __future__ import annotations

import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = ROOT / "data" / "templates" / "atlante-concorsi-universitari"
GOLDEN = ROOT / "data" / "golden-dataset" / "atlante-concorsi-universitari"
GITIGNORE = ROOT / ".gitignore"

EXPECTED_FILES = {
    "source_registry": GOLDEN / "source_registry" / "source_registry.csv",
    "procedures": GOLDEN / "procedures" / "procedures.csv",
    "documents": GOLDEN / "procedures" / "documents.csv",
    "profile_requirements": GOLDEN / "procedures" / "profile_requirements.csv",
    "profile_requirement_items": GOLDEN / "procedures" / "profile_requirement_items.csv",
    "evaluation_criteria": GOLDEN / "procedures" / "evaluation_criteria.csv",
    "evaluation_criterion_items": GOLDEN / "procedures" / "evaluation_criterion_items.csv",
    "committee_members": GOLDEN / "procedures" / "committee_members.csv",
    "candidates": GOLDEN / "procedures" / "candidates.csv",
    "committee_candidate_relations": GOLDEN / "procedures" / "committee_candidate_relations.csv",
    "pilot_metrics": GOLDEN / "pilot_metrics" / "pilot_batch_001_metrics.csv",
}

TEMPLATE_MAP = {
    "source_registry": TEMPLATES / "source_registry_template.csv",
    "procedures": TEMPLATES / "procedures_template.csv",
    "documents": TEMPLATES / "documents_template.csv",
    "profile_requirements": TEMPLATES / "profile_requirements_template.csv",
    "profile_requirement_items": TEMPLATES / "profile_requirement_items_template.csv",
    "evaluation_criteria": TEMPLATES / "evaluation_criteria_template.csv",
    "evaluation_criterion_items": TEMPLATES / "evaluation_criterion_items_template.csv",
    "committee_members": TEMPLATES / "committee_members_template.csv",
    "candidates": TEMPLATES / "candidates_template.csv",
    "committee_candidate_relations": TEMPLATES / "committee_candidate_relations_template.csv",
}

FORBIDDEN_COLUMNS = {
    "conflict_of_interest_confirmed",
    "suspicious",
    "rigged",
    "corruption_flag",
    "confirmed_conflict",
}

FORBIDDEN_HEADER_TERMS = {"suspicious", "rigged", "corrupt", "corruption", "confirmed_conflict"}

ALLOWED_RELATION_TYPES = {
    "same_academic_field",
    "same_current_affiliation",
    "same_past_affiliation",
    "same_department_current",
    "same_department_past",
    "coauthorship_single",
    "coauthorship_recurrent",
    "coauthorship_recent",
    "shared_research_project",
    "shared_research_centre_or_lab",
    "supervisor_student_relation",
    "grant_or_project_hierarchy",
    "declared_abstention_or_challenge",
    "other_documented_relation",
    "no_documented_relation_in_registered_sources",
    "no_relation_found",
    "not_determinable",
}

ALLOWED_PROFILE_ITEM_TYPES = {
    "thematic_keyword",
    "methodological_keyword",
    "experience_requirement",
    "project_lab_centre_reference",
    "language_requirement",
    "specific_combination_term",
    "other_profile_feature",
}

ALLOWED_CRITERION_TYPES = {
    "main_criterion",
    "subcriterion",
    "weight",
    "threshold",
    "profile_linked_criterion",
    "discretionary_criterion",
    "other_criterion_feature",
}

REQUIRED_GITIGNORE_LINES = {
    "data/golden-dataset/atlante-concorsi-universitari/raw_documents/**",
    "!data/golden-dataset/atlante-concorsi-universitari/raw_documents/README.md",
    "!data/golden-dataset/atlante-concorsi-universitari/raw_documents/.gitkeep",
    "data/golden-dataset/atlante-concorsi-universitari/snapshots/**",
    "!data/golden-dataset/atlante-concorsi-universitari/snapshots/README.md",
    "!data/golden-dataset/atlante-concorsi-universitari/snapshots/.gitkeep",
}


def load_header(path: Path) -> list[str]:
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.reader(f)
        try:
            return [h.strip() for h in next(reader)]
        except StopIteration:
            return []


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def is_synthetic_row(row: dict[str, str]) -> bool:
    haystack = " ".join((v or "") for v in row.values()).lower()
    return "synthetic" in haystack or "fictional" in haystack


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    # 1) .gitignore safeguards
    if not GITIGNORE.exists():
        errors.append("Missing .gitignore with golden-dataset safeguards")
    else:
        lines = {line.strip() for line in GITIGNORE.read_text(encoding="utf-8").splitlines() if line.strip()}
        missing = sorted(REQUIRED_GITIGNORE_LINES - lines)
        if missing:
            errors.append(f"Missing required .gitignore safeguard lines: {', '.join(missing)}")

    # 2) expected files
    for key, path in EXPECTED_FILES.items():
        if not path.exists():
            errors.append(f"Missing expected CSV file [{key}]: {path}")

    if errors:
        print("Golden dataset validation report")
        print("-" * 36)
        for err in errors:
            print(f"ERROR: {err}")
        print(f"\nResult: FAILED ({len(errors)} error(s))")
        return 1

    headers: dict[str, list[str]] = {}

    # 3) header checks + template alignment
    for key, path in EXPECTED_FILES.items():
        header = load_header(path)
        headers[key] = header
        if not header:
            errors.append(f"CSV has no header [{key}]: {path}")
            continue

        # Forbidden columns / accusatory terms in headers
        forbidden_cols = sorted(set(header).intersection(FORBIDDEN_COLUMNS))
        if forbidden_cols:
            errors.append(f"Forbidden columns in [{key}]: {', '.join(forbidden_cols)}")

        for col in header:
            lowered = col.lower()
            if any(term in lowered for term in FORBIDDEN_HEADER_TERMS):
                errors.append(f"Forbidden accusatory term in header [{key}]: {col}")

        if key in TEMPLATE_MAP:
            template_header = load_header(TEMPLATE_MAP[key])
            if not template_header:
                errors.append(f"Template header missing [{key}]: {TEMPLATE_MAP[key]}")
                continue
            if header != template_header:
                errors.append(
                    f"Header mismatch [{key}].\n"
                    f"  expected: {template_header}\n"
                    f"  actual:   {header}"
                )

    # 4) mandatory columns
    for key in [
        "procedures",
        "documents",
        "profile_requirements",
        "profile_requirement_items",
        "evaluation_criteria",
        "evaluation_criterion_items",
        "committee_members",
        "candidates",
        "committee_candidate_relations",
    ]:
        if "procedure_id" not in headers.get(key, []):
            errors.append(f"Missing required column procedure_id in [{key}]")

    if "document_type" not in headers.get("documents", []):
        errors.append("Missing required column document_type in [documents]")
    if "source_url" not in headers.get("documents", []):
        errors.append("Missing required column source_url in [documents]")

    # 5) value domain checks for new item-level layers
    profile_item_rows = load_rows(EXPECTED_FILES["profile_requirement_items"])
    for i, row in enumerate(profile_item_rows, start=2):
        if not (row.get("procedure_id") or "").strip():
            errors.append(f"Missing procedure_id at line {i} in profile_requirement_items.csv")
        item_type = (row.get("item_type") or "").strip()
        if item_type and item_type not in ALLOWED_PROFILE_ITEM_TYPES:
            errors.append(f"Invalid item_type at line {i} in profile_requirement_items.csv: {item_type}")

    criterion_item_rows = load_rows(EXPECTED_FILES["evaluation_criterion_items"])
    for i, row in enumerate(criterion_item_rows, start=2):
        if not (row.get("procedure_id") or "").strip():
            errors.append(f"Missing procedure_id at line {i} in evaluation_criterion_items.csv")
        criterion_type = (row.get("criterion_type") or "").strip()
        if criterion_type and criterion_type not in ALLOWED_CRITERION_TYPES:
            errors.append(f"Invalid criterion_type at line {i} in evaluation_criterion_items.csv: {criterion_type}")

    # 6) relation terminology check
    relation_rows = load_rows(EXPECTED_FILES["committee_candidate_relations"])
    for i, row in enumerate(relation_rows, start=2):
        value = (row.get("relation_type") or "").strip()
        if not value:
            warnings.append(f"Empty relation_type at line {i} in committee_candidate_relations.csv")
            continue
        if value not in ALLOWED_RELATION_TYPES:
            errors.append(f"Non-neutral/unknown relation_type at line {i}: {value}")

    # 7) conservative data-presence guard (real-looking rows)
    # If non-empty rows exist in golden CSVs, they must be explicitly synthetic.
    for key, path in EXPECTED_FILES.items():
        rows = load_rows(path)
        for i, row in enumerate(rows, start=2):
            # ignore fully empty rows
            if not any((v or "").strip() for v in row.values()):
                continue
            if not is_synthetic_row(row):
                warnings.append(
                    f"Row may contain non-synthetic data [{key}] line {i}. "
                    "Ensure this is intentional and approved for internal pilot use."
                )

    print("Golden dataset validation report")
    print("-" * 36)
    for err in errors:
        print(f"ERROR: {err}")
    for warn in warnings:
        print(f"WARN: {warn}")

    if errors:
        print(f"\nResult: FAILED ({len(errors)} error(s), {len(warnings)} warning(s))")
        return 1

    print(f"Result: PASSED ({len(warnings)} warning(s))")
    return 0


if __name__ == "__main__":
    sys.exit(main())
