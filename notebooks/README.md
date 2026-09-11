# Notebooks / scripts

Run in order from inside this folder:

1. **`01_clean_data.py`**
   Loads `../data/raw_sales_data.csv`, renames columns to FMCG-style
   business terms, fixes date types, imputes missing margin values by
   category median, and derives `order_month`, `margin_value`, and
   `delivery_days`. Saves to `../data/cleaned_sales_data.csv`.

2. **`02_analysis_and_forecast.py`**
   Reads the cleaned data and produces:
   - a monthly revenue trend chart with a simple 3-month linear forecast
   - a revenue + margin % by region chart
   - a top-10-client revenue concentration chart
   - a margin % by product category chart
   - `../dashboard/powerbi_ready_data.csv` (import this into Power BI/Tableau)
   - `../dashboard/findings.txt` (plain-language summary of the four
     findings above)

Both scripts are plain Python — no Jupyter required — so they're easy to
re-run after any data refresh: `python 01_clean_data.py && python 02_analysis_and_forecast.py`.
