# InsightFlow — Metrics Documentation
**Data Engineer B: Carl Nyameakyere Crankson**  
**Client: TCPR Ltd | Sprint 1 | Team 16**

---

## Overview

This document defines all KPI metrics displayed in the InsightFlow reporting dashboard. It covers the calculation methodology, data sources, refresh schedules, and thresholds for each metric.

---

## 1. Daily Revenue

**File:** `business_metrics.py → kpi_daily_revenue()` / `kpi_revenue_summary()`

| Attribute | Detail |
|---|---|
| **Definition** | Total revenue generated per day, aggregated across all three regions (Accra, Kumasi, Takoradi) |
| **Formula** | `SUM(total_amount)` per `transaction_date` |
| **Source table** | `fact_sales` |
| **Dimensions available** | Region, date, product category |
| **Supporting metric** | 7-day rolling average (smooths short-term volatility) |
| **Profit margin** | `(SUM(profit) / SUM(total_amount)) × 100` where `profit = (unit_price - unit_cost) × quantity - discount_applied` |
| **MoM change** | Compares last 30 days vs prior 30 days: `((last30 - prior30) / prior30) × 100` |
| **Refresh** | Every pipeline run (daily batch) |

---

## 2. Top 5 Products

**File:** `business_metrics.py → kpi_top_products()`

| Attribute | Detail |
|---|---|
| **Definition** | The five best-selling products ranked by either revenue contribution or units sold within the selected period |
| **Revenue formula** | `SUM(total_amount)` grouped by `product_id` |
| **Units formula** | `SUM(quantity)` grouped by `product_id` |
| **Source tables** | `fact_sales` + `dim_product` |
| **Ranking** | Togglable via dashboard filter — Revenue or Units Sold |
| **Dimensions available** | Region, product category |
| **Refresh** | Every pipeline run (daily batch) |

---

## 3. Customer Satisfaction Score

**File:** `business_metrics.py → kpi_satisfaction()` / `kpi_satisfaction_trend()`

| Attribute | Detail |
|---|---|
| **Definition** | Average customer satisfaction rating derived from weekly CSV review files, aggregated across all three regions |
| **Formula** | `MEAN(rating)` where rating is 1–5 |
| **Source table** | `fact_feedback` (ingested from weekly POS CSV files) |
| **Positive rate** | `(COUNT WHERE rating >= 4) / COUNT(total) × 100` |
| **Return rate** | `(COUNT WHERE is_return = TRUE) / COUNT(total) × 100` |
| **Target** | 4.0 / 5.0 (configurable in `config.py → SATISFACTION_TARGET`) |
| **Trend** | Monthly average tracked over time |
| **Dimensions available** | Region, product category |
| **Refresh** | Weekly (aligned with CSV ingestion schedule) |

---

## 4. Inventory Turnover

**File:** `business_metrics.py → kpi_inventory_turnover()` / `kpi_low_stock_alerts()`

| Attribute | Detail |
|---|---|
| **Definition** | Rate at which inventory is sold and replenished — higher rate indicates faster-moving stock |
| **Formula** | `SUM(units_sold) / MEAN(closing_stock)` per product |
| **Source tables** | `inventory` + `dim_product` + `dim_store` |
| **Low stock alert** | Flags any product where `closing_stock < reorder_level` (default: 20 units) |
| **Reorder threshold** | Configurable in `config.py → LOW_STOCK_THRESHOLD` |
| **Dimensions available** | Region, store, product |
| **Refresh** | Every pipeline run (daily batch) |

---

## 5. Regional Comparison

**File:** `business_metrics.py → kpi_regional_comparison()` / `kpi_revenue_by_region_over_time()`

| Attribute | Detail |
|---|---|
| **Definition** | Side-by-side performance metrics for Accra, Kumasi, and Takoradi |
| **Metrics compared** | Total revenue, transaction count, avg order value, avg satisfaction score, total stock |
| **Avg order value** | `SUM(total_amount) / COUNT(transaction_id)` per region |
| **Heatmap** | Transaction volume by region × day of week (identifies peak trading days per region) |
| **Payment methods** | Distribution of payment types across all regions |
| **Source tables** | `fact_sales` + `fact_feedback` + `inventory` + `dim_store` |
| **Refresh** | Every pipeline run (daily batch) |

---

## Data Source Mapping

| Dashboard Section | Primary Table | Joined With |
|---|---|---|
| Revenue | `fact_sales` | `dim_store`, `dim_product`, `dim_customer` |
| Top Products | `fact_sales` | `dim_product` |
| Satisfaction | `fact_feedback` | `dim_store`, `dim_product` |
| Inventory | `inventory` | `dim_store`, `dim_product` |
| Regional | All fact tables | All dimension tables |

---

## Switching from Sample Data to Live Warehouse

1. Open `dashboard/config.py`
2. Change `DATA_SOURCE = "excel"` → `DATA_SOURCE = "postgres"`
3. Update `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD` with the warehouse credentials from the team's `.env` file
4. Rebuild the Docker container: `docker-compose up --build dashboard`

---

## Dashboard Refresh & Caching

The dashboard uses `@st.cache_data(ttl=300)` — data is cached for 5 minutes. To force a refresh, use the browser's reload button or reduce the TTL value in `reporting_dashboard.py`.

---

## Configurable Parameters

All thresholds and labels are set in `dashboard/config.py`:

| Parameter | Default | Purpose |
|---|---|---|
| `CLIENT_NAME` | `"TCPR Ltd"` | Client branding in dashboard header |
| `SYSTEM_NAME` | `"InsightFlow"` | System name in header and tab title |
| `SATISFACTION_TARGET` | `4.0` | Target line on satisfaction gauge and trend chart |
| `LOW_STOCK_THRESHOLD` | `20` | Units below which a reorder alert is triggered |
| `REVENUE_TARGET_DAILY` | `5000.00` | Daily revenue target (GH₵) |
| `REGION_COLORS` | Orange/Navy/Green | Color assigned to each region in charts |
