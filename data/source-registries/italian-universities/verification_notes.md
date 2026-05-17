# Verification notes

## Status semantics

- `verified`: homepage + recruitment/concorsi URL verificati su dominio ufficiale.
- `homepage_only`: homepage verificata; endpoint recruitment plausibile ma da confermare a livello sezione.
- `needs_human_review`: homepage verificata; recruitment URL non fissato in questo pass.
- `not_determinable`: homepage verificata; indice recruitment non determinabile con sufficiente confidenza.

## Coverage metrics (issue #61 run)

- universities mapped: 30
- verified homepage: 30
- recruitment/concorsi page populated: 26
- needing human review / homepage-only / not-determinable: 10

## Next action

Proseguire con completamento full-universe tramite lista istituzionale nazionale approvata e controllo umano dei casi incerti.
