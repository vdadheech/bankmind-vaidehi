import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="BankMind RM Insights", page_icon="🏦", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=IBM+Plex+Mono:wght@600&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
[data-testid="stSidebar"] { background: #0f172a; }
[data-testid="stSidebar"] * { color: #cbd5e1 !important; }
[data-testid="metric-container"] { background: #1e293b; border: 1px solid #334155; border-radius: 10px; padding: 1rem 1.25rem; }
[data-testid="metric-container"] label { color: #94a3b8 !important; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.06em; }
[data-testid="metric-container"] [data-testid="stMetricValue"] { color: #f1f5f9 !important; font-family: 'IBM Plex Mono', monospace; font-size: 1.9rem !important; }
.section-tag { display: inline-block; background: #1e3a5f; color: #60a5fa; font-size: 0.68rem; font-weight: 600; letter-spacing: 0.12em; text-transform: uppercase; padding: 3px 10px; border-radius: 4px; margin-bottom: 6px; }
.stApp { background: #0d1117; color: #e2e8f0; }
.block-container { padding-top: 1.5rem; }
.insight-box { background: #1e293b; border-left: 3px solid #3b82f6; border-radius: 0 8px 8px 0; padding: 0.8rem 1.1rem; margin: 0.5rem 0 1rem 0; font-size: 0.85rem; color: #94a3b8; }
.insight-box strong { color: #e2e8f0; }
</style>
""", unsafe_allow_html=True)

# ── Constants ─────────────────────────────────────────────────────────────────
BLUE  = "#3b82f6"
GREEN = "#22c55e"
AMBER = "#f59e0b"
GRID  = "#334155"
BG    = "rgba(0,0,0,0)"

# Shared layout keys — ONLY things that don't conflict across charts
BASE = dict(
    paper_bgcolor=BG,
    plot_bgcolor=BG,
    font=dict(color="#94a3b8", family="Inter"),
    title_font=dict(color="#e2e8f0", size=15),
    margin=dict(l=10, r=10, t=40, b=10),
)

def apply_base(fig, **extra):
    """Merge BASE with per-chart overrides safely."""
    layout = {**BASE, **extra}
    fig.update_layout(**layout)
    # Always style axes after layout is set
    fig.update_xaxes(gridcolor=GRID, linecolor=GRID, tickfont=dict(color="#64748b"))
    fig.update_yaxes(gridcolor=GRID, linecolor=GRID, tickfont=dict(color="#64748b"))
    return fig

# ── Load data ─────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("bank-full.csv", sep=";")
    except FileNotFoundError:
        df = pd.read_csv("data/bank-full.csv", sep=";")
    df["subscribed"] = (df["y"] == "yes").astype(int)
    df["age_group"] = pd.cut(df["age"], bins=[17,30,45,60,100],
                              labels=["18–30","31–45","46–60","60+"])
    return df

try:
    df = load_data()
except FileNotFoundError:
    st.error("⚠️ Place `bank-full.csv` in the same folder as `app.py` and rerun.")
    st.stop()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🏦 BankMind")
    st.markdown("<small style='color:#475569'>RM Intelligence Dashboard · Track A</small>", unsafe_allow_html=True)
    st.divider()
    age_opts = ["All"] + list(df["age_group"].cat.categories)
    sel_age  = st.selectbox("Age group", age_opts)
    job_opts = ["All"] + sorted(df["job"].unique().tolist())
    sel_job  = st.selectbox("Job type", job_opts)
    edu_opts = ["All"] + sorted(df["education"].unique().tolist())
    sel_edu  = st.selectbox("Education", edu_opts)
    bal_min, bal_max = int(df["balance"].min()), int(df["balance"].max())
    bal_range = st.slider("Balance (€)", bal_min, bal_max, (bal_min, bal_max))
    st.divider()
    st.markdown("<small style='color:#475569'>UCI Bank Marketing · ~45,000 records</small>", unsafe_allow_html=True)

# ── Filter ────────────────────────────────────────────────────────────────────
f = df.copy()
if sel_age != "All": f = f[f["age_group"] == sel_age]
if sel_job != "All": f = f[f["job"] == sel_job]
if sel_edu != "All": f = f[f["education"] == sel_edu]
f = f[(f["balance"] >= bal_range[0]) & (f["balance"] <= bal_range[1])]

# ── Header & KPIs ─────────────────────────────────────────────────────────────
st.markdown("# BankMind · RM Insights Dashboard")
st.markdown(f"<div class='insight-box'>Showing <strong>{len(f):,}</strong> of <strong>{len(df):,}</strong> customer records.</div>", unsafe_allow_html=True)

k1, k2, k3, k4 = st.columns(4)
k1.metric("Customers", f"{len(f):,}")
k2.metric("Subscribers", f"{f['subscribed'].sum():,}")
k3.metric("Subscription Rate", f"{f['subscribed'].mean()*100:.1f}%")
k4.metric("Avg Balance", f"€{f['balance'].mean():,.0f}")
st.markdown("<br>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# Q1 — Job type
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<span class="section-tag">Question 1</span>', unsafe_allow_html=True)
st.subheader("Which job types have the highest subscription rate?")

job_stats = (
    f.groupby("job")["subscribed"]
    .agg(total="count", subs="sum")
    .assign(rate=lambda x: x["subs"] / x["total"] * 100)
    .sort_values("rate")
    .reset_index()
)

col1a, col1b = st.columns([3, 2])
with col1a:
    fig = px.bar(job_stats, x="rate", y="job", orientation="h",
                 text=job_stats["rate"].map("{:.1f}%".format),
                 color="rate", color_continuous_scale=["#1e3a5f", BLUE, "#93c5fd"],
                 labels={"rate": "Subscription Rate (%)", "job": ""},
                 title="Subscription Rate by Job Type")
    fig.update_traces(textposition="outside", textfont_color="#e2e8f0")
    apply_base(fig, height=380, coloraxis_showscale=False)
    st.plotly_chart(fig, width="stretch")

with col1b:
    top = job_stats.iloc[-1]; bot = job_stats.iloc[0]
    st.markdown(f"""<div class='insight-box'><strong>🏆 Highest:</strong> {top['job'].title()} — {top['rate']:.1f}%<br><br>
    <strong>📉 Lowest:</strong> {bot['job'].title()} — {bot['rate']:.1f}%<br><br>
    Top segment converts at <strong>{top['rate']/bot['rate']:.1f}×</strong> the rate of the lowest.</div>""", unsafe_allow_html=True)
    top5 = job_stats.nlargest(5,"rate")[["job","rate","total"]].rename(columns={"job":"Job","rate":"Rate %","total":"Customers"})
    top5["Rate %"] = top5["Rate %"].map("{:.1f}%".format)
    st.dataframe(top5, hide_index=True, use_container_width=True)

st.divider()

# ══════════════════════════════════════════════════════════════════════════════
# Q2 — Balance
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<span class="section-tag">Question 2</span>', unsafe_allow_html=True)
st.subheader("Is there a pattern between account balance and likelihood to subscribe?")

q2 = f[f["balance"] < f["balance"].quantile(0.99)].copy()
q2["balance_bin"] = pd.qcut(q2["balance"], q=8, duplicates="drop")
bal_stats = (
    q2.groupby("balance_bin", observed=True)["subscribed"]
    .agg(total="count", subs="sum")
    .assign(rate=lambda x: x["subs"] / x["total"] * 100)
    .reset_index()
)
bal_stats["bin_label"] = bal_stats["balance_bin"].apply(lambda x: f"€{x.left:,.0f}–{x.right:,.0f}")

col2a, col2b = st.columns([3, 2])
with col2a:
    fig2 = go.Figure()
    fig2.add_trace(go.Bar(x=bal_stats["bin_label"], y=bal_stats["rate"],
                          marker_color=BLUE, marker_opacity=0.85, name="Sub rate %",
                          hovertemplate="<b>%{x}</b><br>Rate: %{y:.1f}%<extra></extra>"))
    fig2.add_trace(go.Scatter(x=bal_stats["bin_label"], y=bal_stats["rate"],
                              mode="lines+markers", line=dict(color=AMBER, width=2),
                              marker=dict(size=7, color=AMBER), name="Trend"))
    apply_base(fig2, height=360, title="Subscription Rate by Balance Decile",
               xaxis_tickangle=-30,
               legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#94a3b8")))
    st.plotly_chart(fig2, width="stretch")

with col2b:
    hi = bal_stats.iloc[-1]["rate"]; lo = bal_stats.iloc[0]["rate"]
    st.markdown(f"""<div class='insight-box'>Highest balance bracket: <strong>{hi:.1f}%</strong> vs lowest: <strong>{lo:.1f}%</strong>.<br><br>
    Higher balance signals greater financial engagement. RMs should flag <strong>high-balance + no-loan</strong> customers as prime targets.</div>""", unsafe_allow_html=True)
    fig_box = px.box(q2, x="y", y="balance", color="y",
                     color_discrete_map={"yes": GREEN, "no": "#475569"},
                     labels={"y": "Subscribed", "balance": "Balance (€)"},
                     title="Balance Distribution by Outcome")
    apply_base(fig_box, height=260, showlegend=False, title_font=dict(color="#e2e8f0", size=13))
    st.plotly_chart(fig_box, width="stretch")

st.divider()

# ══════════════════════════════════════════════════════════════════════════════
# Q3 — Age group
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<span class="section-tag">Question 3</span>', unsafe_allow_html=True)
st.subheader("How does subscription rate differ across age groups?")

age_stats = (
    f.groupby("age_group", observed=True)["subscribed"]
    .agg(total="count", subs="sum")
    .assign(rate=lambda x: x["subs"] / x["total"] * 100,
            no_subs=lambda x: x["total"] - x["subs"])
    .reset_index()
)
labels = age_stats["age_group"].astype(str).tolist()

col3a, col3b = st.columns([2, 3])
with col3a:
    fig_pie = px.pie(age_stats, names="age_group", values="total",
                     color_discrete_sequence=[BLUE, "#60a5fa", "#93c5fd", "#bfdbfe"],
                     title="Customer Distribution by Age", hole=0.45)
    fig_pie.update_traces(textfont_color="white", textinfo="percent+label")
    # Use a separate dict to avoid any key conflicts — no xaxis/yaxis needed for pie
    fig_pie.update_layout(
        paper_bgcolor=BG, plot_bgcolor=BG,
        font=dict(color="#94a3b8", family="Inter"),
        title_font=dict(color="#e2e8f0", size=15),
        margin=dict(l=0, r=0, t=40, b=0),
        showlegend=False, height=300
    )
    st.plotly_chart(fig_pie, width="stretch")

with col3b:
    fig_age = go.Figure()
    fig_age.add_trace(go.Bar(name="Subscribed", x=labels, y=age_stats["subs"].tolist(),
                             marker_color=GREEN))
    fig_age.add_trace(go.Bar(name="Not subscribed", x=labels, y=age_stats["no_subs"].tolist(),
                             marker_color="#1e3a5f"))
    fig_age.add_trace(go.Scatter(x=labels, y=age_stats["rate"].tolist(),
                                 mode="lines+markers+text",
                                 line=dict(color=AMBER, width=2.5),
                                 marker=dict(size=9, color=AMBER),
                                 text=age_stats["rate"].map("{:.1f}%".format).tolist(),
                                 textposition="top center",
                                 textfont=dict(color=AMBER, size=11),
                                 name="Rate %", yaxis="y2"))
    # Build layout dict manually — no PLOTLY_LAYOUT spread to avoid yaxis conflict
    fig_age.update_layout(
        paper_bgcolor=BG, plot_bgcolor=BG,
        font=dict(color="#94a3b8", family="Inter"),
        title_font=dict(color="#e2e8f0", size=15),
        margin=dict(l=10, r=10, t=40, b=10),
        barmode="stack", height=320,
        title="Customers & Subscription Rate by Age Group",
        yaxis=dict(title="Customers", gridcolor=GRID, linecolor=GRID, tickfont=dict(color="#64748b")),
        yaxis2=dict(title="Rate %", overlaying="y", side="right",
                    range=[0, age_stats["rate"].max() * 2],
                    gridcolor="rgba(0,0,0,0)", showgrid=False, tickfont=dict(color=AMBER)),
        xaxis=dict(gridcolor=GRID, linecolor=GRID, tickfont=dict(color="#64748b")),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#94a3b8"),
                    orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    st.plotly_chart(fig_age, width="stretch")

best_age = age_stats.loc[age_stats["rate"].idxmax()]
st.markdown(f"""<div class='insight-box'><strong>Key finding:</strong> The <strong>{best_age['age_group']}</strong> age group 
has the highest subscription rate at <strong>{best_age['rate']:.1f}%</strong>. Both youngest and oldest segments tend to show 
higher engagement — the former are forming new banking habits, the latter are shifting toward wealth preservation.</div>""", unsafe_allow_html=True)

st.divider()

# ══════════════════════════════════════════════════════════════════════════════
# Q4 — Housing loan
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<span class="section-tag">Question 4</span>', unsafe_allow_html=True)
st.subheader("Does having a housing loan reduce uptake of new products?")

housing_rate = (
    f.groupby("housing")["subscribed"]
    .agg(total="count", subs="sum")
    .assign(rate=lambda x: x["subs"] / x["total"] * 100)
    .reset_index()
)

col4a, col4b = st.columns([2, 3])
with col4a:
    fig_h = px.bar(housing_rate, x="housing", y="rate", color="housing",
                   color_discrete_map={"yes": "#ef4444", "no": GREEN},
                   text=housing_rate["rate"].map("{:.1f}%".format),
                   labels={"housing": "Has Housing Loan", "rate": "Subscription Rate (%)"},
                   title="Subscription Rate: Housing Loan vs None")
    fig_h.update_traces(textposition="outside", textfont_color="#e2e8f0")
    apply_base(fig_h, height=320, showlegend=False)
    st.plotly_chart(fig_h, width="stretch")

with col4b:
    cross = f.groupby(["housing","loan"])["subscribed"].mean().mul(100).unstack()
    fig_heat = px.imshow(cross,
                         color_continuous_scale=["#0f172a","#1e3a5f", BLUE,"#93c5fd"],
                         labels=dict(x="Has Personal Loan", y="Has Housing Loan", color="Sub Rate %"),
                         text_auto=".1f",
                         title="Subscription Rate (%) — Housing × Personal Loan",
                         aspect="auto")
    fig_heat.update_layout(
        paper_bgcolor=BG, plot_bgcolor=BG,
        font=dict(color="#94a3b8", family="Inter"),
        title_font=dict(color="#e2e8f0", size=15),
        margin=dict(l=10, r=10, t=40, b=10),
        height=320,
        coloraxis_colorbar=dict(tickfont=dict(color="#94a3b8"))
    )
    st.plotly_chart(fig_heat, width="stretch")

no_rate  = housing_rate.loc[housing_rate["housing"]=="no",  "rate"].values[0]
yes_rate = housing_rate.loc[housing_rate["housing"]=="yes", "rate"].values[0]
st.markdown(f"""<div class='insight-box'><strong>Clear signal:</strong> Customers <em>without</em> a housing loan subscribe at 
<strong>{no_rate:.1f}%</strong> — <strong>{no_rate-yes_rate:.1f}pp higher</strong> than those with one ({yes_rate:.1f}%). 
The heatmap shows <strong>no housing + no personal loan</strong> is the most receptive segment. 
RMs should prioritise debt-free customers.</div>""", unsafe_allow_html=True)

st.divider()

with st.expander("🔎 Explore raw data"):
    st.dataframe(f[["age","age_group","job","education","balance","housing","loan","y"]].head(500),
                 use_container_width=True)
    st.caption(f"Showing first 500 of {len(f):,} filtered records.")

st.markdown("<br><small style='color:#475569'>BankMind · VITB AI Innovators Hub · Track A · UCI Bank Marketing Dataset</small>", unsafe_allow_html=True)
