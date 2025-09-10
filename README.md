# Tableau Thesis — Interactive Data Visualization

A polished Tableau project that showcases interactive dashboards, clear storytelling, and insight‑driven visuals. This repository documents the project, its purpose, and how to view or extend it.

- Live dashboard: (to be published)
- Video walkthrough (2 min): (optional)

## Overview
This project demonstrates best practices for Tableau dashboard design:
- Thoughtful KPIs and visual hierarchy
- Consistent color and typography system
- Intuitive filters and guided interactions
- Performance‑aware calculations and extracts

## Screenshots
<img width="804" alt="Main Dashboard" src="docs/screenshots/example.png">

Add more screenshots in `docs/screenshots/` and reference them here.

## Key Dashboards
- Executive Overview: High‑level KPIs with trend and YoY comparisons
- Drill‑down Analysis: Explore by segments, time, and geography
- Data Quality View: Track missing values, outliers, and refresh status

## Dataset
- Source: Synthetic generator (`scripts/generate_synthetic_sales.py`)
- File: `data/synthetic_sales.csv`
- Grain: Daily orders; product category and customer segment
- Size: ~13,921 rows (1 year)
- Refresh: Re-run the generator script

## Getting Started (Local)
1) Ensure Python 3.9+ is installed
2) Generate data:
```bash
python3 scripts/generate_synthetic_sales.py
```
3) Open Tableau Desktop (2023.1+)
4) Connect to Text/CSV → select `data/synthetic_sales.csv`
5) Build dashboards using `docs/storyboard.md` as a guide
6) Save your workbook in `tableau/` (e.g., `tableau/sales_dashboard.twbx`)

For detailed workbook guidance, see `tableau/README.md`.

## Project Structure
- `scripts/` — data generator
- `data/` — generated CSV for Tableau
- `tableau/` — workbook files (.twb/.twbx) and guidance
- `docs/architecture.md` — data flow, calculations, and performance notes
- `docs/case-study.md` — problem, approach, insights, and outcomes
- `docs/project-brief.md` — goals, users, scope, success criteria
- `docs/data-dictionary.md` — field definitions
- `docs/storyboard.md` — dashboard plan
- `docs/screenshots/` — PNGs/GIFs of key flows
- `tableau thesis.docx` — original write‑up (source notes)

## Implementation Highlights
- Calculated fields with clear naming for maintainability
- Parameters to toggle views without duplicating sheets
- Actions for cross‑filtering and drill‑through navigation
- Extracts or aggregations to keep interactions responsive

## Roadmap
- [ ] Create `tableau/sales_dashboard.twbx` using storyboard
- [ ] Capture 2–4 screenshots and add to `docs/screenshots/`
- [ ] Publish to Tableau Public and update links above

## License
MIT — see `LICENSE` for details.

## Contact
Questions or feedback: open an issue or reach out via GitHub.
