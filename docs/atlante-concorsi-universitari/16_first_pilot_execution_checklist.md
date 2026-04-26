# 16 — First pilot execution checklist (10 procedures)

## Before coding
- [ ] Confirm methodology docs 00–15 are available and current.
- [ ] Confirm schema/template alignment using validation scripts.
- [ ] Confirm pilot universities and 10 target procedures are listed internally.
- [ ] Confirm neutral-language policy and uncertainty policy are understood.

## During document collection
- [ ] Collect only official/public documents.
- [ ] Save documents in procedure-specific raw folder.
- [ ] Preserve source page evidence in snapshots.
- [ ] Record source URL and retrieval date in `documents.csv`.
- [ ] Keep later versions as separate files; do not overwrite.

## During field extraction
- [ ] Fill `procedures.csv` first (anchors and workflow dates).
- [ ] Classify each document with allowed `document_type`.
- [ ] Populate profile and criteria raw fields before derived fields.
- [ ] Use `not_determinable` when evidence is insufficient.

## During relation coding
- [ ] Add relation rows only with documentary evidence.
- [ ] Fill evidence URL and excerpt fields.
- [ ] Use allowed relation taxonomy values only.
- [ ] Set `human_review_required=true` for ambiguous/sensitive records.

## During QA
- [ ] Run `validate_atlante_methodology.py` and `validate_golden_dataset.py`.
- [ ] Complete QA checklist document 11 for each procedure.
- [ ] Ensure no accusatory/legal-conclusive wording in notes.

## After QA
- [ ] Move unresolved issues into `review_notes/`.
- [ ] Save QA reports and hash manifest in `qa_reports/`.
- [ ] Record pilot metrics in `pilot_metrics/pilot_batch_001_metrics.csv`.

## Decide whether codebook needs revision
Revise codebook if at least one is true:
- recurrent ambiguity in same field across >=3 procedures;
- repeated coder disagreement not solved by current definitions;
- frequent fallback to free-text notes for the same concept.

## Decide whether a field should be added/removed/redefined
- **Add field** when critical evidence repeatedly cannot be represented.
- **Remove field** when always empty/non-informative across pilot procedures.
- **Redefine field** when coders interpret it inconsistently despite training.

Document every proposed change with examples and expected downstream impact.
