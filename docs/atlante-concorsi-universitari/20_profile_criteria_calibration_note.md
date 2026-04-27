# 20 — Calibration note (ACU-PILOT-0001, first substantive coding layer)

Date: 2026-04-27
Scope audited:
- `profile_requirements.csv` row `ACU-PILOT-0001-PR-01`
- `evaluation_criteria.csv` row `ACU-PILOT-0001-EC-01`

## What was checked

1. **Internal consistency of raw fields**
   - Profile row: requirement/keyword/method/experience/project/language counts and boolean combination flag.
   - Criteria row: criteria/subcriteria counts, weights/thresholds/eliminatory flags, linkage count, discretionary share.

2. **Internal consistency of derived fields**
   - Recomputed `profile_specificity_score` and class from method formula.
   - Recomputed `criteria_narrowness_score` and class from method formula.
   - Checked `human_review_required` against method rules.

3. **Evidence coherence**
   - Verified excerpts and notes are documentary, neutral, and non-conclusive.

## Calibration conclusion for ACU-PILOT-0001

### Acceptability as-is

**Coding is acceptable as-is; no correction applied.**

- Profile row is internally consistent:
  - score check: `1.5*1 + 1.0*5 + 1.0*4 + 1.2*3 + 1.3*1 + 0.8*0 + 5*1 = 20.4`.
  - class `high` is consistent with method thresholds.
  - `human_review_required=false` is consistent (class not `very_high`; no key-field missingness).

- Criteria row is internally consistent:
  - score check: `1.2*12 + 1.0*10 + 2*1 + 2.5*1 + 2.5*0 + 1.3*2 + 8*0.2 = 31.1`.
  - class `very_high` is consistent with method thresholds.
  - `human_review_required=true` is consistent (class `very_high`).

## Ambiguity point A — Should scoring bands count as subcriteria?

### Proposed calibration rule

Count as `number_of_subcriteria` **only**:
- explicitly enumerated sub-items (e.g., a1/a2/a3; bullet list under a parent criterion), and
- explicitly titled subordinate criteria blocks.

Do **not** count pure scoring bands/grade bands (e.g., ranges or qualitative performance bands used only to assign points) as separate subcriteria unless the document explicitly labels them as autonomous subcriteria.

Rationale: preserves inter-procedure comparability and avoids inflation when documents express grading granularity differently.

## Ambiguity point B — Should productivity objectives count as experience requirements?

### Proposed calibration rule

Count in `number_of_experience_requirements` only statements that explicitly require prior candidate background/track-record (e.g., prior years/roles/track-record in a domain).

Do **not** count forward-looking activity or productivity expectations attached to the post (e.g., expected outputs during appointment) as experience requirements.

Rationale: separates entry constraints from expected future performance.

## Recommended codebook clarification

Add one short clarification box in profile-method/codebook docs with:
- the subcriteria counting rule above;
- the distinction between prior-experience requirements vs forward-looking productivity objectives.

No schema change is necessary for this calibration step.

## Go/no-go for next pilot step

**Go**: it is safe to proceed to coding `ACU-PILOT-0002` with the above calibration rules applied consistently.
