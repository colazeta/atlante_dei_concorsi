# 05 — Exception-based autonomous review policy

## Purpose

This policy moves the agentic review model from **mandatory human review as a default blocker** to **exception-based autonomous review gates**.

Default behaviour is now autonomous continuation, while human review signals are preserved as governance metadata.

## Core decision model

The review gate decider must return exactly one decision:

- `autonomous_allowed`
- `continuation_needed`
- `human_review_required`
- `blocked`

### Default

If no policy breach is detected, the default is `autonomous_allowed` (or `continuation_needed` when work is incomplete but can continue mechanically).

## Required output metadata

Each decision payload must include:

- `confidence_level`
- `verification_status`
- `requires_human_attention`
- `review_reason`
- `blocking_status`

## Non-blocking signals

The following conditions are **non-blocking by policy** and must not block by themselves:

- low confidence only;
- missing recruitment URL;
- `homepage_only` sourcing;
- `not_determinable` classification;
- incomplete coverage that still allows continuation;
- later human assessment needs (`needs_human_review=true`) with no policy breach.

For these cases, set:

- `blocking_status=non_blocking`
- `requires_human_attention=true` when review is advisable.

## Blocking exceptions

Set `blocking_status=blocking` only for explicit policy exceptions:

- policy breach;
- unapproved domain;
- validator failure;
- raw document policy breach;
- relation inference outside approved workflow;
- legal/reputational conclusion generation;
- task outside approved scope.

When a blocking exception exists, decision must be `blocked`.

## Human review semantics

`needs_human_review` and similar flags are attention metadata, not automatic pipeline stops.

Use `human_review_required` only when human judgement is required **and** there is no immediate policy breach; otherwise use `blocked`.

## Governance compatibility

This policy does not authorize:

- dataset expansion outside approved scope;
- taxonomy or schema-semantic changes outside approved issues;
- publication of allegations or legal conclusions;
- committing raw documents/snapshots where excluded by repository policy.

The policy only changes review gating behaviour from default-blocking to exception-based blocking.
