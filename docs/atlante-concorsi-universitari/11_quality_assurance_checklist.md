# 11 — Quality assurance checklist (pre-golden-dataset)

Validate each procedure before inclusion.

## A. Source and provenance
- [ ] `procedure.source_url` present and reachable at coding time.
- [ ] each document row has `source_url`.
- [ ] `official_source_flag` populated for each document.

## B. Minimum documentary coverage
- [ ] at least one `call_notice` document exists.
- [ ] `number_of_positions` extracted OR explicitly unresolved in notes with `human_review_required`.
- [ ] document types belong to taxonomy enum only.

## C. Date coherence
- [ ] `call_publication_date <= deadline_date` when both exist.
- [ ] committee appointment not before call publication unless documented historical exception in notes.
- [ ] outcome/approval dates not earlier than call date unless corrigendum explains chronology.

## D. Committee and candidates
- [ ] each committee member linked to `source_document_id` or explicit source note.
- [ ] each candidate linked to source where publicly available.
- [ ] confidence level set for all committee/candidate rows.

## E. Profile and criteria coding
- [ ] profile raw counts are filled and supported by excerpts.
- [ ] profile class is one of: `low`, `medium`, `high`, `very_high`, `not_determinable`.
- [ ] criteria fields are coherent with `criteria_available`.
- [ ] criteria class is one of: `low`, `medium`, `high`, `very_high`, `not_determinable`.

## F. Documented relations
- [ ] each relation type is in allowed enum.
- [ ] each relation has evidence source URL.
- [ ] sensitive/ambiguous relations have `human_review_required=true`.
- [ ] no field or statement asserts confirmed legal conflict.

## G. Language and uncertainty
- [ ] no unsupported legal conclusion in notes.
- [ ] uncertainty recorded with `not_determinable` or explicit notes.
- [ ] wording remains documentary and neutral.

## Decision
- [ ] **PASS**: procedure enters golden dataset.
- [ ] **HOLD**: pending human review.
- [ ] **REJECT**: insufficient documentation quality.
