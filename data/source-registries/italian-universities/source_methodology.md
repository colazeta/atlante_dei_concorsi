# Source methodology

## Objective

Espandere la registry degli URL ufficiali degli atenei italiani oltre il bootstrap subset, usando fonti istituzionali/autorevoli.

## Method

1. Partenza dal bootstrap subset già presente nel repository.
2. Espansione con ulteriori atenei su domini ufficiali universitari (`.it` istituzionali).
3. Uso della homepage ufficiale come ancoraggio minimo verificabile per ogni ateneo.
4. Inserimento di `recruitment_page_url` solo quando la sezione concorsi/lavora-con-noi è chiaramente identificabile.
5. Quando il percorso non è sufficientemente determinabile: URL vuoto o classificazione `homepage_only` / `needs_human_review` / `not_determinable`.

## Safeguards

- Nessuna invenzione di URL.
- Nessuna raccolta di dati personali, commissioni, relazioni o esiti.
- Nessuna modifica a tassonomie o golden dataset.
- Tracciabilità tramite `source_url`, `retrieval_date`, `notes`.

## Limitation

Copertura estesa ma non ancora completa dell'universo nazionale; completamento richiede lista master istituzionale e verifiche manuali iterative.
