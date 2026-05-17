# ACU-LOOP-0105 — Issue #105 source-intake pack generation

## Scope
Generate governed source-intake packs from the university registry without scraping, downloads, or golden-dataset changes.

## Inputs used
- `data/source-registries/italian-universities/official_university_urls.csv`
- `data/source-registries/italian-universities/missing_universities_to_verify.csv`
- `data/source-registries/italian-universities/manual_review_decisions.csv`

## Actions performed
- Generated one intake pack per eligible registry university (official homepage present) under `docs/executions/source-intake-packs/{university_id}/`.
- Generated aggregate outputs:
  - `docs/executions/source-intake-packs/README.md`
  - `docs/executions/source-intake-packs/source_intake_index.csv`
  - `docs/executions/source-intake-packs/verification_backlog.md`
- Carried uncertainty into `source_risk_notes.md` with non-blocking flags for missing/uncertain recruitment URL data.

## Validation
- `python3 scripts/validate_atlante_methodology.py` → passed.
- `python3 scripts/validate_golden_dataset.py` → passed with existing non-blocking warnings.
- `python3 scripts/validate_agentic_loop_state.py` → passed.

## Blockers
- None.

## Next action
Open draft PR for human review and merge.
