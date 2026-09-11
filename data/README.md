# Data folder

- `raw_sales_data.csv` — original downloaded dataset (order-level sales
  records: date, region, client, product category, discount, margin).
- `cleaned_sales_data.csv` — output of `notebooks/01_clean_data.py`.
  Columns are renamed to business-friendly, FMCG-style names
  (`revenue`, `client_name`, `region`, `product_category`,
  `base_margin_pct`, `margin_value`, `order_month`, etc.) and missing
  margin values are imputed with the category median.

Do not edit `cleaned_sales_data.csv` by hand — regenerate it by running
the cleaning script so the pipeline stays reproducible.
