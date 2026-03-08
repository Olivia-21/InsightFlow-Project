"""
InsightFlow — Reporting Dashboard  v3
Carl Nyameakyere Crankson | Data Engineer B
InsightFlow system · TCPR Ltd client
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys, os

sys.path.insert(0, os.path.dirname(__file__))
from config import (
    CLIENT_NAME, SYSTEM_NAME, REGIONS,
    DATA_SOURCE, EXCEL_PATH, COLOR_PRIMARY, COLOR_SECONDARY,
    COLOR_SUCCESS, COLOR_WARNING, COLOR_NEUTRAL, CHART_PALETTE,
    REGION_COLORS, SATISFACTION_TARGET,
    DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD
)
import business_metrics as bm

# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title=f"{CLIENT_NAME} | {SYSTEM_NAME}",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",   # starts closed — hamburger controls it
)

# ─────────────────────────────────────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
  html, body, [class*="css"] {{ font-family: 'Inter', 'Segoe UI', Arial, sans-serif; }}

  /* ── Hide Streamlit chrome ── */
  #MainMenu, footer, header {{ visibility: hidden; }}
  .block-container {{ padding-top: 0 !important; padding-bottom: 1rem !important; }}

  /* ── NAVBAR ── */
  .navbar {{
    background: linear-gradient(135deg, {COLOR_SECONDARY} 0%, #2563A8 60%, #1a3f6f 100%);
    padding: 0 20px;
    height: 58px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    position: sticky;
    top: 0;
    z-index: 999;
    box-shadow: 0 2px 12px rgba(31,78,121,0.25);
    margin-bottom: 0;
  }}

  .navbar-left {{
    display: flex;
    align-items: center;
    gap: 16px;
  }}

  /* Hamburger button — pure CSS, state managed by Streamlit sidebar */
  .hamburger {{
    display: flex;
    flex-direction: column;
    gap: 5px;
    cursor: pointer;
    padding: 6px;
    border-radius: 6px;
    transition: background 0.2s;
  }}
  .hamburger:hover {{ background: rgba(255,255,255,0.12); }}
  .hamburger span {{
    display: block;
    width: 22px;
    height: 2.5px;
    background: rgba(255,255,255,0.85);
    border-radius: 2px;
  }}

  .navbar-brand {{
    display: flex;
    flex-direction: column;
    line-height: 1.1;
  }}
  .brand-system {{
    font-size: 20px;
    font-weight: 800;
    color: white;
    letter-spacing: -0.3px;
  }}
  .brand-system span {{
    color: {COLOR_PRIMARY};
  }}
  .brand-powered {{
    font-size: 10px;
    color: rgba(255,255,255,0.5);
    letter-spacing: 0.3px;
    font-weight: 400;
  }}

  /* Navbar page tabs */
  .navbar-tabs {{
    display: flex;
    align-items: center;
    gap: 4px;
    height: 100%;
  }}
  .nav-tab {{
    color: rgba(255,255,255,0.65);
    font-size: 13px;
    font-weight: 500;
    padding: 6px 14px;
    border-radius: 6px;
    cursor: pointer;
    transition: all 0.18s;
    white-space: nowrap;
    text-decoration: none;
    border: none;
    background: transparent;
  }}
  .nav-tab:hover {{ color: white; background: rgba(255,255,255,0.10); }}
  .nav-tab.active {{
    color: white;
    background: {COLOR_PRIMARY};
    font-weight: 600;
  }}

  /* Navbar right: client badge + date */
  .navbar-right {{
    display: flex;
    align-items: center;
    gap: 12px;
  }}
  .client-badge {{
    background: rgba(255,255,255,0.12);
    border: 1px solid rgba(255,255,255,0.22);
    color: white;
    padding: 4px 14px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 0.3px;
  }}
  .client-label {{
    font-size: 9px;
    color: rgba(255,255,255,0.45);
    display: block;
    text-align: center;
    margin-top: 1px;
    text-transform: uppercase;
    letter-spacing: 0.4px;
  }}
  .nav-period {{
    color: rgba(255,255,255,0.55);
    font-size: 11px;
  }}

  /* ── FILTER BAR ── */
  .filterbar {{
    background: white;
    border-bottom: 1px solid #E8ECF0;
    padding: 10px 20px;
    display: flex;
    align-items: center;
    gap: 20px;
    margin-bottom: 20px;
    flex-wrap: wrap;
  }}
  .filter-label {{
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    color: {COLOR_NEUTRAL};
    margin-bottom: 2px;
  }}

  /* ── KPI CARDS ── */
  .kpi-row {{ display: flex; gap: 14px; margin-bottom: 22px; }}
  .kpi {{
    flex: 1;
    background: white;
    border-radius: 12px;
    padding: 18px 20px;
    border-left: 4px solid {COLOR_PRIMARY};
    box-shadow: 0 1px 8px rgba(0,0,0,0.07);
    min-width: 0;
  }}
  .kpi.green  {{ border-left-color: {COLOR_SUCCESS}; }}
  .kpi.navy   {{ border-left-color: {COLOR_SECONDARY}; }}
  .kpi.purple {{ border-left-color: #8E44AD; }}
  .kpi.amber  {{ border-left-color: #E67E22; }}

  .kpi-label {{
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.6px;
    color: {COLOR_NEUTRAL};
    margin-bottom: 7px;
  }}
  .kpi-value {{
    font-size: 28px;
    font-weight: 800;
    color: {COLOR_SECONDARY};
    line-height: 1.1;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }}
  .kpi-up   {{ color: {COLOR_SUCCESS}; font-size: 13px; margin-top: 5px; font-weight: 600; }}
  .kpi-down {{ color: {COLOR_WARNING}; font-size: 13px; margin-top: 5px; font-weight: 600; }}
  .kpi-sub  {{ color: #888; font-size: 12px; margin-top: 4px; }}

  /* ── Section header ── */
  .sec-hdr {{
    font-size: 13px;
    font-weight: 700;
    color: {COLOR_SECONDARY};
    text-transform: uppercase;
    letter-spacing: 0.8px;
    padding-bottom: 8px;
    border-bottom: 2px solid {COLOR_PRIMARY};
    margin: 6px 0 18px 0;
  }}

  /* ── Alert boxes ── */
  .alert-warn {{
    background: #FFF8E1; border-left: 4px solid #FFC107;
    border-radius: 8px; padding: 11px 16px;
    font-size: 13px; color: #7A5E00; margin-bottom: 14px;
  }}
  .alert-ok {{
    background: #E8F8F0; border-left: 4px solid {COLOR_SUCCESS};
    border-radius: 8px; padding: 11px 16px;
    font-size: 13px; color: #1A6B3C; margin-bottom: 14px;
  }}

  /* ── Sidebar ── */
  section[data-testid="stSidebar"] {{
    background: #F4F6F9;
    padding-top: 10px;
  }}
  .sb-info {{ font-size: 12px; color: #777; line-height: 2; margin-top: 10px; }}

  /* ── Streamlit widget label tweaks ── */
  label {{ font-size: 12px !important; font-weight: 600 !important; color: {COLOR_SECONDARY} !important; }}
  .stSelectbox div[data-baseweb="select"] {{ font-size: 13px; }}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# Data
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data(ttl=300)
def load_all():
    if DATA_SOURCE == "postgres":
        raw = bm.load_data_postgres(DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD)
    else:
        base = os.path.dirname(os.path.dirname(__file__))
        raw  = bm.load_data_excel(os.path.join(base, EXCEL_PATH))
    return bm.enrich_sales(raw), bm.enrich_feedback(raw), bm.enrich_inventory(raw)


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────
def fmt(v):
    if v >= 1_000_000: return f"GH₵ {v/1_000_000:.2f}M"
    if v >= 1_000:     return f"GH₵ {v/1_000:.1f}K"
    return f"GH₵ {v:,.0f}"

def fmt_short(v):
    if v >= 1_000_000: return f"GH₵{v/1_000_000:.1f}M"
    if v >= 1_000:     return f"GH₵{v/1_000:.0f}K"
    return f"GH₵{v:,.0f}"

BASE = dict(
    plot_bgcolor="white", paper_bgcolor="white",
    font=dict(family="Inter, Arial", color="#222", size=13),
    margin=dict(l=12, r=12, t=42, b=12),
    hoverlabel=dict(bgcolor="white", font_size=13, bordercolor="#DDD"),
)

def ch(fig, h=320):
    fig.update_layout(height=h, **BASE)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


# ─────────────────────────────────────────────────────────────────────────────
# Sidebar  (open/close via hamburger — Streamlit handles the toggle natively)
# ─────────────────────────────────────────────────────────────────────────────
def render_sidebar(sales, feedback):
    with st.sidebar:
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,{COLOR_SECONDARY},{COLOR_PRIMARY});
                    color:white;padding:14px 16px;border-radius:10px;margin-bottom:18px">
          <div style="font-size:18px;font-weight:800">{SYSTEM_NAME}</div>
          <div style="font-size:10px;opacity:.65;margin-top:2px">
            Powered by InsightFlow · Client: {CLIENT_NAME}
          </div>
        </div>""", unsafe_allow_html=True)

        st.markdown(f"""
        <div class="sb-info">
          <b>Data source:</b> {DATA_SOURCE.upper()}<br>
          <b>Transactions:</b> {len(sales):,}<br>
          <b>Reviews:</b> {len(feedback):,}
        </div>""", unsafe_allow_html=True)

        st.markdown("---")
        if DATA_SOURCE == "excel":
            st.info("📁 Sample data active.\n\nSwitch `DATA_SOURCE='postgres'` in `config.py` when pipeline is live.")

        st.markdown("---")
        st.caption("InsightFlow v1.0 · Team 16 · Sprint 1")


