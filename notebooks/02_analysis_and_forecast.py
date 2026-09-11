"""
02_analysis_and_forecast.py
----------------------------
Core analysis for the FMCG Sales & Margin Performance project:
  1. Monthly revenue trend + simple linear forecast (next 3 months)
  2. Revenue and margin by region
  3. Client concentration (top 10 clients' share of revenue)
  4. Category-level margin comparison

Outputs PNG charts to ../dashboard/charts/ for use in the README,
a Power BI-ready CSV, and a short findings.txt summary.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

DATA_PATH = "../data/cleaned_sales_data.csv"
CHART_DIR = "../dashboard/charts"
os.makedirs(CHART_DIR, exist_ok=True)

df = pd.read_csv(DATA_PATH, parse_dates=["order_date"])

findings = []

# ---------------------------------------------------------------
# 1. Monthly revenue trend + simple linear forecast
# ---------------------------------------------------------------
monthly = df.groupby("order_month").agg(
    revenue=("revenue", "sum"),
    margin_value=("margin_value", "sum"),
    orders=("order_id", "nunique"),
).reset_index().sort_values("order_month")

monthly["t"] = np.arange(len(monthly))
coeffs = np.polyfit(monthly["t"], monthly["revenue"], 1)
slope, intercept = coeffs
future_t = np.arange(len(monthly), len(monthly) + 3)
forecast_vals = slope * future_t + intercept

plt.figure(figsize=(11, 5))
x_labels = list(monthly["order_month"]) + [f"F{i+1}" for i in range(3)]
plt.plot(range(len(monthly)), monthly["revenue"], marker="o", label="Actual revenue", linewidth=1.5)
plt.plot(
    range(len(monthly) - 1, len(monthly) + 3),
    [monthly["revenue"].iloc[-1]] + list(forecast_vals),
    linestyle="--", marker="x", color="orange", label="3-month forecast"
)
plt.xticks(range(len(x_labels)), x_labels, rotation=90, fontsize=7)
plt.title("Monthly Revenue Trend with 3-Month Forecast")
plt.ylabel("Revenue ($)")
plt.legend()
plt.tight_layout()
plt.savefig(f"{CHART_DIR}/monthly_revenue_forecast.png", dpi=150)
plt.close()

findings.append(
    f"Monthly revenue trend: slope of ${slope:,.0f}/month "
    f"({'growing' if slope > 0 else 'declining'}). "
    f"Forecast next 3 months: {[f'${v:,.0f}' for v in forecast_vals]}"
)

# ---------------------------------------------------------------
# 2. Revenue and margin by region
# ---------------------------------------------------------------
region_summary = df.groupby("region").agg(
    revenue=("revenue", "sum"),
    margin_value=("margin_value", "sum"),
).reset_index()
region_summary["margin_pct_of_revenue"] = region_summary["margin_value"] / region_summary["revenue"] * 100
region_summary = region_summary.sort_values("revenue", ascending=False)

fig, ax1 = plt.subplots(figsize=(10, 5))
ax1.bar(region_summary["region"], region_summary["revenue"], color="#4C72B0", label="Revenue")
ax1.set_ylabel("Revenue ($)")
ax1.set_xticklabels(region_summary["region"], rotation=45, ha="right")
ax2 = ax1.twinx()
ax2.plot(region_summary["region"], region_summary["margin_pct_of_revenue"], color="#DD8452", marker="o", label="Margin % of revenue")
ax2.set_ylabel("Margin % of revenue")
plt.title("Revenue and Margin % by Region")
fig.tight_layout()
plt.savefig(f"{CHART_DIR}/revenue_margin_by_region.png", dpi=150)
plt.close()

top_region = region_summary.iloc[0]
findings.append(
    f"Top region by revenue: {top_region['region']} (${top_region['revenue']:,.0f}, "
    f"{top_region['margin_pct_of_revenue']:.1f}% margin)."
)

# ---------------------------------------------------------------
# 3. Client concentration
# ---------------------------------------------------------------
client_rev = df.groupby("client_name")["revenue"].sum().sort_values(ascending=False)
top10_share = client_rev.head(10).sum() / client_rev.sum() * 100

plt.figure(figsize=(9, 5))
client_rev.head(10).plot(kind="barh", color="#55A868")
plt.gca().invert_yaxis()
plt.xlabel("Revenue ($)")
plt.title(f"Top 10 Clients by Revenue (= {top10_share:.1f}% of total revenue)")
plt.tight_layout()
plt.savefig(f"{CHART_DIR}/top10_client_concentration.png", dpi=150)
plt.close()

findings.append(
    f"Top 10 clients account for {top10_share:.1f}% of total revenue out of "
    f"{df['client_name'].nunique()} total clients -- a concentration risk worth flagging."
)

# ---------------------------------------------------------------
# 4. Category-level margin comparison
# ---------------------------------------------------------------
cat_summary = df.groupby("product_category").agg(
    revenue=("revenue", "sum"),
    margin_pct=("base_margin_pct", "mean"),
).reset_index().sort_values("revenue", ascending=False)

plt.figure(figsize=(8, 5))
plt.bar(cat_summary["product_category"], cat_summary["margin_pct"] * 100, color="#C44E52")
plt.ylabel("Average base margin (%)")
plt.title("Average Margin % by Product Category")
plt.tight_layout()
plt.savefig(f"{CHART_DIR}/margin_by_category.png", dpi=150)
plt.close()

best_cat = cat_summary.sort_values("margin_pct", ascending=False).iloc[0]
findings.append(
    f"Highest-margin category: {best_cat['product_category']} "
    f"({best_cat['margin_pct']*100:.1f}% avg margin)."
)

# ---------------------------------------------------------------
# Save a Power BI-ready CSV (same as cleaned data, kept separate on purpose)
# ---------------------------------------------------------------
df.to_csv("../dashboard/powerbi_ready_data.csv", index=False)

with open("../dashboard/findings.txt", "w") as f:
    f.write("KEY FINDINGS\n============\n\n")
    for line in findings:
        f.write(f"- {line}\n")

print("Charts saved to dashboard/charts/")
print("\n".join(findings))
