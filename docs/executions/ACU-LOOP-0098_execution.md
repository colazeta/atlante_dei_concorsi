# ACU-LOOP-0098 — Execution log

- **Issue**: #98 — Add GitHub submission flow for manual review decisions from Pages UX.
- **Date (UTC)**: 2026-05-17.
- **Mode**: controlled_implementation.
- **Status**: completed.

## Implemented scope

1. Added two UX actions: **Submit selected decisions to GitHub** and **Submit all decisions to GitHub**.
2. Implemented static-safe prefilled GitHub issue generation containing manual decision payload and governance instructions for follow-up PR persistence.
3. Included explicit selected row count and selection scope in the generated issue body.
4. Preserved and propagated reviewer, note, and review-date metadata already captured in manual decisions.
5. Added fallback copy box when prefilled issue URL length is too large.
6. Preserved existing CSV/JSON export actions without behaviour regression.
7. Preserved explicit wording that submission creates an issue and does not directly commit repository files.

## Governance checks

- Automated registry remains unchanged.
- No golden dataset rows changed.
- No raw documents or snapshots added.
- Submission path remains browser-safe and credential-free.

## Validation results

- `python3 scripts/validate_atlante_methodology.py` → pass.
- `python3 scripts/validate_golden_dataset.py` → pass.
- `python3 scripts/validate_agentic_loop_state.py` → pass.

## Next action

Open draft PR for human review of UX wording, label choice in prefilled issue URL, and payload-size fallback behaviour.
