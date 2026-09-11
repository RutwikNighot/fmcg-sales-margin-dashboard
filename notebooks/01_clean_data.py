"""
01_clean_data.py
-----------------
Loads the raw dataset (data/raw_sales_data.csv), cleans it, and reframes
it with FMCG/CPG-style column names so the analysis mirrors a
Commercial Analyst dataset: client/account, region, product category,
margin, discount, and order priority (used as a proxy for delivery/
service-level urgency).

NOTE on the dataset: this is a public "Superstore"-style dataset
(office supplies/furniture/technology categories), used here as a
stand-in because a public dataset with real client accounts, regional
sales, discounts, and margin fields is hard to find for FMCG
specifically. The columns and structure mirror what a real FMCG sales
dataset looks like (client, region, category, margin %, discount),
so the analysis techniques transfer directly. Be upfront about this
if asked in an interview -- it's honest and shows good judgement.
"""

import pandas as pd
import numpy as np

RAW_PATH = "data/raw_sales_data.csv"
CLEAN_PATH = "data/cleaned_sales_data.csv"

# ---- Load ----
df = pd.read_csv(RAW_PATH)

# ---- Rename columns to FMCG-style, business-friendly names ----
df = df.rename(columns={
    "Order ID": "order_id",
    "Order Date": "order_date",
    "Order Priority": "order_priority",
    "Order Quantity": "quantity",
    "Sales": "revenue",
    "Discount": "discount_rate",
    "Ship Mode": "ship_mode",
    "Profit": "profit",
    "Unit Price": "unit_price",
    "Shipping Cost": "shipping_cost",
    "Customer Name": "client_name",
    "Province": "region_detail",
    "Region": "region",
    "Customer Segment": "client_segment",
    "Product Category": "product_category",
    "Product Sub-Category": "product_subcategory",
    "Product Name": "product_name",
    "Product Container": "pack_type",
    "Product Base Margin": "base_margin_pct",
    "Ship Date": "ship_date",
})

# ---- Clean types ----
df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
df["ship_date"] = pd.to_datetime(df["ship_date"], errors="coerce")
df["base_margin_pct"] = pd.to_numeric(df["base_margin_pct"], errors="coerce")

# ---- Drop rows with no order date (can't analyse trends without it) ----
df = df.dropna(subset=["order_date"])

# ---- Fill missing margin with the category median (simple, defensible approach) ----
df["base_margin_pct"] = df.groupby("product_category")["base_margin_pct"].transform(
    lambda s: s.fillna(s.median())
)

# ---- Derived fields ----
df["order_year"] = df["order_date"].dt.year
df["order_month"] = df["order_date"].dt.to_period("M").astype(str)
df["margin_value"] = df["revenue"] * df["base_margin_pct"]
df["delivery_days"] = (df["ship_date"] - df["order_date"]).dt.days

# ---- Save cleaned file ----
df.to_csv(CLEAN_PATH, index=False)

print(f"Rows before cleaning: (raw file)")
print(f"Rows after cleaning: {len(df):,}")
print(f"Date range: {df['order_date'].min().date()} to {df['order_date'].max().date()}")
print(f"Regions: {df['region'].nunique()} | Categories: {df['product_category'].nunique()} | Clients: {df['client_name'].nunique()}")
print(f"Saved cleaned data to {CLEAN_PATH}")
