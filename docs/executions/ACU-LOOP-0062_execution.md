# ACU-LOOP-0062 — coverage audit after PR #63

## Summary

- Issue target: #61 (post-PR #63 completeness audit)
- Mode: `controlled_implementation`
- Status: `completed`
- Human review required: `True`
- Updated at: `2026-05-17T10:05:00+00:00`

## Scope actually executed

This run executed an audit-only pass on `data/source-registries/italian-universities/official_university_urls.csv`.
No new university rows were added.

## Universe source used

Institutional reference perimeter: MUR pages for the Italian university system (`Le Università`, `Università statali`, `Università non statali riconosciute`, `Università telematiche`) indicating a system size of **99 istituzioni**.

## Coverage audit

- totale atteso (fonte-universo MUR): **99**
- totale presente nel CSV: **80**
- delta stimato: **19** istituzioni da integrare/verificare
- duplicati rilevati su `university_id`: **0**

## Segment checks

- non statali presenti nel CSV: **16**
- telematiche presenti (stima da naming): **6**
- scuole superiori/ordinamento speciale presenti (stima): **5**

## Potentially missing institutions (to verify against MUR lists)

Examples of likely-missing entries include institutions commonly listed in MUR categories, such as:
- Scuola Superiore Meridionale;
- Università di Napoli “L'Orientale” is included, but additional Naples-area institutions and private campuses may require reconciliation;
- some telematiche likely absent (e.g., eCampus, Unitelma Sapienza, Giustino Fortunato already present, others to verify);
- private/non-statali with recognised status may still be incomplete.

A deterministic missing-list requires extracting the full canonical names from the MUR category pages (currently partially inaccessible from this environment due intermittent 403 on some MUR endpoints).

## Recommendation on issue #61

**Do not close yet.**

Reason: registry completeness against the institutional universe is not yet satisfied (`80/99`) and missing-list reconciliation is still open.

## Validation

- `python3 scripts/validate_atlante_methodology.py`
- `python3 scripts/validate_golden_dataset.py`
- `python3 scripts/validate_agentic_loop_state.py`

## Compliance

No golden-dataset rows were modified. No raw documents/snapshots were added.