# ─────────────────────────────────────────────────────────────────────────────
# Navbar  (gradient + hamburger + page tabs + client badge)
# ─────────────────────────────────────────────────────────────────────────────
PAGE_LABELS = ["Revenue", "Top Products", "Satisfaction", "Inventory", "Regional"]

def render_navbar(active_page, period_str):
    tabs_html = "".join([
        f'<span class="nav-tab{" active" if lbl==active_page else ""}">{lbl}</span>'
        for lbl in PAGE_LABELS
    ])
    st.markdown(f"""
    <div class="navbar">
      <div class="navbar-left">
        <div class="hamburger" title="Toggle sidebar">
          <span></span><span></span><span></span>
        </div>
        <div class="navbar-brand">
          <span class="brand-system">Insight<span>Flow</span></span>
          <span class="brand-powered">Retail Intelligence Platform</span>
        </div>
        <div class="navbar-tabs">{tabs_html}</div>
      </div>
      <div class="navbar-right">
        <span class="nav-period">{period_str}</span>
        <div>
          <span class="client-badge">{CLIENT_NAME}</span>
          <span class="client-label">Active Client</span>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# Filter bar  (lives on main page, below navbar)
# ─────────────────────────────────────────────────────────────────────────────
def render_filters(sales, feedback):
    min_d = sales["transaction_date"].min().date()
    max_d = sales["transaction_date"].max().date()

    # Render with Streamlit widgets in columns (styled to look like a bar)
    st.markdown('<div style="background:white;border-bottom:1px solid #E8ECF0;'
                'padding:4px 0 10px 0;margin-bottom:18px">', unsafe_allow_html=True)

    fc1, fc2, fc3, fc4, fc5 = st.columns([2, 1.2, 1.4, 1.4, 0.8])
    with fc1:
        dr = st.date_input("📅 Date Range", value=(min_d, max_d),
                           min_value=min_d, max_value=max_d, label_visibility="visible")
    with fc2:
        region = st.selectbox("🌍 Region", ["All"] + REGIONS)
    with fc3:
        cats = ["All"] + sorted(sales["category"].dropna().unique())
        category = st.selectbox("📦 Product Category", cats)
    with fc4:
        rank_by = st.radio("🏆 Rank Top Products by",
                           ["Revenue", "Units Sold"], horizontal=True)
    with fc5:
        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
        if DATA_SOURCE == "excel":
            st.caption("📁 Sample data")

    st.markdown('</div>', unsafe_allow_html=True)
    return dr, region, category, rank_by


# ─────────────────────────────────────────────────────────────────────────────
# KPI Strip
# ─────────────────────────────────────────────────────────────────────────────
def kpi_strip(sales, feedback, inv, region):
    rev    = bm.kpi_revenue_summary(sales, region)
    sat    = bm.kpi_satisfaction(feedback, region)
    turn   = bm.kpi_inventory_turnover(inv, region)
    alerts = bm.kpi_low_stock_alerts(inv, region)
    top1   = bm.kpi_top_products(sales, region, "revenue", 1)

    mom      = rev["mom_change_pct"]
    mom_cls  = "kpi-up" if mom >= 0 else "kpi-down"
    mom_icon = "▲" if mom >= 0 else "▼"
    avg_t    = round(turn["turnover_rate"].mean(), 1)
    top_name = top1.iloc[0]["product_name"] if len(top1) else "—"
    top_rev  = fmt(top1.iloc[0]["total_revenue"]) if len(top1) else "—"
    n_alerts = len(alerts)
    a_color  = COLOR_WARNING if n_alerts > 0 else COLOR_SUCCESS
    sat_cls  = "kpi-up" if sat["avg_rating"] >= SATISFACTION_TARGET else "kpi-down"

    c1,c2,c3,c4,c5 = st.columns(5)
    with c1:
        st.markdown(f"""<div class="kpi">
          <div class="kpi-label">Total Revenue</div>
          <div class="kpi-value">{fmt(rev['total_revenue'])}</div>
          <div class="{mom_cls}">{mom_icon} {abs(mom):.1f}% vs prior 30d</div>
          <div class="kpi-sub">Profit margin: {rev['profit_margin_pct']}%</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="kpi green">
          <div class="kpi-label">Satisfaction Score</div>
          <div class="kpi-value">{sat['avg_rating']} / 5</div>
          <div class="{sat_cls}">{'▲' if sat['avg_rating']>=SATISFACTION_TARGET else '▼'} {sat['pct_positive']}% positive</div>
          <div class="kpi-sub">{sat['total_reviews']:,} reviews · {sat['return_rate']}% returns</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class="kpi navy">
          <div class="kpi-label">Avg Inventory Turnover</div>
          <div class="kpi-value">{avg_t}x</div>
          <div class="kpi-up">Across {len(turn)} products</div>
          <div class="kpi-sub">Best: {turn.iloc[0]['turnover_rate']}x</div>
        </div>""", unsafe_allow_html=True)
    with c4:
        st.markdown(f"""<div class="kpi purple">
          <div class="kpi-label">Top Product</div>
          <div class="kpi-value" style="font-size:18px;line-height:1.3">{top_name}</div>
          <div class="kpi-up">{top_rev}</div>
          <div class="kpi-sub">By revenue · {region}</div>
        </div>""", unsafe_allow_html=True)
    with c5:
        st.markdown(f"""<div class="kpi amber">
          <div class="kpi-label">Low Stock Alerts</div>
          <div class="kpi-value" style="color:{a_color}">{n_alerts}</div>
          <div class="{'kpi-down' if n_alerts>0 else 'kpi-up'}">
            {'Below reorder level' if n_alerts>0 else 'All stock healthy'}
          </div>
          <div class="kpi-sub">Threshold: 20 units</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<div style='margin-bottom:10px'></div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# Tab 1: Revenue
# ─────────────────────────────────────────────────────────────────────────────
def tab_revenue(sales, region):
    st.markdown('<div class="sec-hdr">Revenue Analysis</div>', unsafe_allow_html=True)
    daily  = bm.kpi_daily_revenue(sales, region)
    by_cat = bm.kpi_revenue_by_category(sales, region)
    weekly = bm.kpi_revenue_by_region_over_time(sales)

    # Row 1: trend line + donut
    c1, c2 = st.columns([2.2, 1])
    with c1:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=daily["transaction_date"], y=daily["total_revenue"],
            name="Daily Revenue",
            line=dict(color=COLOR_PRIMARY, width=2.5),
            fill="tozeroy", fillcolor="rgba(244,121,32,0.10)",
            # Show money labels on every 7th data point to avoid clutter
            text=[fmt_short(v) if i % 7 == 0 else "" for i, v in enumerate(daily["total_revenue"])],
            textposition="top center",
            textfont=dict(size=10, color=COLOR_PRIMARY),
            mode="lines+text",
            hovertemplate="<b>%{x|%b %d}</b><br>Revenue: <b>GH₵ %{y:,.0f}</b><extra></extra>"
        ))
        fig.add_trace(go.Scatter(
            x=daily["transaction_date"], y=daily["7d_avg"],
            name="7-Day Avg",
            line=dict(color=COLOR_SECONDARY, width=2, dash="dot"),
            mode="lines",
            hovertemplate="<b>%{x|%b %d}</b><br>7-Day Avg: <b>GH₵ %{y:,.0f}</b><extra></extra>"
        ))
        fig.update_layout(
            title=dict(text="Daily Revenue with 7-Day Moving Average", font=dict(size=15, color=COLOR_SECONDARY)),
            yaxis=dict(title="GH₵", tickformat=",.0f", gridcolor="#F0F0F0"),
            xaxis=dict(title="", gridcolor="#F8F8F8"),
            # Legend ABOVE the chart — not inside it
            legend=dict(
                orientation="h",
                yanchor="bottom", y=1.08,
                xanchor="left", x=0,
                bgcolor="rgba(0,0,0,0)",
                font=dict(size=12)
            )
        )
        ch(fig, 320)

    with c2:
        # Donut — group small slices to avoid label crowding
        by_cat_sorted = by_cat.sort_values("total_revenue", ascending=False).copy()
        threshold     = by_cat_sorted["total_revenue"].sum() * 0.04  # <4% = "Other"
        major = by_cat_sorted[by_cat_sorted["total_revenue"] >= threshold]
        minor = by_cat_sorted[by_cat_sorted["total_revenue"] < threshold]

        if len(minor) > 1:
            other_row = pd.DataFrame([{
                "category": f"Other ({len(minor)})",
                "total_revenue": minor["total_revenue"].sum(),
                "units_sold": minor["units_sold"].sum()
            }])
            donut_df = pd.concat([major, other_row], ignore_index=True)
        else:
            donut_df = major

        fig2 = px.pie(
            donut_df, values="total_revenue", names="category",
            title="Revenue by Category",
            color_discrete_sequence=CHART_PALETTE,
            hole=0.44
        )
        fig2.update_traces(
            textposition="outside",
            textinfo="label+percent",
            textfont_size=12,
            pull=[0.04] * len(donut_df),     # slight pull for clarity
            hovertemplate="<b>%{label}</b><br>%{percent}<br><b>GH₵ %{value:,.0f}</b><extra></extra>"
        )
        fig2.update_layout(
            showlegend=False,
            title=dict(font=dict(size=15, color=COLOR_SECONDARY)),
            margin=dict(l=20, r=20, t=42, b=20)
        )
        ch(fig2, 320)

    # Row 2: regional weekly area (only when All regions selected)
    if region == "All":
        st.markdown('<div class="sec-hdr">Weekly Revenue by Region</div>', unsafe_allow_html=True)
        fig3 = px.area(
            weekly, x="week", y="total_revenue", color="region",
            color_discrete_map=REGION_COLORS,
            title="Weekly Revenue — Accra · Kumasi · Takoradi",
            labels={"total_revenue": "GH₵", "week": ""},
            hover_data={"total_revenue": ":,.0f"}
        )
        fig3.update_traces(hovertemplate="<b>%{x|%b %d}</b><br>Revenue: <b>GH₵ %{y:,.0f}</b><extra></extra>")
        fig3.update_layout(
            yaxis=dict(title="GH₵", tickformat=",.0f", gridcolor="#F0F0F0"),
            legend=dict(orientation="h", yanchor="bottom", y=1.08, xanchor="left", x=0,
                        font=dict(size=12), bgcolor="rgba(0,0,0,0)")
        )
        ch(fig3, 280)

    # Row 3: category bar + payment methods
    c3, c4 = st.columns(2)
    with c3:
        fig4 = px.bar(
            by_cat.sort_values("total_revenue"),
            x="total_revenue", y="category", orientation="h",
            title="Revenue by Product Category",
            color="total_revenue",
            color_continuous_scale=["#BDD7EE", COLOR_SECONDARY],
            text=[fmt_short(v) for v in by_cat.sort_values("total_revenue")["total_revenue"]]
        )
        fig4.update_traces(textposition="outside", textfont_size=12)
        fig4.update_layout(
            coloraxis_showscale=False,
            xaxis=dict(title="GH₵", tickformat=",.0f"),
            yaxis_title="",
            title=dict(font=dict(size=14, color=COLOR_SECONDARY))
        )
        ch(fig4, 280)

    with c4:
        pay = bm.kpi_payment_methods(sales, region)
        fig5 = px.bar(
            pay, x="payment_method", y="count",
            title="Transactions by Payment Method",
            color="payment_method",
            color_discrete_sequence=CHART_PALETTE,
            text="count"
        )
        fig5.update_traces(textposition="outside", textfont_size=12)
        fig5.update_layout(
            showlegend=False,
            xaxis_title="",
            yaxis=dict(title="Transactions", gridcolor="#F0F0F0"),
            title=dict(font=dict(size=14, color=COLOR_SECONDARY))
        )
        ch(fig5, 280)


