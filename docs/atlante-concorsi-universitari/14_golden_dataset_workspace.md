# 14 — Golden dataset workspace specification

## Goal
Define the operational workspace for manual coding of the first 50–100 procedures.

## Evidence chain
The workspace enforces this chain:
1. official source URL;
2. downloaded/stored raw document;
3. document metadata (`documents.csv`);
4. extracted fields (`procedures/*.csv`);
5. derived indicators (profile/criteria files);
6. QA validation and review notes.

## Operational folders
- `data/golden-dataset/atlante-concorsi-universitari/source_registry/`
- `data/golden-dataset/atlante-concorsi-universitari/procedures/`
- `data/golden-dataset/atlante-concorsi-universitari/raw_documents/`
- `data/golden-dataset/atlante-concorsi-universitari/snapshots/`
- `data/golden-dataset/atlante-concorsi-universitari/review_notes/`
- `data/golden-dataset/atlante-concorsi-universitari/qa_reports/`

## CSV alignment rule
All golden workspace CSV headers must match the corresponding files in
`data/templates/atlante-concorsi-universitari/`.

Any schema/field change must be applied first to:
1. documentation;
2. JSON schema;
3. template CSV;
4. golden dataset workspace CSV.

## Out of scope
- automated crawling;
- scraping runtime;
- dashboards;
- runtime scoring engines;
- agentic browsing execution.
