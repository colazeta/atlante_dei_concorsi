# University registry static UX

## Build data

```bash
python3 scripts/build_university_registry_json.py
python3 scripts/build_mapping_progress_history.py
```

## View locally

Option A (open directly):
- Open `site/index.html` in a browser.

Option B (recommended static server):

```bash
cd site
python3 -m http.server 8000
```

Then visit: `http://localhost:8000`.

## What is shown

- Registry summary cards and searchable university table.
- "Mapping progress over time" tracker driven by `site/data/mapping_progress_history.json`.
- Current mapped total, recruitment URL count, and reconciliation backlog indicator.
- Timeline/progress events with governance-safe labels (partial coverage, coverage audit, reconciliation backlog, needs continuation).
- Manual-confidence focus controls for low-confidence and human-review work.
- Manual decision layer with four controlled values:
  - `accepted`
  - `rejected`
  - `needs_more_evidence`
  - `keep_under_review`

## Manual decision persistence and honest fallback

Because the static UX cannot write directly to repository files, decisions are stored in browser local storage and can be exported/downloaded:

- JSON export from the UI (`manual_review_decisions.json`)
- CSV export from the UI (`manual_review_decisions.csv`)

Exported decisions must be committed manually (or by a follow-up agent task) to repository artifacts such as:

- `data/source-registries/italian-universities/manual_review_decisions.csv`
- `site/data/manual_review_decisions.json`
