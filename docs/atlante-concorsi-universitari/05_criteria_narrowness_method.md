# 05 — Criteria narrowness method

## Scope
This method codes how articulated or narrow documented evaluation criteria appear.
It does not determine procedural validity.

## Raw documentary fields
- `criteria_available`
- `criteria_publication_date`
- `number_of_criteria`
- `number_of_subcriteria`
- `has_weights`
- `has_thresholds`
- `has_eliminatory_criteria`
- `number_of_criteria_linked_to_profile`
- `share_non_quantified_discretionary_criteria`
- `criteria_excerpt_1`
- `criteria_excerpt_2`

## Derived indicator
If `criteria_available=false`, set class to `not_determinable`.
Otherwise:

```
score =
  1.2 * number_of_criteria +
  1.0 * number_of_subcriteria +
  2.0 * has_weights +
  2.5 * has_thresholds +
  2.5 * has_eliminatory_criteria +
  1.3 * number_of_criteria_linked_to_profile +
  8.0 * share_non_quantified_discretionary_criteria
```

Where boolean is `1` if true, `0` if false. The discretionary share is in `[0,1]`.

## Classification
- `low`: score < 8
- `medium`: 8 <= score < 15
- `high`: 15 <= score < 24
- `very_high`: score >= 24
- `not_determinable`: criteria unavailable or insufficiently documented

Field names:
- `criteria_narrowness_score`
- `criteria_narrowness_class`
- `human_review_required`

## Human review rule
Set `human_review_required=true` when:
- class is `very_high`, or
- `share_non_quantified_discretionary_criteria >= 0.60`, or
- criteria are missing but expected from procedure stage.
