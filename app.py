import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="Sales Analytics Dashboard", page_icon="📊", layout="wide")

st.title("📊 Real-Time Sales & Business Analytics")
st.caption("Upload a CSV to refresh the dashboard. The included sample data is synthetic and for demonstration only.")

REQUIRED = ["order_date", "order_id", "product", "category", "region", "quantity", "unit_price", "unit_cost"]

@st.cache_data
def load_sample():
    return pd.read_csv(Path(__file__).parent / "sample_sales.csv")

def prepare_data(df):
    df = df.copy()
    df.columns = [str(c).strip().lower().replace(" ", "_") for c in df.columns]
    missing = [c for c in REQUIRED if c not in df.columns]
    if missing:
        raise ValueError("Missing required columns: " + ", ".join(missing))
    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
    for col in ["quantity", "unit_price", "unit_cost"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df = df.dropna(subset=["order_date", "order_id", "product", "quantity", "unit_price", "unit_cost"])
    df = df[(df["quantity"] >= 0) & (df["unit_price"] >= 0) & (df["unit_cost"] >= 0)]
    df["revenue"] = df["quantity"] * df["unit_price"]
    df["cost"] = df["quantity"] * df["unit_cost"]
    df["profit"] = df["revenue"] - df["cost"]
    df["month"] = df["order_date"].dt.to_period("M").astype(str)
    return df

uploaded = st.sidebar.file_uploader("Upload sales CSV", type=["csv"])
st.sidebar.markdown("**Required columns**")
st.sidebar.code(", ".join(REQUIRED), language="text")
st.sidebar.caption("Tip: use the included sample_sales.csv format.")

try:
    raw = pd.read_csv(uploaded) if uploaded is not None else load_sample()
    df = prepare_data(raw)
except Exception as e:
    st.error(f"Could not load the data: {e}")
    st.stop()

if df.empty:
    st.warning("No valid rows found after cleaning.")
    st.stop()

st.sidebar.header("Filters")
min_date = df["order_date"].min().date()
max_date = df["order_date"].max().date()
date_range = st.sidebar.date_input("Order date range", value=(min_date, max_date), min_value=min_date, max_value=max_date)
regions = sorted(df["region"].dropna().unique().tolist())
selected_regions = st.sidebar.multiselect("Region", regions, default=regions)
categories = sorted(df["category"].dropna().unique().tolist())
selected_categories = st.sidebar.multiselect("Category", categories, default=categories)

filtered = df.copy()
if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
    start, end = pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1]) + pd.Timedelta(days=1) - pd.Timedelta(seconds=1)
    filtered = filtered[(filtered["order_date"] >= start) & (filtered["order_date"] <= end)]
if selected_regions:
    filtered = filtered[filtered["region"].isin(selected_regions)]
else:
    filtered = filtered.iloc[0:0]
if selected_categories:
    filtered = filtered[filtered["category"].isin(selected_categories)]
else:
    filtered = filtered.iloc[0:0]

if filtered.empty:
    st.warning("No rows match these filters. Update the filters in the sidebar.")
    st.stop()

revenue = filtered["revenue"].sum()
profit = filtered["profit"].sum()
orders = filtered["order_id"].nunique()
aov = revenue / orders if orders else 0
margin = (profit / revenue * 100) if revenue else 0

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Total Revenue", f"₹{revenue:,.0f}")
k2.metric("Total Profit", f"₹{profit:,.0f}")
k3.metric("Orders", f"{orders:,}")
k4.metric("Avg. Order Value", f"₹{aov:,.0f}")
k5.metric("Profit Margin", f"{margin:.1f}%")

left, right = st.columns(2)
with left:
    monthly = filtered.groupby("month", as_index=False).agg(revenue=("revenue", "sum"), profit=("profit", "sum"))
    fig = px.line(monthly, x="month", y=["revenue", "profit"], markers=True, title="Monthly Revenue & Profit")
    st.plotly_chart(fig, use_container_width=True)
with right:
    by_category = filtered.groupby("category", as_index=False).agg(revenue=("revenue", "sum"))
    fig = px.bar(by_category.sort_values("revenue", ascending=False), x="category", y="revenue", title="Revenue by Category", text_auto=".2s")
    st.plotly_chart(fig, use_container_width=True)

left, right = st.columns(2)
with left:
    by_product = filtered.groupby("product", as_index=False).agg(revenue=("revenue", "sum"), profit=("profit", "sum"))
    by_product = by_product.sort_values("revenue", ascending=False).head(10)
    fig = px.bar(by_product.sort_values("revenue"), x="revenue", y="product", orientation="h", title="Top 10 Products by Revenue")
    st.plotly_chart(fig, use_container_width=True)
with right:
    by_region = filtered.groupby("region", as_index=False).agg(revenue=("revenue", "sum"), profit=("profit", "sum"))
    fig = px.bar(by_region, x="region", y=["revenue", "profit"], barmode="group", title="Revenue & Profit by Region")
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Data quality & details")
c1, c2, c3 = st.columns(3)
c1.metric("Rows analysed", f"{len(filtered):,}")
c2.metric("Duplicate rows", f"{int(filtered.duplicated().sum()):,}")
c3.metric("Date range", f"{filtered['order_date'].min():%d %b %Y} – {filtered['order_date'].max():%d %b %Y}")

with st.expander("View cleaned data"):
    st.dataframe(filtered.sort_values("order_date", ascending=False), use_container_width=True)

csv_bytes = filtered.to_csv(index=False).encode("utf-8")
st.download_button("⬇️ Download filtered analysis CSV", data=csv_bytes, file_name="sales_analysis_export.csv", mime="text/csv")

st.markdown("---")
st.caption("Portfolio demo: sample records are synthetic. For actual business use, connect an authorized database/API and validate the data before making decisions.")
