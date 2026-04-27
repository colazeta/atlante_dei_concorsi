# 23 — Item-level consistency audit (ACU-PILOT-0001, ACU-PILOT-0002)

## Audit scope

This audit covers only the first two item-coded procedures and only the following files:
- `data/golden-dataset/atlante-concorsi-universitari/procedures/profile_requirements.csv`
- `data/golden-dataset/atlante-concorsi-universitari/procedures/evaluation_criteria.csv`
- `data/golden-dataset/atlante-concorsi-universitari/procedures/profile_requirement_items.csv`
- `data/golden-dataset/atlante-concorsi-universitari/procedures/evaluation_criterion_items.csv`

Procedures audited:
- `ACU-PILOT-0001`
- `ACU-PILOT-0002`

No committee, candidate, or relation files were modified in this step.

---

## Consistency outcome

**Overall outcome: FULL PASS** for the two audited procedures.

Profile item counts now match aggregate profile counts for all requested metrics.
Criteria item decomposition now supports aggregate criteria metrics (main criteria count, subcriteria count, weights, thresholds, profile-linked criteria count, and discretionary representation).

---

## 1) Profile consistency table

| Procedure | Metric | Aggregate value | Item-layer count/check | Status |
|---|---|---:|---:|---|
| ACU-PILOT-0001 | number_of_thematic_keywords | 5 | 5 | OK |
| ACU-PILOT-0001 | number_of_methodological_keywords | 4 | 4 | OK |
| ACU-PILOT-0001 | number_of_experience_requirements | 3 | 3 | OK |
| ACU-PILOT-0001 | number_of_project_lab_centre_references | 1 | 1 | OK |
| ACU-PILOT-0001 | number_of_language_requirements | 0 | 0 | OK |
| ACU-PILOT-0001 | has_highly_specific_topic_method_experience_combination | true | specific_combination_term count = 1 | OK |
| ACU-PILOT-0002 | number_of_thematic_keywords | 5 | 5 | OK |
| ACU-PILOT-0002 | number_of_methodological_keywords | 4 | 4 | OK |
| ACU-PILOT-0002 | number_of_experience_requirements | 1 | 1 | OK |
| ACU-PILOT-0002 | number_of_project_lab_centre_references | 1 | 1 | OK |
| ACU-PILOT-0002 | number_of_language_requirements | 0 | 0 | OK |
| ACU-PILOT-0002 | has_highly_specific_topic_method_experience_combination | false | specific_combination_term count = 0 | OK |

### Profile evidence quality check

For both procedures, each profile item row contains:
- `item_text`
- `source_excerpt`
- `source_document_id`
- `confidence_level`
- `notes`

No accusatory or legally conclusive language was found in profile item rows.

---

## 2) Criteria consistency table

| Procedure | Metric | Aggregate value | Item-layer count/check | Status | Note |
|---|---|---:|---:|---|---|
| ACU-PILOT-0001 | number_of_criteria | 12 | main_criterion count = 12 | OK | Count aligned. |
| ACU-PILOT-0001 | number_of_subcriteria | 10 | subcriterion count = 10 | OK | Count aligned. |
| ACU-PILOT-0001 | has_weights | true | weight count = 2 | OK | Supported by explicit weight rows. |
| ACU-PILOT-0001 | has_thresholds | true | threshold count = 1 | OK | Supported by explicit threshold row. |
| ACU-PILOT-0001 | number_of_criteria_linked_to_profile | 2 | linked criteria count = 2 | OK | Supported by profile-linked rows. |
| ACU-PILOT-0001 | discretionary representation | share_non_quantified_discretionary_criteria = 0.2 | discretionary rows = 2 | OK (support) | Share metric supported by explicit discretionary rows. |
| ACU-PILOT-0002 | number_of_criteria | 11 | main_criterion count = 11 | OK | Count aligned. |
| ACU-PILOT-0002 | number_of_subcriteria | 0 | subcriterion count = 0 | OK | Count aligned. |
| ACU-PILOT-0002 | has_weights | true | weight count = 2 | OK | Supported by explicit weight rows. |
| ACU-PILOT-0002 | has_thresholds | true | threshold count = 1 | OK | Supported by explicit threshold row. |
| ACU-PILOT-0002 | number_of_criteria_linked_to_profile | 2 | linked criteria count = 2 | OK | Supported by profile-linked rows. |
| ACU-PILOT-0002 | discretionary representation | share_non_quantified_discretionary_criteria = 0.4 | discretionary rows = 4 | OK (support) | Share metric supported by explicit discretionary rows. |

### Criteria evidence quality check

For both procedures, each criteria item row contains:
- `criterion_label` and/or `criterion_text`
- `source_excerpt`
- `source_document_id`
- `confidence_level`
- `notes`

No accusatory or legally conclusive language was found in criteria item rows.

---

## 3) Mismatches found

No blocking mismatches remain for the two audited procedures after item-level completion.

---

## 4) Corrections made in this audit step

- Added missing `profile_requirement_items` rows for 0001 and 0002 so item-type counts match aggregate profile counts.
- Added missing `evaluation_criterion_items` rows for 0001 and 0002 to support aggregate criteria decomposition and coded flags.
- Preserved existing item IDs and extended with stable sequential IDs for newly added rows.

No aggregate file was modified in this step.

---

## 5) Remaining ambiguities

No blocking ambiguity remains for consistency checks in procedures 0001 and 0002.

---

## 6) Recommendation

It is safe to start controlled backfill for the remaining eight procedures.

Recommended execution pattern:
1. decompose item layer procedure by procedure;
2. re-run consistency checks after each batch;
3. keep conservative, evidence-linked wording in item rows and notes.
