#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
INVENTORIES_ROOT = ROOT / 'docs/executions/approved-source-inventories'
CLASSIFICATION_INDEX = ROOT / 'docs/executions/document-link-classification/document_link_classification_index.csv'
OUTPUT_DIR = ROOT / 'docs/executions/document-link-triage'
OUTPUT_INDEX = OUTPUT_DIR / 'document_link_triage_index.csv'
OUTPUT_PROGRESS = ROOT / 'site/data/document_link_triage_progress.json'

TRIAGE_STATUSES = {
    'likely_competition_source',
    'possible_competition_source',
    'generic_institutional_page',
    'likely_not_relevant',
    'unknown_requires_review',
}

HEADER = [
    'triage_id',
    'university_id',
    'source_url',
    'link_url',
    'link_text',
    'classified_type',
    'triage_status',
    'triage_confidence',
    'keep_for_review',
    'exclude_from_competition_queue',
    'exclusion_reason',
    'positive_signals',
    'negative_signals',
    'requires_human_attention',
    'observed_at_utc',
    'triaged_at_utc',
]

STRONG_POSITIVE = [
    'concorsi', 'bando', 'bandi', 'selezione', 'selezioni', 'reclutamento',
    'professori', 'professore', 'ricercatori', 'ricercatore', 'assegni',
    'assegno di ricerca', 'tecnologi', 'tecnologo', 'personale tecnico-amministrativo',
    'pta', 'graduatoria', 'ammessi', 'ammissione', 'commissione', 'criteri',
    'valutazione', 'valutazioni', 'approvazione atti', 'atti finali',
    'procedure selettive', 'chiamate', 'lavora con noi', 'lavora-con-noi',
]

WEAK_POSITIVE = [
    'albo', 'avvisi', 'avviso', 'opportunità', 'opportunita', 'carriere',
    'job', 'jobs', 'position', 'positions', 'calls', 'work with us', 'careers',
]

NEGATIVE_GENERIC = [
    'privacy', 'cookie', 'accessibilita', 'accessibilità', 'note legali',
    'credits', 'urp', 'contatti', 'contact', 'contacts', 'mappa del sito',
    'sitemap', 'newsletter', 'facebook', 'twitter', 'linkedin', 'instagram',
    'youtube', 'login', 'area riservata', 'webmail', 'pec', 'rss', 'feed',
    'comunicati stampa', 'press', 'news', 'eventi', 'events', 'calendario',
    'biblioteca', 'library', 'mensa', 'orientamento', 'didattica', 'studenti',
    'students', 'erasmus', 'international', 'campus', 'rubrica', 'telefono',
    'faq', 'helpdesk', 'whistleblowing', 'amministrazione trasparente',
]

GENERIC_PATHS = [
    '/privacy', '/cookie', '/cookies', '/accessibilita', '/accessibilità',
    '/contatti', '/contacts', '/contact', '/sitemap', '/mappa-del-sito',
    '/news', '/eventi', '/events', '/press', '/login', '/user', '/users',
]

COMPETITION_CLASSIFIED_TYPES = {
    'call_notice_candidate',
    'committee_appointment_candidate',
    'evaluation_criteria_candidate',
    'admission_or_candidate_list_candidate',
    'final_acts_approval_candidate',
}

LISTING_CLASSIFIED_TYPES = {'competition_listing', 'recruitment_page'}


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


def norm(value: str | None) -> str:
    return (value or '').strip().lower()


def find_signals(tokens: str, patterns: list[str]) -> list[str]:
    return [p for p in patterns if p in tokens]


def is_external(link_url: str, source_url: str) -> bool:
    link_host = urlparse(link_url).netloc.lower()
    source_host = urlparse(source_url).netloc.lower()
    return bool(link_host and source_host and link_host != source_host)


