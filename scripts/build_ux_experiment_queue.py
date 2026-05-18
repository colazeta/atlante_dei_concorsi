#!/usr/bin/env python3
from __future__ import annotations

import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUTOMATION = ROOT / 'site/data/automation_status.json'
TRIAGE_PROGRESS = ROOT / 'site/data/document_link_triage_progress.json'
TRIAGE_INDEX = ROOT / 'site/data/document_link_triage_index.json'
UX_EVALUATOR = ROOT / 'reports/ux-evaluator/latest_state.json'
UX_ITERATION = ROOT / 'reports/ux-safe-updates/latest_state.json'
OUT = ROOT / 'reports/ux-experiments'
HISTORY = OUT / 'history'
LATEST = OUT / 'latest_state.json'
QUEUE = OUT / 'experiment_queue.json'


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')


def read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except json.JSONDecodeError:
        return {}


def pct(num: int, den: int) -> float:
    return round((num / den) * 100, 2) if den else 0.0


def proposal(pid: str, title: str, problem: str, evidence: dict, change: str, effect: str, risk: str, autonomy: str, files: list[str], checks: list[str]) -> dict:
    score = {'low': 1, 'medium': 2, 'high': 3}.get(risk, 2)
    urgency = 0
    if autonomy == 'broad':
        urgency += 3
    elif autonomy == 'iteration':
        urgency += 2
    else:
        urgency += 1
    if evidence.get('share_pct', 0) >= 50:
        urgency += 3
    elif evidence.get('share_pct', 0) >= 25:
        urgency += 2
    elif evidence.get('count', 0) > 0:
        urgency += 1
    return {
        'experiment_id': pid,
        'title': title,
        'problem_detected': problem,
        'aggregate_evidence': evidence,
        'proposed_ui_change': change,
        'expected_effect': effect,
        'risk_level': risk,
        'suggested_autonomy': autonomy,
        'files_likely_touched': files,
        'validation_checks_required': checks,
        'priority_score': urgency - score,
    }


def build_experiments(automation: dict, triage_progress: dict, triage_entries: list[dict], ux_eval: dict, ux_iteration: dict) -> list[dict]:
    total = int(triage_progress.get('total_triaged_links') or len(triage_entries) or 0)
    kept = int(triage_progress.get('kept_for_review') or 0)
    unknown = int(triage_progress.get('unknown_requires_review') or 0)
    excluded = int(triage_progress.get('excluded_from_competition_queue') or 0)
    possible = int(triage_progress.get('possible_competition_sources') or 0)
    statuses = Counter(e.get('triage_status', '') for e in triage_entries)
    text_counter = Counter((e.get('link_text') or '').strip().lower() for e in triage_entries)
    nav_like = sum(c for txt, c in text_counter.items() if any(tok in txt for tok in ['vai al contenuto', 'vai al menu', 'salta al contenuto', 'skip to']))

    experiments: list[dict] = []
    if kept and pct(kept, total) >= 50:
        experiments.append(proposal(
            'card_review_mode',
            'Introduce card-based one-link review mode',
            'The review queue is large relative to the total triaged corpus.',
            {'count': kept, 'denominator': total, 'share_pct': pct(kept, total)},
            'Add an optional card-based mode showing one candidate link at a time with primary approve/reject/evidence actions.',
            'Reduce cognitive load and make sequential validation easier than scanning a dense table.',
            'medium', 'broad', ['site/index.html'], ['DOM marker for card mode', 'decision export still works', 'audit table remains available'],
        ))
    if unknown and pct(unknown, total) >= 25:
        experiments.append(proposal(
            'unknown_resolution_queue',
            'Create a dedicated unknown-resolution queue',
            'A large share of links remains in unknown/review-required state.',
            {'count': unknown, 'denominator': total, 'share_pct': pct(unknown, total)},
            'Add a saved focus queue for unknown items with explanation prompts and needs-evidence defaults.',
            'Help reviewers resolve uncertain links without mixing them with likely competition pages.',
            'medium', 'iteration', ['site/index.html'], ['unknown filter exists', 'manual decisions still export'],
        ))
    if nav_like:
        experiments.append(proposal(
            'navigation_noise_rule',
            'Strengthen navigation-link suppression',
            'Navigation-like links are reaching the review queue.',
            {'count': nav_like, 'denominator': total, 'share_pct': pct(nav_like, total)},
            'Update deterministic triage to mark skip/menu/content anchors as likely_not_relevant unless other strong competition signals exist.',
            'Reduce false positives before they reach manual validation.',
            'low', 'iteration', ['scripts/build_document_link_triage.py'], ['triage row count consistency', 'excluded links remain auditable'],
        ))
    if possible and pct(possible, total) >= 20:
        experiments.append(proposal(
            'source_summary_first',
            'Add source-level summary before link review',
            'Many pages are possible competition sources but not high-confidence direct evidence.',
            {'count': possible, 'denominator': total, 'share_pct': pct(possible, total)},
            'Add a source-level summary panel grouping links by university/source URL before row-level review.',
            'Let reviewers validate or deprioritise whole source clusters before reviewing every individual link.',
            'medium', 'broad', ['site/index.html', 'site/data/document_link_triage_index.json'], ['source grouping renders', 'row-level audit remains visible'],
        ))
    if not experiments:
        experiments.append(proposal(
            'microcopy_polish',
            'Continue microcopy and affordance polish',
            'No high-friction aggregate signal currently exceeds thresholds.',
            {'count': 0, 'denominator': total, 'share_pct': 0},
            'Refine labels, helper text, empty states and status explanations based on evaluator findings.',
            'Maintain gradual UX improvement without unnecessary structural churn.',
            'low', 'safe', ['site/index.html'], ['DOM markers remain present'],
        ))
    return sorted(experiments, key=lambda x: x['priority_score'], reverse=True)


