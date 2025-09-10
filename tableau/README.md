# Tableau Workbook Guide

## Create the Workbook
1. Open Tableau Desktop (2023.1+)
2. Connect → Text file → select `data/synthetic_sales.csv`
3. Verify field types (dates, numbers) match `docs/data-dictionary.md`
4. Save as `tableau/sales_dashboard.twbx`

## Dashboards (from `docs/storyboard.md`)

### Executive Overview
- KPI cards: Sales, Profit, Margin, Avg Discount
- Line: Monthly Sales with YoY (use DATE_TRUNC + LOD as needed)
- Map: Sales by Region
- Filters: Date range, Segment

### Drill-Down Analysis
- Bars: Sales and Profit by Category → Sub-Category
- Scatter: Profit vs Discount (size by Quantity)
- Detail table: Orders with quick filters

### Data Quality
- Null counts per field (calculated fields)
- Outliers: high discount, negative profit
- Row counts and last refresh date

## Tips & Best Practices
- Use parameters to toggle metrics (Sales/Profit/Margin)
- Prefer Extracts for speed; hide unused fields
- Name calculated fields clearly (prefix with group, e.g., `KPI_`, `DQ_`)
- Use actions for cross-filtering between sheets

## Publish (Optional)
- Tableau Public → Save to profile
- Copy the public URL into the root `README.md` (Live dashboard)

## Screenshots
- After finalizing, export 2–4 PNGs and place under `docs/screenshots/`