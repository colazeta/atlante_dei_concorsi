#!/usr/bin/env python3
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE_DATA = ROOT / 'site' / 'data'
SOURCE_PROGRESS_PATH = SITE_DATA / 'source_inventory_progress.json'
CLASSIFICATION_PROGRESS_PATH = SITE_DATA / 'document_link_classification_progress.json'
OUTPUT_PATH = SITE_DATA / 'automation_status.json'
EXPECTED_REFRESH_CADENCE_MINUTES = 10


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def parse_utc_timestamp(value: str | None) -> datetime | None:
    if not value:
        return None
    text = value.strip()
    if text.endswith('Z'):
        text = text[:-1] + '+00:00'
    try:
        return datetime.fromisoformat(text)
    except ValueError:
        return None


def read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except json.JSONDecodeError:
        return {}


def to_iso_utc(value: datetime | None) -> str | None:
    if value is None:
        return None
    return value.astimezone(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')


def age_minutes(now: datetime, timestamp: datetime | None) -> int | None:
    if timestamp is None:
        return None
    delta = now - timestamp.astimezone(timezone.utc)
    return max(0, int(delta.total_seconds() // 60))


def freshness_status(source_age: int | None, classification_age: int | None) -> str:
    if source_age is None or classification_age is None:
        return 'unknown'
    threshold = EXPECTED_REFRESH_CADENCE_MINUTES * 2
    return 'fresh' if source_age <= threshold and classification_age <= threshold else 'stale'


def main() -> None:
    now = utc_now().replace(microsecond=0)
    source = read_json(SOURCE_PROGRESS_PATH)
    classification = read_json(CLASSIFICATION_PROGRESS_PATH)

    source_updated = parse_utc_timestamp(source.get('updated_at_utc'))
    classification_updated = parse_utc_timestamp(classification.get('updated_at_utc'))

    source_age = age_minutes(now, source_updated)
    classification_age = age_minutes(now, classification_updated)
    freshness = freshness_status(source_age, classification_age)

    warnings: list[str] = []
    if freshness == 'stale':
        warnings.append('Latest progress data appear older than the expected automation cadence.')
    if source_updated is None:
        warnings.append('Source inventory progress timestamp is unavailable.')
    if classification_updated is None:
        warnings.append('Document classification progress timestamp is unavailable.')

    source_counts = {
        'source_run_status': source.get('run_status'),
        'source_no_progress_reason': source.get('no_progress_reason'),
        'total_intake_packs': source.get('total_intake_packs'),
        'source_inventories_created': source.get('inventories_created'),
        'candidate_links_observed': source.get('candidate_links_total'),
        'source_fetch_errors': source.get('fetch_errors', source.get('errors')),
        'source_records_needing_attention': source.get('inventories_needing_attention'),
    }
    classification_counts = {
        'document_links_classified': classification.get('total_classified_links'),
        'classification_records_needing_attention': classification.get('links_requiring_attention'),
    }

    status = {
        'updated_at_utc': to_iso_utc(now),
        'pages_deploy_status': 'generated_predeploy',
        'source_inventory_last_updated_utc': source.get('updated_at_utc'),
        'document_classification_last_updated_utc': classification.get('updated_at_utc'),
        'source_inventory_freshness_minutes': source_age,
        'document_classification_freshness_minutes': classification_age,
        'expected_refresh_cadence_minutes': EXPECTED_REFRESH_CADENCE_MINUTES,
        'freshness_status': freshness,
        'latest_counts': {**source_counts, **classification_counts},
        'warnings': warnings,
        'next_expected_step': 'Continue scheduled source-inventory and document-classification refresh cycle.',
    }

    OUTPUT_PATH.write_text(json.dumps(status, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
