#!/usr/bin/env python3
from __future__ import annotations
import csv
import json
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
INTAKE = ROOT / 'docs/executions/source-intake-packs'
OUT = ROOT / 'docs/executions/approved-source-inventories'
SITE = ROOT / 'site/data/source_inventory_progress.json'
INDEX = INTAKE / 'source_intake_index.csv'

CANDIDATE_HEADER = [
    'university_id', 'source_url', 'link_url', 'link_text', 'link_type_hint',
    'same_domain', 'confidence_level', 'requires_human_attention',
    'blocking_status', 'notes', 'observed_at_utc'
]
OBSERVED_HEADER = [
    'university_id', 'source_url', 'http_status', 'content_type', 'page_title', 'observed_at_utc'
]


def parse_index() -> list[dict]:
    with INDEX.open(newline='', encoding='utf-8') as f:
        rows = list(csv.DictReader(f))
    rows.sort(key=lambda r: r.get('university_id', ''))
    return rows


def write_if_changed(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    previous = path.read_text(encoding='utf-8') if path.exists() else None
    if previous != content:
        path.write_text(content, encoding='utf-8')


def csv_content(rows: list[dict], header: list[str]) -> str:
    from io import StringIO
    buf = StringIO()
    w = csv.DictWriter(buf, fieldnames=header)
    w.writeheader()
    w.writerows(rows)
    return buf.getvalue()


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')
    rows = parse_index()

    by_university = []
    index_rows = []

    for r in rows:
        uid = (r.get('university_id') or '').strip()
        if not uid:
            continue
        inv = OUT / uid
        homepage = (r.get('official_homepage_url') or '').strip()
        recruitment = (r.get('recruitment_page_url') or '').strip()
        requires_attention = (r.get('requires_human_attention', '').strip().lower() in {'true', 'yes'}) or not recruitment
        blocking_status = (r.get('blocking_status') or 'awaiting_bounded_fetch').strip() or 'awaiting_bounded_fetch'

        write_if_changed(inv / 'README.md', (
            f"# Approved source inventory — {uid}\n\n"
            "Generated from intake pack only; no broad crawling, no raw document downloads.\n"
        ))
        write_if_changed(inv / 'fetch_log.md', (
            "# Fetch log\n\n"
            f"- Generated at: {now}\n"
            "- Mode: intake-pack derived scaffold (no network fetch in this run).\n"
            "- Blocking status: pending_fetch\n"
        ))
        write_if_changed(inv / 'observed_links.csv', csv_content([], OBSERVED_HEADER))
        write_if_changed(inv / 'candidate_document_links.csv', csv_content([], CANDIDATE_HEADER))
        write_if_changed(inv / 'source_limits.md', (
            "# Source limits\n\n"
            "- Official URLs from intake pack only.\n"
            "- No PDF/raw-document download.\n"
            "- Candidate links remain neutral hints pending human review.\n"
        ))
        write_if_changed(inv / 'handoff.md', (
            "# Handoff\n\n"
            "Next step: bounded approved URL fetch with human review of uncertain cases.\n"
        ))

        row = {
            'university_id': uid,
            'university_name': (r.get('university_name') or '').strip(),
            'intake_pack_exists': 'yes',
            'inventory_exists': 'yes',
            'homepage_url': homepage,
            'recruitment_url': recruitment,
            'fetch_status': 'pending_fetch',
            'candidate_links_count': '0',
            'requires_human_attention': 'yes' if requires_attention else 'no',
            'blocking_status': blocking_status,
            'last_updated_utc': now,
        }
        index_rows.append(row)
        by_university.append(dict(row))

    index_header = list(index_rows[0].keys()) if index_rows else [
        'university_id', 'university_name', 'intake_pack_exists', 'inventory_exists', 'homepage_url',
        'recruitment_url', 'fetch_status', 'candidate_links_count', 'requires_human_attention',
        'blocking_status', 'last_updated_utc'
    ]
    write_if_changed(OUT / 'source_inventory_index.csv', csv_content(index_rows, index_header))
    write_if_changed(OUT / 'README.md', (
        "# Approved source inventories\n\n"
        f"Generated inventories: {len(index_rows)}\n"
        f"Updated: {now}\n"
    ))

    progress = {
        'updated_at_utc': now,
        'total_intake_packs': len(rows),
        'inventories_created': len(index_rows),
        'inventories_pending': len(index_rows),
        'inventories_with_recruitment_url': sum(1 for x in by_university if x['recruitment_url']),
        'inventories_with_candidate_links': 0,
        'inventories_needing_attention': sum(1 for x in by_university if x['requires_human_attention'] == 'yes'),
        'fetch_errors': 0,
        'candidate_links_total': 0,
        'progress_events': [
            'Scaffolded approved source inventories from intake packs without broad crawling or raw downloads.'
        ],
        'by_university': by_university,
    }

    existing = None
    if SITE.exists():
        try:
            existing = json.loads(SITE.read_text(encoding='utf-8'))
        except Exception:
            existing = None
    if existing:
        comparable_existing = {k: v for k, v in existing.items() if k != 'updated_at_utc'}
        comparable_next = {k: v for k, v in progress.items() if k != 'updated_at_utc'}
        if comparable_existing == comparable_next:
            progress['updated_at_utc'] = existing.get('updated_at_utc', progress['updated_at_utc'])
            for item, old in zip(progress['by_university'], existing.get('by_university', [])):
                if item.get('university_id') == old.get('university_id'):
                    item['last_updated_utc'] = old.get('last_updated_utc', item['last_updated_utc'])

    write_if_changed(SITE, json.dumps(progress, indent=2, ensure_ascii=False) + "\n")


if __name__ == '__main__':
    main()
