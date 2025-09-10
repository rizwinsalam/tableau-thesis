#!/usr/bin/env python3
import csv
import os
import random
from datetime import datetime
from math import ceil

DATA_PATH = "/workspace/data/synthetic_sales.csv"
OUT_DIR = "/workspace/docs/screenshots"
INSIGHTS_MD = "/workspace/docs/insights.md"

random.seed(7)


def ensure_out_dir():
    os.makedirs(OUT_DIR, exist_ok=True)


def load_rows():
    rows = []
    with open(DATA_PATH, newline="") as f:
        reader = csv.DictReader(f)
        for r in reader:
            try:
                r["Order Date"] = datetime.strptime(r["Order Date"], "%Y-%m-%d").date()
                r["Sales"] = float(r["Sales"]) if r["Sales"] else 0.0
                r["Profit"] = float(r["Profit"]) if r["Profit"] else 0.0
                r["Discount"] = float(r["Discount"]) if r["Discount"] else 0.0
                r["Quantity"] = int(r["Quantity"]) if r["Quantity"] else 0
            except Exception:
                continue
            rows.append(r)
    return rows


def month_key(d):
    return datetime(d.year, d.month, 1)


def agg_monthly(rows):
    monthly = {}
    for r in rows:
        m = month_key(r["Order Date"])
        monthly.setdefault(m, 0.0)
        monthly[m] += r["Sales"]
    months = sorted(monthly.keys())
    return months, [monthly[m] for m in months]


def agg_category(rows):
    cat = {}
    for r in rows:
        c = r["Category"]
        cat.setdefault(c, 0.0)
        cat[c] += r["Sales"]
    items = sorted(cat.items(), key=lambda x: x[1], reverse=True)
    return [k for k, _ in items], [v for _, v in items]


def sample_scatter(rows, n=1500):
    if len(rows) <= n:
        return rows
    return random.sample(rows, n)


def compute_kpis(rows):
    total_sales = sum(r["Sales"] for r in rows)
    total_profit = sum(r["Profit"] for r in rows)
    margin = (total_profit / total_sales * 100.0) if total_sales > 0 else 0.0
    avg_discount = sum(r["Discount"] for r in rows) / len(rows) * 100.0 if rows else 0.0
    return total_sales, total_profit, margin, avg_discount


def write_svg(path, svg):
    with open(path, "w") as f:
        f.write(svg)


def fmt_currency(x):
    return f"${x:,.0f}"


def svg_header(width, height):
    return f"<svg xmlns='http://www.w3.org/2000/svg' width='{width}' height='{height}' viewBox='0 0 {width} {height}'>\n"


def svg_footer():
    return "</svg>\n"


def chart_kpis_svg(rows):
    width, height = 1000, 220
    total_sales, total_profit, margin, avg_discount = compute_kpis(rows)
    svg = [svg_header(width, height)]
    svg.append("<rect x='0' y='0' width='1000' height='220' fill='white' />\n")
    x_positions = [80, 360, 640, 840]
    labels = ["Total Sales", "Total Profit", "Margin", "Avg Discount"]
    values = [fmt_currency(total_sales), fmt_currency(total_profit), f"{margin:.1f}%", f"{avg_discount:.1f}%"]
    for x, label, value in zip(x_positions, labels, values):
        svg.append(f"<text x='{x}' y='70' font-size='18' fill='#6b7280' text-anchor='middle'>{label}</text>\n")
        svg.append(f"<text x='{x}' y='140' font-size='34' font-weight='700' fill='#111827' text-anchor='middle'>{value}</text>\n")
    svg.append(svg_footer())
    write_svg(os.path.join(OUT_DIR, "kpi-summary.svg"), "".join(svg))