# ─────────────────────────────────────────────────────────────────────────────
# Tab 2: Top Products
# ─────────────────────────────────────────────────────────────────────────────
def tab_products(sales, region, category, rank_by):
    st.markdown('<div class="sec-hdr">Product Performance</div>', unsafe_allow_html=True)
    df = sales.copy()
    if category != "All":
        df = df[df["category"] == category]

    metric = "revenue" if rank_by == "Revenue" else "units"
    top5   = bm.kpi_top_products(df, region, metric, 5)
    top15  = bm.kpi_top_products(df, region, metric, 15)

    c1, c2 = st.columns(2)
    with c1:
        # Mirrored dual bar — revenue (navy) + units scaled (orange)
        scale = top5["total_revenue"].max() / max(top5["units_sold"].max(), 1)
        fig = go.Figure()
        fig.add_trace(go.Bar(
            name="Revenue (GH₵)", y=top5["product_name"], x=top5["total_revenue"],
            orientation="h", marker_color=COLOR_SECONDARY,
            text=[fmt_short(v) for v in top5["total_revenue"]],
            textposition="inside", insidetextanchor="end",
            textfont=dict(color="white", size=11),
            hovertemplate="<b>%{y}</b><br>Revenue: <b>GH₵ %{x:,.0f}</b><extra></extra>"
        ))
        fig.add_trace(go.Bar(
            name="Units Sold", y=top5["product_name"],
            x=top5["units_sold"] * scale,
            orientation="h", marker_color=f"rgba(244,121,32,0.75)",
            text=[f"{int(v)} units" for v in top5["units_sold"]],
            textposition="inside", insidetextanchor="end",
            textfont=dict(color="white", size=11),
            hovertemplate="<b>%{y}</b><br>Units: <b>%{text}</b><extra></extra>"
        ))
        fig.update_layout(
            title=dict(text="Top 5 Products — Revenue & Units", font=dict(size=14, color=COLOR_SECONDARY)),
            barmode="overlay",
            yaxis=dict(autorange="reversed", title=""),
            xaxis=dict(title="Revenue (GH₵)", tickformat=",.0f"),
            legend=dict(orientation="h", y=1.12, x=0, bgcolor="rgba(0,0,0,0)", font=dict(size=12))
        )
        ch(fig, 300)

    with c2:
        fig2 = px.scatter(
            top15, x="units_sold", y="total_revenue",
            size="transaction_count", color="category",
            text="product_name",
            title="Revenue vs Units Sold  (bubble = transaction count)",
            color_discrete_sequence=CHART_PALETTE,
            hover_data={"total_revenue": ":,.0f", "units_sold": True}
        )
        fig2.update_traces(
            textposition="top center", textfont_size=10,
            hovertemplate="<b>%{text}</b><br>Revenue: GH₵ %{y:,.0f}<br>Units: %{x}<extra></extra>"
        )
        fig2.update_layout(
            xaxis_title="Units Sold",
            yaxis=dict(title="Revenue (GH₵)", tickformat=",.0f"),
            legend=dict(orientation="h", y=1.12, x=0, bgcolor="rgba(0,0,0,0)", font=dict(size=12)),
            title=dict(font=dict(size=14, color=COLOR_SECONDARY))
        )
        ch(fig2, 300)

    c3, c4 = st.columns(2)
    with c3:
        cat_perf = bm.kpi_revenue_by_category(df, region)
        fig3 = px.bar(
            cat_perf, x="category", y=["total_revenue","units_sold"],
            barmode="group", title="Revenue & Units by Category",
            color_discrete_sequence=[COLOR_SECONDARY, COLOR_PRIMARY],
            labels={"value":"Value","variable":""}
        )
        fig3.update_layout(
            xaxis_title="", yaxis_title="Value",
            legend=dict(orientation="h", y=1.12, x=0, bgcolor="rgba(0,0,0,0)", font=dict(size=12)),
            title=dict(font=dict(size=14, color=COLOR_SECONDARY))
        )
        ch(fig3, 270)
    with c4:
        brand_perf = (df.groupby("brand")
                        .agg(total_revenue=("total_amount","sum"))
                        .reset_index()
                        .sort_values("total_revenue", ascending=False).head(8))
        fig4 = px.bar(
            brand_perf.sort_values("total_revenue"),
            x="total_revenue", y="brand", orientation="h",
            title="Top Brands by Revenue",
            color="total_revenue",
            color_continuous_scale=["#BDD7EE", COLOR_SECONDARY],
            text=[fmt_short(v) for v in brand_perf.sort_values("total_revenue")["total_revenue"]]
        )
        fig4.update_traces(textposition="outside", textfont_size=11)
        fig4.update_layout(
            coloraxis_showscale=False,
            xaxis=dict(title="GH₵", tickformat=",.0f"),
            yaxis_title="",
            title=dict(font=dict(size=14, color=COLOR_SECONDARY))
        )
        ch(fig4, 270)

    with st.expander("📋 Full Product Performance Table"):
        tbl = top15[["product_name","category","brand",
                      "total_revenue","units_sold","transaction_count"]].copy()
        tbl.columns = ["Product","Category","Brand","Revenue (GH₵)","Units Sold","Transactions"]
        tbl["Revenue (GH₵)"] = tbl["Revenue (GH₵)"].map(lambda x: f"GH₵ {x:,.2f}")
        st.dataframe(tbl, use_container_width=True, hide_index=True)


