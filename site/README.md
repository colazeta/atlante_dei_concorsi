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
