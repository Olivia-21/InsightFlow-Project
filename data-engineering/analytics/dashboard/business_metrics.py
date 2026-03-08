"""
InsightFlow — Business Metrics
Carl Nyameakyere Crankson | Data Engineer B

All KPI computation logic lives here.
The dashboard imports these functions — keeping metrics separate from UI
makes it easy to unit-test and reuse in report generation.
"""

import pandas as pd
import numpy as np
from config import LOW_STOCK_THRESHOLD


# ── Data Loader ───────────────────────────────────────────────────────────────

def load_data_excel(excel_path: str) -> dict:
    """Load all warehouse tables from the sample Excel file."""
    sheets = ["fact_sales", "fact_feedback", "inventory",
              "dim_product", "dim_customer", "dim_store", "dim_date"]
    result = {}
    for s in sheets:
        df = pd.read_excel(excel_path, sheet_name=s)
        # Normalize column names (Excel headers are uppercase with spaces)
        df.columns = [c.lower().replace(" ", "_") for c in df.columns]
        result[s] = df
    return result


def load_data_postgres(host, port, db, user, password) -> dict:
    """Load all warehouse tables from the PostgreSQL warehouse (live pipeline)."""
    from sqlalchemy import create_engine
    engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{db}")
    tables = ["fact_sales", "fact_feedback", "inventory",
              "dim_product", "dim_customer", "dim_store", "dim_date"]
    return {t: pd.read_sql_table(t, engine) for t in tables}


def enrich_sales(data: dict) -> pd.DataFrame:
    """Join fact_sales with dimension tables for enriched analysis."""
    sales = data["fact_sales"].copy()
    stores   = data["dim_store"][["store_id","store_name","location","store_type"]].rename(columns={"location":"region"})
    products = data["dim_product"][["product_id","product_name","category","brand","unit_cost"]]
    customers= data["dim_customer"][["customer_id","customer_name","loyalty_tier"]]

    sales = (sales
             .merge(stores,    on="store_id",    how="left")
             .merge(products,  on="product_id",  how="left")
             .merge(customers, on="customer_id", how="left"))
    sales["transaction_date"] = pd.to_datetime(sales["transaction_date"])
    sales["profit"] = (
        (sales["unit_price"] - sales["unit_cost"]) * sales["quantity"]
        - sales["discount_applied"]
    )
    return sales


def enrich_feedback(data: dict) -> pd.DataFrame:
    """Join fact_feedback with dimension tables."""
    fb     = data["fact_feedback"].copy()
    stores = data["dim_store"][["store_id","location"]].rename(columns={"location":"region"})
    prods  = data["dim_product"][["product_id","product_name","category"]]
    fb = fb.merge(stores, on="store_id", how="left").merge(prods, on="product_id", how="left")
    fb["review_date"] = pd.to_datetime(fb["review_date"])
    return fb


def enrich_inventory(data: dict) -> pd.DataFrame:
    """Join inventory with dimensions."""
    inv    = data["inventory"].copy()
    stores = data["dim_store"][["store_id","store_name","location"]].rename(columns={"location":"region"})
    prods  = data["dim_product"][["product_id","product_name","category","brand","reorder_level"]]
    inv = inv.merge(stores, on="store_id", how="left").merge(prods, on="product_id", how="left")
    inv["stock_date"] = pd.to_datetime(inv["stock_date"])
    return inv


# ── KPI 1: Daily Revenue ──────────────────────────────────────────────────────

def kpi_daily_revenue(sales: pd.DataFrame, region: str = "All") -> pd.DataFrame:
    """
    Daily revenue aggregated across all regions (or filtered to one).
    Returns a DataFrame with columns: transaction_date, total_revenue, transaction_count.
    """
    df = sales.copy()
    if region != "All":
        df = df[df["region"] == region]
    result = (df.groupby("transaction_date")
                .agg(total_revenue=("total_amount","sum"),
                     transaction_count=("transaction_id","count"),
                     total_profit=("profit","sum"))
                .reset_index()
                .sort_values("transaction_date"))
    result["7d_avg"] = result["total_revenue"].rolling(7, min_periods=1).mean()
    return result