def chart_monthly_svg(months, sales):
    width, height = 1000, 380
    padding = 60
    max_y = max(sales) if sales else 1
    # round up to a nice tick
    tick = 10 ** (len(str(int(max_y))) - 1)
    max_axis = ceil(max_y / tick) * tick
    svg = [svg_header(width, height)]
    svg.append("<rect x='0' y='0' width='1000' height='380' fill='white' />\n")
    # axes
    svg.append(f"<line x1='{padding}' y1='{height-padding}' x2='{width-padding}' y2='{height-padding}' stroke='#9ca3af'/>\n")
    svg.append(f"<line x1='{padding}' y1='{padding}' x2='{padding}' y2='{height-padding}' stroke='#9ca3af'/>\n")
    # points
    n = len(months)
    def x_for(i):
        if n == 1:
            return (width - 2*padding)/2 + padding
        return padding + i * (width - 2*padding) / (n - 1)
    def y_for(v):
        return (height - padding) - (v / max_axis) * (height - 2*padding)
    # line
    pts = [f"{x_for(i)},{y_for(v)}" for i, v in enumerate(sales)]
    svg.append(f"<polyline fill='none' stroke='#2563eb' stroke-width='3' points='{' '.join(pts)}'/>\n")
    # markers
    for i, v in enumerate(sales):
        x = x_for(i)
        y = y_for(v)
        svg.append(f"<circle cx='{x}' cy='{y}' r='3.5' fill='#2563eb' />\n")
    # labels
    svg.append("<text x='500' y='28' font-size='18' font-weight='700' text-anchor='middle'>Monthly Sales Trend</text>\n")
    # y ticks
    for t in range(0, 6):
        val = max_axis * t / 5
        y = y_for(val)
        svg.append(f"<line x1='{padding-5}' y1='{y}' x2='{padding}' y2='{y}' stroke='#9ca3af'/>\n")
        svg.append(f"<text x='{padding-10}' y='{y+4}' font-size='12' text-anchor='end'>{fmt_currency(val)}</text>\n")
    # x tick labels (every 2 months)
    for i, m in enumerate(months):
        if i % 2 == 0 or i == n-1:
            x = x_for(i)
            svg.append(f"<text x='{x}' y='{height-20}' font-size='12' text-anchor='middle'>{m.strftime('%b %y')}</text>\n")
    svg.append(svg_footer())
    write_svg(os.path.join(OUT_DIR, "monthly-sales-trend.svg"), "".join(svg))


def chart_category_svg(categories, values):
    width, height = 800, 300
    padding = 60
    max_x = max(values) if values else 1
    tick = 10 ** (len(str(int(max_x))) - 1)
    max_axis = ceil(max_x / tick) * tick
    bar_h = (height - 2*padding) / max(1, len(categories)) * 0.6
    svg = [svg_header(width, height)]
    svg.append("<rect x='0' y='0' width='800' height='300' fill='white' />\n")
    # axes
    svg.append(f"<line x1='{padding}' y1='{height-padding}' x2='{width-padding}' y2='{height-padding}' stroke='#9ca3af'/>\n")
    svg.append(f"<line x1='{padding}' y1='{padding}' x2='{padding}' y2='{height-padding}' stroke='#9ca3af'/>\n")
    def x_for(v):
        return padding + (v / max_axis) * (width - 2*padding)
    # bars
    for i, (cat, val) in enumerate(zip(categories, values)):
        y = padding + i * (height - 2*padding) / max(1, len(categories))
        svg.append(f"<rect x='{padding}' y='{y}' width='{max(1, x_for(val)-padding)}' height='{bar_h}' fill='#34d399'/>\n")
        svg.append(f"<text x='{padding-8}' y='{y + bar_h/2 + 4}' font-size='12' text-anchor='end'>{cat}</text>\n")
    # title and x ticks
    svg.append("<text x='400' y='28' font-size='18' font-weight='700' text-anchor='middle'>Sales by Category</text>\n")
    for t in range(0, 6):
        val = max_axis * t / 5
        x = x_for(val)
        svg.append(f"<line x1='{x}' y1='{height-padding}' x2='{x}' y2='{height-padding+5}' stroke='#9ca3af'/>\n")
        svg.append(f"<text x='{x}' y='{height-padding+20}' font-size='12' text-anchor='middle'>{fmt_currency(val)}</text>\n")
    svg.append(svg_footer())
    write_svg(os.path.join(OUT_DIR, "sales-by-category.svg"), "".join(svg))


