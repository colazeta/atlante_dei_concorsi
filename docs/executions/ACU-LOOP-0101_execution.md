# ACU-LOOP-0101 — Issue #101 execution log

## Scope
- Implement UX changes requested in issue #101:
  - surface homepage and recruitment URLs in list rows;
  - show manual decision as a separate overlay from automated confidence/verification;
  - add filters for manual decision and URL presence;
  - preserve existing review/export/submission workflow.

## Files changed
- `site/index.html`
- `reports/agentic-loop/ACU-LOOP-0101_state.json`
- `docs/executions/ACU-LOOP-0101_execution.md`

## Validation
- `python3 scripts/validate_atlante_methodology.py` → pass
- `python3 scripts/validate_golden_dataset.py` → pass
- `python3 scripts/validate_agentic_loop_state.py` → fail (pre-existing schema errors in `ACU-LOOP-0099_state.json`)

## Governance checks
- No golden dataset files modified.
- No raw documents/snapshots added.
- No taxonomy/schema semantics changed.

## Next action
Open draft PR for human review.
