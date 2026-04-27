# 06 — Committee-candidate documented relations taxonomy

## Scope
This taxonomy records publicly documented relations between committee members and candidates.
It does not assert proven conflicts.

## Allowed `relation_type` values
- `same_academic_field`
- `same_current_affiliation`
- `same_past_affiliation`
- `same_department_current`
- `same_department_past`
- `coauthorship_single`
- `coauthorship_recurrent`
- `coauthorship_recent`
- `shared_research_project`
- `shared_research_centre_or_lab`
- `supervisor_student_relation`
- `grant_or_project_hierarchy`
- `declared_abstention_or_challenge`
- `other_documented_relation`
- `no_relation_found`
- `not_determinable`

## Required relation fields
- `relation_id`
- `procedure_id`
- `committee_member_person_id_or_name`
- `candidate_person_id_or_name`
- `relation_type`
- `relation_subtype`
- `evidence_source_type`
- `evidence_source_url`
- `evidence_document_id`
- `evidence_text_excerpt`
- `relation_start_date`
- `relation_end_date`
- `relation_recency` (`current`, `recent`, `historical`, `unknown`)
- `relation_intensity` (`weak`, `medium`, `strong`, `not_determinable`)
- `confidence_level` (`low`, `medium`, `high`)
- `relation_relevant_for_review`
- `potential_conflict_review_signal`
- `human_review_required`
- `human_review_status`
- `publication_status` (`internal_only`, `publishable_summary`, `publishable_full`)
- `notes`

## Caution rules
- Never use a field named `conflict_of_interest_confirmed`.
- If evidence is insufficient, set `relation_type=not_determinable` and `human_review_required=true`.
- For absence claims, prefer `no_relation_found` only after documented search protocol.
