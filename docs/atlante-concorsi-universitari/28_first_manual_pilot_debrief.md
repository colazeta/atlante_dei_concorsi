# 28 — First manual pilot debrief (Atlante dei Concorsi Universitari)

## 1) Executive summary

### What the pilot covered
The first manual pilot covered end-to-end coding across 10 procedures (`ACU-PILOT-0001` to `ACU-PILOT-0010`) with layered outputs from procedure/document inventory through committee, candidate, and first-pass relation review.

### Number of procedures
- Total procedures in pilot: **10**.

### Universities covered
- **2 universities**:
  - Università di Bologna
  - Università della Calabria

### Layers completed
- Procedure/document layer: completed for all 10 procedures.
- Profile aggregate and criteria aggregate layers: completed for all 10 procedures.
- Profile item layer: completed for all 10 procedures.
- Criteria item layer: complete for a subset, conservative no-backfill for not-determinable procedures.
- Committee and candidate layers: completed for all 10 procedures with placeholder safeguards where needed.
- Relation layer: first-pass completed for eligible procedures only (`0006..0010`) with conservative procedure-level review rows.

### Overall readiness assessment
**Readiness status: `ready_to_scale_with_conditions`**.

The methodology is stable enough for a larger second-phase pilot, but scaling should remain conditional on conservative extraction controls and explicit handling of inaccessible/noisy official documents.

---

## 2) Completed layers (status summary)

| Layer | Status | Coverage summary |
|---|---|---|
| Procedure/document layer | complete | 10/10 procedures present; required document types present for all procedures in pilot inventory. |
| Profile aggregate layer | complete | 10/10 procedures have profile aggregate rows. |
| Profile item layer | complete | item layer present for all 10 procedures (with conservative item typing and source linkage). |
| Criteria aggregate layer | complete | 10/10 procedures have criteria aggregate rows. |
| Criteria item layer | partial_complete_conservative | complete decomposition support for 0001, 0002, 0006; conservative no-backfill for remaining not-determinable procedures. |
| Committee layer | complete | 10/10 procedures with 3-member committees coded from official appointment docs. |
| Candidate layer | complete_with_placeholders | 10/10 procedures covered; placeholder rule applied for procedures where candidate identity/status remained non-determinable. |
| Relation layer | first_pass_complete_for_eligible_scope | procedure-level first-pass review rows for 0006..0010; no rows for 0001..0005 due to candidate placeholder state. |

---

## 3) What worked well

1. **Source registry/document inventory logic**
   - Procedure/document inventory produced stable traceability from procedure pages to registered documents and IDs.
2. **Procedure-level coding discipline**
   - Core procedure metadata stayed consistently structured across institutions despite heterogeneous source portals.
3. **Document-level auditability**
   - Document IDs and source URLs provide reproducible references for later review and recoding.
4. **Item-level keyword preservation**
   - Profile/criteria item layers preserved documentary granularity and supported aggregate consistency checks where decomposition was feasible.
5. **Conservative placeholder handling**
   - Candidate placeholders were constrained to one row per affected procedure with explicit `not_determinable` semantics and documented limitations.
6. **Registered-source-only relation review**
   - First-pass relation coding correctly used a neutral, non-conclusive outcome for registered-source review without external enrichment.

---

## 4) Main limitations observed

1. **Source-page heterogeneity**
   - Different portal structures and naming conventions reduced extraction uniformity.
2. **Direct attachment URL extraction limits**
   - Some registered attachment URLs were unstable/inaccessible or did not resolve directly in reproducible form.
3. **OCR/noisy PDF extraction**
   - Legibility and extraction quality varied across official documents, especially for acts/outcome details.
4. **Criteria documents not always decomposition-safe**
   - Several criteria documents do not support robust item decomposition without over-interpretation.
5. **Candidate extraction failures from inaccessible/unclear acts**
   - Placeholder candidate rows remained necessary when official identity/status evidence was inaccessible or non-reliably extractable.
6. **Relation coding intentionally limited to registered official sources**
   - This improves neutrality and reproducibility but narrows evidence scope in first pass.

---

## 5) Schema/codebook revisions already made

1. **Added `profile_requirement_items` layer** to support item-level profile decomposition and consistency checks.
2. **Added `evaluation_criterion_items` layer** to support criteria decomposition and aggregate-to-item auditability.
3. **Added `no_documented_relation_in_registered_sources`** to relation taxonomy/schema for neutral registered-source-only review outcomes.
4. **Updated validator** (`validate_golden_dataset.py`) to accept the new relation enum.

---

## 6) Remaining codebook improvements recommended

1. **Minimum decomposition threshold for criteria scoring**
   - Define a minimum documentary granularity threshold before assigning decomposition-backed criteria item metrics.
2. **Explicit rule for `not_determinable` criteria rows**
   - Clarify when to keep aggregate criteria only versus when to add sparse item rows with `not_determinable` semantics.
3. **Clearer treatment of shared/general calls**
   - Add explicit guidance for multi-position/shared appointment documents and cross-linked attachments.
4. **Candidate placeholder rule codification**
   - Promote current placeholder constraints into a single explicit reusable rule block in methodology/codebook.
5. **Relation-review eligibility rule**
   - Codify eligibility preconditions (determinable committee + determinable candidates + reviewed registered sources) before relation-layer first-pass rows.

---

## 7) Scale-readiness decision

**Decision: `ready_to_scale_with_conditions`**.

### Conditions
1. Keep conservative source policy (registered official sources only unless methodology explicitly expanded).
2. Preserve strict placeholder discipline for candidate non-determinability.
3. Require per-batch audit notes for coverage and consistency before relation-layer expansion.
4. Apply decomposition-safety checks before criteria-item backfill in not-determinable procedures.
5. Keep human-review flags active for all neutral/absence relation outcomes.

---

## 8) Recommended next phase

Recommended operational batch:
1. Expand to **30–50 procedures**.
2. Include **4–6 additional universities**.
3. Include **at least one private university**.
4. Increase share of **professor procedures** (I/II fascia) alongside RTT calls.
5. Test **automated document retrieval only after** manual extraction rules and fallback handling are stable per-batch.

---

## 9) Open risks

### Methodological risks
- Over-normalization pressure when source structures differ materially.
- Ambiguity in decomposition boundaries for criteria documents with mixed qualitative/quantitative formats.

### Legal/editorial risks
- Misinterpretation risk if neutral absence-of-evidence outcomes are read as conclusive absence claims.
- Privacy/editorial risk if future scaling weakens current conservative “registered sources only” policy.

### Data-quality risks
- Broken or unstable attachment URLs.
- Noisy extraction from scanned/low-quality PDFs.
- Cross-row naming heterogeneity affecting later linkage logic.

### Operational risks
- Manual throughput constraints for larger batches.
- Review bottlenecks if human-review-required rows accumulate without triage.

---

## 10) Go/no-go recommendation

**Recommendation: GO (conditional).**

It is appropriate to close the first manual pilot issue and open a second-phase scale-up issue, provided the scale-up issue explicitly carries the conditions listed above and preserves conservative non-inferential coding controls.