def chart_scatter_svg(rows):
    width, height = 900, 360
    padding = 60
    xs = [r["Discount"] for r in rows]
    ys = [r["Profit"] for r in rows]
    x_min, x_max = 0.0, max(0.4, max(xs) if xs else 0.4)
    y_min, y_max = (min(ys) if ys else -10.0), (max(ys) if ys else 10.0)
    # pad y range
    y_pad = (y_max - y_min) * 0.1 if y_max > y_min else 1.0
    y_min -= y_pad
    y_max += y_pad

    def x_for(v):
        return padding + (v - x_min) / (x_max - x_min) * (width - 2*padding)

    def y_for(v):
        return (height - padding) - (v - y_min) / (y_max - y_min) * (height - 2*padding)

    svg = [svg_header(width, height)]
    svg.append("<rect x='0' y='0' width='900' height='360' fill='white' />\n")
    # axes
    svg.append(f"<line x1='{padding}' y1='{height-padding}' x2='{width-padding}' y2='{height-padding}' stroke='#9ca3af'/>\n")
    svg.append(f"<line x1='{padding}' y1='{padding}' x2='{padding}' y2='{height-padding}' stroke='#9ca3af'/>\n")
    # points
    for r in rows:
        cx = x_for(r["Discount"])
        cy = y_for(r["Profit"])
        radius = max(2.0, min(6.0, 2.0 + 0.6 * (r["Quantity"] ** 0.5)))
        svg.append(f"<circle cx='{cx:.1f}' cy='{cy:.1f}' r='{radius:.1f}' fill='rgba(99,102,241,0.5)' />\n")
    # labels
    svg.append("<text x='450' y='28' font-size='18' font-weight='700' text-anchor='middle'>Profit vs Discount (size=Quantity)</text>\n")
    # x ticks
    for t in [0.0, 0.1, 0.2, 0.3, 0.4]:
        x = x_for(t)
        svg.append(f"<line x1='{x}' y1='{height-padding}' x2='{x}' y2='{height-padding+5}' stroke='#9ca3af'/>\n")
        svg.append(f"<text x='{x}' y='{height-padding+22}' font-size='12' text-anchor='middle'>{t:.1f}</text>\n")
    # y ticks (5)
    for i in range(6):
        v = y_min + (y_max - y_min) * i / 5
        y = y_for(v)
        svg.append(f"<line x1='{padding-5}' y1='{y}' x2='{padding}' y2='{y}' stroke='#9ca3af'/>\n")
        svg.append(f"<text x='{padding-10}' y='{y+4}' font-size='12' text-anchor='end'>{fmt_currency(v)}</text>\n")
    svg.append(svg_footer())
    write_svg(os.path.join(OUT_DIR, "profit-vs-discount.svg"), "".join(svg))


def write_insights(rows, months, sales, categories, cat_values):
    total_sales, total_profit, margin, avg_discount = compute_kpis(rows)
    # best month
    best_idx = max(range(len(sales)), key=lambda i: sales[i]) if sales else 0
    best_month = months[best_idx].strftime("%b %Y") if months else "N/A"
    best_month_sales = sales[best_idx] if sales else 0.0
    # top category
    top_cat = categories[0] if categories else "N/A"
    top_cat_share = (cat_values[0] / sum(cat_values) * 100.0) if cat_values and sum(cat_values) > 0 else 0.0
    with open(INSIGHTS_MD, "w") as f:
        f.write("# Insights\n\n")
        f.write(f"- Total Sales: {fmt_currency(total_sales)}\n")
        f.write(f"- Total Profit: {fmt_currency(total_profit)}\n")
        f.write(f"- Margin: {margin:.1f}%\n")
        f.write(f"- Average Discount: {avg_discount:.1f}%\n")
        f.write(f"- Best Month: {best_month} ({fmt_currency(best_month_sales)})\n")
        f.write(f"- Top Category: {top_cat} ({top_cat_share:.1f}% of sales)\n")


def main():
    ensure_out_dir()
    rows = load_rows()
    months, sales = agg_monthly(rows)
    categories, cat_values = agg_category(rows)
    # charts
    chart_kpis_svg(rows)
    chart_monthly_svg(months, sales)
    chart_category_svg(categories, cat_values)
    chart_scatter_svg(sample_scatter(rows, 1500))
    write_insights(rows, months, sales, categories, cat_values)
    print(f"Wrote SVG charts to {OUT_DIR} and insights to {INSIGHTS_MD}")


if __name__ == "__main__":
    main()