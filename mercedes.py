"""
Mercedes-Benz Smart Pricing Engine & Dashboard
============================================================
Run with:
    pip install streamlit plotly pandas
    streamlit run mercedes_dashboard.py

Put mercedes_benz_listings_cleaned.csv in the same folder.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Mercedes-Benz Pricing Engine",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }

/* App background */
.stApp { background: #f5f0e8; }

/* Header strip */
.header-block {
    background: #0a0a0a;
    color: #f5f0e8;
    padding: 2.2rem 2.5rem 1.8rem;
    margin: -1rem -1rem 2rem -1rem;
    border-bottom: 3px solid #b8963e;
}
.header-eyebrow {
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: #b8963e;
    margin-bottom: 0.6rem;
}
.header-title {
    font-family: 'Playfair Display', serif;
    font-size: 2.8rem;
    font-weight: 900;
    line-height: 1.05;
    letter-spacing: -0.02em;
    color: #f5f0e8;
}
.header-title span { color: #b8963e; }
.header-sub { color: #c8bfb0; font-size: 0.9rem; margin-top: 0.5rem; font-weight: 300; }

/* Section titles */
.section-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.3rem;
    font-weight: 700;
    color: #0a0a0a;
    border-bottom: 1px solid #ede7d5;
    padding-bottom: 0.5rem;
    margin-bottom: 1rem;
}
.section-num {
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    color: #b8963e;
    border: 1px solid #b8963e;
    padding: 0.1rem 0.35rem;
    margin-right: 0.5rem;
}

/* KPI cards */
.kpi-card {
    background: white;
    border: 1px solid #ede7d5;
    padding: 1.3rem 1.5rem 1rem;
    box-shadow: 0 2px 12px rgba(10,10,10,0.07);
}
.kpi-num {
    font-family: 'Playfair Display', serif;
    font-size: 1.8rem;
    font-weight: 700;
    color: #0a0a0a;
    line-height: 1;
}
.kpi-label {
    font-size: 0.68rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #4a4a4a;
    margin-top: 0.3rem;
}
.kpi-sub {
    font-family: 'DM Mono', monospace;
    font-size: 0.68rem;
    color: #b8963e;
    margin-top: 0.15rem;
}

/* Prediction result box */
.pred-box {
    background: #0a0a0a;
    color: #f5f0e8;
    padding: 2rem;
    border-radius: 0;
    min-height: 260px;
}
.pred-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #b8963e;
    margin-bottom: 0.4rem;
}
.pred-price {
    font-family: 'Playfair Display', serif;
    font-size: 2.8rem;
    font-weight: 900;
    color: #b8963e;
    line-height: 1;
}
.pred-range { font-size: 0.78rem; color: #c8bfb0; margin-top: 0.3rem; }

/* Verdict pills */
.verdict-great  { background: rgba(45,106,79,0.15); color: #4ade80; border: 1px solid rgba(45,106,79,0.35); padding: 0.4rem 1rem; font-family:'DM Mono',monospace; font-size:0.72rem; display:inline-block; margin-top:0.8rem; }
.verdict-good   { background: rgba(45,106,79,0.08); color: #86efac; border: 1px solid rgba(45,106,79,0.2); padding: 0.4rem 1rem; font-family:'DM Mono',monospace; font-size:0.72rem; display:inline-block; margin-top:0.8rem; }
.verdict-fair   { background: rgba(184,150,62,0.12); color: #d4b060; border: 1px solid rgba(184,150,62,0.3); padding: 0.4rem 1rem; font-family:'DM Mono',monospace; font-size:0.72rem; display:inline-block; margin-top:0.8rem; }
.verdict-high   { background: rgba(139,26,26,0.15); color: #fca5a5; border: 1px solid rgba(139,26,26,0.3); padding: 0.4rem 1rem; font-family:'DM Mono',monospace; font-size:0.72rem; display:inline-block; margin-top:0.8rem; }

/* Factor breakdown table */
.factor-row {
    display: flex;
    justify-content: space-between;
    padding: 0.35rem 0;
    border-bottom: 1px solid rgba(255,255,255,0.06);
    font-size: 0.82rem;
}
.factor-label { color: #c8bfb0; }
.factor-pos { color: #4ade80; font-family:'DM Mono',monospace; font-size:0.78rem; }
.factor-neg { color: #fca5a5; font-family:'DM Mono',monospace; font-size:0.78rem; }
.factor-neutral { color: #f5f0e8; font-family:'DM Mono',monospace; font-size:0.78rem; }

/* Premium insight cards */
.premium-card {
    background: #f5f0e8;
    border: 1px solid #ede7d5;
    border-left: 3px solid #b8963e;
    padding: 1.2rem 1.4rem;
}
.premium-val { font-family:'Playfair Display',serif; font-size:1.7rem; font-weight:700; color:#0a0a0a; }
.premium-lbl { font-size:0.68rem; text-transform:uppercase; letter-spacing:0.1em; color:#4a4a4a; margin-bottom:0.3rem; }
.premium-desc { font-size:0.76rem; color:#4a4a4a; margin-top:0.4rem; line-height:1.5; }

/* Deal pills in table */
.pill-hot  { background:#d1fae5; color:#065f46; padding:2px 8px; font-size:0.72rem; border-radius:2px; }
.pill-good { background:#ecfdf5; color:#065f46; padding:2px 8px; font-size:0.72rem; border-radius:2px; }
.pill-fair { background:#fefce8; color:#854d0e; padding:2px 8px; font-size:0.72rem; border-radius:2px; }
.pill-high { background:#fff1f2; color:#9f1239; padding:2px 8px; font-size:0.72rem; border-radius:2px; }

/* Divider */
.gold-divider { border: none; border-top: 1px solid #c8bfb0; margin: 2rem 0; }

/* Hide streamlit branding */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 0 !important; }
</style>
""", unsafe_allow_html=True)


