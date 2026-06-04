# UX experiment plan — 2026-06-04T07:09:13Z

- Proposals: 4

## Top proposals

### card_review_mode: Introduce card-based one-link review mode

- Problem: The review queue is large relative to the total triaged corpus.
- Evidence: `{'count': 194, 'denominator': 300, 'share_pct': 64.67}`
- Change: Add an optional card-based mode showing one candidate link at a time with primary approve/reject/evidence actions.
- Expected effect: Reduce cognitive load and make sequential validation easier than scanning a dense table.
- Risk: `medium`
- Suggested autonomy: `broad`

### source_summary_first: Add source-level summary before link review

- Problem: Many pages are possible competition sources but not high-confidence direct evidence.
- Evidence: `{'count': 80, 'denominator': 300, 'share_pct': 26.67}`
- Change: Add a source-level summary panel grouping links by university/source URL before row-level review.
- Expected effect: Let reviewers validate or deprioritise whole source clusters before reviewing every individual link.
- Risk: `medium`
- Suggested autonomy: `broad`

### unknown_resolution_queue: Create a dedicated unknown-resolution queue

- Problem: A large share of links remains in unknown/review-required state.
- Evidence: `{'count': 114, 'denominator': 300, 'share_pct': 38.0}`
- Change: Add a saved focus queue for unknown items with explanation prompts and needs-evidence defaults.
- Expected effect: Help reviewers resolve uncertain links without mixing them with likely competition pages.
- Risk: `medium`
- Suggested autonomy: `iteration`

### navigation_noise_rule: Strengthen navigation-link suppression

- Problem: Navigation-like links are reaching the review queue.
- Evidence: `{'count': 11, 'denominator': 300, 'share_pct': 3.67}`
- Change: Update deterministic triage to mark skip/menu/content anchors as likely_not_relevant unless other strong competition signals exist.
- Expected effect: Reduce false positives before they reach manual validation.
- Risk: `low`
- Suggested autonomy: `iteration`
