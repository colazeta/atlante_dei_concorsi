#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INVENTORIES_ROOT = ROOT / 'docs/executions/approved-source-inventories'
SOURCE_INDEX_PATH = INVENTORIES_ROOT / 'source_inventory_index.csv'
OUTPUT_DIR = ROOT / 'docs/executions/document-link-classification'
OUTPUT_INDEX_PATH = OUTPUT_DIR / 'document_link_classification_index.csv'
OUTPUT_PROGRESS_PATH = ROOT / 'site/data/document_link_classification_progress.json'

ALLOWED_CLASSIFICATIONS = {
    'call_notice_candidate',
    'committee_appointment_candidate',
    'evaluation_criteria_candidate',
    'admission_or_candidate_list_candidate',
    'final_acts_approval_candidate',
    'competition_listing',
    'recruitment_page',
    'other_official_document_candidate',
    'unknown',
}

CLASSIFICATION_HEADER = [
    'classification_id','university_id','source_url','link_url','link_text','link_type_hint','classified_type',
    'classification_confidence','requires_human_attention','blocking_status','classification_reason','observed_at_utc','classified_at_utc'
]

def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')

def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(encoding='utf-8', newline='') as f:
        return list(csv.DictReader(f))

def write_csv(path: Path, rows: list[dict[str, str]], header: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        writer.writerows(rows)

def classify_candidate_row(row: dict[str, str], uid: str, idx: int, classified_at: str) -> dict[str, str]:
    hint = (row.get('link_type_hint') or '').strip().lower()
    link_text = (row.get('link_text') or '').strip().lower()
    link_url = (row.get('link_url') or '').strip().lower()
    source_url = (row.get('source_url') or '').strip()

    classified_type = 'unknown'
    confidence = 'not_determinable'
    reason = 'No deterministic rule matched available metadata.'

    tokens = f"{hint} {link_text} {link_url}"
    if 'bando' in tokens or 'call' in tokens:
        classified_type = 'call_notice_candidate'; confidence = 'medium'; reason = 'Keyword match: bando/call.'
    elif 'commissione' in tokens or 'committee' in tokens:
        classified_type = 'committee_appointment_candidate'; confidence = 'medium'; reason = 'Keyword match: commissione/committee.'
    elif 'criteri' in tokens or 'criteria' in tokens:
        classified_type = 'evaluation_criteria_candidate'; confidence = 'medium'; reason = 'Keyword match: criteri/criteria.'
    elif 'graduatoria' in tokens or 'ammessi' in tokens or 'ammissione' in tokens:
        classified_type = 'admission_or_candidate_list_candidate'; confidence = 'medium'; reason = 'Keyword match: admission/list terms.'
    elif 'approvazione atti' in tokens or 'atti finali' in tokens:
        classified_type = 'final_acts_approval_candidate'; confidence = 'medium'; reason = 'Keyword match: final acts approval terms.'
    elif 'concorsi' in tokens or 'reclutamento' in tokens:
        classified_type = 'competition_listing'; confidence = 'low'; reason = 'Generic competition/recruitment listing signal.'
    elif source_url and link_url and link_url == source_url:
        classified_type = 'recruitment_page'; confidence = 'low'; reason = 'Link URL equals source URL.'

    if classified_type not in ALLOWED_CLASSIFICATIONS:
        classified_type = 'unknown'
        confidence = 'not_determinable'
        reason = 'Fallback to allowed unknown category.'

    requires_attention = 'yes' if classified_type == 'unknown' or confidence in {'low', 'not_determinable'} else 'no'
    return {
        'classification_id': f'{uid}-cls-{idx:05d}',
        'university_id': uid,
        'source_url': source_url,
        'link_url': row.get('link_url', ''),
        'link_text': row.get('link_text', ''),
        'link_type_hint': row.get('link_type_hint', ''),
        'classified_type': classified_type,
        'classification_confidence': confidence,
        'requires_human_attention': requires_attention,
        'blocking_status': 'non_blocking',
        'classification_reason': reason,
        'observed_at_utc': row.get('observed_at_utc', ''),
        'classified_at_utc': classified_at,
    }

def main() -> None:
    classified_at = now_utc()
    source_index = read_csv(SOURCE_INDEX_PATH)
    classifications: list[dict[str, str]] = []
    by_university: list[dict[str, object]] = []

    for entry in source_index:
        uid = entry.get('university_id', '').strip()
        if not uid:
            continue
        candidate_path = INVENTORIES_ROOT / uid / 'candidate_document_links.csv'
        candidate_rows = read_csv(candidate_path)
        u_classifications = [classify_candidate_row(r, uid, i + 1, classified_at) for i, r in enumerate(candidate_rows)]
        classifications.extend(u_classifications)

        unknown_count = sum(1 for r in u_classifications if r['classified_type'] == 'unknown')
        attention_count = sum(1 for r in u_classifications if r['requires_human_attention'] == 'yes')
        by_university.append({
            'university_id': uid,
            'university_name': entry.get('university_name', ''),
            'candidate_links_count': len(candidate_rows),
            'classified_links_count': len(u_classifications),
            'unknown_links_count': unknown_count,
            'requires_attention_count': attention_count,
            'last_updated_utc': classified_at,
        })

    write_csv(OUTPUT_INDEX_PATH, classifications, CLASSIFICATION_HEADER)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    (OUTPUT_DIR / 'README.md').write_text(
        '# Document link classification\n\nNeutral, source-oriented classification of candidate links from approved source inventories.\n',
        encoding='utf-8',
    )
    (OUTPUT_DIR / 'classification_rules.md').write_text(
        '# Classification rules\n\nThis layer applies lightweight keyword-based neutral categories to candidate links.\nUnknown and low-confidence results remain visible and are marked for human attention.\n',
        encoding='utf-8',
    )
    (OUTPUT_DIR / 'classification_progress.md').write_text(
        f'# Classification progress\n\n- Updated at UTC: {classified_at}\n- Universities processed: {len(by_university)}\n- Candidate links observed: {sum(x["candidate_links_count"] for x in by_university)}\n',
        encoding='utf-8',
    )
    (OUTPUT_DIR / 'handoff.md').write_text(
        '# Handoff\n\nNext step: human review of unknown/low-confidence classifications; no raw-document download in this run.\n',
        encoding='utf-8',
    )

    progress = {
        'updated_at_utc': classified_at,
        'universities_processed': len(by_university),
        'universities_with_candidate_links': sum(1 for x in by_university if x['candidate_links_count'] > 0),
        'total_candidate_links': sum(x['candidate_links_count'] for x in by_university),
        'total_classified_links': sum(x['classified_links_count'] for x in by_university),
        'unknown_links': sum(x['unknown_links_count'] for x in by_university),
        'depth_1_pages_followed': 0,
        'fetch_errors': 0,
        'links_requiring_attention': sum(x['requires_attention_count'] for x in by_university),
        'progress_events': ['Built governed document-link classification layer from approved source-inventory candidate-link files.'],
        'by_university': by_university,
    }
    OUTPUT_PROGRESS_PATH.write_text(json.dumps(progress, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')

if __name__ == '__main__':
    main()