# ── Pricing Model ─────────────────────────────────────────────────────────────
MODEL_BASES = {
    'GLE': 46734, 'GLS': 52956, 'AMG GLC 43': 45197, 'CLE': 49496,
    'GLB': 34295, 'GLA': 27165, 'GLC': 26943, 'C-Class': 28630,
    'S-Class': 57153, 'E-Class': 29983, 'EQS': 55127, 'Metris': 28325,
    'Sprinter': 36959, 'A-Class': 24267, 'AMG G 63': 140992,
    'M-Class': 11997, 'GLK-Class': 11488, 'Unknown': 40310, 'AMG S 63': 120000,
}
MEAN_AGE   = 7.2
MEAN_MILES = 52_000
AGE_COEF   = -1_850
MILE_COEF  = -0.09
FMATIC_PREMIUM = 3_200


def predict(age: int, mileage: int, is_4matic: bool, model: str) -> float:
    base = MODEL_BASES.get(model, 40_310)
    pred = base + (age - MEAN_AGE) * AGE_COEF + (mileage - MEAN_MILES) * MILE_COEF
    if is_4matic:
        pred += FMATIC_PREMIUM
    return max(5_000, pred)


def deal_label(pct: float) -> str:
    if pct > 20:  return "🔥 Hot Deal"
    if pct > 5:   return "✓ Good Value"
    if pct >= -5: return "~ Fair"
    return "↑ Priced High"


def deal_pill_class(pct: float) -> str:
    if pct > 20:  return "pill-hot"
    if pct > 5:   return "pill-good"
    if pct >= -5: return "pill-fair"
    return "pill-high"


# ── Load data ─────────────────────────────────────────────────────────────────
@st.cache_data
def load_data() -> pd.DataFrame:
    df = pd.read_csv("mercedes_benz_listings_cleaned.csv")
    df["predicted"] = df.apply(
        lambda r: predict(r["Vehicle_Age"], r["Mileage_Miles"], bool(r["Is_4MATIC"]), r["Model_Series"]), axis=1
    )
    df["discount_pct"] = (df["predicted"] - df["Price_USD"]) / df["predicted"] * 100
    df["deal_label"]   = df["discount_pct"].apply(deal_label)
    return df

df = load_data()

# ── Plotly theme ──────────────────────────────────────────────────────────────
GOLD       = "#b8963e"
GOLD_LIGHT = "#d4b060"
INK        = "#0a0a0a"
PAPER      = "#f5f0e8"
SILVER     = "#c8bfb0"
CREAM      = "#ede7d5"

PLOTLY_LAYOUT = dict(
    paper_bgcolor="white",
    plot_bgcolor="white",
    font=dict(family="DM Sans", color="#0a0a0a"),
    margin=dict(l=16, r=16, t=30, b=16),
)
AXIS_STYLE = dict(
    showgrid=True,
    tickfont=dict(color=INK, size=11),
    title=dict(font=dict(color=INK, size=12)),
    zerolinecolor=SILVER
)

LEGEND_STYLE = dict(
    font=dict(color=INK, size=11),
    bgcolor="rgba(0,0,0,0)"
)


