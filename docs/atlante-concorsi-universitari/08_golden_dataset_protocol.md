# 08 — Golden dataset protocol (50–100 procedures)

## Objective
Create an initial manually coded dataset for quality control and method calibration.

## Sampling frame
- Select **5–8 universities** balancing:
  - public/private;
  - geographic macro-area;
  - large/medium/small institutions.
- Select **50–100 procedures** across position types and academic fields.

## Selection steps
1. Register official source URLs in the source registry.
2. Sample procedures from a fixed period window (e.g., previous 18 months).
3. Ensure coverage of complete and partial-documentation procedures.

## Manual coding workflow
1. Create `procedure` row with core metadata.
2. Register every retrieved act as a `document` with type taxonomy.
3. Extract profile requirements and criteria fields with excerpts.
4. Register committee members and candidates only when publicly documented.
5. Code documented relations using evidence URLs and excerpts.
6. Populate derived indicators only after raw fields are complete.

## Uncertainty and over-interpretation safeguards
- Use `not_determinable` when public evidence is insufficient.
- Do not infer legal conclusions.
- Keep evidence snippets short and attributable.
- Mark ambiguous records with `human_review_required=true`.

## Human review triggers
Flag for review when:
- key workflow documents are missing;
- profile specificity class is `very_high`;
- criteria narrowness class is `very_high`;
- relation records include `coauthorship_recurrent`, `supervisor_student_relation`, or `grant_or_project_hierarchy` with `confidence_level` not low.

## Quality checks
- Double-code at least 15% of procedures.
- Measure coder agreement on document type and relation type.
- Reconcile disagreements with written adjudication notes.