def kpi_revenue_summary(sales: pd.DataFrame, region: str = "All") -> dict:
    """Summary stats for the revenue KPI card."""
    df = sales.copy()
    if region != "All":
        df = df[df["region"] == region]

    total   = df["total_amount"].sum()
    profit  = df["profit"].sum()
    margin  = (profit / total * 100) if total > 0 else 0

    # Month-on-month change: compare last 30 days vs prior 30
    latest_date = df["transaction_date"].max()
    last30  = df[df["transaction_date"] >= latest_date - pd.Timedelta(days=30)]["total_amount"].sum()
    prior30 = df[(df["transaction_date"] >= latest_date - pd.Timedelta(days=60)) &
                 (df["transaction_date"] <  latest_date - pd.Timedelta(days=30))]["total_amount"].sum()
    mom_pct = ((last30 - prior30) / prior30 * 100) if prior30 > 0 else 0

    return {
        "total_revenue":      round(total, 2),
        "total_profit":       round(profit, 2),
        "profit_margin_pct":  round(margin, 1),
        "last_30d_revenue":   round(last30, 2),
        "mom_change_pct":     round(mom_pct, 1),
    }


# ── KPI 2: Top 5 Products ─────────────────────────────────────────────────────

def kpi_top_products(sales: pd.DataFrame, region: str = "All",
                     metric: str = "revenue", n: int = 5) -> pd.DataFrame:
    """
    Top N products by revenue or units sold.
    metric: "revenue" | "units"
    """
    df = sales.copy()
    if region != "All":
        df = df[df["region"] == region]

    result = (df.groupby(["product_id","product_name","category","brand"])
                .agg(total_revenue=("total_amount","sum"),
                     units_sold=("quantity","sum"),
                     transaction_count=("transaction_id","count"))
                .reset_index())
    sort_col = "total_revenue" if metric == "revenue" else "units_sold"
    return result.sort_values(sort_col, ascending=False).head(n).reset_index(drop=True)


def kpi_revenue_by_category(sales: pd.DataFrame, region: str = "All") -> pd.DataFrame:
    """Revenue breakdown by product category."""
    df = sales.copy()
    if region != "All":
        df = df[df["region"] == region]
    return (df.groupby("category")
              .agg(total_revenue=("total_amount","sum"),
                   units_sold=("quantity","sum"))
              .reset_index()
              .sort_values("total_revenue", ascending=False))


# ── KPI 3: Customer Satisfaction Score ───────────────────────────────────────

def kpi_satisfaction(feedback: pd.DataFrame, region: str = "All") -> dict:
    """
    Overall satisfaction KPI.
    Returns avg rating, distribution, and trend.
    """
    df = feedback.copy()
    if region != "All":
        df = df[df["region"] == region]

    avg_rating   = df["rating"].mean()
    total_reviews= len(df)
    pct_positive = (df["rating"] >= 4).sum() / total_reviews * 100 if total_reviews else 0
    return_rate  = df["is_return"].sum() / total_reviews * 100 if total_reviews else 0

    dist = df["rating"].value_counts().sort_index().reset_index()
    dist.columns = ["rating","count"]
    dist["label"] = dist["rating"].map({1:"★ Very Poor",2:"★★ Poor",
                                         3:"★★★ Average",4:"★★★★ Good",5:"★★★★★ Excellent"})
    return {
        "avg_rating":     round(avg_rating, 2),
        "total_reviews":  total_reviews,
        "pct_positive":   round(pct_positive, 1),
        "return_rate":    round(return_rate, 1),
        "distribution":   dist,
    }


def kpi_satisfaction_trend(feedback: pd.DataFrame, region: str = "All") -> pd.DataFrame:
    """Monthly average satisfaction score trend."""
    df = feedback.copy()
    if region != "All":
        df = df[df["region"] == region]
    df["month"] = df["review_date"].dt.to_period("M")
    return (df.groupby("month")
              .agg(avg_rating=("rating","mean"), review_count=("review_id","count"))
              .reset_index()
              .assign(month=lambda x: x["month"].astype(str)))


def kpi_satisfaction_by_category(feedback: pd.DataFrame, region: str = "All") -> pd.DataFrame:
    df = feedback.copy()
    if region != "All":
        df = df[df["region"] == region]
    return (df.groupby("category")
              .agg(avg_rating=("rating","mean"), review_count=("review_id","count"))
              .reset_index()
              .sort_values("avg_rating", ascending=False))


