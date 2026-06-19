import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="BankMind RM Insights",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  /* Import fonts */
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;600&display=swap');

  html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

  /* Dark sidebar */
  [data-testid="stSidebar"] {
    background: #0f172a;
  }
  [data-testid="stSidebar"] * { color: #cbd5e1 !important; }
  [data-testid="stSidebar"] .stSelectbox label,
  [data-testid="stSidebar"] .stMultiSelect label { color: #94a3b8 !important; font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.05em; }

  /* Metric cards */
  [data-testid="metric-container"] {
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 10px;
    padding: 1rem 1.25rem;
  }
  [data-testid="metric-container"] label { color: #94a3b8 !important; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.06em; }
  [data-testid="metric-container"] [data-testid="stMetricValue"] { color: #f1f5f9 !important; font-family: 'IBM Plex Mono', monospace; font-size: 1.9rem !important; }
  [data-testid="metric-container"] [data-testid="stMetricDelta"] { font-size: 0.8rem; }

  /* Section headers */
  .section-tag {
    display: inline-block;
    background: #1e3a5f;
    color: #60a5fa;
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    padding: 3px 10px;
    border-radius: 4px;
    margin-bottom: 6px;
  }

  /* Main background */
  .stApp { background: #0d1117; color: #e2e8f0; }
  .block-container { padding-top: 1.5rem; }

  /* Plotly chart borders */
  .js-plotly-plot { border-radius: 10px; }
  
  /* Info box */
  .insight-box {
    background: #1e293b;
    border-left: 3px solid #3b82f6;
    border-radius: 0 8px 8px 0;
    padding: 0.8rem 1.1rem;
    margin: 0.5rem 0 1rem 0;
    font-size: 0.85rem;
    color: #94a3b8;
  }
  .insight-box strong { color: #e2e8f0; }
</style>
""", unsafe_allow_html=True)

# ── Load data ─────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    """Load and lightly clean the UCI Bank Marketing dataset."""
    try:
        df = pd.read_csv("bank-full.csv", sep=";")
    except FileNotFoundError:
        # Fallback path if user places it elsewhere
        df = pd.read_csv("data/bank-full.csv", sep=";")

    # Binary encode target
    df["subscribed"] = (df["y"] == "yes").astype(int)

    # Age bins
    df["age_group"] = pd.cut(
        df["age"],
        bins=[17, 30, 45, 60, 100],
        labels=["18–30", "31–45", "46–60", "60+"]
    )

    # Clean 'unknown' in key cols for display (keep originals)
    df["job_clean"] = df["job"].replace("unknown", "Unknown")
    df["education_clean"] = df["education"].replace("unknown", "Unknown")

    return df

try:
    df = load_data()
except FileNotFoundError:
    st.error("⚠️ **Dataset not found.** Place `bank-full.csv` in the same directory as `app.py` and rerun.")
    st.stop()

# ── Sidebar filters ───────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🏦 BankMind")
    st.markdown("<small style='color:#475569'>RM Intelligence Dashboard · Track A</small>", unsafe_allow_html=True)
    st.divider()

    st.markdown("**Filter dataset**")

    # Age group filter
    age_opts = ["All"] + list(df["age_group"].cat.categories)
    sel_age = st.selectbox("Age group", age_opts)

    # Job filter
    job_opts = ["All"] + sorted(df["job"].unique().tolist())
    sel_job = st.selectbox("Job type", job_opts)

    # Education filter
    edu_opts = ["All"] + sorted(df["education"].unique().tolist())
    sel_edu = st.selectbox("Education level", edu_opts)

    # Balance range
    bal_min, bal_max = int(df["balance"].min()), int(df["balance"].max())
    bal_range = st.slider("Account balance (€)", bal_min, bal_max, (bal_min, bal_max))

    st.divider()
    st.markdown("<small style='color:#475569'>Data: UCI Bank Marketing<br>~45,000 customer records</small>", unsafe_allow_html=True)

# ── Apply filters ─────────────────────────────────────────────────────────────
filtered = df.copy()
if sel_age != "All":
    filtered = filtered[filtered["age_group"] == sel_age]
if sel_job != "All":
    filtered = filtered[filtered["job"] == sel_job]
if sel_edu != "All":
    filtered = filtered[filtered["education"] == sel_edu]
filtered = filtered[(filtered["balance"] >= bal_range[0]) & (filtered["balance"] <= bal_range[1])]

# ── Colour palette (consistent across charts) ─────────────────────────────────
BLUE   = "#3b82f6"
GREEN  = "#22c55e"
AMBER  = "#f59e0b"
SLATE  = "#94a3b8"
BG     = "#1e293b"
GRID   = "#334155"
CHART_BG = "rgba(0,0,0,0)"

PLOTLY_LAYOUT = dict(
    paper_bgcolor=CHART_BG,
    plot_bgcolor=CHART_BG,
    font=dict(color="#94a3b8", family="Inter"),
    title_font=dict(color="#e2e8f0", size=15),
    xaxis=dict(gridcolor=GRID, linecolor=GRID, tickfont=dict(color="#64748b")),
    yaxis=dict(gridcolor=GRID, linecolor=GRID, tickfont=dict(color="#64748b")),
    margin=dict(l=10, r=10, t=40, b=10),
)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("# BankMind · RM Insights Dashboard")
st.markdown(f"<div class='insight-box'>Showing <strong>{len(filtered):,}</strong> of <strong>{len(df):,}</strong> customer records · Use the sidebar to filter by demographics and balance range.</div>", unsafe_allow_html=True)

# ── KPI row ───────────────────────────────────────────────────────────────────
k1, k2, k3, k4 = st.columns(4)

total        = len(filtered)
subscribers  = filtered["subscribed"].sum()
sub_rate     = subscribers / total * 100 if total else 0
avg_balance  = filtered["balance"].mean()
median_age   = int(filtered["age"].median())

k1.metric("Customers", f"{total:,}")
k2.metric("Subscribers (y=yes)", f"{subscribers:,}")
k3.metric("Subscription Rate", f"{sub_rate:.1f}%")
k4.metric("Avg Balance", f"€{avg_balance:,.0f}")

st.markdown("<br>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# Q1 — Subscription rate by job type
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<span class="section-tag">Question 1</span>', unsafe_allow_html=True)
st.subheader("Which job types have the highest subscription rate?")

job_stats = (
    filtered.groupby("job")
    .agg(total=("subscribed", "count"), subs=("subscribed", "sum"))
    .assign(rate=lambda x: x["subs"] / x["total"] * 100)
    .sort_values("rate", ascending=True)
    .reset_index()
)

col_q1a, col_q1b = st.columns([3, 2])

with col_q1a:
    fig_job = px.bar(
        job_stats, x="rate", y="job",
        orientation="h",
        text=job_stats["rate"].map("{:.1f}%".format),
        color="rate",
        color_continuous_scale=["#1e3a5f", BLUE, "#93c5fd"],
        labels={"rate": "Subscription Rate (%)", "job": ""},
        title="Subscription Rate by Job Type",
    )
    fig_job.update_traces(textposition="outside", textfont_color="#e2e8f0")
    fig_job.update_layout(**PLOTLY_LAYOUT, coloraxis_showscale=False, height=380)
    st.plotly_chart(fig_job, use_container_width=True)

with col_q1b:
    st.markdown("<br><br>", unsafe_allow_html=True)
    top_job    = job_stats.iloc[-1]
    bottom_job = job_stats.iloc[0]
    st.markdown(f"""
    <div class='insight-box'>
    <strong>🏆 Highest:</strong> <strong>{top_job['job'].title()}</strong> — {top_job['rate']:.1f}% subscription rate
    ({top_job['subs']:,} of {top_job['total']:,} customers).<br><br>
    <strong>📉 Lowest:</strong> <strong>{bottom_job['job'].title()}</strong> — {bottom_job['rate']:.1f}%.<br><br>
    RMs should prioritise outreach to <strong>{top_job['job'].title()}</strong> 
    and <strong>{job_stats.iloc[-2]['job'].title()}</strong> segments — they convert at nearly 
    <strong>{top_job['rate']/bottom_job['rate']:.1f}×</strong> the rate of the lowest segment.
    </div>
    """, unsafe_allow_html=True)

    # Mini table
    st.markdown("**Top 5 job types**")
    top5 = job_stats.nlargest(5, "rate")[["job", "rate", "total"]].rename(
        columns={"job": "Job", "rate": "Rate %", "total": "Customers"}
    )
    top5["Rate %"] = top5["Rate %"].map("{:.1f}%".format)
    st.dataframe(top5, hide_index=True, use_container_width=True)

st.divider()

# ══════════════════════════════════════════════════════════════════════════════
# Q2 — Account balance vs subscription
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<span class="section-tag">Question 2</span>', unsafe_allow_html=True)
st.subheader("Is there a pattern between account balance and likelihood to subscribe?")

col_q2a, col_q2b = st.columns([3, 2])

with col_q2a:
    # Bin balance into deciles, compute rate per bin
    q2 = filtered.copy()
    q2 = q2[q2["balance"] < q2["balance"].quantile(0.99)]  # clip extreme outliers for viz
    q2["balance_bin"] = pd.qcut(q2["balance"], q=8, duplicates="drop")
    bal_stats = (
        q2.groupby("balance_bin", observed=True)
        .agg(total=("subscribed", "count"), subs=("subscribed", "sum"))
        .assign(rate=lambda x: x["subs"] / x["total"] * 100)
        .reset_index()
    )
    bal_stats["bin_label"] = bal_stats["balance_bin"].apply(
        lambda x: f"€{x.left:,.0f}–{x.right:,.0f}"
    )

    fig_bal = go.Figure()
    fig_bal.add_trace(go.Bar(
        x=bal_stats["bin_label"], y=bal_stats["rate"],
        marker_color=BLUE, marker_opacity=0.85,
        name="Sub rate %",
        hovertemplate="<b>%{x}</b><br>Rate: %{y:.1f}%<extra></extra>",
    ))
    fig_bal.add_trace(go.Scatter(
        x=bal_stats["bin_label"], y=bal_stats["rate"],
        mode="lines+markers",
        line=dict(color=AMBER, width=2),
        marker=dict(size=7, color=AMBER),
        name="Trend",
    ))
    fig_bal.update_layout(**PLOTLY_LAYOUT, title="Subscription Rate by Balance Decile",
                          xaxis_tickangle=-30, height=360,
                          legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#94a3b8")))
    st.plotly_chart(fig_bal, use_container_width=True)

with col_q2b:
    st.markdown("<br><br>", unsafe_allow_html=True)
    high_bal_rate = bal_stats.iloc[-1]["rate"]
    low_bal_rate  = bal_stats.iloc[0]["rate"]
    st.markdown(f"""
    <div class='insight-box'>
    Customers in the <strong>highest balance bracket</strong> subscribe at <strong>{high_bal_rate:.1f}%</strong> 
    vs <strong>{low_bal_rate:.1f}%</strong> in the lowest.<br><br>
    Higher balance generally signals greater financial engagement and trust in banking products — 
    these customers are more receptive to term deposits.<br><br>
    RMs should flag <strong>high-balance + no-existing-loan</strong> customers as prime targets.
    </div>
    """, unsafe_allow_html=True)

    # Violin of balance, grouped by y
    fig_vio = px.box(
        filtered[filtered["balance"] < filtered["balance"].quantile(0.95)],
        x="y", y="balance", color="y",
        color_discrete_map={"yes": GREEN, "no": "#475569"},
        labels={"y": "Subscribed", "balance": "Balance (€)"},
        title="Balance Distribution",
    )
    fig_vio.update_layout(**PLOTLY_LAYOUT, height=250,
                          showlegend=False, title_font_size=13)
    st.plotly_chart(fig_vio, use_container_width=True)

st.divider()

# ══════════════════════════════════════════════════════════════════════════════
# Q3 — Subscription rate by age group
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<span class="section-tag">Question 3</span>', unsafe_allow_html=True)
st.subheader("How does subscription rate differ across age groups?")

age_stats = (
    filtered.groupby("age_group", observed=True)
    .agg(total=("subscribed", "count"), subs=("subscribed", "sum"))
    .assign(rate=lambda x: x["subs"] / x["total"] * 100,
            no_subs=lambda x: x["total"] - x["subs"])
    .reset_index()
)

col_q3a, col_q3b = st.columns([2, 3])

with col_q3a:
    fig_age_pie = px.pie(
        age_stats, names="age_group", values="total",
        color_discrete_sequence=[BLUE, "#60a5fa", "#93c5fd", "#bfdbfe"],
        title="Customer Distribution by Age",
        hole=0.45,
    )
    fig_age_pie.update_traces(textfont_color="white", textinfo="percent+label")
    fig_age_pie.update_layout(**PLOTLY_LAYOUT, height=300,
                               showlegend=False, margin=dict(l=0, r=0, t=40, b=0))
    st.plotly_chart(fig_age_pie, use_container_width=True)

with col_q3b:
    # Grouped bar: subscribers vs non-subscribers per age group
    fig_age = go.Figure()
    fig_age.add_trace(go.Bar(
        name="Subscribed", x=age_stats["age_group"].astype(str),
        y=age_stats["subs"], marker_color=GREEN,
        hovertemplate="<b>%{x}</b><br>Subscribed: %{y:,}<extra></extra>",
    ))
    fig_age.add_trace(go.Bar(
        name="Not subscribed", x=age_stats["age_group"].astype(str),
        y=age_stats["no_subs"], marker_color="#1e3a5f",
        hovertemplate="<b>%{x}</b><br>Not subscribed: %{y:,}<extra></extra>",
    ))
    # Overlay rate line
    fig_age.add_trace(go.Scatter(
        x=age_stats["age_group"].astype(str), y=age_stats["rate"],
        mode="lines+markers+text",
        line=dict(color=AMBER, width=2.5),
        marker=dict(size=9, color=AMBER),
        text=age_stats["rate"].map("{:.1f}%".format),
        textposition="top center",
        textfont=dict(color=AMBER, size=11),
        name="Rate %", yaxis="y2",
    ))
    fig_age.update_layout(
        **PLOTLY_LAYOUT,
        barmode="stack", height=320,
        title="Customers & Subscription Rate by Age Group",
        yaxis=dict(title="Customers", gridcolor=GRID, linecolor=GRID),
        yaxis2=dict(title="Rate %", overlaying="y", side="right",
                    range=[0, age_stats["rate"].max() * 2],
                    gridcolor="rgba(0,0,0,0)", showgrid=False, tickfont=dict(color=AMBER)),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#94a3b8"), orientation="h",
                    yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    st.plotly_chart(fig_age, use_container_width=True)

# Insight row
best_age = age_stats.loc[age_stats["rate"].idxmax()]
st.markdown(f"""
<div class='insight-box'>
<strong>Key finding:</strong> The <strong>{best_age['age_group']}</strong> age group has the highest subscription 
rate at <strong>{best_age['rate']:.1f}%</strong>. Younger (18–30) and older (60+) customers tend to show higher 
engagement with new products — the former due to digital-first banking habits, the latter due to wealth 
accumulation and retirement planning needs.
</div>
""", unsafe_allow_html=True)

st.divider()

# ══════════════════════════════════════════════════════════════════════════════
# Q4 — Housing loan vs subscription
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<span class="section-tag">Question 4</span>', unsafe_allow_html=True)
st.subheader("Does having a housing loan reduce uptake of new products?")

col_q4a, col_q4b = st.columns([2, 3])

with col_q4a:
    housing_stats = (
        filtered.groupby(["housing", "y"])
        .size().reset_index(name="count")
    )
    housing_rate = (
        filtered.groupby("housing")
        .agg(total=("subscribed", "count"), subs=("subscribed", "sum"))
        .assign(rate=lambda x: x["subs"] / x["total"] * 100)
        .reset_index()
    )

    fig_housing = px.bar(
        housing_rate, x="housing", y="rate",
        color="housing",
        color_discrete_map={"yes": "#ef4444", "no": GREEN},
        text=housing_rate["rate"].map("{:.1f}%".format),
        labels={"housing": "Has Housing Loan", "rate": "Subscription Rate (%)"},
        title="Subscription Rate: Housing Loan vs None",
    )
    fig_housing.update_traces(textposition="outside", textfont_color="#e2e8f0")
    fig_housing.update_layout(**PLOTLY_LAYOUT, showlegend=False, height=320)
    st.plotly_chart(fig_housing, use_container_width=True)

with col_q4b:
    # Cross-tab heatmap: housing × personal loan
    cross = (
        filtered.groupby(["housing", "loan"])
        .agg(rate=("subscribed", "mean"))
        .reset_index()
    )
    cross["rate"] = cross["rate"] * 100
    cross_pivot = cross.pivot(index="housing", columns="loan", values="rate")

    fig_heat = px.imshow(
        cross_pivot,
        color_continuous_scale=["#0f172a", "#1e3a5f", BLUE, "#93c5fd"],
        labels=dict(x="Has Personal Loan", y="Has Housing Loan", color="Sub Rate %"),
        text_auto=".1f",
        title="Subscription Rate (%) — Housing × Personal Loan",
        aspect="auto",
    )
    fig_heat.update_layout(**PLOTLY_LAYOUT, height=320,
                           coloraxis_colorbar=dict(tickfont=dict(color="#94a3b8")))
    st.plotly_chart(fig_heat, use_container_width=True)

# Insight
no_housing_rate  = housing_rate.loc[housing_rate["housing"] == "no", "rate"].values[0]
yes_housing_rate = housing_rate.loc[housing_rate["housing"] == "yes", "rate"].values[0]
delta = no_housing_rate - yes_housing_rate
st.markdown(f"""
<div class='insight-box'>
<strong>Clear signal:</strong> Customers <em>without</em> a housing loan subscribe at 
<strong>{no_housing_rate:.1f}%</strong> — <strong>{delta:.1f} percentage points higher</strong> than those with one 
({yes_housing_rate:.1f}%). The heatmap shows that <strong>no housing loan + no personal loan</strong> 
is the most receptive segment. RMs should prioritise debt-free customers for new product pitches.
</div>
""", unsafe_allow_html=True)

st.divider()

# ══════════════════════════════════════════════════════════════════════════════
# Bonus: Raw data explorer
# ══════════════════════════════════════════════════════════════════════════════
with st.expander("🔎 Explore raw data"):
    st.dataframe(
        filtered[["age", "age_group", "job", "education", "balance",
                   "housing", "loan", "y"]].head(500),
        use_container_width=True,
    )
    st.caption(f"Showing first 500 rows of {len(filtered):,} filtered records.")

st.markdown("<br><small style='color:#475569'>BankMind · VITB AI Innovators Hub · Track A · Data sourced from UCI Bank Marketing Dataset</small>", unsafe_allow_html=True)
