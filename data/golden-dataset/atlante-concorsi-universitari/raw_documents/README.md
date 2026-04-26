# Raw documents storage guide

Store only documents from official/public university sources.

## Recommended layout

```
raw_documents/
  university_slug/
    procedure_id/
      01_call_notice.pdf
      02_committee_appointment.pdf
      03_evaluation_criteria.pdf
      04_minutes.pdf
      05_acts_approval.pdf
```

## Rules
- Use official documents only.
- Keep original filenames when useful, but prefix files with ordering numbers.
- Do not overwrite files; store later versions as separate files (`v2`, `v3`, etc.).
- Record source URL and retrieval date in `procedures/documents.csv`.
- Compute and store file hash (`file_hash`) where possible.
