# ─────────────────────────────────────────────────────────────────────────────
# InsightFlow — Dashboard Configuration
# Carl Nyameakyere Crankson | Data Engineer B
#
# SWITCHING FROM SAMPLE DATA TO LIVE PIPELINE:
#   1. Change DATA_SOURCE from "excel" to "postgres"
#   2. Fill in DB_* variables with the warehouse connection details
#   3. Delete or comment out EXCEL_PATH
# ─────────────────────────────────────────────────────────────────────────────

# ── Client / Branding ─────────────────────────────────────────────────────────
CLIENT_NAME   = "TCPR Ltd"          # ← Change client name here
SYSTEM_NAME   = "InsightFlow"
DASHBOARD_SUBTITLE = "Retail Business Intelligence Dashboard"
REGIONS       = ["Accra", "Kumasi", "Takoradi"]

# ── Data Source ───────────────────────────────────────────────────────────────
# Options: "excel" | "postgres"
DATA_SOURCE   = "excel"

# Excel path (temporary sample data — remove once pipeline is live)
EXCEL_PATH    = "data/insightflow_sample_data.xlsx"

# PostgreSQL Warehouse connection (used when DATA_SOURCE = "postgres")
DB_HOST       = "postgres-warehouse"   # Docker service name from docker-compose
DB_PORT       = 5433
DB_NAME       = "insightflow_warehouse"
DB_USER       = "warehouse_user"
DB_PASSWORD   = "warehouse_pass"       # Use env variable in production

# ── Brand Colors (from Amalitech / InsightFlow palette) ───────────────────────
COLOR_PRIMARY     = "#F47920"   # Orange
COLOR_SECONDARY   = "#1F4E79"   # Navy
COLOR_SUCCESS     = "#27AE60"   # Green
COLOR_WARNING     = "#E74C3C"   # Red
COLOR_NEUTRAL     = "#7F8C8D"   # Gray
COLOR_LIGHT_BG    = "#F8F9FA"   # Light background
COLOR_CHART_BG    = "#FFFFFF"

# Chart color palette (for multi-series charts)
CHART_PALETTE     = [
    "#F47920",  # Orange (primary)
    "#1F4E79",  # Navy
    "#27AE60",  # Green
    "#E74C3C",  # Red
    "#9B59B6",  # Purple
    "#2980B9",  # Blue
]

# Regional color map
REGION_COLORS = {
    "Accra":     "#F47920",
    "Kumasi":    "#1F4E79",
    "Takoradi":  "#27AE60",
}

# ── KPI Thresholds ────────────────────────────────────────────────────────────
SATISFACTION_TARGET   = 4.0      # Target avg rating out of 5
LOW_STOCK_THRESHOLD   = 20       # Units — flags reorder needed
REVENUE_TARGET_DAILY  = 5000.00  # Daily revenue target (GHS)
