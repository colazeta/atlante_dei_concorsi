# 25 — Committee/Candidate initial audit (ACU-PILOT-0001, ACU-PILOT-0002)

## Audit scope

Audited files only:
- `data/golden-dataset/atlante-concorsi-universitari/procedures/committee_members.csv`
- `data/golden-dataset/atlante-concorsi-universitari/procedures/candidates.csv`

Procedures in scope:
- `ACU-PILOT-0001`
- `ACU-PILOT-0002`

No committee-candidate relation coding was performed in this audit step.

---

## 1) Committee extraction table

| Procedure | Committee row count | source_document_id populated | source_url populated | role_in_committee populated/explicit | affiliation populated/explicit | confidence_level populated | Audit result |
|---|---:|---|---|---|---|---|---|
| ACU-PILOT-0001 | 3 | Yes (all rows) | Yes (all rows) | Yes (`componente`) | Yes (all rows have affiliation) | Yes (all `high`) | Pass |
| ACU-PILOT-0002 | 3 | Yes (all rows) | Yes (all rows) | Yes (`componente`) | Yes (all rows have affiliation) | Yes (all `high`) | Pass |

Notes:
- For both procedures, the appointment document indicates that president/secretary are identified in first meeting, so role is currently coded as `componente` for listed members.

---

## 2) Candidate extraction table

| Procedure | Candidate rows present | person_name=`not_determinable` | candidate_status=`not_determinable` | source_document_id populated | source_url populated | Notes explain extraction limitation | Audit result |
|---|---:|---|---|---|---|---|---|
| ACU-PILOT-0001 | 1 | Yes | Yes | Yes (`ACU-PILOT-0001-DOC-01`) | Yes | Yes (registered official acts URL returned site error in extraction pass) | Pass with documented limitation |
| ACU-PILOT-0002 | 1 | Yes | Yes | Yes (`ACU-PILOT-0002-DOC-01`) | Yes | Yes (official acts source reachable but extracted text not sufficiently legible) | Pass with documented limitation |

---

## 3) Placeholder rule decision

### Decision: **accepted** (methodologically appropriate, with strict constraints)

A single `not_determinable` candidate placeholder row is acceptable **only** when an official outcome/acts/admission source is documented for the procedure but candidate identities/statuses cannot be reliably extracted from accessible official content.

Operational rule:
1. use **one** placeholder candidate row per affected procedure only;
2. do not create multiple placeholder rows;
3. do not infer the number or identity of candidates;
4. set:
   - `person_name=not_determinable`
   - `candidate_status=not_determinable`;
5. include explicit limitation note referencing the official source condition (inaccessible or insufficiently legible extraction).

This preserves conservative traceability without introducing unsupported identities.

---

## 4) Recommendation for scaling to remaining procedures

Scaling is conditionally safe for committee/candidate extraction if the same conservative protocol is applied:
- extract committee members only from official appointment documents;
- extract candidates only from official acts/outcome/admission/evaluation documents;
- use one placeholder `not_determinable` candidate row only under the strict rule above;
- avoid inference and keep source-linked notes for every limitation.

Status recommendation: **safe to scale with conservative controls**.
