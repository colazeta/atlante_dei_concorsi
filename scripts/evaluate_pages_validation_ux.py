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
    bucket = int(datetime.fromisoformat(stamp.replace('Z', '+00:00')).timestamp() // 1800)
    return FOCUS_AREAS[bucket % len(FOCUS_AREAS)]


def choose_route(findings: list[dict], checks: dict, focus: str) -> dict:
    high = sum(1 for f in findings if f.get('severity') == 'high')
    medium = sum(1 for f in findings if f.get('severity') == 'medium')
    core_missing = not checks.get('has_priority_queue') or not checks.get('has_triage_filters') or not checks.get('has_progress_cards')
    structural_focus = focus in {'review progress visibility', 'table density and scanability', 'triage filter discoverability'}
    if high >= 2 or core_missing:
        level = 'broad'; problem = 'systemic_ui_gap'
    elif high or medium >= 2 or structural_focus:
        level = 'iteration'; problem = 'workflow_friction'
    elif medium:
        level = 'safe'; problem = 'local_affordance_gap'
    else:
        level = 'safe'; problem = 'minor_polish'
    return {'recommended_autonomy': level, 'primary_problem_type': problem}


def build_paths(findings: list[dict], checks: dict, focus: str) -> list[dict]:
    paths = []
    if not checks.get('has_single_row_approve') or not checks.get('has_single_row_reject'):
        paths.append({'path_id': 'row_actions', 'goal': 'Let reviewers decide each row directly.', 'scope': 'review_controls', 'files': ['site/index.html']})
    if not checks.get('has_single_row_submit'):
        paths.append({'path_id': 'single_submit', 'goal': 'Let reviewers submit one decision without creating a batch.', 'scope': 'static_js_for_review_flow', 'files': ['site/index.html']})
    if not checks.get('has_unreviewed_filter'):
        paths.append({'path_id': 'unreviewed_queue', 'goal': 'Expose one-click access to unreviewed items.', 'scope': 'review_controls', 'files': ['site/index.html']})
    if not checks.get('has_review_mode_banner'):
        paths.append({'path_id': 'review_guidance', 'goal': 'Make the end-to-end validation journey explicit.', 'scope': 'layout_sections', 'files': ['site/index.html']})
    if focus == 'table density and scanability':
        paths.append({'path_id': 'table_scanability', 'goal': 'Improve readability when many links are present.', 'scope': 'layout_sections', 'files': ['site/index.html']})
    return paths or [{'path_id': 'incremental_polish', 'goal': 'Continue incremental UX polish.', 'scope': 'microcopy', 'files': ['site/index.html']}]


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
        'has_unreviewed_filter': 'show-unreviewed' in html,
        'has_review_mode_banner': 'ux-iteration-banner' in html,
        'triage_metrics_available': bool(latest.get('triaged_links')),
        'triage_progress_available': bool(triage.get('total_triaged_links')),
    }
    findings = []
    def add(sev, ptype, issue, fix, safe=True):
        findings.append({'severity': sev, 'problem_type': ptype, 'issue': issue, 'proposed_fix': fix, 'files_likely_touched': ['site/index.html'], 'patch_safe': safe})
    if not checks['has_single_row_approve'] or not checks['has_single_row_reject']:
        add('high', 'missing_row_actions', 'Reviewer cannot approve/reject each row with one click.', 'Add row-level approve/reject controls.')
    if not checks['has_single_row_submit']:
        add('medium', 'missing_single_submit', 'Reviewer cannot submit one row directly.', 'Add a per-row submit action.')
    if not checks['has_triage_filters']:
        add('high', 'missing_triage_filters', 'Triage filters are missing or incomplete.', 'Expose triage and keep/exclude filters.', False)
    if not checks['has_unreviewed_filter']:
        add('medium', 'missing_unreviewed_filter', 'Reviewer cannot isolate unreviewed items quickly.', 'Add one-click unreviewed filter.')
    if not checks['has_review_mode_banner']:
        add('medium', 'missing_review_guidance', 'Review journey is not explicit enough.', 'Add review-mode guidance section.')
    if not checks['triage_metrics_available']:
        findings.append({'severity': 'medium', 'problem_type': 'missing_metrics', 'issue': 'Triage metrics are not visible in automation status.', 'proposed_fix': 'Expose triage metrics in status.', 'files_likely_touched': ['scripts/build_automation_status.py', 'site/index.html'], 'patch_safe': False})
    if not findings:
        findings.append({'severity': 'low', 'problem_type': 'minor_polish', 'issue': f'No blocking UX gap detected for focus area: {focus}.', 'proposed_fix': 'Continue monitoring.', 'files_likely_touched': [], 'patch_safe': False})
    route = choose_route(findings, checks, focus)
    paths = build_paths(findings, checks, focus)
    return {'checks': checks, 'findings': findings, 'diagnosis': {**route, 'improvement_paths': paths}}


def main() -> None:
    stamp = now_utc()
    focus = pick_focus(stamp)
    result = evaluate(read_text(SITE), read_json(AUTOMATION), read_json(TRIAGE), focus)
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
        'diagnosis': result['diagnosis'],
        'recommended_autonomy': result['diagnosis']['recommended_autonomy'],
        'improvement_paths': result['diagnosis']['improvement_paths'],
        'human_review_required': any(f['severity'] in {'high', 'medium'} for f in result['findings']),
        'next_action': result['diagnosis']['improvement_paths'][0]['goal'],
    }
    LATEST.write_text(json.dumps(state, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    lines = [f'# Pages UX evaluator report — {stamp}', '', f'- Focus area: `{focus}`', f'- Recommended autonomy: `{state["recommended_autonomy"]}`', f'- Primary problem type: `{state["diagnosis"]["primary_problem_type"]}`', '', '## Improvement paths', '']
    for path in state['improvement_paths']:
        lines += [f'### {path["path_id"]}', f'- Goal: {path["goal"]}', f'- Scope: `{path["scope"]}`', f'- Files: {", ".join(path["files"])}', '']
    lines += ['## Findings', '']
    for item in result['findings']:
        lines += [f'### {item["severity"].upper()} — {item["issue"]}', f'- Problem type: `{item.get("problem_type")}`', f'- Proposed fix: {item["proposed_fix"]}', '']
    (HISTORY / report_name).write_text('\n'.join(lines), encoding='utf-8')


if __name__ == '__main__':
    main()
