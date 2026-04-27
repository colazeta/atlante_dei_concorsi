# Atlante dei Concorsi Universitari

Repository for the methodological and data-modelling foundation of a documentary atlas of Italian university recruitment procedures.

Current package version: `v0.1-methodology-and-pilot-workspace`.

## What this module contains

- Methodological documentation (`docs/atlante-concorsi-universitari/00-13`) for scope, coding rules, taxonomies, quality checks, publication language, and pilot setup.
- Technology-neutral JSON Schemas (`schemas/atlante-concorsi-universitari/`) for procedures, documents, profile/criteria coding, committee members, candidates, documented relations, and source registry entries.
- CSV templates (`data/templates/atlante-concorsi-universitari/`) aligned with schema fields for manual coding and import pipelines.
- A lightweight validation script (`scripts/validate_atlante_methodology.py`) to check expected files, JSON validity, and schema/CSV header alignment.

## What this module does **not** contain yet

- Crawlers or scraping implementations.
- Dashboard or public UI.
- Runtime risk-scoring engine.
- Agentic browsing/verification runtime.

## Run validation

From repository root:

```bash
python3 scripts/validate_atlante_methodology.py
python3 scripts/validate_golden_dataset.py
```

Expected output on success:

```text
Validation passed: expected files, JSON parsing, and schema/CSV header alignment are OK.
```

## Golden dataset workspace (manual phase)

- Workspace root: `data/golden-dataset/atlante-concorsi-universitari/`.
- Place manually downloaded official files in `raw_documents/`.
- Enter coded records in `procedures/*.csv` and `source_registry/source_registry.csv`.
- Store reviewer decisions in `review_notes/` and QA outputs in `qa_reports/`.
- This phase is manual and evidence-preserving; no public allegation or legal conclusion is produced.
- Real collected raw files are ignored by default via `.gitignore` safeguards.

### Initialize one procedure workspace

```bash
python3 scripts/init_golden_procedure.py \
  --university-slug university_a \
  --procedure-id ACU-TEST-0001
```

### Build document hash manifest

```bash
python3 scripts/hash_golden_documents.py
```

This writes `data/golden-dataset/atlante-concorsi-universitari/qa_reports/document_hash_manifest.csv`.

### Pilot metrics

- Record pilot execution metrics in `data/golden-dataset/atlante-concorsi-universitari/pilot_metrics/pilot_batch_001_metrics.csv`.
- Keep pilot artifacts internal and non-public during this phase.
- Execute the first real 10-procedure pilot using `docs/atlante-concorsi-universitari/18_pilot_runbook.md`.

## Next development phase (recommended)

1. Build ingestion connectors that only collect official/public documentary sources.
2. Implement deterministic parsers that populate raw fields first, then derived indicators.
3. Add pipeline-level schema validation and QA workflow gates before golden dataset ingestion.
4. Introduce controlled publication views that enforce neutral language and uncertainty labels.
