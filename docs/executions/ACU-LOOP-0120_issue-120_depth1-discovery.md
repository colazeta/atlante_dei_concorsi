# ACU-LOOP-0120 — Issue #120 bounded depth-1 discovery

- Date (UTC): 2026-05-17
- Scope: add bounded depth-1 discovery on approved source pages; keep governance safeguards.

## Changes
- Added depth controls and keyword-gated, same-domain depth-1 follow logic in approved-source fetch script.
- Added required candidate output fields (`discovery_depth`, `parent_url`, `keyword_match`).
- Added dedicated workflow `.github/workflows/approved-source-fetch.yml` with bounded CLI controls.
- Updated progress builders for new candidate header and aggregate progress keys.

## Governance notes
- No raw HTML or raw documents committed.
- No golden-dataset rows modified.
- Fetch remains bounded and non-recursive (`--depth` limited to 0/1).

## Validation
- `python3 scripts/validate_atlante_methodology.py`: passed.
- `python3 scripts/validate_golden_dataset.py`: passed with warnings (existing non-synthetic data warnings).
- `python3 scripts/validate_agentic_loop_state.py`: passed after fixing legacy malformed state file `ACU-LOOP-0113_state.json`.

## Next action
- Human review of depth-1 discovery results in pilot runs, then bounded batch execution via workflow_dispatch.
