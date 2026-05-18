#!/usr/bin/env python3
from __future__ import annotations
import argparse, csv, json
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

ROOT = Path(__file__).resolve().parents[1]
INV_ROOT = ROOT / 'docs/executions/approved-source-inventories'
INTAKE_INDEX = ROOT / 'docs/executions/source-intake-packs/source_intake_index.csv'
SOURCE_INDEX = INV_ROOT / 'source_inventory_index.csv'
SOURCE_PROGRESS = ROOT / 'site/data/source_inventory_progress.json'
CAND_PROGRESS = ROOT / 'site/data/document_link_classification_progress.json'

CAND_HDR = [
    'university_id', 'source_url', 'discovery_depth', 'parent_url', 'link_url',
    'link_text', 'link_type_hint', 'same_domain', 'keyword_match',
    'confidence_level', 'requires_human_attention', 'blocking_status',
    'notes', 'observed_at_utc'
]
OBS_HDR = [
    'university_id', 'source_url', 'http_status', 'content_type',
    'page_title', 'observed_at_utc', 'error'
]
SOURCE_HDR = [
    'university_id', 'university_name', 'intake_pack_exists', 'inventory_exists',
    'homepage_url', 'recruitment_url', 'fetch_status', 'candidate_links_count',
    'requires_human_attention', 'blocking_status', 'last_updated_utc'
]
ALLOWED_HINTS = {
    'call_notice_candidate', 'committee_appointment_candidate',
    'evaluation_criteria_candidate', 'admission_or_candidate_list_candidate',
    'final_acts_approval_candidate', 'recruitment_page', 'competition_listing',
    'other_official_document_candidate', 'unknown'
}
CONTROLLED_KEYWORDS = [
    'concorsi', 'bandi', 'reclutamento', 'selezioni', 'professori',
    'ricercatori', 'assegni', 'albo', 'chiamate', 'valutazioni comparative',
    'procedure selettive', 'lavora con noi'
]


class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self._href = None
        self._txt = []
        self.title = ''
        self._in_title = False

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            self._href = dict(attrs).get('href')
            self._txt = []
        if tag == 'title':
            self._in_title = True

    def handle_endtag(self, tag):
        if tag == 'a' and self._href:
            self.links.append((self._href, ' '.join(''.join(self._txt).split())))
            self._href = None
            self._txt = []
        if tag == 'title':
            self._in_title = False

    def handle_data(self, data):
        if self._href is not None:
            self._txt.append(data)
        if self._in_title:
            self.title += data


def now():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, str]], header: list[str]):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=header)
        w.writeheader()
        w.writerows(rows)


def normalise_url(value: str | None) -> str:
    value = (value or '').strip()
    if not value or value.upper() == 'MISSING':
        return ''
    return value


def hint(url, text):
    t = f"{url} {text}".lower()
    if any(k in t for k in ['bando', 'call']):
        return 'call_notice_candidate'
    if any(k in t for k in ['commissione', 'committee']):
        return 'committee_appointment_candidate'
    if any(k in t for k in ['criteri', 'criteria']):
        return 'evaluation_criteria_candidate'
    if any(k in t for k in ['graduatoria', 'ammissione', 'ammessi']):
        return 'admission_or_candidate_list_candidate'
    if any(k in t for k in ['approvazione atti', 'atti finali']):
        return 'final_acts_approval_candidate'
    if any(k in t for k in ['concorsi', 'reclutamento', 'lavora-con-noi']):
        return 'competition_listing'
    if any(k in t for k in ['pdf', '.doc', '.odt']):
        return 'other_official_document_candidate'
    return 'unknown'


def keyword_match(url, text):
    t = f"{url} {text}".lower()
    return any(k in t for k in CONTROLLED_KEYWORDS)


def fetch(url):
    req = Request(url, headers={'User-Agent': 'atlante-agent/1.0'})
    with urlopen(req, timeout=20) as r:
        ctype = r.headers.get('content-type', '')
        status = getattr(r, 'status', 200)
        data = r.read(1_000_000)
    return status, ctype, data


def source_index_by_id(source_idx):
    return {r.get('university_id', ''): r for r in source_idx}


