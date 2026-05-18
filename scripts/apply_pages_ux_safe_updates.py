#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'site/index.html'
UX_STATE = ROOT / 'reports/ux-evaluator/latest_state.json'
OUT = ROOT / 'reports/ux-safe-updates'
LATEST = OUT / 'latest_state.json'

ALLOWED_FILES = [
    'site/index.html',
    'site/data/automation_status.json',
    'reports/ux-evaluator/latest_state.json',
    'reports/ux-safe-updates/latest_state.json',
]


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')


def read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except json.JSONDecodeError:
        return {}


def replace_once(text: str, before: str, after: str, updates: list[dict[str, str]], update_id: str, reason: str) -> str:
    if before in text and after not in text:
        updates.append({'id': update_id, 'reason': reason, 'file': 'site/index.html', 'scope': 'ui_iteration'})
        return text.replace(before, after)
    return text


def apply_microcopy_updates(text: str, updates: list[dict[str, str]]) -> str:
    replacements = [
        ('add-quick-approve-label','<button class="quick-approve good" data-key="${esc(k)}">Approva</button>','<button class="quick-approve good" data-key="${esc(k)}" title="Conferma questo link come rilevante per la coda concorsi">Approva</button>','Add explanatory title to row-level approve action.'),
        ('add-quick-reject-label','<button class="quick-reject bad" data-key="${esc(k)}">Non pertinente</button>','<button class="quick-reject bad" data-key="${esc(k)}" title="Escludi/deprioritizza questo link dalla coda concorsi">Non pertinente</button>','Add explanatory title to row-level reject action.'),
        ('add-submit-one-label','<button class="submit-one" data-key="${esc(k)}">Invia singolo</button>','<button class="submit-one" data-key="${esc(k)}" title="Apri una issue GitHub solo per questa decisione">Invia singolo</button>','Clarify per-row submission behaviour.'),
        ('clarify-bulk-submission-label','<button id="submit-link-decisions-github" type="button">Invia tutte le decisioni</button>','<button id="submit-link-decisions-github" type="button" title="Crea una issue GitHub con tutte le decisioni locali">Invia tutte le decisioni</button>','Clarify that mass submission creates a governed GitHub issue.'),
        ('clarify-selected-submission-label','<button id="submit-selected-link-decisions-github" type="button">Invia selezionati</button>','<button id="submit-selected-link-decisions-github" type="button" title="Crea una issue GitHub con le sole decisioni selezionate">Invia selezionati</button>','Clarify selected submission scope.'),
    ]
    for update_id, before, after, reason in replacements:
        text = replace_once(text, before, after, updates, update_id, reason)
    return text


