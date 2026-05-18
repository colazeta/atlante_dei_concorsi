#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'reports/auto-merge-gate'
LATEST = OUT / 'latest_state.json'

TIER4_PATH_PREFIXES = (
    '.github/workflows/',
    'scripts/governed_auto_merge_gate.py',
    'schemas/',
)
TIER1_PREFIXES = (
    'reports/',
    'site/data/',
    'docs/executions/approved-source-inventories/',
    'docs/executions/document-link-classification/',
    'docs/executions/document-link-triage/',
)
TIER2_FILES = (
    'site/index.html',
)


def run(cmd: list[str], check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, text=True, capture_output=True, check=check)


def gh_json(args: list[str]) -> dict:
    cp = run(['gh', *args])
    return json.loads(cp.stdout or '{}')


def classify(files: list[str]) -> tuple[str, list[str]]:
    reasons = []
    if any(path.startswith(TIER4_PATH_PREFIXES) for path in files):
        return 'tier4', ['Touches workflow/script/schema or merge-gate controlled path.']
    if files and all(path.startswith(TIER1_PREFIXES) for path in files):
        return 'tier1', ['Generated reports/data artefacts only.']
    if files and all(path in TIER2_FILES or path.startswith(TIER1_PREFIXES) for path in files):
        return 'tier2', ['Static Pages UI/data-only update.']
    reasons.append('Mixed application/data change that is not tier4.')
    return 'tier3', reasons


def all_required_checks_green(pr: dict) -> tuple[bool, list[str]]:
    # Prefer the mergeable state exposed by GitHub plus statusCheckRollup when available.
    failures = []
    checks = pr.get('statusCheckRollup') or []
    if isinstance(checks, list) and checks:
        for item in checks:
            conclusion = (item.get('conclusion') or item.get('state') or '').upper()
            name = item.get('name') or item.get('context') or 'unknown'
            if conclusion not in {'SUCCESS', 'NEUTRAL', 'SKIPPED'}:
                failures.append(f'{name}:{conclusion}')
    # If GitHub does not expose checks here, rely on mergeable plus branch protection elsewhere.
    return (not failures), failures


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--pr', required=True)
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()

    pr_number = args.pr
    pr = gh_json(['pr', 'view', pr_number, '--json', 'number,title,author,mergeable,headRefName,baseRefName,files,labels,statusCheckRollup,isDraft'])
    files = [f['path'] for f in pr.get('files', [])]
    tier, reasons = classify(files)
    labels = {label.get('name') for label in pr.get('labels', [])}
    mergeable = pr.get('mergeable') == 'MERGEABLE'
    draft = bool(pr.get('isDraft'))
    checks_green, check_failures = all_required_checks_green(pr)

    allowed = tier in {'tier1', 'tier2', 'tier3'} and not draft and mergeable and checks_green
    if 'tier4' in labels or 'no-auto-merge' in labels:
        allowed = False
        reasons.append('Explicit blocking label present.')
    if 'allow-tier3-automerge' not in labels and tier == 'tier3':
        # Tier 3 can auto-merge, but requires explicit label because it may include mixed app/data changes.
        allowed = False
        reasons.append('Tier3 requires allow-tier3-automerge label.')

    state = {
        'gate_id': 'AUTO-MERGE-GATE-0001',
        'pr_number': pr.get('number'),
        'title': pr.get('title'),
        'head': pr.get('headRefName'),
        'base': pr.get('baseRefName'),
        'tier': tier,
        'files': files,
        'labels': sorted(labels),
        'mergeable': mergeable,
        'draft': draft,
        'checks_green': checks_green,
        'check_failures': check_failures,
        'allowed_to_merge': allowed,
        'reasons': reasons,
        'applied': False,
    }

    OUT.mkdir(parents=True, exist_ok=True)
    if allowed and args.apply:
        cp = run(['gh', 'pr', 'merge', str(pr_number), '--squash', '--delete-branch'], check=False)
        state['applied'] = cp.returncode == 0
        state['merge_stdout'] = cp.stdout[-2000:]
        state['merge_stderr'] = cp.stderr[-2000:]
        if cp.returncode != 0:
            state['allowed_to_merge'] = False
            state['reasons'].append('gh pr merge failed at execution time.')
    LATEST.write_text(json.dumps(state, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    print(json.dumps(state, indent=2, ensure_ascii=False))
    return 0 if (not args.apply or state.get('applied') or not allowed) else 1


if __name__ == '__main__':
    sys.exit(main())