def ensure_source_rows(intake, source_idx, stamp):
    existing = source_index_by_id(source_idx)
    for r in intake:
        uid = r.get('university_id', '')
        if not uid:
            continue
        homepage = normalise_url(r.get('official_homepage_url'))
        recruitment = normalise_url(r.get('recruitment_page_url'))
        if uid not in existing:
            row = {
                'university_id': uid,
                'university_name': r.get('university_name', ''),
                'intake_pack_exists': 'yes',
                'inventory_exists': 'yes',
                'homepage_url': homepage,
                'recruitment_url': recruitment,
                'fetch_status': 'pending_fetch',
                'candidate_links_count': '0',
                'requires_human_attention': 'yes' if r.get('requires_human_attention') == 'true' else 'no',
                'blocking_status': 'awaiting_bounded_fetch' if (homepage or recruitment) else 'missing_approved_url',
                'last_updated_utc': stamp,
            }
            source_idx.append(row)
            existing[uid] = row
        else:
            existing[uid]['university_name'] = existing[uid].get('university_name') or r.get('university_name', '')
            existing[uid]['intake_pack_exists'] = existing[uid].get('intake_pack_exists') or 'yes'
            existing[uid]['inventory_exists'] = existing[uid].get('inventory_exists') or 'yes'
            existing[uid]['homepage_url'] = homepage
            existing[uid]['recruitment_url'] = recruitment
            if existing[uid].get('fetch_status') in {'', 'pending_fetch'}:
                existing[uid]['blocking_status'] = 'awaiting_bounded_fetch' if (homepage or recruitment) else 'missing_approved_url'
    return source_idx


