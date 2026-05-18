#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRIAGE_CSV = ROOT / 'docs/executions/document-link-triage/document_link_triage_index.csv'
OUTPUT_JSON = ROOT / 'site/data/document_link_triage_index.json'


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(encoding='utf-8', newline='') as f:
        return list(csv.DictReader(f))


def main() -> None:
    rows = read_csv(TRIAGE_CSV)
    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_JSON.write_text(json.dumps({
        'metadata': {
            'source': str(TRIAGE_CSV.relative_to(ROOT)),
            'row_count': len(rows),
            'note': 'Generated static JSON copy of governed document-link triage CSV for GitHub Pages validation UI.'
        },
        'entries': rows,
    }, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
