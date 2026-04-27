# 15 — First manual pilot protocol (empirical dry run)

## Scope
Initial dry run to test whether codebook, schemas, CSVs, and QA checklist are operational on real procedures.

## Pilot size
- 2 pilot universities only;
- 5 procedures per university;
- 10 procedures total.

## Constraints
- manual collection only;
- no automated crawling;
- no public-facing publication;
- no legal or disciplinary conclusions.

## Steps
1. Select two pilot universities using heterogeneity rules in document 12.
2. Register sources in `source_registry/source_registry.csv`.
3. Manually collect official documents and store them in `raw_documents/`.
4. Fill procedures CSV set under `procedures/`.
5. Run validation scripts and complete QA checklist.
6. Record unresolved items in `review_notes/`.
7. Produce one pilot QA report in `qa_reports/`.

## Metrics to record
- time needed to code one procedure;
- number of documents found per procedure;
- number of expected documents not found;
- fields successfully extracted;
- fields frequently `not_determinable`;
- ambiguity in document classification;
- ambiguity in candidate identification;
- ambiguity in committee-candidate relations;
- profile specificity coding difficulties;
- criteria narrowness coding difficulties;
- QA failure rate;
- required schema/codebook changes.

## Expected output of dry run
- validated dataset for 10 procedures;
- consolidated list of blocking ambiguities;
- prioritized improvements for methodology and schemas before scaling to 50–100 procedures.
