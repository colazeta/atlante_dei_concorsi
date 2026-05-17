# Verification notes

## Status semantics

- `verified`: homepage + recruitment/concorsi URL verificati su dominio ufficiale.
- `homepage_only`: homepage verificata; endpoint recruitment plausibile ma da confermare a livello sezione.
- `needs_human_review`: homepage verificata; recruitment URL non fissato in questo pass.
- `not_determinable`: homepage verificata; indice recruitment non determinabile con sufficiente confidenza.

## Coverage metrics (issue #61 run)

- universities mapped: 80
- verified homepage: 80
- recruitment/concorsi page populated: 28
- needing human review / homepage-only / not-determinable: 61

## Next action

Completare la verifica endpoint recruitment sui casi residuali e riconciliare periodicamente contro master-list istituzionale aggiornata.