# ─────────────────────────────────────────────────────────────────────────────
# Tab 3: Satisfaction
# ─────────────────────────────────────────────────────────────────────────────
def tab_satisfaction(feedback, region):
    st.markdown('<div class="sec-hdr">Customer Satisfaction</div>', unsafe_allow_html=True)
    sat    = bm.kpi_satisfaction(feedback, region)
    trend  = bm.kpi_satisfaction_trend(feedback, region)
    by_cat = bm.kpi_satisfaction_by_category(feedback, region)
    dist   = sat["distribution"]

    c1, c2, c3 = st.columns([1, 1.4, 1.6])
    with c1:
        color   = COLOR_SUCCESS if sat["avg_rating"] >= SATISFACTION_TARGET else COLOR_WARNING
        pct_bar = int((sat["avg_rating"] / 5) * 100)
        st.markdown(f"""
        <div style="background:white;border-radius:12px;padding:28px 22px;
                    box-shadow:0 1px 8px rgba(0,0,0,.07);text-align:center">
          <div style="font-size:11px;font-weight:700;text-transform:uppercase;
                      letter-spacing:.7px;color:{COLOR_NEUTRAL};margin-bottom:12px">
            Overall Score
          </div>
          <div style="font-size:62px;font-weight:800;color:{color};line-height:1">
            {sat['avg_rating']}
          </div>
          <div style="font-size:15px;color:{COLOR_NEUTRAL};margin:6px 0 16px 0">out of 5.0</div>
          <div style="background:#EEE;border-radius:6px;height:9px;overflow:hidden;margin-bottom:18px">
            <div style="background:linear-gradient(90deg,{color},{COLOR_PRIMARY});
                        width:{pct_bar}%;height:9px;border-radius:6px"></div>
          </div>
          <div style="display:flex;justify-content:space-around;font-size:13px">
            <div><b style="font-size:18px;color:{COLOR_SECONDARY}">{sat['total_reviews']:,}</b><br>
                 <span style="color:#999">Reviews</span></div>
            <div><b style="font-size:18px;color:{COLOR_SUCCESS}">{sat['pct_positive']}%</b><br>
                 <span style="color:#999">Positive</span></div>
            <div><b style="font-size:18px;color:{COLOR_WARNING}">{sat['return_rate']}%</b><br>
                 <span style="color:#999">Returns</span></div>
          </div>
        </div>""", unsafe_allow_html=True)

    with c2:
        colors_map = {1:"#E74C3C",2:"#E67E22",3:"#F1C40F",4:"#2ECC71",5:"#27AE60"}
        fig = go.Figure(go.Bar(
            x=dist["label"], y=dist["count"],
            marker_color=[colors_map[r] for r in dist["rating"]],
            text=dist["count"], textposition="outside",
            textfont=dict(size=13)
        ))
        fig.update_layout(
            title=dict(text="Rating Distribution", font=dict(size=14, color=COLOR_SECONDARY)),
            xaxis_title="", yaxis=dict(title="Reviews", gridcolor="#F0F0F0"),
            showlegend=False
        )
        ch(fig, 300)

    with c3:
        fig2 = px.bar(
            by_cat.sort_values("avg_rating"),
            x="avg_rating", y="category", orientation="h",
            title="Avg Rating by Product Category",
            color="avg_rating",
            color_continuous_scale=["#E74C3C","#F1C40F","#27AE60"],
            range_color=[1,5],
            text=[f"{v:.2f} ★" for v in by_cat.sort_values("avg_rating")["avg_rating"]]
        )
        fig2.add_vline(x=SATISFACTION_TARGET, line_dash="dash",
                       line_color=COLOR_SECONDARY, line_width=1.5,
                       annotation_text=f"Target {SATISFACTION_TARGET}",
                       annotation_position="top right",
                       annotation_font_size=12)
        fig2.update_traces(textposition="outside", textfont_size=12)
        fig2.update_layout(
            xaxis=dict(range=[0,5.8], title="Avg Rating"),
            yaxis_title="", coloraxis_showscale=False,
            title=dict(font=dict(size=14, color=COLOR_SECONDARY))
        )
        ch(fig2, 300)

    if len(trend) > 1:
        st.markdown('<div class="sec-hdr">Satisfaction Trend Over Time</div>', unsafe_allow_html=True)
        fig3 = go.Figure()
        fig3.add_trace(go.Bar(
            x=trend["month"], y=trend["review_count"], name="Review Count",
            marker_color="rgba(31,78,121,0.12)", yaxis="y2"
        ))
        fig3.add_trace(go.Scatter(
            x=trend["month"], y=trend["avg_rating"], name="Avg Rating",
            mode="lines+markers+text",
            line=dict(color=COLOR_SUCCESS, width=2.5),
            marker=dict(size=8),
            text=[f"{v:.2f}" for v in trend["avg_rating"]],
            textposition="top center",
            textfont=dict(size=11, color=COLOR_SUCCESS),
            hovertemplate="<b>%{x}</b><br>Avg Rating: <b>%{y:.2f}</b><extra></extra>"
        ))
        fig3.add_hline(y=SATISFACTION_TARGET, line_dash="dash",
                       line_color=COLOR_WARNING, line_width=1.5,
                       annotation_text=f"Target {SATISFACTION_TARGET}",
                       annotation_font_size=12)
        fig3.update_layout(
            title=dict(text="Monthly Satisfaction Score & Review Volume",
                       font=dict(size=14, color=COLOR_SECONDARY)),
            yaxis=dict(title="Avg Rating", range=[0,5.5], side="left", gridcolor="#F0F0F0"),
            yaxis2=dict(title="Review Count", overlaying="y", side="right"),
            xaxis_title="",
            legend=dict(orientation="h", y=1.12, x=0, bgcolor="rgba(0,0,0,0)", font=dict(size=12))
        )
        ch(fig3, 290)


