#!/usr/bin/env python3
"""Validate Atlante methodology docs/schemas/templates consistency."""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs" / "atlante-concorsi-universitari"
SCHEMAS = ROOT / "schemas" / "atlante-concorsi-universitari"
TEMPLATES = ROOT / "data" / "templates" / "atlante-concorsi-universitari"

EXPECTED_DOCS = [
    "00_scope_and_publication_principles.md",
    "01_unit_of_analysis_and_workflow.md",
    "02_codebook.md",
    "03_document_taxonomy.md",
    "04_profile_specificity_method.md",
    "05_criteria_narrowness_method.md",
    "06_committee_candidate_relations_taxonomy.md",
    "07_source_registry_template.md",
    "08_golden_dataset_protocol.md",
    "09_manual_coding_guide.md",
    "10_ai_extraction_instructions.md",
    "11_quality_assurance_checklist.md",
    "12_pilot_university_selection.md",
    "13_publication_language_policy.md",
]

MAPPINGS = [
    ("procedure.schema.json", "procedures_template.csv"),
    ("document.schema.json", "documents_template.csv"),
    ("profile_requirement.schema.json", "profile_requirements_template.csv"),
    ("evaluation_criterion.schema.json", "evaluation_criteria_template.csv"),
    ("committee_member.schema.json", "committee_members_template.csv"),
    ("candidate.schema.json", "candidates_template.csv"),
    ("committee_candidate_relation.schema.json", "committee_candidate_relations_template.csv"),
    ("source_registry_entry.schema.json", "source_registry_template.csv"),
]


def fail(msg: str) -> None:
    print(f"ERROR: {msg}")


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def csv_header(path: Path) -> list[str]:
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.reader(f)
        try:
            header = next(reader)
        except StopIteration:
            return []
    return [h.strip() for h in header]


def main() -> int:
    errors = 0

    # Expected files
    for name in EXPECTED_DOCS:
        if not (DOCS / name).exists():
            fail(f"Missing expected doc file: {DOCS / name}")
            errors += 1

    for schema_name, csv_name in MAPPINGS:
        schema_path = SCHEMAS / schema_name
        csv_path = TEMPLATES / csv_name

        if not schema_path.exists():
            fail(f"Missing schema: {schema_path}")
            errors += 1
            continue
        if not csv_path.exists():
            fail(f"Missing CSV template: {csv_path}")
            errors += 1
            continue

        try:
            schema_obj = load_json(schema_path)
        except json.JSONDecodeError as exc:
            fail(f"Invalid JSON in {schema_name}: {exc}")
            errors += 1
            continue

        properties = schema_obj.get("properties", {})
        if not isinstance(properties, dict) or not properties:
            fail(f"Schema {schema_name} has no properties object")
            errors += 1
            continue

        header = csv_header(csv_path)
        if not header:
            fail(f"CSV template {csv_name} has no header")
            errors += 1
            continue

        schema_fields = set(properties.keys())
        csv_fields = set(header)

        missing_in_csv = sorted(schema_fields - csv_fields)
        extra_in_csv = sorted(csv_fields - schema_fields)

        if missing_in_csv:
            fail(f"CSV {csv_name} missing schema fields: {', '.join(missing_in_csv)}")
            errors += 1
        if extra_in_csv:
            fail(f"CSV {csv_name} has extra fields not in schema: {', '.join(extra_in_csv)}")
            errors += 1

    if errors:
        print(f"\nValidation failed with {errors} error(s).")
        return 1

    print("Validation passed: expected files, JSON parsing, and schema/CSV header alignment are OK.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
