# 37 — Phase 2 Padova document-layer audit (ACU-P2-0006..0011)

## Audit scope

Issue: #38.

Procedures audited:
- ACU-P2-0006
- ACU-P2-0007
- ACU-P2-0008
- ACU-P2-0009
- ACU-P2-0010
- ACU-P2-0011

Files audited:
- `data/golden-dataset/atlante-concorsi-universitari/procedures/procedures.csv`
- `data/golden-dataset/atlante-concorsi-universitari/procedures/documents.csv`
- `docs/atlante-concorsi-universitari/33_phase2_id_mapping.md`

Focus checks:
- segmentation correctness for the shared Padova page (`https://www.unipd.it/procedura-2025RTT01`);
- position-specific document attribution;
- absence of over-attribution;
- consistency with ID mapping note;
- CSV integrity;
- taxonomy (`document_type`) usage.

---

## 1) Mapping consistency (procedures.csv vs ID mapping)

All six Padova procedures are present in `procedures.csv` and align with mapping #33 on:
- procedure IDs: ACU-P2-0006..0011;
- shared source URL: `https://www.unipd.it/procedura-2025RTT01`;
- per-position procedure references (`pos. 1`, `2`, `3`, `4`, `12`, `13`);
- type: `RTT`.

Result: **mapping coherence confirmed** for the audited Padova block.

---

## 2) Shared-page segmentation and position-specific attribution

Observed implementation pattern:
- each procedure row explicitly encodes one position slice in `procedure_code` and notes;
- each procedure has 5 document rows tied to that same procedure ID;
- document notes explicitly constrain attribution to the matching position sub-section.

Per-procedure pattern (uniform):
- `call_notice`
- `committee_appointment`
- `evaluation_criteria`
- `admission_list`
- `acts_approval`

Result: **segmentation is conservative and position-specific**, with no cross-linking of document IDs across different Padova positions.

---

## 3) Over-attribution risk assessment

Findings:
- no document row for ACU-P2-0006..0011 is assigned to more than one `procedure_id`;
- no row text indicates importing sibling-position evidence into another position;
- notes repeatedly enforce the “constrained sub-section only” rule.

Residual risk:
- because all six procedures point to the same shared page URL, traceability relies heavily on title/notes discipline.

Conclusion:
- **no over-attribution detected** in current CSV rows;
- keep strict position markers in future additions (especially when adding attachment-specific URLs).

---

## 4) Taxonomy use audit (`document_type`)

For ACU-P2-0006..0011, document types used are:
- `call_notice`
- `committee_appointment`
- `evaluation_criteria`
- `admission_list`
- `acts_approval`

Assessment:
- taxonomy use is valid and internally consistent;
- no fallback `other` was used for this block;
- type set is appropriate for a complete stage-chain representation of each constrained position slice.

---

## 5) CSV integrity checks

Checks performed on scoped files:
- parser-level readability and stable column shape;
- no malformed quoting in newly added Padova rows;
- `git diff --check` clean (no whitespace/line-ending defects in current state).

Result: **CSV integrity OK** for audited Padova additions.

---

## 6) Audit decision

Decision for ACU-P2-0006..0011:
- **APPROVED** for next-layer coding.

Conditions to carry forward:
1. preserve one-ID/one-position segmentation;
2. prefer attachment-level URLs when available in later refinement;
3. maintain anti-over-attribution wording in notes for any newly appended documents;
4. keep validation cadence (`hash`, methodology validator, dataset validator, `git diff --check`) per micro-batch.

---

## 7) Progression recommendation

Padova document-layer audit status: **PASS**.

Recommended next step:
- proceed to Napoli Federico II document-layer coding for ACU-P2-0012..0016 under the same shared-source segmentation discipline.
