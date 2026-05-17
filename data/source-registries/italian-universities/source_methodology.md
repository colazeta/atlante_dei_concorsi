# Source methodology

## Objective

Riconciliare l'universo atteso degli atenei riconosciuti (99) con la registry locale, senza introdurre URL non verificati.

## Authoritative universe source

Perimetro istituzionale MUR (categorie: università statali, non statali legalmente riconosciute, telematiche, scuole superiori a ordinamento speciale), usato come fonte di universo atteso.

## Method

1. Verifica del totale atteso (99) rispetto alle righe già presenti nel CSV principale (80).
2. Produzione di riconciliazione **row-level** per il delta (19 istituzioni).
3. Per ciascuna istituzione mancante: valorizzazione homepage ufficiale quando determinabile da dominio istituzionale.
4. Lasciare `recruitment_page_url` vuoto quando non determinabile con confidenza robusta.
5. Uso di stati non bloccanti (`homepage_only`, `needs_human_review`, `not_determinable`) per preservare l'incertezza.
6. Nessun cambiamento a golden dataset o raccolta raw.

## Output policy

- Se la verifica piena è disponibile: aggiornare `official_university_urls.csv`.
- Se la verifica piena non è completa: usare `missing_universities_to_verify.csv` con una riga per istituzione mancante (fallback adottato in questo pass).