# ═══════════════════════════════════════════════════════════════════════════════
# HEADER
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="header-block">
  <div class="header-eyebrow">Data Science Portfolio · Mercedes-Benz Market Intelligence</div>
  <div class="header-title">Smart <span>Pricing</span> Engine</div>
  <div class="header-sub">ML-powered valuation & deal detection across 108 certified listings · 2005–2025</div>
</div>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# 00  KPI STRIP
# ═══════════════════════════════════════════════════════════════════════════════
k1, k2, k3, k4, k5 = st.columns(5)

kpis = [
    (k1, f"${df['Price_USD'].mean():,.0f}",   "Average Listing Price",   "↕ $6.4K – $170K range"),
    (k2, "$39,410",                            "AMG Badge Premium",       "avg over non-AMG models"),
    (k3, "$1,850/yr",                          "Annual Depreciation",     "per year of vehicle age"),
    (k4, "$0.09/mi",                           "Price Drop Per Mile",     "across all model lines"),
    (k5, f"{df['Is_4MATIC'].mean()*100:.0f}%", "4MATIC Equipped",         "+$3,200 premium on avg"),
]

for col, num, lbl, sub in kpis:
    with col:
        st.markdown(f"""
        <div class="kpi-card">
          <div class="kpi-num">{num}</div>
          <div class="kpi-label">{lbl}</div>
          <div class="kpi-sub">{sub}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<hr class='gold-divider'>", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# 01  SMART PRICING ENGINE
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-title"><span class="section-num">01</span>Smart Pricing Engine — Estimate Fair Market Value</div>', unsafe_allow_html=True)

left, right = st.columns([1, 1.2], gap="large")

with left:
    c1, c2 = st.columns(2)
    with c1:
        model_choice = st.selectbox("Model Series", sorted([
            "GLA","GLC","GLE","GLS","GLB","C-Class","E-Class","S-Class",
            "A-Class","CLE","EQS","AMG G 63","AMG GLC 43","Sprinter","Unknown"
        ]), index=2)
        mileage_inp = st.number_input("Mileage (miles)", min_value=0, max_value=300_000,
                                       value=35_000, step=1_000)
    with c2:
        year_inp    = st.selectbox("Vehicle Year", list(range(2025, 2004, -1)), index=3)
        body_inp    = st.selectbox("Body Type", ["SUV","Sedan","Coupe","Sports/Roadster","Van/Commercial","Other"])

    col_amg, col_4m = st.columns(2)
    with col_amg:
        amg_inp = st.radio("AMG Package", ["No AMG", "AMG ✦"], horizontal=True)
    with col_4m:
        fmatic_inp = st.radio("4MATIC AWD", ["RWD", "4MATIC"], index=1, horizontal=True)

    run = st.button("⬡  Predict Fair Market Value", use_container_width=True, type="primary")

with right:
    age_val    = 2026 - year_inp
    is_4m      = fmatic_inp == "4MATIC"
    is_amg     = amg_inp == "AMG ✦"
    pred_val   = predict(age_val, mileage_inp, is_4m, model_choice)
    lo, hi     = pred_val * 0.88, pred_val * 1.12

    age_eff    = (age_val - MEAN_AGE) * AGE_COEF
    mile_eff   = (mileage_inp - MEAN_MILES) * MILE_COEF
    base_val   = MODEL_BASES.get(model_choice, 40_310)

    def fmt_signed(v):
        sign = "+" if v >= 0 else ""
        return f"{sign}${v:,.0f}"

    verdict_map = {
        "great": ("verdict-great", "🔥 Excellent Deal"),
        "good":  ("verdict-good",  "✓ Good Value"),
        "fair":  ("verdict-fair",  "~ Fair Market Price"),
        "high":  ("verdict-high",  "↑ Above Market"),
    }

    if run:
        vkey = "great" if 15 > 20 else "fair"  # Engine shows estimate only — no listing price
    vcls, vtxt = "verdict-fair", "~ Estimated Market Value"

    fmatic_row = f'<div class="factor-row"><span class="factor-label">4MATIC premium</span><span class="factor-pos">+$3,200</span></div>' if is_4m else ""
    amg_note   = f'<div class="factor-row"><span class="factor-label">AMG (base includes badge)</span><span class="factor-neutral">—</span></div>' if is_amg else ""

    st.markdown(f"""
    <div class="pred-box">
      <div class="pred-label">Model Estimate · {model_choice} {year_inp}</div>
      <div class="pred-price">${pred_val:,.0f}</div>
      <div class="pred-range">Fair value range: ${lo:,.0f} – ${hi:,.0f}</div>
      <div class="{vcls}">{vtxt}</div>
      <div style="margin-top:1.4rem;border-top:1px solid rgba(255,255,255,0.1);padding-top:1rem;">
        <div class="factor-row"><span class="factor-label">Model base ({model_choice})</span><span class="factor-neutral">${base_val:,}</span></div>
        <div class="factor-row"><span class="factor-label">Age adjustment ({age_val} yrs)</span><span class="{'factor-neg' if age_eff < 0 else 'factor-pos'}">{fmt_signed(age_eff)}</span></div>
        <div class="factor-row"><span class="factor-label">Mileage adjustment</span><span class="{'factor-neg' if mile_eff < 0 else 'factor-pos'}">{fmt_signed(mile_eff)}</span></div>
        {fmatic_row}
        {amg_note}
      </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<hr class='gold-divider'>", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# 02–03  SCATTER + DONUT
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-title"><span class="section-num">02–03</span>Price Distribution & Listing Breakdown</div>', unsafe_allow_html=True)

chart_l, chart_r = st.columns([1.5, 1], gap="large")

with chart_l:
    df_plot = df.copy()
    df_plot["Category"] = df_plot.apply(
        lambda r: "AMG" if r["Is_AMG"] else ("4MATIC" if r["Is_4MATIC"] else "Standard"), axis=1
    )
    scatter = px.scatter(
        df_plot, x="Mileage_Miles", y="Price_USD",
        color="Category",
        color_discrete_map={"AMG": GOLD, "4MATIC": INK, "Standard": SILVER},
        hover_name="Vehicle_Name",
        hover_data={"Price_USD": ":$,.0f", "Mileage_Miles": ":,", "Category": True},
        labels={"Mileage_Miles": "Mileage", "Price_USD": "Listed Price (USD)"},
        title="Price vs Mileage — All 108 Listings",
    )
    scatter.update_traces(marker=dict(size=7, opacity=0.78))
    scatter.update_layout(
        **PLOTLY_LAYOUT,
        legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="left", x=0,**LEGEND_STYLE),
        xaxis=dict(tickformat=",.0f",gridcolor=CREAM,**AXIS_STYLE),
        yaxis=dict(tickprefix="$", tickformat=",.0f",gridcolor=CREAM,**AXIS_STYLE),
        title_font=dict(family="Playfair Display", size=14, color=INK),
    )
    st.plotly_chart(scatter, use_container_width=True, key="scatter_chart")

