# FMCG-Style Sales & Margin Performance Dashboard

**Author:** Rutwik Nighot — Master of Information Systems, University of Melbourne
**Skills demonstrated:** Python (pandas), data cleaning, statistical forecasting, Power BI dashboarding, business analysis

## Problem statement

Commercial and category analysts in FMCG/CPG businesses need to answer three
questions on a recurring basis: *Where is revenue coming from? Which regions
and clients carry margin risk? Where is the business heading next quarter?*
This project builds a small end-to-end analytics workflow that answers all
three, using the skillset (Power BI, SQL, Python, financial modelling) I list
on my resume, applied to a sales dataset structured the way a real
supplier's commercial dataset is structured — by region, client account,
product category, discount rate, and margin.

## About the dataset

This uses a public "Superstore"-style sales dataset (order-level records
with region, client, product category, discount, and margin fields), not a
literal FMCG company's data — a public dataset with real client accounts,
regional sales, and margin percentages specific to FMCG is not available.
The column structure (region → client → category → margin % → discount) is
functionally identical to what a supplier's commercial dataset looks like,
so the analysis techniques — regional performance, client concentration
risk, margin-by-category, revenue forecasting — transfer directly. I'm
upfront about this substitution; the value of the project is in the
analysis method, not the specific dataset.

## What's in this repo

```
fmcg-sales-margin-dashboard/
├── data/
│   ├── raw_sales_data.csv          # original downloaded dataset
│   └── cleaned_sales_data.csv      # cleaned + reframed with FMCG-style columns
├── notebooks/
│   ├── 01_clean_data.py            # cleaning & column reframing script
│   └── 02_analysis_and_forecast.py # charts + linear revenue forecast
├── dashboard/
│   ├── charts/                     # PNG exports of each chart (for quick viewing)
│   ├── powerbi_ready_data.csv      # import this directly into Power BI / Tableau
│   └── findings.txt                # plain-text summary of key findings
└── README.md
```

## Key findings (from `dashboard/findings.txt`)

- **Revenue trend:** monthly revenue is gently declining over the four-year
  window; a simple linear forecast projects the next three months.
- **Regional performance:** one region contributes over half of total
  revenue — useful for prioritising account coverage.
- **Client concentration:** the top 10 clients (out of ~800) make up a
  measurable share of total revenue — a concentration-risk flag any
  commercial team should track.
- **Category margin:** margin percentage varies meaningfully by product
  category, which should inform discounting strategy.

## How to reproduce

```bash
pip install pandas matplotlib
python notebooks/01_clean_data.py
python notebooks/02_analysis_and_forecast.py
```

Then open `dashboard/powerbi_ready_data.csv` in Power BI Desktop or Tableau
Public to build the interactive dashboard (revenue by region/category,
client concentration table, margin trend line).

## Why this project

I spent two years in technical sales across chemical and dairy
manufacturing — managing 150+ B2B accounts, tracking regional revenue, and
negotiating around margin and discount. This project is the same commercial
questions, approached from the analyst's side of the table instead of the
sales rep's: building the dashboard instead of being the line item on it.
