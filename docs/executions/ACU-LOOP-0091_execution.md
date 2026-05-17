# ACU-LOOP-0091 — Execution log

- **Issue**: #91 — Publish static mapping UX under `site/` using GitHub Pages.
- **Date (UTC)**: 2026-05-17.
- **Mode**: controlled implementation.
- **Status**: completed.

## Scope implemented

1. Added a dedicated GitHub Actions workflow to build mapping JSON assets and deploy `site/` to GitHub Pages.
2. Configured trigger policy for manual runs and pushes to `main` when relevant mapping UX files change.
3. Preserved governance boundaries by publishing only static UX assets (no raw documents/snapshots; no candidate/committee rows; no relation inference or risk scoring).

## Files changed

- `.github/workflows/deploy-pages.yml`
- `docs/executions/ACU-LOOP-0091_execution.md`
- `reports/agentic-loop/ACU-LOOP-0091_state.json`

## Validation and checks

- `python3 scripts/build_university_registry_json.py` → pass.
- `python3 scripts/build_mapping_progress_history.py` → pass.
- `python3 scripts/validate_atlante_methodology.py` → pass.
- `python3 scripts/validate_golden_dataset.py` → pass with existing warning-level notices only.
- `python3 scripts/validate_agentic_loop_state.py` → pass.

## Governance safeguards confirmation

- No golden-dataset row publication introduced.
- No raw PDFs/snapshots/documents exposed via workflow artifact path.
- No candidate or committee level data added.
- No relation inference, risk scoring, wrongdoing implication, or legal conclusion logic introduced.
- Existing uncertainty/confidence/not-determinable handling remains in generated static payloads.

## Next action

Open a draft PR titled **"Publish mapping UX with GitHub Pages"** for maintainer review and merge.