# ── KPI 4: Inventory Turnover ─────────────────────────────────────────────────

def kpi_inventory_turnover(inv: pd.DataFrame, region: str = "All") -> pd.DataFrame:
    """
    Inventory turnover per product.
    Turnover = Total Units Sold / Average Inventory Level
    Higher = selling through stock faster (good).
    """
    df = inv.copy()
    if region != "All":
        df = df[df["region"] == region]

    result = (df.groupby(["product_id","product_name","category","brand"])
                .agg(total_sold=("units_sold","sum"),
                     avg_stock=("closing_stock","mean"),
                     total_received=("units_received","sum"),
                     current_stock=("closing_stock","last"))
                .reset_index())
    result["turnover_rate"] = result.apply(
        lambda r: round(r["total_sold"] / r["avg_stock"], 2) if r["avg_stock"] > 0 else 0, axis=1)
    result["needs_reorder"] = result["current_stock"] < LOW_STOCK_THRESHOLD
    return result.sort_values("turnover_rate", ascending=False).reset_index(drop=True)


def kpi_low_stock_alerts(inv: pd.DataFrame, region: str = "All") -> pd.DataFrame:
    """Products currently below reorder threshold."""
    df = inv.copy()
    if region != "All":
        df = df[df["region"] == region]
    latest = df.sort_values("stock_date").groupby(["store_id","product_id"]).last().reset_index()
    # Ensure reorder_level column always exists
    if "reorder_level" not in latest.columns:
        latest["reorder_level"] = LOW_STOCK_THRESHOLD
    return latest[latest["closing_stock"] < LOW_STOCK_THRESHOLD].sort_values("closing_stock")


def kpi_stock_by_region(inv: pd.DataFrame) -> pd.DataFrame:
    """Current total stock level by region."""
    latest = inv.sort_values("stock_date").groupby(["store_id","product_id"]).last().reset_index()
    return (latest.groupby("region")
                  .agg(total_stock=("closing_stock","sum"),
                       low_stock_items=("needs_reorder","sum"))
                  .reset_index())


# ── KPI 5: Regional Comparison ────────────────────────────────────────────────

def kpi_regional_comparison(sales: pd.DataFrame, feedback: pd.DataFrame,
                              inv: pd.DataFrame) -> pd.DataFrame:
    """
    Side-by-side KPI summary for all three regions.
    """
    rev = (sales.groupby("region")
                .agg(total_revenue=("total_amount","sum"),
                     total_transactions=("transaction_id","count"),
                     total_units=("quantity","sum"))
                .reset_index())
    rev["avg_order_value"] = (rev["total_revenue"] / rev["total_transactions"]).round(2)

    sat = (feedback.groupby("region")
                   .agg(avg_satisfaction=("rating","mean"),
                        total_reviews=("review_id","count"))
                   .reset_index())
    sat["avg_satisfaction"] = sat["avg_satisfaction"].round(2)

    inv_latest = inv.sort_values("stock_date").groupby(["store_id","product_id"]).last().reset_index()
    stock = (inv_latest.groupby("region")
                       .agg(total_stock=("closing_stock","sum"))
                       .reset_index())

    result = rev.merge(sat, on="region", how="left").merge(stock, on="region", how="left")
    return result


def kpi_revenue_by_region_over_time(sales: pd.DataFrame) -> pd.DataFrame:
    """Weekly revenue by region — for the trend comparison chart."""
    df = sales.copy()
    df["week"] = df["transaction_date"].dt.to_period("W").dt.start_time
    return (df.groupby(["week","region"])
              .agg(total_revenue=("total_amount","sum"))
              .reset_index())


# ── Bonus KPI: Payment Method Analysis ───────────────────────────────────────

def kpi_payment_methods(sales: pd.DataFrame, region: str = "All") -> pd.DataFrame:
    df = sales.copy()
    if region != "All":
        df = df[df["region"] == region]
    return (df.groupby("payment_method")
              .agg(count=("transaction_id","count"),
                   total_revenue=("total_amount","sum"))
              .reset_index()
              .sort_values("count", ascending=False))
