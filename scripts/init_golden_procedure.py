#!/usr/bin/env python3
"""Initialize folder structure for one manually collected golden-dataset procedure."""

from __future__ import annotations

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data" / "golden-dataset" / "atlante-concorsi-universitari"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Initialize golden procedure workspace folders")
    parser.add_argument("--university-slug", required=True, help="University slug, e.g. university_a")
    parser.add_argument("--procedure-id", required=True, help="Procedure id, e.g. ACU-TEST-0001")
    return parser.parse_args()


def write_readme(path: Path, university_slug: str, procedure_id: str) -> None:
    readme = path / "README.md"
    if readme.exists():
        return
    content = f"""# Procedure workspace

- `university_slug`: `{university_slug}`
- `procedure_id`: `{procedure_id}`

## Instructions
- Place official documents in `raw_documents/{university_slug}/{procedure_id}/`.
- Name files with ordering prefix (e.g., `01_call_notice.pdf`, `02_committee_appointment.pdf`).
- Record source URLs and retrieval dates in `data/golden-dataset/atlante-concorsi-universitari/procedures/documents.csv`.
- Do not write legal conclusions in notes.
- If a committee-candidate relation is uncertain, mark as `not_determinable` or keep review status `pending`.
"""
    readme.write_text(content, encoding="utf-8")


def main() -> int:
    args = parse_args()

    targets = [
        BASE / "raw_documents" / args.university_slug / args.procedure_id,
        BASE / "snapshots" / args.university_slug / args.procedure_id,
        BASE / "review_notes" / args.university_slug / args.procedure_id,
        BASE / "qa_reports" / args.university_slug / args.procedure_id,
    ]

    for path in targets:
        path.mkdir(parents=True, exist_ok=True)
        write_readme(path, args.university_slug, args.procedure_id)

    print("Initialized procedure workspace:")
    for path in targets:
        print(f"- {path.relative_to(ROOT)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