def main() -> None:
    stamp = now_utc()
    automation = read_json(AUTOMATION)
    triage_progress = read_json(TRIAGE_PROGRESS)
    triage_index = read_json(TRIAGE_INDEX)
    ux_eval = read_json(UX_EVALUATOR)
    ux_iteration = read_json(UX_ITERATION)
    entries = triage_index.get('entries', [])
    experiments = build_experiments(automation, triage_progress, entries, ux_eval, ux_iteration)
    OUT.mkdir(parents=True, exist_ok=True)
    HISTORY.mkdir(parents=True, exist_ok=True)
    state = {
        'experiment_loop_id': 'UX-EXPERIMENT-LOOP-0001',
        'status': 'completed',
        'created_at_utc': stamp,
        'updated_at_utc': stamp,
        'input_files': [
            str(AUTOMATION.relative_to(ROOT)),
            str(TRIAGE_PROGRESS.relative_to(ROOT)),
            str(TRIAGE_INDEX.relative_to(ROOT)),
            str(UX_EVALUATOR.relative_to(ROOT)),
            str(UX_ITERATION.relative_to(ROOT)),
        ],
        'aggregate_counts': {
            'triaged_links': triage_progress.get('total_triaged_links'),
            'kept_for_review': triage_progress.get('kept_for_review'),
            'excluded_from_competition_queue': triage_progress.get('excluded_from_competition_queue'),
            'unknown_requires_review': triage_progress.get('unknown_requires_review'),
            'possible_competition_sources': triage_progress.get('possible_competition_sources'),
        },
        'proposal_count': len(experiments),
        'top_experiment': experiments[0] if experiments else None,
        'governance': {
            'personal_data_collection': False,
            'external_analytics': False,
            'automatic_merge': False,
            'pr_based': True,
        },
    }
    LATEST.write_text(json.dumps(state, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    QUEUE.write_text(json.dumps({'updated_at_utc': stamp, 'experiments': experiments}, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    report = HISTORY / f'{stamp.replace(":", "").replace("-", "")}_experiment_plan.md'
    lines = [f'# UX experiment plan — {stamp}', '', f'- Proposals: {len(experiments)}', '', '## Top proposals', '']
    for exp in experiments[:5]:
        lines += [f'### {exp["experiment_id"]}: {exp["title"]}', '', f'- Problem: {exp["problem_detected"]}', f'- Evidence: `{exp["aggregate_evidence"]}`', f'- Change: {exp["proposed_ui_change"]}', f'- Expected effect: {exp["expected_effect"]}', f'- Risk: `{exp["risk_level"]}`', f'- Suggested autonomy: `{exp["suggested_autonomy"]}`', '']
    report.write_text('\n'.join(lines), encoding='utf-8')


if __name__ == '__main__':
    main()
