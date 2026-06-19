import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="BankMind", page_icon="🏦", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=IBM+Plex+Mono:wght@400;600&display=swap');
html, body, [class*="css"], .stApp { font-family: 'Inter', sans-serif !important; background: #07090f !important; color: #e2e8f0; }
.block-container { padding: 1.5rem 2rem 2rem 2rem !important; max-width: 100% !important; }
[data-testid="stSidebar"] { background: #0c0f1a !important; border-right: 1px solid #1e2540; }
[data-testid="stSidebar"] * { color: #8892b0 !important; font-family: 'Inter', sans-serif !important; }
[data-testid="stSidebar"] h1,[data-testid="stSidebar"] h2,[data-testid="stSidebar"] h3 { color: #ccd6f6 !important; }
[data-testid="stSidebar"] .stSelectbox label,[data-testid="stSidebar"] .stSlider label { font-size:0.7rem !important; text-transform:uppercase; letter-spacing:0.1em; color:#4a5568 !important; font-weight:600 !important; }
[data-testid="stSidebar"] [data-baseweb="select"] > div { background:#111827 !important; border-color:#1e2540 !important; border-radius:8px !important; }
[data-testid="metric-container"] { background:#0f1629 !important; border:1px solid #1e2a4a !important; border-radius:14px !important; padding:1.1rem 1.4rem !important; }
[data-testid="metric-container"] label { color:#4a5568 !important; font-size:0.7rem !important; font-weight:600 !important; text-transform:uppercase; letter-spacing:0.1em; }
[data-testid="metric-container"] [data-testid="stMetricValue"] { color:#e2e8f0 !important; font-family:'IBM Plex Mono',monospace !important; font-size:1.75rem !important; font-weight:600 !important; }
[data-testid="metric-container"] [data-testid="stMetricDelta"] { font-size:0.78rem !important; }
h1 { font-size:1.6rem !important; font-weight:700 !important; color:#ccd6f6 !important; letter-spacing:-0.02em; }
h2,h3 { color:#a8b2d8 !important; font-weight:600 !important; }
.stag { display:inline-block; background:#1a1f3c; color:#7c3aed; font-size:0.65rem; font-weight:700; letter-spacing:0.14em; text-transform:uppercase; padding:3px 10px; border-radius:20px; border:1px solid #2d2260; margin-bottom:6px; }
.ibox { background:#0c0f1a; border-left:2px solid #7c3aed; border-radius:0 10px 10px 0; padding:0.85rem 1.1rem; margin:0.4rem 0 0.8rem; font-size:0.83rem; line-height:1.6; color:#64748b; }
.ibox strong { color:#a8b2d8; }
hr { border-color:#1e2540 !important; margin:1.5rem 0 !important; }
::-webkit-scrollbar { width:4px; } ::-webkit-scrollbar-track { background:#07090f; } ::-webkit-scrollbar-thumb { background:#1e2540; border-radius:4px; }
</style>
""", unsafe_allow_html=True)

# ── Colours ───────────────────────────────────────────────────────────────────
PURPLE = "#7c3aed"; INDIGO = "#6366f1"; VIOLET = "#a78bfa"
CYAN   = "#22d3ee"; GREEN  = "#10b981"; RED    = "#f43f5e"
GRID   = "#1e2540"; PAPER  = "rgba(0,0,0,0)"; FONT   = "#8892b0"

def _layout(**kw):
    """Return a clean layout dict — caller owns every key, no shared dict conflicts."""
    base = dict(
        paper_bgcolor=PAPER, plot_bgcolor=PAPER,
        font=dict(color=FONT, family="Inter, sans-serif"),
        title_font=dict(color="#a8b2d8", size=14),
        hoverlabel=dict(bgcolor="#111827", bordercolor="#1e2540",
                        font_color="#e2e8f0", font_family="Inter"),
        margin=dict(l=8, r=8, t=36, b=8),
    )
    base.update(kw)   # caller overrides win — no duplicate risk
    return base

def _axes(fig, x_angle=0):
    fig.update_xaxes(gridcolor=GRID, linecolor=GRID,
                     tickfont=dict(color="#334155", size=11), tickangle=x_angle)
    fig.update_yaxes(gridcolor=GRID, linecolor=GRID,
                     tickfont=dict(color="#334155", size=11))
    return fig

# ── Data ──────────────────────────────────────────────────────────────────────
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
    st.error("⚠️  Place `bank-full.csv` in the repo root and rerun."); st.stop()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("<div style='padding:1rem 0 0.5rem'><div style='font-size:1.1rem;font-weight:700;color:#ccd6f6'>🏦 BankMind</div><div style='font-size:0.7rem;color:#2d3a5e;margin-top:2px;text-transform:uppercase;letter-spacing:.1em'>RM Intelligence · Track A</div></div>", unsafe_allow_html=True)
    st.divider()
    sel_age = st.selectbox("Age group",  ["All"] + list(df["age_group"].cat.categories))
    sel_job = st.selectbox("Job type",   ["All"] + sorted(df["job"].unique()))
    sel_edu = st.selectbox("Education",  ["All"] + sorted(df["education"].unique()))
    b0, b1  = int(df["balance"].min()), int(df["balance"].max())
    bal     = st.slider("Balance (€)", b0, b1, (b0, b1))
    st.divider()
    st.markdown(f"<div style='font-size:.72rem;color:#2d3a5e;line-height:1.7'>UCI Bank Marketing<br>{len(df):,} customer records</div>", unsafe_allow_html=True)

# ── Filter ────────────────────────────────────────────────────────────────────
f = df.copy()
if sel_age != "All": f = f[f["age_group"] == sel_age]
if sel_job != "All": f = f[f["job"]       == sel_job]
if sel_edu != "All": f = f[f["education"] == sel_edu]
f = f[f["balance"].between(bal[0], bal[1])]

if len(f) == 0:
    st.warning("No records match the current filters. Adjust the sidebar."); st.stop()

# ── Header + KPIs ─────────────────────────────────────────────────────────────
st.markdown("## Customer Subscription Intelligence")
st.markdown(f"<div style='font-size:.82rem;color:#334155;margin-top:-8px;margin-bottom:16px'>{len(f):,} of {len(df):,} records</div>", unsafe_allow_html=True)

k1,k2,k3,k4 = st.columns(4)
sub_rate = f["subscribed"].mean() * 100
k1.metric("Total customers",     f"{len(f):,}")
k2.metric("Subscribers (y=yes)", f"{f['subscribed'].sum():,}")
k3.metric("Subscription rate",   f"{sub_rate:.1f}%", delta=f"{sub_rate-11.7:+.1f}pp vs baseline")
k4.metric("Avg account balance", f"€{f['balance'].mean():,.0f}")
st.markdown("<br>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# Q1 – Job type
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<span class="stag">Q1</span>', unsafe_allow_html=True)
st.markdown("### Job types vs subscription rate")

js = (f.groupby("job")["subscribed"]
        .agg(total="count", subs="sum")
        .assign(rate=lambda x: x["subs"] / x["total"] * 100)
        .sort_values("rate").reset_index())

ca, cb = st.columns([3,2])
with ca:
    fig = go.Figure(go.Bar(
        x=js["rate"], y=js["job"], orientation="h",
        marker=dict(color=[PURPLE if r == js["rate"].max() else "#1e2a4a" for r in js["rate"]],
                    line=dict(width=0)),
        text=js["rate"].map("{:.1f}%".format),
        textposition="outside", textfont=dict(color="#64748b", size=11),
        hovertemplate="<b>%{y}</b>: %{x:.1f}%<extra></extra>",
    ))
    fig.update_layout(**_layout(height=370))
    fig.update_xaxes(showgrid=False, showticklabels=False, linecolor=GRID)
    fig.update_yaxes(gridcolor=GRID, linecolor=GRID, tickfont=dict(color="#334155", size=11))
    st.plotly_chart(fig, use_container_width=True)

with cb:
    top = js.iloc[-1]; bot = js.iloc[0]
    second = js.iloc[-2] if len(js) >= 2 else top
    ratio  = top["rate"] / bot["rate"] if bot["rate"] > 0 else 0
    st.markdown(f"""<div class='ibox'>
    <strong>Highest · {top['job'].title()}</strong> — {top['rate']:.1f}%<br>
    <strong>Lowest · {bot['job'].title()}</strong> — {bot['rate']:.1f}%<br><br>
    Top segment converts at <strong>{ratio:.1f}×</strong> the rate of the lowest.
    RMs should prioritise <strong>{top['job'].title()}</strong> and
    <strong>{second['job'].title()}</strong> outreach.
    </div>""", unsafe_allow_html=True)
    top5 = js.nlargest(5,"rate")[["job","rate","total"]].copy()
    top5.columns = ["Job","Rate","Customers"]
    top5["Rate"] = top5["Rate"].map("{:.1f}%".format)
    st.dataframe(top5, hide_index=True, use_container_width=True)

st.divider()

# ══════════════════════════════════════════════════════════════════════════════
# Q2 – Balance
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<span class="stag">Q2</span>', unsafe_allow_html=True)
st.markdown("### Account balance vs likelihood to subscribe")

q2 = f[f["balance"] < f["balance"].quantile(0.99)].copy()
q2["balance_bin"] = pd.qcut(q2["balance"], q=8, duplicates="drop")
bs = (q2.groupby("balance_bin", observed=True)["subscribed"]
        .agg(total="count", subs="sum")
        .assign(rate=lambda x: x["subs"] / x["total"] * 100).reset_index())
bs["lbl"] = bs["balance_bin"].apply(lambda x: f"€{x.left:,.0f}–{x.right:,.0f}")

ca, cb = st.columns([3,2])
with ca:
    fig2 = go.Figure()
    fig2.add_trace(go.Bar(
        x=bs["lbl"], y=bs["rate"],
        marker=dict(color=bs["rate"].tolist(),
                    colorscale=[[0,"#1a1040"],[0.5,PURPLE],[1.0,VIOLET]],
                    line=dict(width=0)),
        hovertemplate="<b>%{x}</b><br>Rate: %{y:.1f}%<extra></extra>", name="Rate",
    ))
    fig2.add_trace(go.Scatter(
        x=bs["lbl"], y=bs["rate"].tolist(),
        mode="lines+markers",
        line=dict(color=CYAN, width=1.5, dash="dot"),
        marker=dict(size=5, color=CYAN), name="Trend",
        hovertemplate="%{y:.1f}%<extra>Trend</extra>",
    ))
    fig2.update_layout(**_layout(
        height=320,
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color=FONT), orientation="h", y=1.1, x=0),
    ))
    _axes(fig2, x_angle=-25)
    st.plotly_chart(fig2, use_container_width=True)

with cb:
    hi = bs.iloc[-1]["rate"]; lo = bs.iloc[0]["rate"]
    yes_med = f[f["y"]=="yes"]["balance"].median()
    no_med  = f[f["y"]=="no"]["balance"].median()
    st.markdown(f"""<div class='ibox'>
    Highest bracket: <strong>{hi:.1f}%</strong> · Lowest: <strong>{lo:.1f}%</strong><br><br>
    Median balance — subscribers: <strong>€{yes_med:,.0f}</strong><br>
    Median balance — non-subscribers: <strong>€{no_med:,.0f}</strong><br><br>
    Flag <strong>high-balance + no-loan</strong> customers as prime targets.
    </div>""", unsafe_allow_html=True)
    fig_box = px.box(q2, x="y", y="balance", color="y",
                     color_discrete_map={"yes": GREEN, "no": "#1e2a4a"},
                     labels={"y":"","balance":"Balance (€)"})
    fig_box.update_traces(marker_size=3, line_width=1.2)
    fig_box.update_layout(**_layout(height=220, showlegend=False, title="Balance by outcome",
                                    title_font=dict(color="#a8b2d8", size=13)))
    _axes(fig_box)
    st.plotly_chart(fig_box, use_container_width=True)

st.divider()

# ══════════════════════════════════════════════════════════════════════════════
# Q3 – Age groups  (dual-axis chart — layout built manually, no helper spread)
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<span class="stag">Q3</span>', unsafe_allow_html=True)
st.markdown("### Subscription rate across age groups")

ag = (f.groupby("age_group", observed=True)["subscribed"]
        .agg(total="count", subs="sum")
        .assign(rate=lambda x: x["subs"] / x["total"] * 100,
                no_subs=lambda x: x["total"] - x["subs"])
        .reset_index())
lbls = ag["age_group"].astype(str).tolist()

ca, cb = st.columns([2,3])
with ca:
    fig_pie = go.Figure(go.Pie(
        labels=lbls, values=ag["total"].tolist(), hole=0.52,
        marker=dict(colors=[PURPLE, INDIGO, VIOLET, "#312e81"],
                    line=dict(color="#07090f", width=2)),
        textfont=dict(color="#e2e8f0", size=12),
        hovertemplate="<b>%{label}</b><br>%{value:,} customers (%{percent})<extra></extra>",
    ))
    fig_pie.update_layout(
        paper_bgcolor=PAPER, plot_bgcolor=PAPER,
        font=dict(color=FONT, family="Inter"),
        margin=dict(l=0, r=0, t=8, b=0),
        showlegend=False, height=280,
        annotations=[dict(text="by age", x=0.5, y=0.5,
                          font=dict(size=11, color="#334155"), showarrow=False)],
    )
    st.plotly_chart(fig_pie, use_container_width=True)

with cb:
    fig_age = go.Figure()
    fig_age.add_trace(go.Bar(
        name="Subscribed", x=lbls, y=ag["subs"].tolist(),
        marker=dict(color=PURPLE, line=dict(width=0)),
        hovertemplate="<b>%{x}</b><br>Subscribed: %{y:,}<extra></extra>",
    ))
    fig_age.add_trace(go.Bar(
        name="Not subscribed", x=lbls, y=ag["no_subs"].tolist(),
        marker=dict(color="#111827", line=dict(color=GRID, width=1)),
        hovertemplate="<b>%{x}</b><br>Not subscribed: %{y:,}<extra></extra>",
    ))
    fig_age.add_trace(go.Scatter(
        x=lbls, y=ag["rate"].tolist(),
        mode="lines+markers+text",
        line=dict(color=CYAN, width=2), marker=dict(size=8, color=CYAN),
        text=ag["rate"].map("{:.1f}%".format).tolist(),
        textposition="top center", textfont=dict(color=CYAN, size=11),
        name="Rate %", yaxis="y2",
        hovertemplate="<b>%{x}</b><br>Rate: %{y:.1f}%<extra></extra>",
    ))
    # Dual-axis layout — built entirely here, no shared dict spread
    fig_age.update_layout(
        paper_bgcolor=PAPER, plot_bgcolor=PAPER,
        font=dict(color=FONT, family="Inter"),
        title_font=dict(color="#a8b2d8", size=14),
        hoverlabel=dict(bgcolor="#111827", bordercolor="#1e2540",
                        font_color="#e2e8f0", font_family="Inter"),
        margin=dict(l=8, r=8, t=36, b=8),
        barmode="stack", height=280,
        xaxis=dict(gridcolor=GRID, linecolor=GRID, tickfont=dict(color="#334155", size=12)),
        yaxis=dict(title="Customers", gridcolor=GRID, linecolor=GRID,
                   tickfont=dict(color="#334155")),
        yaxis2=dict(title="Rate %", overlaying="y", side="right",
                    range=[0, ag["rate"].max() * 2.5],
                    showgrid=False, tickfont=dict(color=CYAN, size=11)),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color=FONT),
                    orientation="h", y=1.12, x=0),
    )
    st.plotly_chart(fig_age, use_container_width=True)

best = ag.loc[ag["rate"].idxmax()]
st.markdown(f"""<div class='ibox'><strong>{best['age_group']}</strong> age group leads at
<strong>{best['rate']:.1f}%</strong>. Youngest (forming habits) and oldest (wealth preservation)
segments are most receptive to new products.</div>""", unsafe_allow_html=True)
st.divider()

# ══════════════════════════════════════════════════════════════════════════════
# Q4 – Housing loan
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<span class="stag">Q4</span>', unsafe_allow_html=True)
st.markdown("### Does a housing loan reduce new product uptake?")

hr = (f.groupby("housing")["subscribed"]
        .agg(total="count", subs="sum")
        .assign(rate=lambda x: x["subs"] / x["total"] * 100)
        .reset_index())

# Safe lookup with fallback
def get_rate(housing_val):
    rows = hr.loc[hr["housing"] == housing_val, "rate"]
    return rows.values[0] if len(rows) > 0 else 0.0

no_r  = get_rate("no")
yes_r = get_rate("yes")

ca, cb = st.columns([2,3])
with ca:
    fig_h = go.Figure(go.Bar(
        x=hr["housing"].tolist(), y=hr["rate"].tolist(),
        marker=dict(color=[GREEN if h == "no" else RED for h in hr["housing"].tolist()],
                    line=dict(width=0)),
        text=hr["rate"].map("{:.1f}%".format).tolist(),
        textposition="outside", textfont=dict(color="#64748b"),
        hovertemplate="<b>%{x}</b>: %{y:.1f}%<extra></extra>",
    ))
    fig_h.update_layout(**_layout(height=300, showlegend=False))
    fig_h.update_xaxes(gridcolor=GRID, linecolor=GRID, tickfont=dict(color="#334155"),
                       ticktext=["No loan","Has loan"], tickvals=["no","yes"])
    fig_h.update_yaxes(gridcolor=GRID, linecolor=GRID, tickfont=dict(color="#334155"))
    st.plotly_chart(fig_h, use_container_width=True)

with cb:
    cross = f.groupby(["housing","loan"])["subscribed"].mean().mul(100).unstack()
    fig_heat = px.imshow(
        cross,
        color_continuous_scale=[[0,"#07090f"],[0.4,"#1a1040"],[0.7,PURPLE],[1.0,VIOLET]],
        labels=dict(x="Personal loan", y="Housing loan", color="Sub rate %"),
        text_auto=".1f", aspect="auto",
        zmin=0, zmax=float(cross.values.max()) * 1.1,
    )
    fig_heat.update_traces(textfont=dict(color="#e2e8f0", size=15))
    # Heatmap layout — fully explicit
    fig_heat.update_layout(
        paper_bgcolor=PAPER, plot_bgcolor=PAPER,
        font=dict(color=FONT, family="Inter"),
        margin=dict(l=8, r=8, t=8, b=8),
        height=300,
        coloraxis_colorbar=dict(tickfont=dict(color=FONT, size=10),
                                title=dict(text="", side="right")),
    )
    fig_heat.update_xaxes(tickfont=dict(color="#334155", size=12), linecolor=GRID)
    fig_heat.update_yaxes(tickfont=dict(color="#334155", size=12), linecolor=GRID)
    st.plotly_chart(fig_heat, use_container_width=True)

delta = no_r - yes_r
st.markdown(f"""<div class='ibox'>
<strong>No housing loan → {no_r:.1f}%</strong> vs
<strong>has housing loan → {yes_r:.1f}%</strong>
({delta:.1f}pp difference).
Debt-free customers are most receptive.
<strong>No housing + no personal loan</strong> is the prime RM target.
</div>""", unsafe_allow_html=True)
st.divider()

with st.expander("🔎 Raw data explorer"):
    st.dataframe(
        f[["age","age_group","job","education","balance","housing","loan","y"]].head(500),
        use_container_width=True,
    )
    st.caption(f"First 500 of {len(f):,} filtered rows.")

st.markdown("<br><div style='font-size:.7rem;color:#1e2540;text-align:center'>BankMind · VITB AI Innovators Hub · Track A · UCI Bank Marketing Dataset</div>", unsafe_allow_html=True)
