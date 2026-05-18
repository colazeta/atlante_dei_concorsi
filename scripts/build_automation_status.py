#!/usr/bin/env python3
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE_DATA = ROOT / 'site' / 'data'
SOURCE_PROGRESS_PATH = SITE_DATA / 'source_inventory_progress.json'
CLASSIFICATION_PROGRESS_PATH = SITE_DATA / 'document_link_classification_progress.json'
TRIAGE_PROGRESS_PATH = SITE_DATA / 'document_link_triage_progress.json'
CONFIRMATION_PROGRESS_PATH = SITE_DATA / 'document_link_confirmation_progress.json'
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


def freshness_status(*ages: int | None) -> str:
    if any(age is None for age in ages):
        return 'unknown'
    threshold = EXPECTED_REFRESH_CADENCE_MINUTES * 2
    return 'fresh' if all(age <= threshold for age in ages if age is not None) else 'stale'


def main() -> None:
    now = utc_now().replace(microsecond=0)
    source = read_json(SOURCE_PROGRESS_PATH)
    classification = read_json(CLASSIFICATION_PROGRESS_PATH)
    triage = read_json(TRIAGE_PROGRESS_PATH)
    confirmation = read_json(CONFIRMATION_PROGRESS_PATH)

    source_updated = parse_utc_timestamp(source.get('updated_at_utc'))
    classification_updated = parse_utc_timestamp(classification.get('updated_at_utc'))
    triage_updated = parse_utc_timestamp(triage.get('updated_at_utc'))
    confirmation_updated = parse_utc_timestamp(confirmation.get('updated_at_utc'))

    source_age = age_minutes(now, source_updated)
    classification_age = age_minutes(now, classification_updated)
    triage_age = age_minutes(now, triage_updated) if triage else None
    confirmation_age = age_minutes(now, confirmation_updated) if confirmation else None
    freshness_inputs = [source_age, classification_age]
    if triage:
        freshness_inputs.append(triage_age)
    if confirmation:
        freshness_inputs.append(confirmation_age)
    freshness = freshness_status(*freshness_inputs)

    warnings: list[str] = []
    if freshness == 'stale':
        warnings.append('Latest progress data appear older than the expected automation cadence.')
    if source_updated is None:
        warnings.append('Source inventory progress timestamp is unavailable.')
    if classification_updated is None:
        warnings.append('Document classification progress timestamp is unavailable.')
    if triage and triage_updated is None:
        warnings.append('Document-link triage progress timestamp is unavailable.')
    if confirmation and confirmation_updated is None:
        warnings.append('Document-link confirmation progress timestamp is unavailable.')

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
    triage_counts = {
        'triaged_links': triage.get('total_triaged_links'),
        'triage_kept_for_review': triage.get('kept_for_review'),
        'triage_excluded_from_competition_queue': triage.get('excluded_from_competition_queue'),
        'triage_requires_human_attention': triage.get('requires_human_attention'),
        'triage_likely_competition_sources': triage.get('likely_competition_sources'),
        'triage_possible_competition_sources': triage.get('possible_competition_sources'),
        'triage_generic_institutional_pages': triage.get('generic_institutional_pages'),
        'triage_likely_not_relevant': triage.get('likely_not_relevant'),
        'triage_unknown_requires_review': triage.get('unknown_requires_review'),
    } if triage else {}
    confirmation_counts = {
        'confirmation_links_checked': confirmation.get('links_checked'),
        'confirmation_confirmed_links': confirmation.get('confirmed_links'),
        'confirmation_review_links': confirmation.get('review_links'),
    } if confirmation else {}

    status = {
        'updated_at_utc': to_iso_utc(now),
        'pages_deploy_status': 'generated_predeploy',
        'source_inventory_last_updated_utc': source.get('updated_at_utc'),
        'document_classification_last_updated_utc': classification.get('updated_at_utc'),
        'document_triage_last_updated_utc': triage.get('updated_at_utc') if triage else None,
        'document_confirmation_last_updated_utc': confirmation.get('updated_at_utc') if confirmation else None,
        'source_inventory_freshness_minutes': source_age,
        'document_classification_freshness_minutes': classification_age,
        'document_triage_freshness_minutes': triage_age,
        'document_confirmation_freshness_minutes': confirmation_age,
        'expected_refresh_cadence_minutes': EXPECTED_REFRESH_CADENCE_MINUTES,
        'freshness_status': freshness,
        'latest_counts': {**source_counts, **classification_counts, **triage_counts, **confirmation_counts},
        'top_triage_exclusion_reasons': triage.get('top_exclusion_reasons', []) if triage else [],
        'warnings': warnings,
        'next_expected_step': 'Continue scheduled source-inventory, document-classification, relevance-triage and confirmation refresh cycle.',
    }

    OUTPUT_PATH.write_text(json.dumps(status, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
