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


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')


def read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except json.JSONDecodeError:
        return {}


def apply_replacements(text: str) -> tuple[str, list[dict[str, str]]]:
    updates: list[dict[str, str]] = []
    replacements = [
        {
            'id': 'add-quick-approve-label',
            'before': '<button class="quick-approve good" data-key="${esc(k)}">Approva</button>',
            'after': '<button class="quick-approve good" data-key="${esc(k)}" title="Conferma questo link come rilevante per la coda concorsi">Approva</button>',
            'reason': 'Add explanatory title to row-level approve action.',
        },
        {
            'id': 'add-quick-reject-label',
            'before': '<button class="quick-reject bad" data-key="${esc(k)}">Non pertinente</button>',
            'after': '<button class="quick-reject bad" data-key="${esc(k)}" title="Escludi/deprioritizza questo link dalla coda concorsi">Non pertinente</button>',
            'reason': 'Add explanatory title to row-level reject action.',
        },
        {
            'id': 'add-submit-one-label',
            'before': '<button class="submit-one" data-key="${esc(k)}">Invia singolo</button>',
            'after': '<button class="submit-one" data-key="${esc(k)}" title="Apri una issue GitHub solo per questa decisione">Invia singolo</button>',
            'reason': 'Clarify per-row submission behaviour.',
        },
        {
            'id': 'clarify-bulk-submission-label',
            'before': '<button id="submit-link-decisions-github" type="button">Invia tutte le decisioni</button>',
            'after': '<button id="submit-link-decisions-github" type="button" title="Crea una issue GitHub con tutte le decisioni locali">Invia tutte le decisioni</button>',
            'reason': 'Clarify that mass submission creates a governed GitHub issue.',
        },
        {
            'id': 'clarify-selected-submission-label',
            'before': '<button id="submit-selected-link-decisions-github" type="button">Invia selezionati</button>',
            'after': '<button id="submit-selected-link-decisions-github" type="button" title="Crea una issue GitHub con le sole decisioni selezionate">Invia selezionati</button>',
            'reason': 'Clarify selected submission scope.',
        },
    ]
    for item in replacements:
        if item['before'] in text and item['after'] not in text:
            text = text.replace(item['before'], item['after'])
            updates.append({'id': item['id'], 'reason': item['reason'], 'file': 'site/index.html'})
    return text, updates


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--apply', action='store_true', help='Apply whitelisted safe UI updates.')
    args = parser.parse_args()

    stamp = now_utc()
    ux_state = read_json(UX_STATE)
    html = SITE.read_text(encoding='utf-8') if SITE.exists() else ''
    proposed_html, updates = apply_replacements(html)

    status = 'no_updates_available'
    if updates and args.apply:
        SITE.write_text(proposed_html, encoding='utf-8')
        status = 'applied'
    elif updates:
        status = 'updates_available'

    OUT.mkdir(parents=True, exist_ok=True)
    state = {
        'safe_updater_id': 'PAGES-UX-SAFE-UPDATER-0001',
        'status': status,
        'created_at_utc': stamp,
        'updated_at_utc': stamp,
        'apply_mode': args.apply,
        'source_evaluator_fingerprint': ux_state.get('fingerprint'),
        'source_focus_area': ux_state.get('focus_area'),
        'updates': updates,
        'allowed_files': ['site/index.html'],
        'prohibited_actions': [
            'direct_main_mutation',
            'layout_rewrite_without_review',
            'business_logic_change',
            'data_deletion',
        ],
        'next_action': 'Open or update a governed PR for applied safe updates.' if updates else 'Continue monitoring UX evaluator findings.',
    }
    LATEST.write_text(json.dumps(state, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