with chart_r:
    body_counts = df["Body_Type"].value_counts()
    donut = go.Figure(go.Pie(
        labels=body_counts.index,
        values=body_counts.values,
        hole=0.62,
        marker=dict(colors=[INK, GOLD, CREAM, SILVER, "#4a4a4a", GOLD_LIGHT]),
        textfont=dict(family="DM Sans", size=11),
    ))
    donut.update_layout(
        **PLOTLY_LAYOUT,
        title=dict(text="Listings by Body Type", font=dict(family="Playfair Display", size=14, color=INK)),
        legend=dict(**LEGEND_STYLE),
        annotations=[dict(text=f"<b>{len(df)}</b><br>listings", x=0.5, y=0.5,
                          font=dict(size=13, family="Playfair Display", color=INK),
                          showarrow=False)],
    )
    donut.update_traces(
        textfont=dict(color=INK, size=11)
    )
    
    st.plotly_chart(donut, use_container_width=True, key="donut_chart")

st.markdown("<hr class='gold-divider'>", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# 04  DEPRECIATION CURVES + MODEL BARS
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-title"><span class="section-num">04</span>Depreciation Curves by Model Line</div>', unsafe_allow_html=True)

dep_l, dep_r = st.columns([1.8, 1], gap="large")

with dep_l:
    focus_models = ["GLE", "GLC", "C-Class", "E-Class", "S-Class", "GLS"]
    palette      = [GOLD, INK, "#080808", SILVER, GOLD_LIGHT, "#070606"]

    fig_dep = go.Figure()
    for model_name, color in zip(focus_models, palette):
        subset = df[df["Model_Series"] == model_name].groupby("Vehicle_Age")["Price_USD"].mean().reset_index()
        fig_dep.add_trace(go.Scatter(
            x=subset["Vehicle_Age"], y=subset["Price_USD"],
            mode="lines+markers", name=model_name,
            line=dict(color=color, width=2.5), marker=dict(size=5),
        ))

    fig_dep.update_layout(
        **PLOTLY_LAYOUT,
        title=dict(text="Average Price by Vehicle Age", font=dict(family="Playfair Display", size=14, color=INK)),
        xaxis=dict(title=dict(text="Vehicle Age (years)", font=dict(color=INK, size=12)), showgrid=True, tickfont=dict(color=INK, size=11), zerolinecolor=SILVER),
        yaxis=dict(title=dict(text="Avg Price (USD)", font=dict(color=INK, size=12)), tickprefix="$", tickformat=",.0f", showgrid=True, tickfont=dict(color=INK, size=11), zerolinecolor=SILVER),
        legend=dict(orientation="h", yanchor="bottom", y=-0.28, xanchor="left", x=0,
                    **LEGEND_STYLE),
    )
    st.plotly_chart(fig_dep, use_container_width=True, key="dep_chart")

with dep_r:
    model_avg = (
        df[df["Model_Series"] != "Unknown"]
        .groupby("Model_Series")["Price_USD"]
        .mean()
        .sort_values(ascending=True)
        .tail(12)
    )
    bar_h = go.Figure(go.Bar(
        x=model_avg.values, y=model_avg.index,
        orientation="h",
        marker=dict(
            color=model_avg.values,
            colorscale=[[0, SILVER], [1, GOLD]],
            showscale=False,
        ),
        text=[f"${v:,.0f}" for v in model_avg.values],
        textposition="outside",
        textfont=dict(family="DM Mono", size=10, color=INK),
    ))
    bar_h.update_layout(
        **PLOTLY_LAYOUT,
        title=dict(text="Avg Price by Model Series", font=dict(family="Playfair Display", size=14, color=INK)),
        xaxis=dict(tickprefix="$", tickformat=",.0f", gridcolor=CREAM, showticklabels=False, tickfont=dict(color=INK, size=11)),
        yaxis=dict(tickfont=dict(family="DM Sans", size=10, color=INK)),
        height=420,
        
    )
    st.plotly_chart(bar_h, use_container_width=True, key="bar_h_chart")

st.markdown("<hr class='gold-divider'>", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# 05  PREMIUM BREAKDOWN
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-title"><span class="section-num">05</span>Premium Drivers — What Actually Moves the Price</div>', unsafe_allow_html=True)

p1, p2, p3 = st.columns(3)
premiums = [
    (p1, "🏁", "AMG Badge Premium", "+$39,410",
     "Average price uplift for AMG-badged vehicles over equivalent non-AMG models. The G 63 tops at $141K avg."),
    (p2, "❄️", "4MATIC AWD Premium", "+$3,200",
     "Average premium buyers pay for all-wheel drive. 69% of the dataset is 4MATIC equipped."),
    (p3, "📉", "Annual Depreciation", "−$1,850/yr",
     "Estimated value lost per year of vehicle age. Mileage compounds this at $0.09 per additional mile."),
]
for col, icon, lbl, val, desc in premiums:
    with col:
        st.markdown(f"""
        <div class="premium-card">
          <div style="font-size:1.4rem;margin-bottom:0.6rem;">{icon}</div>
          <div class="premium-lbl">{lbl}</div>
          <div class="premium-val">{val}</div>
          <div class="premium-desc">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

# AMG vs non-AMG box plot
st.markdown("<br>", unsafe_allow_html=True)
df_amg = df.copy()
df_amg["Type"] = df_amg["Is_AMG"].map({1: "AMG", 0: "Non-AMG"})
box = px.box(
    df_amg, x="Type", y="Price_USD", color="Type",
    color_discrete_map={"AMG": GOLD, "Non-AMG": INK},
    points="all",
    hover_name="Vehicle_Name",
    labels={"Price_USD": "Price (USD)", "Type": ""},
    title="AMG vs Non-AMG — Price Distribution",
)
box.update_layout(**PLOTLY_LAYOUT,
                  title_font=dict(family="Playfair Display", size=14, color=INK),
                  yaxis=dict(tickprefix="$", tickformat=",.0f", **AXIS_STYLE),
                  showlegend=False),
            
st.plotly_chart(box, use_container_width=True, key="box_chart")

st.markdown("<hr class='gold-divider'>", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# 06  LIVE DEAL SCANNER
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-title"><span class="section-num">06</span>Live Deal Scanner — All 108 Listings Ranked</div>', unsafe_allow_html=True)

# Filter controls
fc1, fc2, fc3, fc4 = st.columns([1, 1, 1, 2])
with fc1:
    deal_filter = st.selectbox("Deal Type", ["All Listings", "🔥 Hot Deals (>20%)", "✓ Good Deals (5–20%)", "~ Fair Value", "↑ Priced High"])
with fc2:
    amg_filter = st.selectbox("Badge", ["All", "AMG Only", "Non-AMG"])
with fc3:
    body_filter = st.selectbox("Body", ["All"] + sorted(df["Body_Type"].unique().tolist()))
with fc4:
    search_term = st.text_input("Search", placeholder="Search model or name...")

# Apply filters
filtered = df.copy()

if deal_filter == "🔥 Hot Deals (>20%)":
    filtered = filtered[filtered["discount_pct"] > 20]
elif deal_filter == "✓ Good Deals (5–20%)":
    filtered = filtered[(filtered["discount_pct"] > 5) & (filtered["discount_pct"] <= 20)]
elif deal_filter == "~ Fair Value":
    filtered = filtered[(filtered["discount_pct"] >= -5) & (filtered["discount_pct"] <= 5)]
elif deal_filter == "↑ Priced High":
    filtered = filtered[filtered["discount_pct"] < -5]

if amg_filter == "AMG Only":
    filtered = filtered[filtered["Is_AMG"] == 1]
elif amg_filter == "Non-AMG":
    filtered = filtered[filtered["Is_AMG"] == 0]

if body_filter != "All":
    filtered = filtered[filtered["Body_Type"] == body_filter]

if search_term:
    mask = (
        filtered["Vehicle_Name"].str.lower().str.contains(search_term.lower()) |
        filtered["Model_Series"].str.lower().str.contains(search_term.lower())
    )
    filtered = filtered[mask]

# Sort
filtered = filtered.sort_values("discount_pct", ascending=False).reset_index(drop=True)

st.caption(f"Showing {len(filtered)} of {len(df)} listings")

# Display table
display_cols = {
    "Vehicle_Name":  "Vehicle",
    "Year":          "Year",
    "Mileage_Miles": "Mileage",
    "Price_USD":     "Listed Price",
    "predicted":     "Model Estimate",
    "discount_pct":  "Deal Score %",
    "deal_label":    "Verdict",
    "Is_AMG":        "AMG",
    "Is_4MATIC":     "4MATIC",
}
table = filtered[list(display_cols.keys())].rename(columns=display_cols)
table["Mileage"]        = table["Mileage"].apply(lambda v: f"{v:,.0f} mi")
table["Listed Price"]   = table["Listed Price"].apply(lambda v: f"${v:,.0f}")
table["Model Estimate"] = table["Model Estimate"].apply(lambda v: f"${v:,.0f}")
table["Deal Score %"]   = table["Deal Score %"].apply(lambda v: f"{v:+.1f}%")
table["AMG"]            = table["AMG"].apply(lambda v: "✦" if v else "")
table["4MATIC"]         = table["4MATIC"].apply(lambda v: "✓" if v else "")

st.dataframe(
    table,
    use_container_width=True,
    height=480,
    column_config={
        "Vehicle":        st.column_config.TextColumn("Vehicle", width="large"),
        "Year":           st.column_config.NumberColumn("Year", format="%d"),
        "Deal Score %":   st.column_config.TextColumn("Deal Score"),
        "Verdict":        st.column_config.TextColumn("Verdict"),
    },
    hide_index=True,
)

# Deal score histogram
hist = px.histogram(
    df, x="discount_pct", nbins=30,
    color_discrete_sequence=[GOLD],
    labels={"discount_pct": "Deal Score % (positive = below market estimate)"},
    title="Deal Score Distribution — All Listings",
)
hist.add_vline(x=0, line_dash="dash", line_color=INK, annotation_text="Fair Value", annotation_position="top right")
hist.update_layout(**PLOTLY_LAYOUT,
                   title_font=dict(family="Playfair Display", size=14, color=INK),
                   xaxis=dict(**AXIS_STYLE),
                   yaxis=dict(title=dict(text="Count", font=dict(color=INK, size=12)), showgrid=True, tickfont=dict(color=INK, size=11), zerolinecolor=SILVER))
st.plotly_chart(hist, use_container_width=True, key="hist_chart")

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;padding:2rem 0 1rem;font-size:0.72rem;color:#c8bfb0;letter-spacing:0.08em;">
  Mercedes-Benz Smart Pricing Engine · Portfolio Project · Pricing model uses regression on model series, age, mileage & equipment
</div>
""", unsafe_allow_html=True)