def triage_row(row: dict[str, str], idx: int, triaged_at: str) -> dict[str, str]:
    uid = row.get('university_id', '').strip()
    source_url = row.get('source_url', '').strip()
    link_url = row.get('link_url', '').strip()
    link_text = row.get('link_text', '').strip()
    classified_type = row.get('classified_type', '').strip() or 'unknown'

    parsed_path = urlparse(link_url).path.lower()
    tokens = ' '.join([
        norm(link_text),
        norm(link_url),
        norm(parsed_path.replace('-', ' ').replace('_', ' ')),
        norm(classified_type),
    ])

    positive = find_signals(tokens, STRONG_POSITIVE)
    weak_positive = find_signals(tokens, WEAK_POSITIVE)
    negative = find_signals(tokens, NEGATIVE_GENERIC)
    negative.extend([p for p in GENERIC_PATHS if p in parsed_path])
    negative = sorted(set(negative))
    positive = sorted(set(positive + weak_positive))

    external = is_external(link_url, source_url)
    if external:
        negative.append('external_domain')

    triage_status = 'unknown_requires_review'
    confidence = 'not_determinable'
    keep = 'yes'
    exclude = 'no'
    exclusion_reason = ''
    requires_attention = 'yes'

    if classified_type in COMPETITION_CLASSIFIED_TYPES and positive:
        triage_status = 'likely_competition_source'
        confidence = 'high'
        keep = 'yes'
        exclude = 'no'
        requires_attention = 'no'
    elif classified_type in LISTING_CLASSIFIED_TYPES or positive:
        triage_status = 'possible_competition_source'
        confidence = 'medium' if positive else 'low'
        keep = 'yes'
        exclude = 'no'
        requires_attention = 'yes'
    elif negative and not positive:
        if any(sig in negative for sig in ['privacy', 'cookie', 'sitemap', 'mappa del sito', 'accessibilita', 'accessibilità', 'note legali', 'credits', 'external_domain']):
            triage_status = 'likely_not_relevant'
            confidence = 'medium'
            exclusion_reason = 'Negative navigation/legal/external-domain signal without competition signal.'
        else:
            triage_status = 'generic_institutional_page'
            confidence = 'low'
            exclusion_reason = 'Generic institutional or service-page signal without competition signal.'
        keep = 'no'
        exclude = 'yes'
        requires_attention = 'no' if confidence == 'medium' else 'yes'
    elif not link_text and not link_url:
        triage_status = 'unknown_requires_review'
        confidence = 'not_determinable'
        keep = 'yes'
        exclude = 'no'
        requires_attention = 'yes'
    else:
        triage_status = 'unknown_requires_review'
        confidence = 'not_determinable'
        keep = 'yes'
        exclude = 'no'
        requires_attention = 'yes'

    if triage_status not in TRIAGE_STATUSES:
        triage_status = 'unknown_requires_review'
        confidence = 'not_determinable'
        keep = 'yes'
        exclude = 'no'
        exclusion_reason = ''
        requires_attention = 'yes'

    if exclude == 'yes' and not exclusion_reason:
        exclusion_reason = 'Excluded from competition queue by deterministic non-pertinence rule.'

    return {
        'triage_id': f'{uid}-triage-{idx:05d}',
        'university_id': uid,
        'source_url': source_url,
        'link_url': link_url,
        'link_text': link_text,
        'classified_type': classified_type,
        'triage_status': triage_status,
        'triage_confidence': confidence,
        'keep_for_review': keep,
        'exclude_from_competition_queue': exclude,
        'exclusion_reason': exclusion_reason,
        'positive_signals': ';'.join(sorted(set(positive))),
        'negative_signals': ';'.join(sorted(set(negative))),
        'requires_human_attention': requires_attention,
        'observed_at_utc': row.get('observed_at_utc', ''),
        'triaged_at_utc': triaged_at,
    }


def count_candidate_links_from_inventories() -> int:
    total = 0
    for path in INVENTORIES_ROOT.glob('*/candidate_document_links.csv'):
        total += len(read_csv(path))
    return total


def main() -> None:
    triaged_at = now_utc()
    classified_rows = read_csv(CLASSIFICATION_INDEX)
    triaged = [triage_row(row, idx + 1, triaged_at) for idx, row in enumerate(classified_rows)]
    write_csv(OUTPUT_INDEX, triaged, HEADER)

    status_counts = Counter(row['triage_status'] for row in triaged)
    exclusion_reasons = Counter(row['exclusion_reason'] for row in triaged if row['exclusion_reason'])
    total_candidate_inventory = count_candidate_links_from_inventories()
    kept = sum(1 for row in triaged if row['keep_for_review'] == 'yes')
    excluded = sum(1 for row in triaged if row['exclude_from_competition_queue'] == 'yes')
    attention = sum(1 for row in triaged if row['requires_human_attention'] == 'yes')

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / 'README.md').write_text(
        '# Document link triage\n\nDeterministic, reversible relevance triage for candidate links observed from approved university source pages.\nNo records are deleted; links may only be marked as kept, excluded/deprioritised, or requiring review.\n',
        encoding='utf-8',
    )
    (OUTPUT_DIR / 'triage_rules.md').write_text(
        '# Triage rules\n\nThe triage layer applies transparent positive and negative lexical/path signals.\nPositive competition signals retain links for review. Negative navigation, legal, contact, social, login, sitemap, privacy or external-domain signals may exclude links from the competition queue only when no competition signal is present.\nUnknown or conflicting cases remain reviewable.\n',
        encoding='utf-8',
    )
    (OUTPUT_DIR / 'triage_progress.md').write_text(
        f'# Triage progress\n\n- Updated at UTC: {triaged_at}\n- Triaged links: {len(triaged)}\n- Kept for review: {kept}\n- Excluded/deprioritised: {excluded}\n- Requiring attention: {attention}\n',
        encoding='utf-8',
    )
    (OUTPUT_DIR / 'handoff.md').write_text(
        '# Handoff\n\nNext step: review likely/possible competition sources first, then inspect unknown cases. Excluded records remain auditable and reversible.\n',
        encoding='utf-8',
    )

    progress = {
        'updated_at_utc': triaged_at,
        'total_candidate_links_from_inventories': total_candidate_inventory,
        'total_classified_links_read': len(classified_rows),
        'total_triaged_links': len(triaged),
        'kept_for_review': kept,
        'excluded_from_competition_queue': excluded,
        'requires_human_attention': attention,
        'likely_competition_sources': status_counts.get('likely_competition_source', 0),
        'possible_competition_sources': status_counts.get('possible_competition_source', 0),
        'generic_institutional_pages': status_counts.get('generic_institutional_page', 0),
        'likely_not_relevant': status_counts.get('likely_not_relevant', 0),
        'unknown_requires_review': status_counts.get('unknown_requires_review', 0),
        'top_exclusion_reasons': [
            {'reason': reason, 'count': count}
            for reason, count in exclusion_reasons.most_common(10)
        ],
        'progress_events': [
            'Built governed deterministic relevance triage from document-link classification output.'
        ],
    }
    OUTPUT_PROGRESS.write_text(json.dumps(progress, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
