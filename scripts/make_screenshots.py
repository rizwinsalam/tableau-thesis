#!/usr/bin/env python3
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

DATA_PATH = "/workspace/data/synthetic_sales.csv"
OUT_DIR = "/workspace/docs/screenshots"

sns.set_theme(style="whitegrid", context="talk")
plt.rcParams.update({
    "figure.dpi": 140,
    "savefig.bbox": "tight",
})


def ensure_out_dir():
    os.makedirs(OUT_DIR, exist_ok=True)


def load_data():
    df = pd.read_csv(DATA_PATH, parse_dates=["Order Date"])
    df["Month"] = df["Order Date"].values.astype("datetime64[M]")
    df["Margin"] = np.where(df["Sales"] > 0, (df["Profit"] / df["Sales"]) * 100.0, 0.0)
    return df


def chart_kpis(df):
    total_sales = df["Sales"].sum()
    total_profit = df["Profit"].sum()
    avg_discount = df["Discount"].mean() * 100.0
    margin = (total_profit / total_sales) * 100.0 if total_sales > 0 else 0

    fig, ax = plt.subplots(figsize=(10, 3))
    ax.axis("off")
    ax.text(0.0, 0.7, "Total Sales", fontsize=14, color="#6b7280")
    ax.text(0.0, 0.3, f"${total_sales:,.0f}", fontsize=24, weight="bold")

    ax.text(0.35, 0.7, "Total Profit", fontsize=14, color="#6b7280")
    ax.text(0.35, 0.3, f"${total_profit:,.0f}", fontsize=24, weight="bold")

    ax.text(0.65, 0.7, "Margin", fontsize=14, color="#6b7280")
    ax.text(0.65, 0.3, f"{margin:.1f}%", fontsize=24, weight="bold")

    ax.text(0.85, 0.7, "Avg Discount", fontsize=14, color="#6b7280")
    ax.text(0.85, 0.3, f"{avg_discount:.1f}%", fontsize=24, weight="bold")

    fig.savefig(os.path.join(OUT_DIR, "kpi-summary.png"))
    plt.close(fig)


def chart_monthly_trend(df):
    monthly = df.groupby("Month", as_index=False).agg(Sales=("Sales", "sum"))
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(data=monthly, x="Month", y="Sales", marker="o", ax=ax, color="#2563eb")
    ax.set_title("Monthly Sales Trend")
    ax.set_xlabel("")
    ax.set_ylabel("Sales ($)")
    ax.ticklabel_format(axis="y", style="plain")
    fig.autofmt_xdate()
    fig.savefig(os.path.join(OUT_DIR, "monthly-sales-trend.png"))
    plt.close(fig)


def chart_category_contrib(df):
    cat = df.groupby("Category", as_index=False).agg(Sales=("Sales", "sum"))
    cat = cat.sort_values("Sales", ascending=False)
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(data=cat, x="Sales", y="Category", ax=ax, color="#34d399")
    ax.set_title("Sales by Category")
    ax.set_xlabel("Sales ($)")
    ax.set_ylabel("")
    ax.ticklabel_format(axis="x", style="plain")
    fig.savefig(os.path.join(OUT_DIR, "sales-by-category.png"))
    plt.close(fig)


def chart_profit_vs_discount(df):
    sample = df.sample(n=min(len(df), 3000), random_state=7)
    fig, ax = plt.subplots(figsize=(9, 6))
    sns.scatterplot(data=sample, x="Discount", y="Profit", size="Quantity", hue="Category",
                    palette="Set2", alpha=0.6, ax=ax)
    ax.set_title("Profit vs Discount (size=Quantity)")
    ax.set_xlabel("Discount")
    ax.set_ylabel("Profit ($)")
    ax.legend(title="Category", bbox_to_anchor=(1.02, 1), loc="upper left")
    ax.ticklabel_format(axis="y", style="plain")
    fig.savefig(os.path.join(OUT_DIR, "profit-vs-discount.png"))
    plt.close(fig)


def compute_insights(df):
    insights = {}
    insights["total_sales"] = float(df["Sales"].sum())
    insights["total_profit"] = float(df["Profit"].sum())
    insights["margin_pct"] = float((df["Profit"].sum() / df["Sales"].sum()) * 100.0)
    monthly = df.groupby("Month").agg(Sales=("Sales", "sum"))
    insights["best_month"] = monthly["Sales"].idxmax().strftime("%b %Y")
    insights["best_month_sales"] = float(monthly["Sales"].max())
    by_cat = df.groupby("Category").agg(Sales=("Sales", "sum"))
    top_cat = by_cat["Sales"].idxmax()
    insights["top_category"] = str(top_cat)
    insights["top_category_share_pct"] = float(by_cat.loc[top_cat, "Sales"] / by_cat["Sales"].sum() * 100.0)
    return insights


def write_insights_md(insights):
    path = "/workspace/docs/insights.md"
    with open(path, "w") as f:
        f.write("# Insights\n\n")
        f.write(f"- Total Sales: ${insights['total_sales']:,.0f}\n")
        f.write(f"- Total Profit: ${insights['total_profit']:,.0f}\n")
        f.write(f"- Margin: {insights['margin_pct']:.1f}%\n")
        f.write(f"- Best Month: {insights['best_month']} (${'{:,.0f}'.format(insights['best_month_sales'])})\n")
        f.write(f"- Top Category: {insights['top_category']} ({insights['top_category_share_pct']:.1f}% of sales)\n")
    return path


def main():
    ensure_out_dir()
    df = load_data()
    chart_kpis(df)
    chart_monthly_trend(df)
    chart_category_contrib(df)
    chart_profit_vs_discount(df)
    insights = compute_insights(df)
    md_path = write_insights_md(insights)
    print(f"Saved charts to {OUT_DIR} and insights to {md_path}")


if __name__ == "__main__":
    main()