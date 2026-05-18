#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import re
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
TRIAGE_JSON = ROOT / 'site/data/document_link_triage_index.json'
OUT = ROOT / 'docs/executions/document-link-confirmation'
SITE_OUT = ROOT / 'site/data/document_link_confirmation_progress.json'
INDEX = OUT / 'document_link_confirmation_index.csv'

HEADER = [
    'confirmation_id', 'university_id', 'source_url', 'link_url', 'link_text',
    'triage_status', 'confirmation_status', 'confirmation_confidence',
    'strong_signals', 'weak_signals', 'negative_signals', 'http_status',
    'content_type', 'requires_human_attention', 'reason', 'checked_at_utc'
]

STRONG_PATTERNS = [
    r'\bbando\b', r'\bconcors[oi]\b', r'procedure? selettiv[ae]',
    r'reclutamento', r'professor[ei]', r'ricercator[ei]', r'assegn[oi] di ricerca',
    r'commissione giudicatrice', r'criteri di valutazione', r'graduatoria',
    r'approvazione atti', r'personale tecnico amministrativo', r'valutazione comparativa'
]
WEAK_PATTERNS = [
    r'albo', r'avvis[oi]', r'selezion[ei]', r'lavor[ao] con noi', r'posizion[ei]',
    r'career', r'job', r'call', r'opportunit[àa]'
]
NEGATIVE_PATTERNS = [
    r'privacy', r'cookie', r'accessibilit[àa]', r'contatti', r'sitemap',
    r'newsletter', r'facebook', r'instagram', r'linkedin', r'youtube'
]

class TextParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []
        self._skip = False
    def handle_starttag(self, tag, attrs):
        if tag in {'script', 'style', 'noscript'}:
            self._skip = True
    def handle_endtag(self, tag):
        if tag in {'script', 'style', 'noscript'}:
            self._skip = False
    def handle_data(self, data):
        if not self._skip:
            self.parts.append(data)
    def text(self) -> str:
        return ' '.join(' '.join(self.parts).split())

def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')

def read_triage() -> list[dict[str, str]]:
    if not TRIAGE_JSON.exists():
        return []
    return json.loads(TRIAGE_JSON.read_text(encoding='utf-8')).get('entries', [])

def fetch_text(url: str) -> tuple[str, str, str]:
    req = Request(url, headers={'User-Agent': 'atlante-agent/1.0'})
    with urlopen(req, timeout=20) as r:
        status = str(getattr(r, 'status', 200))
        ctype = r.headers.get('content-type', '')
        data = r.read(800_000)
    if 'html' in ctype.lower():
        parser = TextParser()
        parser.feed(data.decode('utf-8', errors='ignore'))
        return status, ctype, parser.text().lower()
    return status, ctype, data[:120_000].decode('utf-8', errors='ignore').lower()

def hits(text: str, patterns: list[str]) -> list[str]:
    out = []
    for p in patterns:
        if re.search(p, text, flags=re.IGNORECASE):
            out.append(p)
    return out

def classify(row: dict[str, str], stamp: str, idx: int) -> dict[str, str]:
    url = row.get('link_url', '')
    triage_status = row.get('triage_status', '')
    if not url or urlparse(url).scheme not in {'http', 'https'}:
        return make_row(row, idx, stamp, 'review', 'not_determinable', [], [], [], '', '', 'Invalid or missing URL.')
    if row.get('exclude_from_competition_queue') == 'yes':
        return make_row(row, idx, stamp, 'review', 'low', [], [], [], '', '', 'Excluded/deprioritised by triage; kept in review, not confirmed.')
    try:
        status, ctype, text = fetch_text(url)
    except (HTTPError, URLError, TimeoutError, ValueError) as e:
        return make_row(row, idx, stamp, 'review', 'not_determinable', [], [], [], '', '', f'Fetch failed: {str(e)[:160]}')
    strong = hits(text, STRONG_PATTERNS)
    weak = hits(text, WEAK_PATTERNS)
    negative = hits(text, NEGATIVE_PATTERNS)
    if len(strong) >= 2 or (strong and triage_status in {'likely_competition_source', 'possible_competition_source'}):
        return make_row(row, idx, stamp, 'confirmed', 'high' if len(strong) >= 2 else 'medium', strong, weak, negative, status, ctype, 'Strong competition/procedure evidence found on fetched page.')
    if strong or len(weak) >= 2:
        return make_row(row, idx, stamp, 'review', 'medium', strong, weak, negative, status, ctype, 'Partial signals found; not enough for confirmation.')
    return make_row(row, idx, stamp, 'review', 'low', strong, weak, negative, status, ctype, 'No sufficient competition/procedure evidence found.')

def make_row(row, idx, stamp, status, conf, strong, weak, neg, http_status, ctype, reason):
    return {
        'confirmation_id': f"{row.get('university_id','')}-confirm-{idx:05d}",
        'university_id': row.get('university_id',''),
        'source_url': row.get('source_url',''),
        'link_url': row.get('link_url',''),
        'link_text': row.get('link_text',''),
        'triage_status': row.get('triage_status',''),
        'confirmation_status': status,
        'confirmation_confidence': conf,
        'strong_signals': ';'.join(strong),
        'weak_signals': ';'.join(weak),
        'negative_signals': ';'.join(neg),
        'http_status': http_status,
        'content_type': ctype,
        'requires_human_attention': 'no' if status == 'confirmed' else 'yes',
        'reason': reason,
        'checked_at_utc': stamp,
    }

def main() -> None:
    stamp = now()
    rows = read_triage()
    candidates = [r for r in rows if r.get('keep_for_review') == 'yes'][:60]
    confirmed = [classify(r, stamp, i + 1) for i, r in enumerate(candidates)]
    OUT.mkdir(parents=True, exist_ok=True)
    with INDEX.open('w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=HEADER)
        w.writeheader(); w.writerows(confirmed)
    counts = {
        'updated_at_utc': stamp,
        'triage_links_read': len(rows),
        'links_checked': len(confirmed),
        'confirmed_links': sum(1 for r in confirmed if r['confirmation_status'] == 'confirmed'),
        'review_links': sum(1 for r in confirmed if r['confirmation_status'] == 'review'),
        'progress_events': ['Built controlled competition-evidence confirmation layer from fetched candidate links.'],
    }
    SITE_OUT.write_text(json.dumps(counts, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    (OUT / 'README.md').write_text('# Document link confirmation\n\nControlled evidence confirmation layer. Confirmed means strong public-competition/procedure signals were found on the fetched page. Non-confirmed links remain in review. No raw page content is stored.\n', encoding='utf-8')

if __name__ == '__main__':
    main()
