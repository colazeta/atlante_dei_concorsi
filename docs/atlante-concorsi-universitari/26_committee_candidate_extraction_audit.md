# 26 — Committee/Candidate extraction cross-procedure audit (ACU-PILOT-0001 … ACU-PILOT-0010)

## Audit scope

Audited files only:
- `data/golden-dataset/atlante-concorsi-universitari/procedures/committee_members.csv`
- `data/golden-dataset/atlante-concorsi-universitari/procedures/candidates.csv`

No relation coding was performed.
No modifications were made to procedures/documents/criteria/methodology/schema files.

---

## 1) Committee coverage table

Expected minimum committee size used for this audit: **3 members per procedure**.

| Procedure | Committee rows | Min size met (>=3) | procedure_id present | person_name present or `not_determinable` | role_in_committee populated or `not_determinable` | affiliation populated or `not_determinable` | source_document_id populated | source_url populated | confidence_level populated | Result |
|---|---:|---|---|---|---|---|---|---|---|---|
| ACU-PILOT-0001 | 3 | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Pass |
| ACU-PILOT-0002 | 3 | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Pass |
| ACU-PILOT-0003 | 3 | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Pass |
| ACU-PILOT-0004 | 3 | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Pass |
| ACU-PILOT-0005 | 3 | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Pass |
| ACU-PILOT-0006 | 3 | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Pass |
| ACU-PILOT-0007 | 3 | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Pass |
| ACU-PILOT-0008 | 3 | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Pass |
| ACU-PILOT-0009 | 3 | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Pass |
| ACU-PILOT-0010 | 3 | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Pass |

---

## 2) Candidate coverage table

Allowed status values checked:
- `admitted`
- `excluded`
- `evaluated`
- `withdrawn`
- `winner`
- `eligible`
- `not_determinable`

| Procedure | Candidate rows | Determinable rows | Placeholder rows (`not_determinable`) | Candidate statuses valid | source_document_id populated | source_url populated | confidence_level populated | Placeholder-rule compliant |
|---|---:|---:|---:|---|---|---|---|---|
| ACU-PILOT-0001 | 1 | 0 | 1 | Yes | Yes | Yes | Yes | Yes |
| ACU-PILOT-0002 | 1 | 0 | 1 | Yes | Yes | Yes | Yes | Yes |
| ACU-PILOT-0003 | 1 | 0 | 1 | Yes | Yes | Yes | Yes | Yes |
| ACU-PILOT-0004 | 1 | 0 | 1 | Yes | Yes | Yes | Yes | Yes |
| ACU-PILOT-0005 | 1 | 0 | 1 | Yes | Yes | Yes | Yes | Yes |
| ACU-PILOT-0006 | 1 | 1 | 0 | Yes | Yes | Yes | Yes | N/A |
| ACU-PILOT-0007 | 7 | 7 | 0 | Yes | Yes | Yes | Yes | N/A |
| ACU-PILOT-0008 | 1 | 1 | 0 | Yes | Yes | Yes | Yes | N/A |
| ACU-PILOT-0009 | 5 | 5 | 0 | Yes | Yes | Yes | Yes | N/A |
| ACU-PILOT-0010 | 4 | 4 | 0 | Yes | Yes | Yes | Yes | N/A |

---

## 3) Placeholder candidate table

| Procedure | Placeholder rows | At most one placeholder row | `person_name=not_determinable` | `candidate_status=not_determinable` | Notes explain extraction limitation | Audit result |
|---|---:|---|---|---|---|---|
| ACU-PILOT-0001 | 1 | Yes | Yes | Yes | Yes | Pass |
| ACU-PILOT-0002 | 1 | Yes | Yes | Yes | Yes | Pass |
| ACU-PILOT-0003 | 1 | Yes | Yes | Yes | Yes | Pass |
| ACU-PILOT-0004 | 1 | Yes | Yes | Yes | Yes | Pass |
| ACU-PILOT-0005 | 1 | Yes | Yes | Yes | Yes | Pass |

---

## 4) Data-quality checks

Checks performed:
- duplicate committee members within same procedure;
- duplicate candidate rows within same procedure;
- inconsistent naming formats;
- missing source references;
- notes language that implies conflicts/irregularities/legal conclusions.

Findings:
1. **Duplicates**
   - No duplicate committee member rows detected within the same procedure.
   - No exact duplicate candidate rows detected within the same procedure.
2. **Missing source references**
   - No missing `source_document_id`, `source_url`, or `confidence_level` in audited rows.
3. **Naming consistency**
   - Minor heterogeneity in naming style (e.g., some committee names in “Surname Name” order in older rows vs “Name Surname” in later rows), but not a blocking integrity issue for current extraction traceability.
4. **Notes language review**
   - Notes remain procedural/traceability-oriented and do not include conflict allegations or legal conclusions.

---

## 5) Corrections made, if any

- **No corrections were made** to `committee_members.csv` or `candidates.csv` in this audit step.
- This step adds documentation only.

---

## 6) Recommendation

Status recommendation: **safe to proceed to `committee_candidate_relations.csv` coding**, with conservative controls maintained:
- keep source-linked relation assertions only;
- avoid inference where relation evidence is not explicit;
- preserve placeholder discipline where candidate identity/status is non-determinable.
