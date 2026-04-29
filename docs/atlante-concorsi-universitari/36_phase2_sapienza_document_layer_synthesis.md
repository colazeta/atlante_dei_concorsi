# 36 — Phase 2 Sapienza document-layer synthesis (ACU-P2-0001..0005)

## Scope and sources

Issue: #35.

This synthesis consolidates Sapienza document-layer lessons from ACU-P2-0001..0005, using:
- `docs/atlante-concorsi-universitari/34_phase2_sapienza_document_layer_audit.md`
- `docs/atlante-concorsi-universitari/35_phase2_sapienza_shared_call_document_audit.md`
- `docs/atlante-concorsi-universitari/33_phase2_id_mapping.md`
- `data/golden-dataset/atlante-concorsi-universitari/procedures/procedures.csv`
- `data/golden-dataset/atlante-concorsi-universitari/procedures/documents.csv`

Constraint applied: no CSV edits in this step.

---

## 1) Coverage across Sapienza ACU-P2-0001..0005

### ACU-P2-0001..0003 (micro-batch 1)

From audit #34:
- ACU-P2-0001, ACU-P2-0002, ACU-P2-0003 are present in `procedures.csv` with one row each and mapping-aligned university/type/reference consistency.
- Document-layer coverage is complete enough for coding progression, with core taxonomy types present and no CSV structural defects detected in scope.

### ACU-P2-0004..0005 (shared-call micro-batch)

From audit #35:
- ACU-P2-0004 and ACU-P2-0005 were audited with explicit shared-call boundary controls.
- ACU-P2-0004 is defensible as one constrained sub-procedure.
- ACU-P2-0005 is correctly maintained as narrow/partial in a shared 14-position context.
- No documentary/CSV consistency correction was required.

### Consolidated coverage statement

Sapienza ACU-P2-0001..0005 now has:
- documented document-layer audit coverage for all five IDs;
- explicit shared-call rules for the two difficult cases (0004/0005);
- no unresolved CSV integrity blockers at this stage.

---

## 2) What worked well

1. **Mapping-to-procedure consistency checks**
   - The mapping note to procedure/document-layer cross-check pattern used in #34 scaled well and kept attribution conservative.

2. **Neutral documentary audit framing**
   - The “no enrichment / no relationship inference” constraint prevented scope drift and reduced interpretive noise.

3. **Shared-call risk containment**
   - Treating shared calls as constrained sub-procedure slices with explicit boundary language was effective for avoiding over-attribution.

4. **Validation cadence**
   - Re-running hash + methodology + dataset validation + git structural checks on each micro-batch keeps regressions visible early.

---

## 3) Shared-call handling lessons (key for Padova)

1. **One ACU-P2 ID = one constrained documentary slice**
   - Never absorb sibling-position documents into the focal ID.

2. **Prefer under-attribution over over-attribution**
   - If a document’s applicability to the chosen slice is ambiguous, do not attach it until traceability is clear.

3. **Shared global call artifacts**
   - Shared call notices may be referenced, but downstream stage documents (commission/criteria/acts) must be sub-procedure-specific before assignment.

4. **Keep narrow/partial explicitly labeled where needed**
   - ACU-P2-0005 style cases should preserve partiality instead of forcing artificial completeness.

---

## 4) Taxonomy backlog (document types)

Backlog items emerging from #34/#35:

1. **Interview/colloquio notices**
   - Recurrent use-cases currently landing in `other` may justify a dedicated taxonomy class in a future controlled update.

2. **Multi-file criteria packages**
   - Cases where “criteria stage” spans preliminary minutes + dedicated criteria annex should remain representable without being mistaken for duplicates.

Backlog implication:
- Taxonomy is usable now, but these two patterns should be considered in the next taxonomy refinement cycle.

---

## 5) CSV/validator lessons

1. **CSV hygiene remains critical**
   - Prior lesson on unquoted commas remains valid: every row must preserve column shape to avoid silent shifts.

2. **Validator hardening value**
   - The current validator stack is effective for structural/schema checks and warning visibility.
   - Maintain strict use of `git diff --check` + parser/validator runs in every batch.

3. **Warnings interpretation discipline**
   - Existing non-synthetic-data warnings are informational in this internal pilot context; they should be tracked but not conflated with structural failure.

---

## 6) Readiness decisions

### Sapienza next-layer coding readiness

Decision: **READY**.

Rationale:
- ACU-P2-0001..0003 already passed document-layer consistency.
- ACU-P2-0004..0005 shared-call risk has been explicitly constrained and approved.
- No CSV/document consistency defects requiring correction were found in scope.

### Proceed to Padova document-layer?

Decision: **YES, proceed to Padova (ACU-P2-0006..0011)**.

Condition set to carry forward:
- apply the same shared-page/sub-position boundary discipline used for Sapienza shared-call controls;
- keep conservative attribution and taxonomy guardrails active;
- preserve the same validation cadence per micro-batch.

---

## 7) Final synthesis statement

Sapienza phase-2 document-layer work (ACU-P2-0001..0005) is sufficiently audited and methodologically stable to move forward.

Operational recommendation:
- close Sapienza document-layer synthesis as complete;
- open/execute Padova document-layer coding for ACU-P2-0006..0011 under the same anti-over-attribution and CSV-hardening discipline.