def select_picks(intake, source_idx, args):
    idx = source_index_by_id(source_idx)
    eligible = []
    for r in intake:
        uid = r.get('university_id', '')
        if args.university_id and uid != args.university_id:
            continue
        homepage = normalise_url(r.get('official_homepage_url'))
        recruitment = normalise_url(r.get('recruitment_page_url'))
        if not homepage and not recruitment:
            continue
        current = idx.get(uid, {})
        fetch_status = current.get('fetch_status', 'pending_fetch')
        candidate_count = int((current.get('candidate_links_count') or '0').strip() or '0')
        if args.refetch or fetch_status != 'fetched' or candidate_count == 0:
            eligible.append(r)
    return eligible[:max(args.batch_size, 0)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--batch-size', type=int, default=5)
    ap.add_argument('--university-id', default='')
    ap.add_argument('--max-links-per-page', type=int, default=40)
    ap.add_argument('--max-follow-links-per-university', type=int, default=10)
    ap.add_argument('--depth', type=int, choices=[0, 1], default=0)
    ap.add_argument('--refetch', action='store_true', help='Refetch already fetched universities.')
    args = ap.parse_args()

    intake = read_csv(INTAKE_INDEX)
    source_idx = read_csv(SOURCE_INDEX)
    before_source = SOURCE_PROGRESS.read_text(encoding='utf-8') if SOURCE_PROGRESS.exists() else ''
    before_cand = CAND_PROGRESS.read_text(encoding='utf-8') if CAND_PROGRESS.exists() else ''

    stamp = now()
    source_idx = ensure_source_rows(intake, source_idx, stamp)
    picks = select_picks(intake, source_idx, args)
    idx = source_index_by_id(source_idx)

    errors = 0
    universities_fetched = 0
    seed_urls_attempted = 0
    depth_1_pages_followed = 0
    candidate_links_found = 0

    for r in picks:
        uid = r['university_id']
        inv = INV_ROOT / uid
        inv.mkdir(parents=True, exist_ok=True)
        recruitment_url = normalise_url(r.get('recruitment_page_url'))
        homepage_url = normalise_url(r.get('official_homepage_url'))
        urls = [u for u in [recruitment_url, homepage_url] if u]
        source_url = urls[0] if urls else ''
        obs = read_csv(inv / 'observed_links.csv')
        cand = read_csv(inv / 'candidate_document_links.csv')
        before_count = len(cand)
        log_lines = [f"- {stamp} | uid={uid}"]
        fetched_success = False

        if not source_url:
            obs.append({
                'university_id': uid, 'source_url': '', 'http_status': '',
                'content_type': '', 'page_title': '', 'observed_at_utc': stamp,
                'error': 'missing_approved_url'
            })
            log_lines.append('  - skipped: missing approved URL in intake index')
        else:
            seed_urls_attempted += 1
            try:
                status, ctype, data = fetch(source_url)
                universities_fetched += 1
                fetched_success = True
                body = data.decode('utf-8', errors='ignore')
                p = LinkParser()
                p.feed(body)
                obs.append({
                    'university_id': uid, 'source_url': source_url,
                    'http_status': str(status), 'content_type': ctype,
                    'page_title': p.title.strip(), 'observed_at_utc': stamp,
                    'error': ''
                })
                srcdom = urlparse(source_url).netloc
                to_follow = []
                seen = {(c.get('link_url'), c.get('parent_url')) for c in cand}
                for href, text in p.links:
                    if len(cand) - before_count >= args.max_links_per_page:
                        break
                    absu = urljoin(source_url, href)
                    pu = urlparse(absu)
                    if pu.scheme not in {'http', 'https'}:
                        continue
                    same = 'yes' if pu.netloc == srcdom else 'no'
                    km = 'yes' if keyword_match(absu, text) else 'no'
                    h = hint(absu, text)
                    h = h if h in ALLOWED_HINTS else 'unknown'
                    key = (absu, source_url)
                    if key not in seen:
                        cand.append({
                            'university_id': uid, 'source_url': source_url,
                            'discovery_depth': '0', 'parent_url': source_url,
                            'link_url': absu, 'link_text': text[:300],
                            'link_type_hint': h, 'same_domain': same,
                            'keyword_match': km,
                            'confidence_level': 'low' if h == 'unknown' else 'medium',
                            'requires_human_attention': 'yes',
                            'blocking_status': 'needs_human_review',
                            'notes': 'Observed on approved source page with bounded discovery controls.',
                            'observed_at_utc': stamp
                        })
                        seen.add(key)
                    if args.depth == 1 and same == 'yes' and km == 'yes' and len(to_follow) < args.max_follow_links_per_university:
                        to_follow.append((absu, text))

                for follow_url, _t in to_follow:
                    try:
                        f_status, f_ctype, f_data = fetch(follow_url)
                        depth_1_pages_followed += 1
                        fb = f_data.decode('utf-8', errors='ignore')
                        fp = LinkParser()
                        fp.feed(fb)
                        obs.append({
                            'university_id': uid, 'source_url': follow_url,
                            'http_status': str(f_status), 'content_type': f_ctype,
                            'page_title': fp.title.strip(),
                            'observed_at_utc': stamp, 'error': ''
                        })
                        per_page = 0
                        for fhref, ftext in fp.links:
                            if per_page >= args.max_links_per_page:
                                break
                            fabs = urljoin(follow_url, fhref)
                            fu = urlparse(fabs)
                            if fu.scheme not in {'http', 'https'}:
                                continue
                            fsame = 'yes' if fu.netloc == srcdom else 'no'
                            fkm = 'yes' if keyword_match(fabs, ftext) else 'no'
                            if fsame != 'yes' or fkm != 'yes':
                                continue
                            fh = hint(fabs, ftext)
                            fh = fh if fh in ALLOWED_HINTS else 'unknown'
                            key = (fabs, follow_url)
                            if key in seen:
                                continue
                            cand.append({
                                'university_id': uid, 'source_url': source_url,
                                'discovery_depth': '1', 'parent_url': follow_url,
                                'link_url': fabs, 'link_text': ftext[:300],
                                'link_type_hint': fh, 'same_domain': fsame,
                                'keyword_match': fkm,
                                'confidence_level': 'low' if fh == 'unknown' else 'medium',
                                'requires_human_attention': 'yes',
                                'blocking_status': 'needs_human_review',
                                'notes': 'Observed from bounded depth-1 same-domain keyword-relevant follow link.',
                                'observed_at_utc': stamp
                            })
                            seen.add(key)
                            per_page += 1
                    except (HTTPError, URLError, TimeoutError, ValueError) as e:
                        obs.append({
                            'university_id': uid, 'source_url': follow_url,
                            'http_status': '', 'content_type': '', 'page_title': '',
                            'observed_at_utc': stamp,
                            'error': f'depth1:{str(e)[:220]}'
                        })
                        errors += 1
                log_lines.append(
                    f'  - fetched: {source_url} status={status} depth={args.depth} '
                    f'follow_links={len(to_follow)} links_recorded={len(cand) - before_count}'
                )
            except (HTTPError, URLError, TimeoutError, ValueError) as e:
                obs.append({
                    'university_id': uid, 'source_url': source_url,
                    'http_status': '', 'content_type': '', 'page_title': '',
                    'observed_at_utc': stamp, 'error': str(e)[:240]
                })
                log_lines.append(f'  - error: {source_url} err={e}')
                errors += 1

        candidate_links_found += max(0, len(cand) - before_count)
        write_csv(inv / 'observed_links.csv', obs, OBS_HDR)
        write_csv(inv / 'candidate_document_links.csv', cand, CAND_HDR)
        flog = inv / 'fetch_log.md'
        existing = flog.read_text(encoding='utf-8') if flog.exists() else '# Fetch log\n\n'
        flog.write_text(existing + '\n' + '\n'.join(log_lines) + '\n', encoding='utf-8')

        row = idx.get(uid)
        if row:
            row['homepage_url'] = homepage_url
            row['recruitment_url'] = recruitment_url
            row['fetch_status'] = 'fetched' if source_url and fetched_success else 'pending_fetch'
            row['candidate_links_count'] = str(len(cand))
            row['requires_human_attention'] = 'yes'
            row['blocking_status'] = 'needs_human_review' if len(cand) else ('fetch_failed' if source_url else 'missing_approved_url')
            row['last_updated_utc'] = stamp

    if source_idx:
        write_csv(SOURCE_INDEX, source_idx, SOURCE_HDR)

    if len(picks) == 0:
        run_status = 'skipped_no_eligible_urls'
        no_progress_reason = 'No pending approved recruitment/homepage URL was eligible in the selected batch.'
    elif seed_urls_attempted == 0:
        run_status = 'skipped_no_eligible_urls'
        no_progress_reason = 'Selected universities had no approved recruitment/homepage URL.'
    elif errors > 0 and universities_fetched == 0:
        run_status = 'failed_fetch'
        no_progress_reason = 'All eligible source fetch attempts failed.'
    elif candidate_links_found == 0:
        run_status = 'completed_no_links'
        no_progress_reason = 'Fetch completed but no new candidate links were discovered under bounded rules.'
    else:
        run_status = 'productive'
        no_progress_reason = ''

    progress = {
        'updated_at_utc': stamp,
        'run_mode': 'bounded_approved_source_fetch',
        'batch_size': len(picks),
        'depth': args.depth,
        'universities_selected': len(picks),
        'universities_fetched': universities_fetched,
        'seed_urls_attempted': seed_urls_attempted,
        'depth_1_pages_followed': depth_1_pages_followed,
        'candidate_links_found': candidate_links_found,
        'fetch_errors': errors,
        'output_files_changed': 0,
        'run_status': run_status,
        'no_progress_reason': no_progress_reason,
        'notes': [
            'Fetched only approved intake URLs; depth limited to 1; same-domain and keyword-relevant follow links only; no raw document capture.',
            'Source inventory index is hydrated from the governed source-intake index before selecting eligible rows.'
        ]
    }

    SOURCE_PROGRESS.parent.mkdir(parents=True, exist_ok=True)
    SOURCE_PROGRESS.write_text(json.dumps(progress, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    records_requiring_attention = sum(1 for r in source_idx if r.get('requires_human_attention') == 'yes')
    CAND_PROGRESS.write_text(json.dumps({
        'updated_at_utc': stamp,
        'status': 'candidate_links_populated_for_batch',
        'batch_size': len(picks),
        'errors': errors,
        'depth': args.depth,
        'records_requiring_attention': records_requiring_attention,
        'candidate_links_found': candidate_links_found,
        'run_status': run_status,
        'no_progress_reason': no_progress_reason
    }, indent=2) + '\n', encoding='utf-8')

    after_source = SOURCE_PROGRESS.read_text(encoding='utf-8') if SOURCE_PROGRESS.exists() else ''
    after_cand = CAND_PROGRESS.read_text(encoding='utf-8') if CAND_PROGRESS.exists() else ''
    output_files_changed = int(before_source != after_source) + int(before_cand != after_cand)
    progress['output_files_changed'] = output_files_changed
    if output_files_changed == 0:
        progress['run_status'] = 'no_output_change'
        if not progress['no_progress_reason']:
            progress['no_progress_reason'] = 'Progress artifacts were unchanged after execution.'
    SOURCE_PROGRESS.write_text(json.dumps(progress, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