def apply_iteration_updates(text: str, updates: list[dict[str, str]]) -> str:
    """Apply broader but still governed UI iterations.

    This is intentionally more autonomous than the original microcopy-only updater:
    it can add workflow guidance, keyboard shortcut documentation and review-mode
    affordances. It still opens PRs rather than mutating main directly.
    """
    if 'id="ux-iteration-banner"' not in text:
        marker = '<section class="panel"><h2>Stato dell’automazione</h2>'
        banner = (
            '<section class="panel" id="ux-iteration-banner">'
            '<h2>Modalità revisione rapida</h2>'
            '<p class="small">Percorso consigliato: filtra i link, usa Approva / Non pertinente / Più evidenza su ogni riga, poi invia una singola decisione o un batch tramite issue GitHub. Le decisioni restano locali finché non vengono esportate o inviate.</p>'
            '<div class="toolbar"><button type="button" onclick="document.getElementById(\'focus-likely\').click()">1. Parti dai probabili concorsi</button>'
            '<button type="button" onclick="document.getElementById(\'focus-unknown\').click()">2. Risolvi gli incerti</button>'
            '<button type="button" onclick="document.getElementById(\'focus-excluded\').click()">3. Controlla gli esclusi</button></div>'
            '</section>\n\n  '
        )
        if marker in text:
            text = text.replace(marker, banner + marker)
            updates.append({'id': 'add-review-mode-banner', 'reason': 'Add a guided review-mode banner to make the reviewer workflow explicit.', 'file': 'site/index.html', 'scope': 'ui_iteration'})
    if 'Scorciatoie:' not in text:
        before = '<p id="link-table-status" class="small">Caricamento link…</p>'
        after = '<p id="link-table-status" class="small">Caricamento link…</p><p class="small">Scorciatoie: usa i pulsanti rapidi per validare riga per riga; usa “Invia singolo” per persistere una sola decisione; usa “Invia selezionati” per batch piccoli.</p>'
        text = replace_once(text, before, after, updates, 'add-link-table-shortcuts-copy', 'Add inline guidance above the link validation table.',)
    if 'decision-filter' in text and 'Mostra non revisionati' not in text:
        before = '<button id="clear-link-filters" type="button">Pulisci filtri</button>'
        after = '<button id="show-unreviewed" type="button">Mostra non revisionati</button><button id="clear-link-filters" type="button">Pulisci filtri</button>'
        text = replace_once(text, before, after, updates, 'add-unreviewed-filter-button', 'Add a one-click control for unreviewed items.',)
        hook = "document.getElementById('clear-link-filters').onclick=()=>{['link-search','triage-filter','keep-filter','attention-filter','classified-filter','decision-filter'].forEach(id=>document.getElementById(id).value='');applyLinkFilters()};"
        replacement = "document.getElementById('show-unreviewed').onclick=()=>{document.getElementById('decision-filter').value='';app.filtered=app.triage.filter(r=>!app.linkDecisions[linkKey(r)]).sort((a,b)=>priorityRank(a.triage_status)-priorityRank(b.triage_status));renderPriorityQueue();renderTriageRows();renderReviewProgress()};" + hook
        text = replace_once(text, hook, replacement, updates, 'wire-unreviewed-filter-button', 'Wire the unreviewed-items control in the validation UI.')
    return text


def apply_updates(text: str, autonomy: str) -> tuple[str, list[dict[str, str]]]:
    updates: list[dict[str, str]] = []
    text = apply_microcopy_updates(text, updates)
    if autonomy in {'iteration', 'broad'}:
        text = apply_iteration_updates(text, updates)
    return text, updates


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--apply', action='store_true', help='Apply governed UI updates.')
    parser.add_argument('--autonomy', choices=['safe', 'iteration', 'broad'], default='iteration')
    args = parser.parse_args()

    stamp = now_utc()
    ux_state = read_json(UX_STATE)
    html = SITE.read_text(encoding='utf-8') if SITE.exists() else ''
    proposed_html, updates = apply_updates(html, args.autonomy)

    status = 'no_updates_available'
    if updates and args.apply:
        SITE.write_text(proposed_html, encoding='utf-8')
        status = 'applied'
    elif updates:
        status = 'updates_available'

    OUT.mkdir(parents=True, exist_ok=True)
    state = {
        'safe_updater_id': 'PAGES-UX-ITERATION-AGENT-0001',
        'status': status,
        'created_at_utc': stamp,
        'updated_at_utc': stamp,
        'apply_mode': args.apply,
        'autonomy_level': args.autonomy,
        'source_evaluator_fingerprint': ux_state.get('fingerprint'),
        'source_focus_area': ux_state.get('focus_area'),
        'updates': updates,
        'allowed_files': ALLOWED_FILES,
        'allowed_change_scopes': ['microcopy', 'workflow_guidance', 'review_controls', 'layout_sections', 'static_js_for_review_flow'],
        'prohibited_actions': [
            'direct_main_mutation',
            'automatic_merge',
            'data_deletion',
            'secret_or_token_handling',
            'external_network_dependency',
            'removal_of_audit_visibility',
        ],
        'next_action': 'Open or update a governed PR for applied UX iteration updates.' if updates else 'Continue monitoring UX evaluator findings.',
    }
    LATEST.write_text(json.dumps(state, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
