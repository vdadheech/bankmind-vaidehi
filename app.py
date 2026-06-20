import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(
    page_title="BankMind · RM Intelligence",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════════
# THEME
# ══════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=IBM+Plex+Mono:wght@400;500;600&display=swap');

/* ── Reset & base ─────────────────────────────── */
*, html, body { box-sizing: border-box; }
html, body, [class*="css"], .stApp {
    font-family: 'Inter', sans-serif !important;
    background: #060811 !important;
    color: #c9d1e0;
}
.block-container { padding: 0 !important; max-width: 100% !important; }

/* ── Sidebar ───────────────────────────────────── */
[data-testid="stSidebar"] {
    background: #0a0d17 !important;
    border-right: 1px solid #12182e;
    width: 240px !important;
}
[data-testid="stSidebar"] > div { padding: 0 !important; }
[data-testid="stSidebar"] * { color: #7a85a0 !important; }
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stSlider label {
    font-size: 0.65rem !important; font-weight: 600 !important;
    text-transform: uppercase; letter-spacing: 0.12em;
    color: #2e3a56 !important;
}
[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background: #0f1525 !important;
    border: 1px solid #1a2340 !important;
    border-radius: 8px !important;
    color: #7a85a0 !important;
    font-size: 0.82rem !important;
}
[data-testid="stSidebar"] [data-baseweb="select"] * { color: #7a85a0 !important; }
section[data-testid="stSidebar"] hr { border-color: #12182e !important; }

/* ── Main top nav bar ──────────────────────────── */
.topbar {
    display: flex; align-items: center; justify-content: space-between;
    padding: 14px 32px 14px 28px;
    background: #0a0d17;
    border-bottom: 1px solid #12182e;
}
.topbar-left { display: flex; align-items: center; gap: 12px; }
.topbar-logo {
    width: 32px; height: 32px; border-radius: 8px;
    background: linear-gradient(135deg, #6d28d9, #4f46e5);
    display: flex; align-items: center; justify-content: center;
    font-size: 16px;
}
.topbar-title { font-size: 1rem; font-weight: 700; color: #e2e8f0; letter-spacing: -0.02em; }
.topbar-sub   { font-size: 0.7rem; color: #2e3a56; text-transform: uppercase; letter-spacing: 0.1em; }
.topbar-right { display: flex; align-items: center; gap: 16px; }
.nav-pill {
    font-size: 0.72rem; font-weight: 600; padding: 5px 14px;
    border-radius: 20px; cursor: pointer; letter-spacing: 0.04em;
}
.nav-pill.active { background: #1e1b4b; color: #818cf8; border: 1px solid #312e81; }
.nav-pill.muted  { color: #2e3a56; border: 1px solid transparent; }
.status-dot { width: 6px; height: 6px; background: #10b981; border-radius: 50%; display: inline-block; margin-right: 5px; }

/* ── Page wrapper ──────────────────────────────── */
.page-wrap { padding: 24px 32px 32px 28px; }

/* ── Section label ─────────────────────────────── */
.section-label {
    font-size: 0.6rem; font-weight: 700; letter-spacing: 0.18em;
    text-transform: uppercase; color: #312e81;
    margin-bottom: 2px;
}
.section-title {
    font-size: 1.05rem; font-weight: 700; color: #c9d1e0;
    letter-spacing: -0.01em; margin-bottom: 14px; margin-top: 0;
}

/* ── KPI cards ─────────────────────────────────── */
[data-testid="metric-container"] {
    background: #0d1120 !important;
    border: 1px solid #12182e !important;
    border-radius: 12px !important;
    padding: 18px 20px 16px !important;
    position: relative;
    overflow: hidden;
}
[data-testid="metric-container"]::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, #6d28d9, #4f46e5);
}
[data-testid="metric-container"] label {
    color: #2e3a56 !important; font-size: 0.65rem !important;
    font-weight: 700 !important; text-transform: uppercase; letter-spacing: 0.12em;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #e2e8f0 !important; font-family: 'IBM Plex Mono', monospace !important;
    font-size: 1.7rem !important; font-weight: 600 !important; line-height: 1.2;
}
[data-testid="metric-container"] [data-testid="stMetricDelta"] {
    font-size: 0.72rem !important; font-family: 'IBM Plex Mono', monospace !important;
}

/* ── Chart card ────────────────────────────────── */
.chart-card {
    background: #0d1120;
    border: 1px solid #12182e;
    border-radius: 14px;
    padding: 20px 20px 12px 20px;
    margin-bottom: 20px;
}
.chart-card-title {
    font-size: 0.82rem; font-weight: 600; color: #7a85a0;
    text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 12px;
}

/* ── Insight strip ─────────────────────────────── */
.insight-strip {
    background: #0d1120;
    border: 1px solid #12182e;
    border-radius: 10px;
    padding: 14px 18px;
    margin-bottom: 20px;
    font-size: 0.82rem;
    color: #4a5568;
    line-height: 1.65;
    display: flex; align-items: flex-start; gap: 12px;
}
.insight-icon { font-size: 1rem; margin-top: 1px; flex-shrink: 0; }
.insight-strip strong { color: #a5b4fc; }

/* ── Section divider ───────────────────────────── */
.sec-divider {
    border: none; border-top: 1px solid #0f1525;
    margin: 28px 0 24px;
}

/* ── Filter bar ────────────────────────────────── */
.filter-bar {
    display: flex; align-items: center; gap: 8px;
    background: #0d1120; border: 1px solid #12182e;
    border-radius: 10px; padding: 10px 16px; margin-bottom: 24px;
    font-size: 0.75rem; color: #2e3a56;
}
.filter-label { font-weight: 600; text-transform: uppercase; letter-spacing: 0.1em; margin-right: 4px; }

/* ── Record count badge ────────────────────────── */
.rec-badge {
    display: inline-flex; align-items: center; gap: 6px;
    background: #0f1525; border: 1px solid #1a2340;
    border-radius: 6px; padding: 3px 10px;
    font-size: 0.72rem; color: #2e3a56; font-family: 'IBM Plex Mono', monospace;
}

/* ── Dataframe tweaks ──────────────────────────── */
[data-testid="stDataFrame"] { border-radius: 8px; overflow: hidden; }

/* ── Scrollbar ─────────────────────────────────── */
::-webkit-scrollbar { width: 3px; height: 3px; }
::-webkit-scrollbar-track { background: #060811; }
::-webkit-scrollbar-thumb { background: #12182e; border-radius: 4px; }

/* ── Streamlit widget chrome ───────────────────── */
div[data-testid="stHorizontalBlock"] > div { gap: 16px !important; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# COLOUR CONSTANTS
# ══════════════════════════════════════════════════════════════════
P   = "#6d28d9"   # purple
I   = "#4f46e5"   # indigo
VI  = "#818cf8"   # violet light
CY  = "#22d3ee"   # cyan
GR  = "#10b981"   # green
RE  = "#f43f5e"   # red
AM  = "#f59e0b"   # amber
GRID= "#12182e"
BG  = "rgba(0,0,0,0)"
FC  = "#4a5568"   # font colour muted

def _lay(**kw):
    d = dict(
        paper_bgcolor=BG, plot_bgcolor=BG,
        font=dict(color=FC, family="Inter, sans-serif", size=11),
        title_font=dict(color="#7a85a0", size=12, family="Inter"),
        hoverlabel=dict(bgcolor="#0f1525", bordercolor="#1a2340",
                        font_color="#c9d1e0", font_family="Inter", font_size=12),
        margin=dict(l=4, r=4, t=28, b=4),
    )
    d.update(kw)
    return d

def ax(fig, xa=0, hide_x=False, hide_y=False):
    fig.update_xaxes(gridcolor=GRID, linecolor=GRID, zeroline=False,
                     tickfont=dict(color="#1e2a3a", size=10), tickangle=xa,
                     showticklabels=not hide_x)
    fig.update_yaxes(gridcolor=GRID, linecolor=GRID, zeroline=False,
                     tickfont=dict(color="#1e2a3a", size=10),
                     showticklabels=not hide_y)
    return fig

# ══════════════════════════════════════════════════════════════════
# DATA
# ══════════════════════════════════════════════════════════════════
@st.cache_data
def load():
    for p in ["bank-full.csv", "data/bank-full.csv"]:
        try:
            df = pd.read_csv(p, sep=";")
            df["subscribed"] = (df["y"] == "yes").astype(int)
            df["age_group"]  = pd.cut(df["age"], bins=[17,30,45,60,100],
                                       labels=["18–30","31–45","46–60","60+"])
            return df
        except FileNotFoundError:
            continue
    return None

df = load()
if df is None:
    st.error("⚠️  Place `bank-full.csv` in the repo root."); st.stop()

# ══════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style='padding:20px 20px 4px;'>
      <div style='display:flex;align-items:center;gap:10px;margin-bottom:18px;'>
        <div style='width:30px;height:30px;border-radius:8px;background:linear-gradient(135deg,#6d28d9,#4f46e5);
             display:flex;align-items:center;justify-content:center;font-size:15px;'>🏦</div>
        <div>
          <div style='font-size:.9rem;font-weight:700;color:#c9d1e0;letter-spacing:-.01em;'>BankMind</div>
          <div style='font-size:.6rem;color:#1e2a3a;text-transform:uppercase;letter-spacing:.1em;'>RM Intelligence</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='padding:0 16px;'>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:.6rem;font-weight:700;text-transform:uppercase;letter-spacing:.12em;color:#1e2a3a;margin-bottom:10px;'>Segment Filters</div>", unsafe_allow_html=True)

    sel_age = st.selectbox("Age group",  ["All"] + list(df["age_group"].cat.categories))
    sel_job = st.selectbox("Job type",   ["All"] + sorted(df["job"].unique()))
    sel_edu = st.selectbox("Education",  ["All"] + sorted(df["education"].unique()))
    b0, b1  = int(df["balance"].min()), int(df["balance"].max())
    bal     = st.slider("Balance range (€)", b0, b1, (b0, b1))
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(f"""
    <div style='position:absolute;bottom:0;left:0;right:0;padding:16px 20px;
         border-top:1px solid #12182e;background:#0a0d17;'>
      <div style='font-size:.62rem;color:#1e2a3a;line-height:1.8;'>
        <span style='color:#2e3a56;'>Dataset</span> UCI Bank Marketing<br>
        <span style='color:#2e3a56;'>Records</span>
        <span style='font-family:IBM Plex Mono;'>{len(df):,}</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# FILTER
# ══════════════════════════════════════════════════════════════════
f = df.copy()
if sel_age != "All": f = f[f["age_group"] == sel_age]
if sel_job != "All": f = f[f["job"]       == sel_job]
if sel_edu != "All": f = f[f["education"] == sel_edu]
f = f[f["balance"].between(bal[0], bal[1])]

if len(f) == 0:
    st.warning("No records match filters. Adjust the sidebar."); st.stop()

sub_rate = f["subscribed"].mean() * 100
avg_bal  = f["balance"].mean()

# ══════════════════════════════════════════════════════════════════
# TOP NAV
# ══════════════════════════════════════════════════════════════════
st.markdown(f"""
<div class='topbar'>
  <div class='topbar-left'>
    <div class='topbar-logo'>🏦</div>
    <div>
      <div class='topbar-title'>Customer Subscription Intelligence</div>
      <div class='topbar-sub'>Bank Marketing Analytics · Track A</div>
    </div>
  </div>
  <div class='topbar-right'>
    <span class='nav-pill active'>Overview</span>
    <span class='nav-pill muted'>Segments</span>
    <span class='nav-pill muted'>Trends</span>
    <div style='font-size:.72rem;color:#2e3a56;'>
      <span class='status-dot'></span>
      <span style='font-family:IBM Plex Mono;'>{len(f):,}</span> records
    </div>
  </div>
</div>
<div class='page-wrap'>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# KPI ROW
# ══════════════════════════════════════════════════════════════════
k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Total customers",      f"{len(f):,}")
k2.metric("Subscribers",          f"{f['subscribed'].sum():,}")
k3.metric("Subscription rate",    f"{sub_rate:.1f}%",
          delta=f"{sub_rate-11.7:+.1f}pp vs full set")
k4.metric("Avg balance",          f"€{avg_bal:,.0f}")
k5.metric("Median age",           f"{int(f['age'].median())} yrs")

st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# Q1 + Q4  ── side by side top row
# ══════════════════════════════════════════════════════════════════
col_left, col_right = st.columns([3, 2], gap="large")

# ── Q1 Job type ───────────────────────────────────────────────────
with col_left:
    st.markdown("<div class='section-label'>Question 1</div><div class='section-title'>Subscription rate by job type</div>", unsafe_allow_html=True)

    js = (f.groupby("job")["subscribed"]
            .agg(total="count", subs="sum")
            .assign(rate=lambda x: x["subs"] / x["total"] * 100)
            .sort_values("rate").reset_index())

    # Colour: highlight top 3
    n = len(js)
    colors = [P if i >= n-1 else (I if i >= n-2 else (VI if i >= n-3 else "#141d35"))
              for i in range(n)]

    fig_job = go.Figure(go.Bar(
        x=js["rate"], y=js["job"], orientation="h",
        marker=dict(color=colors, line=dict(width=0)),
        text=js["rate"].map("{:.1f}%".format),
        textposition="outside", textfont=dict(color="#2e3a56", size=10),
        hovertemplate="<b>%{y}</b><br>Rate: %{x:.1f}%<extra></extra>",
    ))
    fig_job.update_layout(**_lay(height=340))
    ax(fig_job, hide_x=True)
    st.plotly_chart(fig_job, use_container_width=True)

# ── Q4 Housing loan heatmap ───────────────────────────────────────
with col_right:
    st.markdown("<div class='section-label'>Question 4</div><div class='section-title'>Loan profile vs subscription</div>", unsafe_allow_html=True)

    cross = f.groupby(["housing","loan"])["subscribed"].mean().mul(100).unstack()
    fig_heat = px.imshow(
        cross,
        color_continuous_scale=[[0,"#060811"],[0.35,"#1e1b4b"],[0.7,P],[1.0,VI]],
        labels=dict(x="Personal loan", y="Housing loan", color="%"),
        text_auto=".1f", aspect="auto",
        zmin=0, zmax=float(cross.values.max()) * 1.15,
    )
    fig_heat.update_traces(textfont=dict(color="#e2e8f0", size=17, family="IBM Plex Mono"))
    fig_heat.update_layout(
        paper_bgcolor=BG, plot_bgcolor=BG,
        font=dict(color=FC, family="Inter"),
        margin=dict(l=4, r=4, t=8, b=4),
        height=160,
        coloraxis_showscale=False,
    )
    fig_heat.update_xaxes(tickfont=dict(color="#2e3a56", size=11), linecolor=GRID, side="bottom")
    fig_heat.update_yaxes(tickfont=dict(color="#2e3a56", size=11), linecolor=GRID)
    st.plotly_chart(fig_heat, use_container_width=True)

    # Mini bar below heatmap
    hr = (f.groupby("housing")["subscribed"]
            .agg(total="count", subs="sum")
            .assign(rate=lambda x: x["subs"]/x["total"]*100).reset_index())
    no_r  = hr.loc[hr["housing"]=="no",  "rate"].values[0] if len(hr.loc[hr["housing"]=="no"])  > 0 else 0
    yes_r = hr.loc[hr["housing"]=="yes", "rate"].values[0] if len(hr.loc[hr["housing"]=="yes"]) > 0 else 0

    fig_hb = go.Figure(go.Bar(
        x=["No loan", "Has loan"], y=[no_r, yes_r],
        marker=dict(color=[GR, RE], line=dict(width=0)),
        text=[f"{no_r:.1f}%", f"{yes_r:.1f}%"],
        textposition="outside", textfont=dict(color="#2e3a56", size=11, family="IBM Plex Mono"),
        hovertemplate="<b>%{x}</b>: %{y:.1f}%<extra></extra>",
    ))
    fig_hb.update_layout(**_lay(height=140, margin=dict(l=4,r=4,t=8,b=4)))
    ax(fig_hb, hide_x=False)
    fig_hb.update_xaxes(tickfont=dict(color="#2e3a56", size=11))
    st.plotly_chart(fig_hb, use_container_width=True)

# Insight row
top_job = js.iloc[-1]; bot_job = js.iloc[0]
ratio   = top_job["rate"] / bot_job["rate"] if bot_job["rate"] > 0 else 0
delta_h = no_r - yes_r
st.markdown(f"""
<div style='display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:24px;'>
  <div class='insight-strip'>
    <div class='insight-icon'>💼</div>
    <div><strong>{top_job['job'].title()}</strong> leads at <strong>{top_job['rate']:.1f}%</strong> —
    {ratio:.1f}× the rate of <strong>{bot_job['job'].title()}</strong> ({bot_job['rate']:.1f}%).
    RMs should prioritise retired &amp; student segments for cold outreach.</div>
  </div>
  <div class='insight-strip'>
    <div class='insight-icon'>🏠</div>
    <div>Customers <strong>without a housing loan</strong> subscribe at <strong>{no_r:.1f}%</strong>
    vs <strong>{yes_r:.1f}%</strong> with one — a <strong>{delta_h:.1f}pp gap</strong>.
    Debt-free customers are the most receptive segment.</div>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<hr class='sec-divider'>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# Q2 + Q3  ── side by side bottom row
# ══════════════════════════════════════════════════════════════════
col_a, col_b = st.columns([3, 2], gap="large")

# ── Q2 Balance ────────────────────────────────────────────────────
with col_a:
    st.markdown("<div class='section-label'>Question 2</div><div class='section-title'>Account balance vs subscription likelihood</div>", unsafe_allow_html=True)

    q2 = f[f["balance"] < f["balance"].quantile(0.99)].copy()
    q2["balance_bin"] = pd.qcut(q2["balance"], q=8, duplicates="drop")
    bs = (q2.groupby("balance_bin", observed=True)["subscribed"]
            .agg(total="count", subs="sum")
            .assign(rate=lambda x: x["subs"]/x["total"]*100).reset_index())
    bs["lbl"] = bs["balance_bin"].apply(lambda x: f"€{x.left:,.0f}–{x.right:,.0f}")

    fig_bal = go.Figure()
    fig_bal.add_trace(go.Bar(
        x=bs["lbl"], y=bs["rate"], name="Rate %",
        marker=dict(
            color=bs["rate"].tolist(),
            colorscale=[[0,"#141d35"],[0.5,I],[1.0,VI]],
            line=dict(width=0),
        ),
        hovertemplate="<b>%{x}</b><br>%{y:.1f}%<extra></extra>",
    ))
    fig_bal.add_trace(go.Scatter(
        x=bs["lbl"], y=bs["rate"].tolist(), mode="lines+markers", name="Trend",
        line=dict(color=CY, width=1.5, dash="dot"),
        marker=dict(size=4, color=CY),
        hovertemplate="%{y:.1f}%<extra>Trend</extra>",
    ))
    fig_bal.update_layout(**_lay(
        height=290,
        legend=dict(bgcolor="rgba(0,0,0,0)", orientation="h", y=1.1, x=0,
                    font=dict(color="#2e3a56", size=10)),
    ))
    ax(fig_bal, xa=-30)
    st.plotly_chart(fig_bal, use_container_width=True)

    # Box plots
    fig_box = go.Figure()
    for val, col, lbl in [("yes", GR, "Subscribed"), ("no", "#1a2340", "Not subscribed")]:
        d = q2[q2["y"]==val]["balance"]
        fig_box.add_trace(go.Box(
            x=[lbl]*len(d), y=d.tolist(), name=lbl,
            marker_color=col, line_color=col,
            marker_size=2, line_width=1.2,
            boxmean=True,
            hovertemplate=f"<b>{lbl}</b><br>%{{y:,.0f}} €<extra></extra>",
        ))
    fig_box.update_layout(**_lay(height=180, showlegend=False, margin=dict(l=4,r=4,t=8,b=4)))
    ax(fig_box)
    st.plotly_chart(fig_box, use_container_width=True)

# ── Q3 Age groups ─────────────────────────────────────────────────
with col_b:
    st.markdown("<div class='section-label'>Question 3</div><div class='section-title'>Subscription rate by age group</div>", unsafe_allow_html=True)

    ag = (f.groupby("age_group", observed=True)["subscribed"]
            .agg(total="count", subs="sum")
            .assign(rate=lambda x: x["subs"]/x["total"]*100,
                    no_subs=lambda x: x["total"]-x["subs"])
            .reset_index())
    lbls = ag["age_group"].astype(str).tolist()

    # Donut
    fig_donut = go.Figure(go.Pie(
        labels=lbls, values=ag["total"].tolist(), hole=0.6,
        marker=dict(colors=[P, I, VI, "#312e81"], line=dict(color="#060811", width=2)),
        textfont=dict(color="#c9d1e0", size=11),
        hovertemplate="<b>%{label}</b><br>%{value:,} (%{percent})<extra></extra>",
        textinfo="percent+label",
    ))
    best_age_label = ag.loc[ag["rate"].idxmax(), "age_group"]
    fig_donut.update_layout(
        paper_bgcolor=BG, plot_bgcolor=BG,
        font=dict(color=FC, family="Inter"), showlegend=False,
        margin=dict(l=0,r=0,t=0,b=0), height=200,
        annotations=[dict(text=f"<b style='color:#c9d1e0'>{best_age_label}</b><br><span style='color:#2e3a56;font-size:9px'>top group</span>",
                          x=0.5, y=0.5, showarrow=False,
                          font=dict(size=12, color="#c9d1e0"))],
    )
    st.plotly_chart(fig_donut, use_container_width=True)

    # Horizontal rate bars
    fig_age_bar = go.Figure()
    rate_colors = [P if r == ag["rate"].max() else "#1a2340" for r in ag["rate"]]
    fig_age_bar.add_trace(go.Bar(
        x=ag["rate"].tolist(), y=lbls, orientation="h",
        marker=dict(color=rate_colors, line=dict(width=0)),
        text=ag["rate"].map("{:.1f}%".format).tolist(),
        textposition="outside", textfont=dict(color="#2e3a56", size=10, family="IBM Plex Mono"),
        hovertemplate="<b>%{y}</b>: %{x:.1f}%<extra></extra>",
    ))
    # Subscriber count overlay
    fig_age_bar.add_trace(go.Scatter(
        x=ag["rate"].tolist(), y=lbls, mode="markers",
        marker=dict(
            size=ag["subs"].div(ag["subs"].max()).mul(20).add(4).tolist(),
            color=CY, opacity=0.7,
        ),
        hovertemplate="<b>%{y}</b><br>Subscribers: %{customdata:,}<extra></extra>",
        customdata=ag["subs"].tolist(), showlegend=False, name=""
    ))
    fig_age_bar.update_layout(**_lay(height=200, margin=dict(l=4,r=4,t=8,b=4)))
    ax(fig_age_bar, hide_x=True)
    st.plotly_chart(fig_age_bar, use_container_width=True)

    # Mini stat pills
    best = ag.loc[ag["rate"].idxmax()]
    yes_m = f[f["y"]=="yes"]["balance"].median()
    no_m  = f[f["y"]=="no"]["balance"].median()
    st.markdown(f"""
    <div style='display:flex;gap:8px;flex-wrap:wrap;margin-top:4px;'>
      <div style='background:#0f1525;border:1px solid #1a2340;border-radius:8px;padding:8px 12px;flex:1;'>
        <div style='font-size:.6rem;color:#2e3a56;text-transform:uppercase;letter-spacing:.1em;margin-bottom:3px;'>Top age group</div>
        <div style='font-size:.9rem;font-weight:700;color:#c9d1e0;font-family:IBM Plex Mono;'>{best['age_group']}</div>
        <div style='font-size:.72rem;color:{P};font-family:IBM Plex Mono;'>{best['rate']:.1f}%</div>
      </div>
      <div style='background:#0f1525;border:1px solid #1a2340;border-radius:8px;padding:8px 12px;flex:1;'>
        <div style='font-size:.6rem;color:#2e3a56;text-transform:uppercase;letter-spacing:.1em;margin-bottom:3px;'>Median bal · sub</div>
        <div style='font-size:.9rem;font-weight:700;color:#c9d1e0;font-family:IBM Plex Mono;'>€{yes_m:,.0f}</div>
        <div style='font-size:.72rem;color:{GR};font-family:IBM Plex Mono;'>vs €{no_m:,.0f}</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# BOTTOM — insight row + data explorer
# ══════════════════════════════════════════════════════════════════
hi_bal = bs.iloc[-1]["rate"]; lo_bal = bs.iloc[0]["rate"]
st.markdown(f"""
<div style='display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:24px;margin-bottom:8px;'>
  <div class='insight-strip'>
    <div class='insight-icon'>💰</div>
    <div>Highest balance tier converts at <strong>{hi_bal:.1f}%</strong> vs <strong>{lo_bal:.1f}%</strong> for
    the lowest — a <strong>{hi_bal-lo_bal:.1f}pp spread</strong>. Subscribers hold a meaningfully higher
    median balance (€{yes_m:,.0f} vs €{no_m:,.0f}).</div>
  </div>
  <div class='insight-strip'>
    <div class='insight-icon'>📊</div>
    <div><strong>11.7%</strong> baseline subscription rate across the full dataset.
    The current filtered view is at <strong>{sub_rate:.1f}%</strong>
    ({sub_rate-11.7:+.1f}pp). Use sidebar filters to drill into high-value segments.</div>
  </div>
</div>
""", unsafe_allow_html=True)

with st.expander("🔎  Raw data explorer — first 500 rows"):
    st.dataframe(
        f[["age","age_group","job","education","balance","housing","loan","y"]].head(500),
        use_container_width=True,
    )
    st.caption(f"{len(f):,} total records match current filters.")

st.markdown("""
<div style='margin-top:32px;padding-top:16px;border-top:1px solid #0f1525;
     text-align:center;font-size:.65rem;color:#12182e;letter-spacing:.06em;'>
  BANKMIND · VITB AI INNOVATORS HUB · TRACK A · UCI BANK MARKETING DATASET
</div>
</div>
""", unsafe_allow_html=True)
