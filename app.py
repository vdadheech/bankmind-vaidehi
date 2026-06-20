import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(
    page_title="BankMind Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,400&family=JetBrains+Mono:wght@400;500&display=swap');

/* ─── Reset ─────────────────────────────────────── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html, body, .stApp, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
    background: #f8f9fc !important;
    color: #111827;
}
.block-container { padding: 0 !important; max-width: 100% !important; }
section[data-testid="stSidebar"] { display: none; }

/* ─── Top nav ────────────────────────────────────── */
.nav {
    height: 56px;
    background: #fff;
    border-bottom: 1px solid #e5e7eb;
    display: flex; align-items: center; justify-content: space-between;
    padding: 0 28px;
    position: sticky; top: 0; z-index: 100;
}
.nav-brand { display: flex; align-items: center; gap: 10px; }
.nav-icon {
    width: 28px; height: 28px; border-radius: 7px;
    background: #111827;
    display: flex; align-items: center; justify-content: center;
    font-size: 13px;
}
.nav-name { font-size: .9rem; font-weight: 700; color: #111827; letter-spacing: -.02em; }
.nav-links { display: flex; gap: 2px; }
.nav-link {
    font-size: .78rem; font-weight: 500; padding: 5px 12px;
    border-radius: 6px; color: #6b7280; cursor: pointer;
}
.nav-link.on { background: #f3f4f6; color: #111827; font-weight: 600; }
.nav-right { display: flex; align-items: center; gap: 10px; font-size: .75rem; color: #9ca3af; }
.live-dot { width: 6px; height: 6px; background: #10b981; border-radius: 50%; display: inline-block; }

/* ─── Filter bar ─────────────────────────────────── */
.fbar {
    background: #fff;
    border-bottom: 1px solid #e5e7eb;
    padding: 10px 28px;
    display: flex; align-items: center; gap: 12px;
    flex-wrap: wrap;
}
.fbar-label { font-size: .68rem; font-weight: 700; text-transform: uppercase;
              letter-spacing: .1em; color: #9ca3af; margin-right: 4px; }

/* ─── Main canvas ────────────────────────────────── */
.canvas { padding: 24px 28px 40px; }

/* ─── KPI strip ──────────────────────────────────── */
.kpi-grid { display: grid; grid-template-columns: repeat(5,1fr); gap: 12px; margin-bottom: 24px; }
.kpi {
    background: #fff;
    border: 1px solid #e5e7eb;
    border-radius: 10px;
    padding: 16px 18px;
    position: relative;
    overflow: hidden;
}
.kpi-label { font-size: .65rem; font-weight: 700; text-transform: uppercase;
             letter-spacing: .12em; color: #9ca3af; margin-bottom: 6px; }
.kpi-val   { font-size: 1.6rem; font-weight: 800; color: #111827; letter-spacing: -.03em;
             font-family: 'JetBrains Mono', monospace; line-height: 1; }
.kpi-sub   { font-size: .7rem; margin-top: 5px; color: #9ca3af; }
.kpi-sub b { color: #111827; }
.kpi-accent { position: absolute; bottom: 0; left: 0; right: 0; height: 3px; }
.kpi:nth-child(1) .kpi-accent { background: #6366f1; }
.kpi:nth-child(2) .kpi-accent { background: #10b981; }
.kpi:nth-child(3) .kpi-accent { background: #f59e0b; }
.kpi:nth-child(4) .kpi-accent { background: #3b82f6; }
.kpi:nth-child(5) .kpi-accent { background: #ec4899; }
.kpi-up   { color: #10b981 !important; }
.kpi-down { color: #ef4444 !important; }

/* ─── Chart card ─────────────────────────────────── */
.card {
    background: #fff;
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 16px;
    height: 100%;
}
.card-header { display: flex; align-items: flex-start; justify-content: space-between; margin-bottom: 4px; }
.card-title  { font-size: .82rem; font-weight: 700; color: #111827; }
.card-sub    { font-size: .72rem; color: #9ca3af; margin-bottom: 14px; }
.card-tag    {
    font-size: .6rem; font-weight: 700; text-transform: uppercase; letter-spacing: .1em;
    padding: 2px 8px; border-radius: 4px; background: #f3f4f6; color: #6b7280;
}

/* ─── Insight box ────────────────────────────────── */
.insight {
    background: #fafafa;
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    padding: 12px 14px;
    font-size: .76rem;
    color: #6b7280;
    line-height: 1.6;
    margin-top: 12px;
}
.insight strong { color: #111827; }
.insight-row { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 20px; }

/* ─── Section header ─────────────────────────────── */
.sec { display: flex; align-items: center; gap: 10px; margin: 24px 0 16px; }
.sec-line { flex: 1; height: 1px; background: #e5e7eb; }
.sec-text { font-size: .65rem; font-weight: 700; text-transform: uppercase;
            letter-spacing: .14em; color: #d1d5db; white-space: nowrap; }

/* ─── Stat pills ─────────────────────────────────── */
.pills { display: flex; gap: 8px; flex-wrap: wrap; margin-top: 10px; }
.pill {
    background: #f3f4f6; border-radius: 8px; padding: 8px 12px;
    font-size: .72rem; color: #6b7280; flex: 1; min-width: 100px;
}
.pill-val { font-size: 1rem; font-weight: 700; color: #111827; font-family:'JetBrains Mono',monospace; }
.pill-lbl { font-size: .6rem; text-transform: uppercase; letter-spacing: .08em; color: #9ca3af; margin-bottom: 2px; }

/* ─── Selectbox tweaks ───────────────────────────── */
[data-testid="stSidebar"] { display: none !important; }
[data-baseweb="select"] > div {
    background: #f9fafb !important; border: 1px solid #e5e7eb !important;
    border-radius: 7px !important; font-size: .78rem !important; color: #374151 !important;
    min-height: 32px !important;
}
.stSelectbox label, [data-testid="stWidgetLabel"] {
    font-size: .65rem !important; font-weight: 700 !important;
    text-transform: uppercase; letter-spacing: .1em; color: #9ca3af !important;
}
[data-testid="stSlider"] label {
    font-size: .65rem !important; font-weight: 700 !important;
    text-transform: uppercase; letter-spacing: .08em; color: #9ca3af !important;
}
[data-testid="stSlider"] > div > div { color: #6366f1 !important; }
div[data-baseweb="slider"] div[role="slider"] { background: #6366f1 !important; border-color: #6366f1 !important; }
div[data-baseweb="slider"] [data-testid="stSliderTrackFill"] { background: #6366f1 !important; }

/* ─── Dataframe ──────────────────────────────────── */
[data-testid="stDataFrame"] iframe { border-radius: 8px !important; }
[data-testid="stDataFrame"] { border: 1px solid #e5e7eb; border-radius: 8px; overflow: hidden; }

/* ─── Footer ─────────────────────────────────────── */
.foot { border-top: 1px solid #f3f4f6; padding: 20px 0 4px; text-align: center;
        font-size: .65rem; color: #d1d5db; letter-spacing: .08em; }
</style>
""", unsafe_allow_html=True)

# ── Palette ───────────────────────────────────────────────────────
INDIGO  = "#6366f1"
GREEN   = "#10b981"
AMBER   = "#f59e0b"
BLUE    = "#3b82f6"
PINK    = "#ec4899"
RED     = "#ef4444"
SLATE   = "#64748b"
GRID    = "#f1f5f9"
BG      = "rgba(0,0,0,0)"

def lay(**kw):
    d = dict(
        paper_bgcolor=BG, plot_bgcolor=BG,
        font=dict(family="Inter, sans-serif", color="#6b7280", size=11),
        title_font=dict(family="Inter", color="#111827", size=13),
        hoverlabel=dict(bgcolor="#111827", bordercolor="#374151",
                        font_color="#f9fafb", font_family="Inter", font_size=12),
        margin=dict(l=2, r=2, t=4, b=2),
    )
    d.update(kw)
    return d

def axes(fig, xa=0):
    fig.update_xaxes(gridcolor=GRID, linecolor="#e5e7eb", zeroline=False,
                     tickfont=dict(color="#9ca3af", size=10), tickangle=xa,
                     automargin=True)
    fig.update_yaxes(gridcolor=GRID, linecolor="#e5e7eb", zeroline=False,
                     tickfont=dict(color="#9ca3af", size=10), automargin=True)
    return fig

# ── Data ──────────────────────────────────────────────────────────
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
    st.error("⚠️  Add `bank-full.csv` to the repo root."); st.stop()

# ─────────────────────────────────────────────────────────────────
# NAV
# ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="nav">
  <div class="nav-brand">
    <div class="nav-icon">📊</div>
    <span class="nav-name">BankMind</span>
  </div>
  <div class="nav-links">
    <span class="nav-link on">Overview</span>
    <span class="nav-link">Segments</span>
    <span class="nav-link">Trends</span>
    <span class="nav-link">Export</span>
  </div>
  <div class="nav-right">
    <span class="live-dot"></span> Live · UCI Bank Marketing
  </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────
# FILTER BAR (inline, no sidebar)
# ─────────────────────────────────────────────────────────────────
st.markdown("""
<div style='background:#fff;border-bottom:1px solid #e5e7eb;padding:8px 28px 0;
     display:flex;align-items:center;gap:8px;'>
  <span style='font-size:.65rem;font-weight:700;text-transform:uppercase;
       letter-spacing:.12em;color:#9ca3af;white-space:nowrap;margin-right:4px;'>
    Filters
  </span>
</div>
""", unsafe_allow_html=True)

fc1, fc2, fc3, fc4, fc5 = st.columns([1, 1, 1, 2, 1])
with fc1:
    sel_age = st.selectbox("Age group", ["All"] + list(df["age_group"].cat.categories),
                           label_visibility="visible")
with fc2:
    sel_job = st.selectbox("Job type", ["All"] + sorted(df["job"].unique()),
                           label_visibility="visible")
with fc3:
    sel_edu = st.selectbox("Education", ["All"] + sorted(df["education"].unique()),
                           label_visibility="visible")
with fc4:
    # UCI dataset has negative balances (overdrafts) — show full real range but label clearly
    b0 = int(df["balance"].min())
    b1 = int(df["balance"].max())
    bal = st.slider(
        f"Account balance (€{b0:,} to €{b1:,})",
        min_value=b0, max_value=b1, value=(b0, b1),
    )
with fc5:
    st.markdown(
        "<div style='padding-top:28px;font-size:.7rem;color:#9ca3af;'>"
        "⚠️ Negative = overdraft</div>",
        unsafe_allow_html=True,
    )

# ─────────────────────────────────────────────────────────────────
# FILTER
# ─────────────────────────────────────────────────────────────────
f = df.copy()
if sel_age != "All": f = f[f["age_group"] == sel_age]
if sel_job != "All": f = f[f["job"]       == sel_job]
if sel_edu != "All": f = f[f["education"] == sel_edu]
f = f[f["balance"].between(bal[0], bal[1])]
if len(f) == 0:
    st.warning("No records match — adjust the filters above."); st.stop()

sub_rate = f["subscribed"].mean() * 100
avg_bal  = f["balance"].mean()
yes_med  = f[f["y"]=="yes"]["balance"].median()
no_med   = f[f["y"]=="no"]["balance"].median()
delta_pp = sub_rate - 11.7

# ─────────────────────────────────────────────────────────────────
# KPI STRIP
# ─────────────────────────────────────────────────────────────────
sign   = "▲" if delta_pp >= 0 else "▼"
dcolor = "kpi-up" if delta_pp >= 0 else "kpi-down"

st.markdown(f"""
<div class="canvas">
<div class="kpi-grid">
  <div class="kpi">
    <div class="kpi-label">Total customers</div>
    <div class="kpi-val">{len(f):,}</div>
    <div class="kpi-sub">of <b>{len(df):,}</b> total records</div>
    <div class="kpi-accent"></div>
  </div>
  <div class="kpi">
    <div class="kpi-label">Subscribers</div>
    <div class="kpi-val">{f['subscribed'].sum():,}</div>
    <div class="kpi-sub">confirmed y = yes</div>
    <div class="kpi-accent"></div>
  </div>
  <div class="kpi">
    <div class="kpi-label">Subscription rate</div>
    <div class="kpi-val">{sub_rate:.1f}%</div>
    <div class="kpi-sub"><b class="{dcolor}">{sign} {abs(delta_pp):.1f}pp</b> vs 11.7% baseline</div>
    <div class="kpi-accent"></div>
  </div>
  <div class="kpi">
    <div class="kpi-label">Avg balance</div>
    <div class="kpi-val">€{avg_bal:,.0f}</div>
    <div class="kpi-sub">mean account balance</div>
    <div class="kpi-accent"></div>
  </div>
  <div class="kpi">
    <div class="kpi-label">Median age</div>
    <div class="kpi-val">{int(f['age'].median())}</div>
    <div class="kpi-sub">years old</div>
    <div class="kpi-accent"></div>
  </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────
# ROW 1  ─  Q1 (wide) + Q4 pie (narrow)
# ─────────────────────────────────────────────────────────────────
r1a, r1b = st.columns([5, 3], gap="medium")

# Q1 — Job type
with r1a:
    st.markdown("""
    <div class="card">
      <div class="card-header">
        <div>
          <div class="card-title">Subscription rate by job type</div>
          <div class="card-sub">Which customer professions convert most reliably?</div>
        </div>
        <div class="card-tag">Q1</div>
      </div>
    """, unsafe_allow_html=True)

    js = (f.groupby("job")["subscribed"]
            .agg(total="count", subs="sum")
            .assign(rate=lambda x: x["subs"]/x["total"]*100)
            .sort_values("rate").reset_index())

    palette = [GRID]*len(js)
    palette[-1] = INDIGO
    if len(js) > 1: palette[-2] = "#a5b4fc"
    if len(js) > 2: palette[-3] = "#c7d2fe"

    fig = go.Figure(go.Bar(
        x=js["rate"], y=js["job"], orientation="h",
        marker=dict(color=palette, line=dict(width=0)),
        text=js["rate"].map("{:.1f}%".format),
        textposition="outside",
        cliponaxis=False,
        textfont=dict(color="#9ca3af", size=10, family="JetBrains Mono"),
        hovertemplate="<b>%{y}</b><br>%{x:.1f}% subscription rate<extra></extra>",
    ))
    fig.update_layout(**lay(height=300, margin=dict(l=4, r=44, t=8, b=4)))
    fig.update_xaxes(showgrid=False, showticklabels=False, linecolor="#e5e7eb",
                      zeroline=False, range=[0, js["rate"].max() * 1.18])
    fig.update_yaxes(gridcolor=GRID, linecolor="#e5e7eb", zeroline=False,
                     tickfont=dict(color="#374151", size=11), automargin=True)

    top_j = js.iloc[-1]; bot_j = js.iloc[0]
    ratio  = top_j["rate"]/bot_j["rate"] if bot_j["rate"] > 0 else 0

    st.plotly_chart(fig, use_container_width=True)
    st.markdown(f"""
    <div class="insight">
      <strong>{top_j['job'].title()}</strong> leads at <strong>{top_j['rate']:.1f}%</strong> — 
      {ratio:.1f}× the rate of <strong>{bot_j['job'].title()}</strong> ({bot_j['rate']:.1f}%).
      Students and retired customers are structurally more open to fixed-income products. 
      RM outreach should prioritise these segments first.
    </div>
    </div>
    """, unsafe_allow_html=True)

# Q4 — Housing loan
with r1b:
    st.markdown("""
    <div class="card">
      <div class="card-header">
        <div>
          <div class="card-title">Housing loan impact</div>
          <div class="card-sub">Does existing debt reduce new product uptake?</div>
        </div>
        <div class="card-tag">Q4</div>
      </div>
    """, unsafe_allow_html=True)

    hr = (f.groupby("housing")["subscribed"]
            .agg(total="count", subs="sum")
            .assign(rate=lambda x: x["subs"]/x["total"]*100).reset_index())
    no_r  = hr.loc[hr["housing"]=="no",  "rate"].values[0] if (hr["housing"]=="no").any()  else 0
    yes_r = hr.loc[hr["housing"]=="yes", "rate"].values[0] if (hr["housing"]=="yes").any() else 0

    # Donut
    fig_d = go.Figure(go.Pie(
        labels=["No loan", "Has loan"],
        values=[no_r, yes_r],
        hole=0.68,
        marker=dict(colors=[GREEN, "#fee2e2"], line=dict(color="#fff", width=3)),
        textinfo="none",
        hovertemplate="<b>%{label}</b><br>%{value:.1f}%<extra></extra>",
        direction="clockwise", sort=False,
    ))
    fig_d.update_layout(
        paper_bgcolor=BG, plot_bgcolor=BG,
        font=dict(family="Inter"), showlegend=False,
        margin=dict(l=0,r=0,t=0,b=0), height=160,
        annotations=[dict(
            text=f"<b style='font-size:22px;color:#111827'>{no_r:.0f}%</b><br><span style='font-size:11px;color:#9ca3af'>no-loan rate</span>",
            x=0.5, y=0.5, showarrow=False, align="center",
        )],
    )
    st.plotly_chart(fig_d, use_container_width=True)

    # Cross tab bars
    cross_df = (f.groupby(["housing","loan"])["subscribed"]
                 .mean().mul(100).reset_index()
                 .rename(columns={"subscribed":"rate"}))
    cross_df["label"] = cross_df.apply(
        lambda r: ("✓ No housing" if r["housing"]=="no" else "✗ Housing")
                + (" + no personal" if r["loan"]=="no" else " + personal"), axis=1)
    cross_df = cross_df.sort_values("rate", ascending=True)

    colors_c = [GREEN if "✓" in l and "no personal" in l
                else (RED if "✗" in l and "personal" in l
                else AMBER) for l in cross_df["label"]]

    fig_cb = go.Figure(go.Bar(
        y=cross_df["label"], x=cross_df["rate"], orientation="h",
        marker=dict(color=colors_c, line=dict(width=0)),
        text=cross_df["rate"].map("{:.1f}%".format),
        textposition="outside",
        cliponaxis=False,
        textfont=dict(color="#9ca3af", size=10, family="JetBrains Mono"),
        hovertemplate="<b>%{y}</b><br>%{x:.1f}%<extra></extra>",
    ))
    fig_cb.update_layout(**lay(height=160, margin=dict(l=4, r=44, t=8, b=4)))
    fig_cb.update_xaxes(showgrid=False, showticklabels=False, linecolor="#e5e7eb",
                         zeroline=False, range=[0, cross_df["rate"].max() * 1.25])
    fig_cb.update_yaxes(tickfont=dict(color="#374151", size=9.5), linecolor="#e5e7eb",
                         zeroline=False, gridcolor=GRID, automargin=True)

    st.plotly_chart(fig_cb, use_container_width=True)
    st.markdown(f"""
    <div class="insight">
      Customers <strong>without any loans</strong> subscribe at <strong>{cross_df['rate'].max():.1f}%</strong>.
      Those with both loans: just <strong>{cross_df['rate'].min():.1f}%</strong>.
      Debt-free customers are <strong>{cross_df['rate'].max()/max(cross_df['rate'].min(),0.1):.1f}×</strong> more likely to convert.
    </div>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────
# ROW 2  ─  Q2 balance (wide) + Q3 age (narrow)
# ─────────────────────────────────────────────────────────────────
st.markdown('<div class="sec"><div class="sec-line"></div><div class="sec-text">Financial profile &amp; demographics</div><div class="sec-line"></div></div>', unsafe_allow_html=True)

r2a, r2b = st.columns([5, 3], gap="medium")

# Q2 — Balance
with r2a:
    st.markdown("""
    <div class="card">
      <div class="card-header">
        <div>
          <div class="card-title">Account balance vs subscription likelihood</div>
          <div class="card-sub">Does account wealth predict willingness to subscribe?</div>
        </div>
        <div class="card-tag">Q2</div>
      </div>
    """, unsafe_allow_html=True)

    q2 = f[f["balance"] < f["balance"].quantile(0.99)].copy()
    q2["balance_bin"] = pd.qcut(q2["balance"], q=8, duplicates="drop")
    bs = (q2.groupby("balance_bin", observed=True)["subscribed"]
            .agg(total="count", subs="sum")
            .assign(rate=lambda x: x["subs"]/x["total"]*100).reset_index())
    bs["lbl"] = bs["balance_bin"].apply(lambda x: f"€{x.left:,.0f}–{x.right:,.0f}")

    fig_b = go.Figure()
    # Background bars (customer count, normalised)
    fig_b.add_trace(go.Bar(
        x=bs["lbl"], y=bs["total"] / bs["total"].max() * bs["rate"].max() * 0.6,
        marker=dict(color="#f3f4f6", line=dict(width=0)),
        name="Volume (scaled)", hoverinfo="skip",
    ))
    # Rate bars
    fig_b.add_trace(go.Bar(
        x=bs["lbl"], y=bs["rate"],
        marker=dict(
            color=bs["rate"].tolist(),
            colorscale=[[0,"#e0e7ff"],[0.5,INDIGO],[1.0,"#312e81"]],
            line=dict(width=0),
        ),
        name="Rate %",
        hovertemplate="<b>%{x}</b><br>Subscription rate: %{y:.1f}%<extra></extra>",
    ))
    # Trend line
    fig_b.add_trace(go.Scatter(
        x=bs["lbl"], y=bs["rate"].tolist(), mode="lines+markers",
        line=dict(color=AMBER, width=2),
        marker=dict(size=5, color=AMBER, line=dict(color="#fff", width=1.5)),
        name="Trend",
        hovertemplate="%{y:.1f}%<extra>Trend</extra>",
    ))
    fig_b.update_layout(**lay(
        height=260, barmode="overlay",
        legend=dict(bgcolor="rgba(0,0,0,0)", orientation="h", y=1.15, x=0,
                    font=dict(color="#9ca3af", size=10)),
    ))
    axes(fig_b, xa=-30)

    st.plotly_chart(fig_b, use_container_width=True)

    # Median comparison pills
    st.markdown(f"""
    <div class="pills">
      <div class="pill">
        <div class="pill-lbl">Subscriber median balance</div>
        <div class="pill-val">€{yes_med:,.0f}</div>
      </div>
      <div class="pill">
        <div class="pill-lbl">Non-subscriber median balance</div>
        <div class="pill-val" style="color:#6b7280">€{no_med:,.0f}</div>
      </div>
      <div class="pill">
        <div class="pill-lbl">Highest bracket rate</div>
        <div class="pill-val" style="color:{INDIGO}">{bs['rate'].max():.1f}%</div>
      </div>
    </div>
    <div class="insight" style="margin-top:10px">
      Higher balance tiers convert significantly better. The top bracket ({bs.iloc[-1]['lbl']}) 
      subscribes at <strong>{bs['rate'].max():.1f}%</strong> vs <strong>{bs['rate'].min():.1f}%</strong> 
      for the lowest. RMs should flag <strong>high-balance, debt-free</strong> customers as priority leads.
    </div>
    </div>
    """, unsafe_allow_html=True)

# Q3 — Age groups
with r2b:
    st.markdown("""
    <div class="card">
      <div class="card-header">
        <div>
          <div class="card-title">Age group breakdown</div>
          <div class="card-sub">Subscription rate across life stages</div>
        </div>
        <div class="card-tag">Q3</div>
      </div>
    """, unsafe_allow_html=True)

    ag = (f.groupby("age_group", observed=True)["subscribed"]
            .agg(total="count", subs="sum")
            .assign(rate=lambda x: x["subs"]/x["total"]*100,
                    no_subs=lambda x: x["total"]-x["subs"])
            .reset_index())
    lbls = ag["age_group"].astype(str).tolist()
    best = ag.loc[ag["rate"].idxmax()]

    # Lollipop chart
    fig_ag = go.Figure()
    for _, row in ag.iterrows():
        col = INDIGO if row["age_group"] == best["age_group"] else "#e0e7ff"
        # Stem
        fig_ag.add_shape(type="line",
            x0=0, x1=row["rate"], y0=str(row["age_group"]), y1=str(row["age_group"]),
            line=dict(color=col, width=2))
    # Dots
    fig_ag.add_trace(go.Scatter(
        x=ag["rate"].tolist(), y=lbls,
        mode="markers+text",
        marker=dict(
            size=16,
            color=[INDIGO if l == str(best["age_group"]) else "#e0e7ff" for l in lbls],
            line=dict(color="#fff", width=2),
        ),
        text=ag["rate"].map("{:.1f}%".format).tolist(),
        textposition="middle right",
        textfont=dict(color="#374151", size=10, family="JetBrains Mono"),
        hovertemplate="<b>%{y}</b><br>%{x:.1f}%<extra></extra>",
    ))
    fig_ag.update_layout(**lay(height=200, margin=dict(l=4,r=60,t=4,b=4)))
    fig_ag.update_xaxes(showgrid=True, gridcolor=GRID, linecolor="#e5e7eb", zeroline=False,
                        range=[0, ag["rate"].max()*1.5], showticklabels=False)
    fig_ag.update_yaxes(gridcolor=GRID, linecolor="#e5e7eb", zeroline=False,
                        tickfont=dict(color="#374151", size=12))
    st.plotly_chart(fig_ag, use_container_width=True)

    # Stacked volume bar
    fig_sv = go.Figure()
    fig_sv.add_trace(go.Bar(
        name="Subscribed", x=ag["subs"].tolist(), y=lbls, orientation="h",
        marker=dict(color=INDIGO, line=dict(width=0)),
        hovertemplate="<b>%{y}</b><br>Subscribed: %{x:,}<extra></extra>",
    ))
    fig_sv.add_trace(go.Bar(
        name="Not subscribed", x=ag["no_subs"].tolist(), y=lbls, orientation="h",
        marker=dict(color="#f3f4f6", line=dict(color="#e5e7eb", width=1)),
        hovertemplate="<b>%{y}</b><br>Not subscribed: %{x:,}<extra></extra>",
    ))
    fig_sv.update_layout(**lay(
        height=180, barmode="stack",
        legend=dict(bgcolor="rgba(0,0,0,0)", orientation="h", y=1.15, x=0,
                    font=dict(color="#9ca3af", size=10)),
        margin=dict(l=4,r=4,t=24,b=4),
    ))
    fig_sv.update_xaxes(showgrid=True, gridcolor=GRID, linecolor="#e5e7eb", zeroline=False,
                         tickfont=dict(color="#9ca3af", size=9))
    fig_sv.update_yaxes(gridcolor=GRID, linecolor="#e5e7eb", zeroline=False,
                         tickfont=dict(color="#374151", size=11))
    st.plotly_chart(fig_sv, use_container_width=True)

    st.markdown(f"""
    <div class="insight">
      <strong>{best['age_group']}</strong> has the highest rate at <strong>{best['rate']:.1f}%</strong>.
      Young adults are forming new banking habits; older customers are focused on wealth preservation —
      both make natural fits for term deposits.
    </div>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────────
with st.expander("🔎  Raw data explorer"):
    st.dataframe(
        f[["age","age_group","job","education","balance","housing","loan","y"]].head(500),
        use_container_width=True,
    )
    st.caption(f"Showing first 500 of {len(f):,} filtered records.")

st.markdown("""
<div class="foot">BANKMIND · VITB AI INNOVATORS HUB · TRACK A · UCI BANK MARKETING DATASET</div>
</div>
""", unsafe_allow_html=True)
