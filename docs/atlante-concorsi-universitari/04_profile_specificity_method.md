# 04 — Profile specificity method

## Scope
This method codes how specific the advertised profile appears in documentary terms.
It does not establish irregularity.

## Raw documentary fields
- `number_of_profile_requirements`
- `number_of_thematic_keywords`
- `number_of_methodological_keywords`
- `number_of_experience_requirements`
- `number_of_project_lab_centre_references`
- `number_of_language_requirements`
- `has_highly_specific_topic_method_experience_combination`
- `profile_excerpt_1`
- `profile_excerpt_2`

## Derived indicator
`profile_specificity_score` is explainable and decomposable:

```
score =
  1.5 * number_of_profile_requirements +
  1.0 * number_of_thematic_keywords +
  1.0 * number_of_methodological_keywords +
  1.2 * number_of_experience_requirements +
  1.3 * number_of_project_lab_centre_references +
  0.8 * number_of_language_requirements +
  5.0 * has_highly_specific_topic_method_experience_combination
```

Where boolean is `1` if true, `0` if false.

## Classification
- `low`: score < 8
- `medium`: 8 <= score < 15
- `high`: 15 <= score < 24
- `very_high`: score >= 24
- `not_determinable`: profile section unavailable or not extractable

Field names:
- `profile_specificity_score`
- `profile_specificity_class`
- `human_review_required`

## Human review rule
Set `human_review_required=true` when:
- class is `very_high`, or
- key raw fields are `not_determinable`.
