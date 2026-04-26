# Golden dataset workspace — Atlante Concorsi Universitari

This workspace is dedicated to the first **manual** coding cycle (50–100 procedures).

## Purpose
Preserve a verifiable chain of evidence:

`official source URL -> raw document file -> document metadata row -> extracted fields -> derived indicators -> QA review`.

## Structure
- `source_registry/source_registry.csv`: source endpoints by university.
- `procedures/*.csv`: coded records aligned with the official templates.
- `raw_documents/`: manually downloaded official documents.
- `snapshots/`: evidence of source pages as seen at collection time.
- `review_notes/`: coding/reviewer notes for uncertainty and decisions.
- `qa_reports/`: QA output files and validation reports.

## Principles
- Manual collection only in this phase.
- No crawler, no scraping runtime, no dashboard.
- No legal conclusions or public allegations.
- Use neutral documentary language only.
