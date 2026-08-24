# UX experiment plan — 2026-08-24T15:19:16Z

- Proposals: 4

## Top proposals

### card_review_mode: Introduce card-based one-link review mode

- Problem: The review queue is large relative to the total triaged corpus.
- Evidence: `{'count': 230, 'denominator': 340, 'share_pct': 67.65}`
- Change: Add an optional card-based mode showing one candidate link at a time with primary approve/reject/evidence actions.
- Expected effect: Reduce cognitive load and make sequential validation easier than scanning a dense table.
- Risk: `medium`
- Suggested autonomy: `broad`

### unknown_resolution_queue: Create a dedicated unknown-resolution queue

- Problem: A large share of links remains in unknown/review-required state.
- Evidence: `{'count': 149, 'denominator': 340, 'share_pct': 43.82}`
- Change: Add a saved focus queue for unknown items with explanation prompts and needs-evidence defaults.
- Expected effect: Help reviewers resolve uncertain links without mixing them with likely competition pages.
- Risk: `medium`
- Suggested autonomy: `iteration`

### navigation_noise_rule: Strengthen navigation-link suppression

- Problem: Navigation-like links are reaching the review queue.
- Evidence: `{'count': 12, 'denominator': 340, 'share_pct': 3.53}`
- Change: Update deterministic triage to mark skip/menu/content anchors as likely_not_relevant unless other strong competition signals exist.
- Expected effect: Reduce false positives before they reach manual validation.
- Risk: `low`
- Suggested autonomy: `iteration`

### source_summary_first: Add source-level summary before link review

- Problem: Many pages are possible competition sources but not high-confidence direct evidence.
- Evidence: `{'count': 81, 'denominator': 340, 'share_pct': 23.82}`
- Change: Add a source-level summary panel grouping links by university/source URL before row-level review.
- Expected effect: Let reviewers validate or deprioritise whole source clusters before reviewing every individual link.
- Risk: `medium`
- Suggested autonomy: `broad`