# ─────────────────────────────────────────────────────────────────────────────
# Tab 4: Inventory
# ─────────────────────────────────────────────────────────────────────────────
def tab_inventory(inv, region):
    st.markdown('<div class="sec-hdr">Inventory Turnover</div>', unsafe_allow_html=True)
    turnover  = bm.kpi_inventory_turnover(inv, region)
    alerts    = bm.kpi_low_stock_alerts(inv, region)
    by_region = bm.kpi_stock_by_region(inv)
    n = len(alerts)

    if n > 0:
        st.markdown(f'<div class="alert-warn">⚠️  <b>{n} items</b> are below the reorder threshold of 20 units — see detail table below.</div>',
                    unsafe_allow_html=True)
    else:
        st.markdown('<div class="alert-ok">✅  All products are above reorder thresholds.</div>',
                    unsafe_allow_html=True)

    c1, c2 = st.columns([1.6, 1])
    with c1:
        top10   = turnover.head(10)
        c_turns = [COLOR_WARNING if r else COLOR_SUCCESS for r in top10["needs_reorder"]]
        fig = go.Figure(go.Bar(
            y=top10["product_name"], x=top10["turnover_rate"],
            orientation="h", marker_color=c_turns,
            text=[f"{v:.1f}x" for v in top10["turnover_rate"]],
            textposition="outside", textfont=dict(size=12)
        ))
        fig.update_layout(
            title=dict(text="Inventory Turnover Rate — Top 10 Products",
                       font=dict(size=14, color=COLOR_SECONDARY)),
            xaxis=dict(title="Turnover Rate", gridcolor="#F0F0F0"),
            yaxis=dict(autorange="reversed", title=""),
            annotations=[dict(x=0.99, y=-0.10, xref="paper", yref="paper", showarrow=False,
                              text="🟢 Stock OK     🟠 Needs Reorder",
                              font=dict(size=11, color=COLOR_NEUTRAL), xanchor="right")]
        )
        ch(fig, 360)
    with c2:
        fig2 = px.bar(
            by_region, x="region",
            y=["total_stock","low_stock_items"], barmode="group",
            title="Stock Levels by Region",
            color_discrete_map={"total_stock":COLOR_SECONDARY,"low_stock_items":COLOR_WARNING},
            labels={"value":"Units","variable":""}
        )
        fig2.update_layout(
            xaxis_title="", yaxis=dict(title="Units", gridcolor="#F0F0F0"),
            legend=dict(orientation="h", y=1.12, x=0, bgcolor="rgba(0,0,0,0)", font=dict(size=12)),
            title=dict(font=dict(size=14, color=COLOR_SECONDARY))
        )
        ch(fig2, 360)

    if n > 0:
        st.markdown('<div class="sec-hdr">Low Stock Detail</div>', unsafe_allow_html=True)
        available = [c for c in ["region","store_id","product_name","category",
                                  "closing_stock","reorder_level"] if c in alerts.columns]
        tbl = alerts[available].copy()
        col_rename = {"region":"Region","store_id":"Store","product_name":"Product",
                      "category":"Category","closing_stock":"Current Stock",
                      "reorder_level":"Reorder Level"}
        tbl.columns = [col_rename.get(c,c) for c in tbl.columns]
        st.dataframe(tbl.sort_values("Current Stock"), use_container_width=True, hide_index=True)

    with st.expander("📋 Full Inventory Turnover Table"):
        disp = turnover[["product_name","category","brand","turnover_rate",
                          "total_sold","avg_stock","current_stock","needs_reorder"]].copy()
        disp.columns = ["Product","Category","Brand","Turnover Rate",
                        "Total Sold","Avg Stock","Current Stock","Needs Reorder"]
        st.dataframe(disp, use_container_width=True, hide_index=True)


