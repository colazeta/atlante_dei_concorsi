# Verification notes — issue #61 continuation

## Coverage snapshot

- Universo atteso (fonte istituzionale MUR): **99**.
- Righe presenti in `official_university_urls.csv`: **80**.
- Delta riconciliato a livello riga: **19** in `missing_universities_to_verify.csv`.

## Reconciliation outcome

- 19/19 istituzioni mancanti tracciate con una riga dedicata.
- Homepage ufficiale presente per tutte le 19 righe.
- Recruitment URL lasciato vuoto dove non determinabile in modo affidabile.
- Stati usati: principalmente `homepage_only`, con casi `needs_human_review` per ambiguità denominative/deduplica canonica.

## Safeguards respected

- Nessuna modifica al golden dataset.
- Nessun documento raw/PDF/snapshot aggiunto.
- Nessuna inferenza su candidati, commissioni, relazioni o profili reputazionali.
