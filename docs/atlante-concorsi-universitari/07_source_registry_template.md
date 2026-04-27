# 07 — Source registry template

The registry tracks documentary source endpoints by university.

## Required fields
- `source_registry_entry_id`
- `university_name`
- `university_type`
- `main_competitions_url`
- `albo_online_url`
- `amministrazione_trasparente_url`
- `recruitment_page_url`
- `archive_url`
- `source_type` (`static_html`, `dynamic_html`, `albo_portal`, `pdf_list`, `mixed`, `unknown`)
- `update_frequency_observed`
- `scraping_difficulty` (`low`, `medium`, `high`)
- `archive_depth`
- `robots_or_access_notes`
- `last_checked_at`
- `notes`

## Usage notes
- Keep one row per university and source cluster.
- If multiple relevant source clusters exist, create multiple rows.
- Preserve exact URLs and update `last_checked_at` at each review.
