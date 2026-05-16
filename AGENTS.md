# AGENTS — Atlante dei Concorsi Universitari

This repository may be operated by coding and research agents only under a governed, evidence-preserving workflow.

## Core rule

Agents may automate repository mechanics, validation, documentation updates and controlled preparation work. They must not automate allegations, legal conclusions, reputational judgements or uncontrolled source expansion.

## Allowed actions

Agents may:

- read repository documentation, schemas, templates, CSV files, issues, pull requests and validation outputs;
- create or update execution logs under `docs/executions/`;
- create or update loop state files under `reports/agentic-loop/`;
- update documentation describing method, governance, QA, stop conditions or execution status;
- initialise empty or clearly synthetic workspaces when explicitly instructed;
- run repository validation scripts;
- open draft pull requests for review;
- comment on issues or pull requests with progress summaries and blockers.

## Restricted actions requiring explicit approval

Agents must stop and request human review before:

- adding a new university/source domain not already approved in the relevant issue or documentation;
- collecting or coding real procedure data beyond the approved pilot scope;
- changing coding taxonomies or schema semantics;
- modifying relation taxonomy values;
- changing publication-language safeguards;
- adding new scraping, crawling or bulk-fetching behaviour;
- changing `.gitignore` safeguards for raw documents or snapshots;
- moving from dry-run mode to substantive dataset expansion.

## Prohibited actions

Agents must not:

- publish findings from the golden dataset;
- create or imply legal conclusions;
- use accusatory language;
- create a `conflict_of_interest_confirmed` field or equivalent;
- infer conflicts or relations from weak name similarity;
- treat coauthorship as automatic conflict;
- treat same affiliation as automatic conflict;
- treat absence of evidence as evidence of absence unless the documented search path supports that coding rule;
- commit raw documents or snapshots where repository policy excludes them;
- run large-scale scraping;
- bypass validation failures;
- silently delete uncertainty markers, caveats, review notes, source references or QA warnings.

## Execution discipline

Each agentic run must produce or update:

1. a machine-readable state file in `reports/agentic-loop/`;
2. a human-readable execution log in `docs/executions/`;
3. a clear next-action or stop condition;
4. validation results or a reason why validation could not be completed.

## Stop conditions

Agents must stop when any of the following is true:

- domain approval is required;
- human review is required;
- a relation or identity match is uncertain;
- validation fails for a non-trivial reason;
- the next step would collect, code or publish real data outside the approved scope;
- the next step would require a judgement about wrongdoing, conflict of interest, legality or intent;
- CI status is unknown after a material change;
- the repository state is inconsistent with the issue instructions.

## Required validations

For ordinary methodology or loop-foundation changes, run:

```bash
python3 scripts/validate_atlante_methodology.py
python3 scripts/validate_golden_dataset.py
python3 scripts/validate_agentic_loop_state.py
```

If a validator cannot be run, the execution log must explain why and mark the run as blocked or partially verified.
