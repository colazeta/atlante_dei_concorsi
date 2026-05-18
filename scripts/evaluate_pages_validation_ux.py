#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'site/index.html'
AUTOMATION = ROOT / 'site/data/automation_status.json'
TRIAGE = ROOT / 'site/data/document_link_triage_progress.json'
OUT = ROOT / 'reports/ux-evaluator'
HISTORY = OUT / 'history'
LATEST = OUT / 'latest_state.json'

FOCUS_AREAS = [
    'single-row validation speed',
    'bulk submission clarity',
    'triage filter discoverability',
    'review progress visibility',
    'excluded-link auditability',
    'empty and stale states',
    'accessibility and keyboard navigation',
    'table density and scanability',
]


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')


def read_text(path: Path) -> str:
    return path.read_text(encoding='utf-8') if path.exists() else ''


def read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except json.JSONDecodeError:
        return {}


def pick_focus(stamp: str) -> str:
    minute_bucket = int(datetime.fromisoformat(stamp.replace('Z', '+00:00')).timestamp() // 1800)
    return FOCUS_AREAS[minute_bucket % len(FOCUS_AREAS)]


def evaluate(html: str, automation: dict, triage: dict, focus: str) -> dict:
    latest = automation.get('latest_counts', {})
    checks = {
        'has_single_row_approve': 'quick-approve' in html,
        'has_single_row_reject': 'quick-reject' in html,
        'has_single_row_submit': 'submit-one' in html,
        'has_bulk_submit': 'submit-link-decisions-github' in html,
        'has_selected_submit': 'submit-selected-link-decisions-github' in html,
        'has_priority_queue': 'priority-queue' in html,
        'has_triage_filters': 'triage-filter' in html and 'keep-filter' in html,
        'has_progress_cards': 'review-progress-cards' in html,
        'triage_metrics_available': bool(latest.get('triaged_links')),
        'triage_progress_available': bool(triage.get('total_triaged_links')),
    }

    findings = []
    if not checks['has_single_row_approve'] or not checks['has_single_row_reject']:
        findings.append({
            'severity': 'high',
            'issue': 'The reviewer cannot approve/reject each row with one click.',
            'proposed_fix': 'Add row-level quick action buttons for approve, reject and needs-more-evidence.',
            'files_likely_touched': ['site/index.html'],
            'automatic_patch_safe': True,
        })
    if not checks['has_single_row_submit']:
        findings.append({
            'severity': 'medium',
            'issue': 'The reviewer cannot submit a single validated row directly.',
            'proposed_fix': 'Add a per-row submit action that opens a prefilled GitHub issue for that row.',
            'files_likely_touched': ['site/index.html'],
            'automatic_patch_safe': True,
        })
    if not checks['has_triage_filters']:
        findings.append({
            'severity': 'high',
            'issue': 'Triage filters are missing or incomplete.',
            'proposed_fix': 'Expose triage status and keep/exclude filters in the sticky filter bar.',
            'files_likely_touched': ['site/index.html'],
            'automatic_patch_safe': False,
        })
    if not checks['triage_metrics_available']:
        findings.append({
            'severity': 'medium',
            'issue': 'Automation status does not expose triage metrics.',
            'proposed_fix': 'Ensure automation_status.json includes triaged, kept, excluded and unknown counts.',
            'files_likely_touched': ['scripts/build_automation_status.py', 'site/index.html'],
            'automatic_patch_safe': False,
        })
    if not findings:
        findings.append({
            'severity': 'low',
            'issue': f'No blocking UX gap detected for focus area: {focus}.',
            'proposed_fix': 'Continue monitoring and use manual reviewer feedback to refine microcopy and workflow density.',
            'files_likely_touched': [],
            'automatic_patch_safe': False,
        })

    return {'checks': checks, 'findings': findings}


def main() -> None:
    stamp = now_utc()
    focus = pick_focus(stamp)
    html = read_text(SITE)
    automation = read_json(AUTOMATION)
    triage = read_json(TRIAGE)
    result = evaluate(html, automation, triage, focus)
    digest = hashlib.sha256(json.dumps(result, sort_keys=True).encode()).hexdigest()[:16]

    OUT.mkdir(parents=True, exist_ok=True)
    HISTORY.mkdir(parents=True, exist_ok=True)
    report_name = f'{stamp.replace(":", "").replace("-", "").replace("Z", "Z")}_report.md'
    state = {
        'evaluator_id': 'PAGES-UX-EVALUATOR-0001',
        'status': 'completed',
        'created_at_utc': stamp,
        'updated_at_utc': stamp,
        'focus_area': focus,
        'fingerprint': digest,
        'checks': result['checks'],
        'findings': result['findings'],
        'human_review_required': any(f['severity'] in {'high', 'medium'} for f in result['findings']),
        'next_action': result['findings'][0]['proposed_fix'] if result['findings'] else 'Continue monitoring.',
    }
    LATEST.write_text(json.dumps(state, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')

    lines = [
        f'# Pages UX evaluator report — {stamp}',
        '',
        f'- Focus area: `{focus}`',
        f'- Fingerprint: `{digest}`',
        f'- Human review required: `{state["human_review_required"]}`',
        '',
        '## Checks',
        '',
    ]
    lines.extend([f'- `{k}`: `{v}`' for k, v in result['checks'].items()])
    lines.extend(['', '## Findings', ''])
    for item in result['findings']:
        lines.extend([
            f'### {item["severity"].upper()} — {item["issue"]}',
            '',
            f'- Proposed fix: {item["proposed_fix"]}',
            f'- Files likely touched: {", ".join(item["files_likely_touched"]) or "none"}',
            f'- Automatic patch safe: `{item["automatic_patch_safe"]}`',
            '',
        ])
    (HISTORY / report_name).write_text('\n'.join(lines), encoding='utf-8')


if __name__ == '__main__':
    main()