# ─────────────────────────────────────────────────────────────────────────────
# Tab 5: Regional
# ─────────────────────────────────────────────────────────────────────────────
def tab_regional(sales, feedback, inv):
    st.markdown('<div class="sec-hdr">Regional Comparison — Accra · Kumasi · Takoradi</div>',
                unsafe_allow_html=True)
    comp = bm.kpi_regional_comparison(sales, feedback, inv)

    c1, c2 = st.columns(2)
    with c1:
        fig = px.bar(
            comp, x="region", y="total_revenue",
            title="Total Revenue by Region",
            color="region", color_discrete_map=REGION_COLORS,
            text=[fmt(v) for v in comp["total_revenue"]]
        )
        fig.update_traces(textposition="outside", textfont_size=13)
        fig.update_layout(
            showlegend=False, xaxis_title="",
            yaxis=dict(title="GH₵", tickformat=",.0f", gridcolor="#F0F0F0"),
            title=dict(font=dict(size=14, color=COLOR_SECONDARY))
        )
        ch(fig, 280)
    with c2:
        fig2 = px.bar(
            comp, x="region", y="avg_order_value",
            title="Average Order Value by Region",
            color="region", color_discrete_map=REGION_COLORS,
            text=[fmt(v) for v in comp["avg_order_value"]]
        )
        fig2.update_traces(textposition="outside", textfont_size=13)
        fig2.update_layout(
            showlegend=False, xaxis_title="",
            yaxis=dict(title="GH₵", tickformat=",.0f", gridcolor="#F0F0F0"),
            title=dict(font=dict(size=14, color=COLOR_SECONDARY))
        )
        ch(fig2, 280)

    c3, c4 = st.columns(2)
    with c3:
        fig3 = go.Figure()
        fig3.add_trace(go.Bar(
            name="Avg Satisfaction",
            x=comp["region"], y=comp["avg_satisfaction"],
            marker_color=[REGION_COLORS.get(r, COLOR_NEUTRAL) for r in comp["region"]],
            text=[f"{v:.2f} ★" for v in comp["avg_satisfaction"]],
            textposition="outside", textfont=dict(size=13), yaxis="y"
        ))
        fig3.add_trace(go.Scatter(
            name="Review Count",
            x=comp["region"], y=comp["total_reviews"],
            mode="lines+markers",
            marker=dict(size=10, color=COLOR_SECONDARY),
            line=dict(color=COLOR_SECONDARY, width=2), yaxis="y2"
        ))
        fig3.add_hline(y=SATISFACTION_TARGET, line_dash="dash",
                       line_color=COLOR_WARNING, yref="y",
                       annotation_text=f"Target {SATISFACTION_TARGET}",
                       annotation_font_size=12)
        fig3.update_layout(
            title=dict(text="Satisfaction Score & Reviews by Region",
                       font=dict(size=14, color=COLOR_SECONDARY)),
            yaxis=dict(range=[0,5.5], title="Avg Rating", side="left", gridcolor="#F0F0F0"),
            yaxis2=dict(title="Review Count", overlaying="y", side="right"),
            legend=dict(orientation="h", y=1.12, x=0, bgcolor="rgba(0,0,0,0)", font=dict(size=12))
        )
        ch(fig3, 280)
    with c4:
        sales["day_name"] = sales["transaction_date"].dt.day_name()
        day_order = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
        heat = sales.groupby(["region","day_name"]).size().reset_index(name="count")
        heat["day_name"] = pd.Categorical(heat["day_name"], categories=day_order, ordered=True)
        pivot = heat.sort_values("day_name").pivot(
            index="region", columns="day_name", values="count").fillna(0)
        fig4 = px.imshow(
            pivot, color_continuous_scale=["#EBF3FB", COLOR_PRIMARY],
            title="Transaction Volume — Region × Day of Week",
            aspect="auto",
            text_auto=True
        )
        fig4.update_coloraxes(showscale=False)
        fig4.update_layout(
            paper_bgcolor="white", font_family="Inter, Arial",
            margin=dict(l=10,r=10,t=42,b=10), height=280,
            title=dict(font=dict(size=14, color=COLOR_SECONDARY)),
            font=dict(size=12)
        )
        st.plotly_chart(fig4, use_container_width=True, config={"displayModeBar": False})

    st.markdown('<div class="sec-hdr">Regional KPI Summary</div>', unsafe_allow_html=True)
    disp = comp.copy()
    disp["total_revenue"]    = disp["total_revenue"].map(lambda x: f"GH₵ {x:,.2f}")
    disp["avg_order_value"]  = disp["avg_order_value"].map(lambda x: f"GH₵ {x:,.2f}")
    disp["avg_satisfaction"] = disp["avg_satisfaction"].map(lambda x: f"{x:.2f} / 5")
    disp["total_stock"]      = disp["total_stock"].map(lambda x: f"{int(x):,}")
    disp.columns = ["Region","Total Revenue","Transactions","Units Sold",
                    "Avg Order Value","Avg Satisfaction","Reviews","Total Stock"]
    st.dataframe(disp, use_container_width=True, hide_index=True)


# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────
def main():
    try:
        with st.spinner("Loading..."):
            s_raw, f_raw, i_raw = load_all()
    except Exception as e:
        st.error(f"Failed to load data: {e}")
        st.info("Ensure `data/insightflow_sample_data.xlsx` exists, or update DATA_SOURCE in config.py")
        st.stop()

    render_sidebar(s_raw, f_raw)

    dr, region, category, rank_by = render_filters(s_raw, f_raw)

    # Period string for navbar
    s_str = str(dr[0]) if len(dr) > 0 else "—"
    e_str = str(dr[1]) if len(dr) > 1 else s_str
    period_str = f"{s_str} → {e_str}"

    # Active page via Streamlit tabs (in navbar visually, tabs rendered below)
    render_navbar("Revenue", period_str)   # active tab label is always the selected one

    # Apply date filter
    start = pd.Timestamp(dr[0])
    end   = pd.Timestamp(dr[1] if len(dr) > 1 else dr[0])
    sales    = s_raw[(s_raw["transaction_date"] >= start) & (s_raw["transaction_date"] <= end)]
    feedback = f_raw[(f_raw["review_date"]       >= start) & (f_raw["review_date"]       <= end)]
    inv      = i_raw[(i_raw["stock_date"]         >= start) & (i_raw["stock_date"]         <= end)]

    if len(sales) == 0:
        st.warning("No data found for the selected filters.")
        st.stop()

    kpi_strip(sales, feedback, inv, region)

    # Streamlit tabs — styled to blend with navbar
    t1,t2,t3,t4,t5 = st.tabs([
        "📈  Revenue",
        "🏆  Top Products",
        "😊  Satisfaction",
        "📦  Inventory",
        "🗺️  Regional"
    ])
    with t1: tab_revenue(sales, region)
    with t2: tab_products(sales, region, category, rank_by)
    with t3: tab_satisfaction(feedback, region)
    with t4: tab_inventory(inv, region)
    with t5: tab_regional(sales, feedback, inv)


if __name__ == "__main__":
    main()
