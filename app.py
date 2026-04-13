import streamlit as st
import yfinance as yf
import pandas as pd
from streamlit_lightweight_charts import renderLightweightCharts

# ================= PAGE CONFIG =================
st.set_page_config(layout="wide", page_title="Quant Terminal", page_icon="📈")

# ================= UI =================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:ital,wght@0,400;0,700;1,400&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ---- ROOT RESET ---- */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

/* ---- BASE ---- */
html, body, .stApp {
    background-color: #080A0F !important;
    color: #C8D0DC !important;
    font-family: 'DM Sans', sans-serif !important;
}

.block-container {
    padding: 1.5rem 2.5rem 2rem 2.5rem !important;
    max-width: 100% !important;
}

/* ---- SCANLINE OVERLAY ---- */
.stApp::before {
    content: '';
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background: repeating-linear-gradient(
        0deg,
        transparent,
        transparent 2px,
        rgba(0, 255, 200, 0.012) 2px,
        rgba(0, 255, 200, 0.012) 4px
    );
    pointer-events: none;
    z-index: 9999;
}

/* ---- SIDEBAR ---- */
[data-testid="stSidebar"] {
    background: #0D1017 !important;
    border-right: 1px solid rgba(0, 229, 180, 0.12) !important;
}

[data-testid="stSidebar"] .block-container {
    padding: 2rem 1.5rem !important;
}

/* Sidebar title */
[data-testid="stSidebar"] h1 {
    font-family: 'Space Mono', monospace !important;
    font-size: 1rem !important;
    letter-spacing: 0.18em !important;
    text-transform: uppercase !important;
    color: #00E5B4 !important;
    padding-bottom: 1.2rem !important;
    border-bottom: 1px solid rgba(0, 229, 180, 0.2) !important;
    margin-bottom: 1.5rem !important;
}

/* Sidebar labels */
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stTextInput label {
    font-family: 'Space Mono', monospace !important;
    font-size: 0.62rem !important;
    letter-spacing: 0.14em !important;
    text-transform: uppercase !important;
    color: #4A5568 !important;
    margin-bottom: 0.4rem !important;
}

/* Sidebar inputs */
[data-testid="stSidebar"] input,
[data-testid="stSidebar"] .stTextInput input {
    background: #111520 !important;
    border: 1px solid rgba(0, 229, 180, 0.18) !important;
    border-radius: 4px !important;
    color: #00E5B4 !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.95rem !important;
    padding: 0.55rem 0.75rem !important;
    transition: border-color 0.2s !important;
}

[data-testid="stSidebar"] input:focus {
    border-color: #00E5B4 !important;
    box-shadow: 0 0 0 2px rgba(0, 229, 180, 0.1) !important;
}

/* Selectbox */
[data-testid="stSidebar"] .stSelectbox > div > div {
    background: #111520 !important;
    border: 1px solid rgba(0, 229, 180, 0.18) !important;
    border-radius: 4px !important;
    color: #C8D0DC !important;
}

/* Checkboxes */
[data-testid="stSidebar"] .stCheckbox label {
    font-family: 'Space Mono', monospace !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
    color: #8892A4 !important;
}

[data-testid="stSidebar"] .stCheckbox span[data-baseweb="checkbox"] {
    background: #111520 !important;
    border: 1px solid rgba(0, 229, 180, 0.3) !important;
    border-radius: 2px !important;
}

/* Divider */
[data-testid="stSidebar"] hr {
    border-color: rgba(0, 229, 180, 0.1) !important;
    margin: 1.5rem 0 !important;
}

/* ---- REFRESH BUTTON ---- */
[data-testid="stSidebar"] .stButton button {
    width: 100% !important;
    background: transparent !important;
    border: 1px solid rgba(0, 229, 180, 0.4) !important;
    border-radius: 4px !important;
    color: #00E5B4 !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.7rem !important;
    letter-spacing: 0.14em !important;
    text-transform: uppercase !important;
    padding: 0.6rem !important;
    cursor: pointer !important;
    transition: all 0.2s !important;
    margin-top: 0.5rem !important;
}

[data-testid="stSidebar"] .stButton button:hover {
    background: rgba(0, 229, 180, 0.08) !important;
    border-color: #00E5B4 !important;
    box-shadow: 0 0 12px rgba(0, 229, 180, 0.15) !important;
}

/* ---- HEADER / TICKER BANNER ---- */
h1, h2, h3 {
    font-family: 'Space Mono', monospace !important;
}

/* Subheader (chart title) */
.stApp h3 {
    font-size: 0.78rem !important;
    letter-spacing: 0.22em !important;
    text-transform: uppercase !important;
    color: #3A4459 !important;
    font-weight: 400 !important;
    margin-bottom: 0.5rem !important;
    padding-bottom: 0.5rem !important;
    border-bottom: 1px solid #13181F !important;
}

/* ---- METRIC CARDS ---- */
[data-testid="stMetric"] {
    background: #0D1017 !important;
    border: 1px solid #161C27 !important;
    border-radius: 6px !important;
    padding: 1rem 1.25rem !important;
    position: relative !important;
    overflow: hidden !important;
    transition: border-color 0.2s !important;
}

[data-testid="stMetric"]::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 3px; height: 100%;
    background: linear-gradient(180deg, #00E5B4, transparent);
}

[data-testid="stMetric"]:hover {
    border-color: rgba(0, 229, 180, 0.2) !important;
}

[data-testid="stMetricLabel"] {
    font-family: 'Space Mono', monospace !important;
    font-size: 0.6rem !important;
    letter-spacing: 0.18em !important;
    text-transform: uppercase !important;
    color: #3A4459 !important;
    margin-bottom: 0.4rem !important;
}

[data-testid="stMetricValue"] {
    font-family: 'Space Mono', monospace !important;
    font-size: 1.35rem !important;
    color: #E8EDF5 !important;
    font-weight: 700 !important;
    line-height: 1.2 !important;
}

[data-testid="stMetricDelta"] {
    font-family: 'Space Mono', monospace !important;
    font-size: 0.72rem !important;
    margin-top: 0.3rem !important;
}

[data-testid="stMetricDelta"] svg { display: none !important; }

/* Positive delta */
[data-testid="stMetricDelta"][data-direction="up"] {
    color: #00E5B4 !important;
}

/* Negative delta */
[data-testid="stMetricDelta"][data-direction="down"] {
    color: #FF4D6A !important;
}

/* ---- CHART CONTAINER ---- */
.element-container iframe {
    border-radius: 4px !important;
}

/* ---- EXPANDER (Raw Data) ---- */
[data-testid="stExpander"] {
    background: #0D1017 !important;
    border: 1px solid #161C27 !important;
    border-radius: 6px !important;
    margin-top: 1rem !important;
}

[data-testid="stExpander"] summary {
    font-family: 'Space Mono', monospace !important;
    font-size: 0.68rem !important;
    letter-spacing: 0.14em !important;
    text-transform: uppercase !important;
    color: #3A4459 !important;
    padding: 0.8rem 1rem !important;
}

[data-testid="stExpander"] summary:hover {
    color: #00E5B4 !important;
}

/* ---- DATAFRAME ---- */
[data-testid="stDataFrame"] {
    background: transparent !important;
}

.stDataFrame thead th {
    background: #080A0F !important;
    color: #3A4459 !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.62rem !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    border-bottom: 1px solid #161C27 !important;
}

.stDataFrame tbody td {
    font-family: 'Space Mono', monospace !important;
    font-size: 0.78rem !important;
    color: #8892A4 !important;
    border-bottom: 1px solid #0F1318 !important;
}

.stDataFrame tbody tr:hover td {
    background: #111520 !important;
    color: #C8D0DC !important;
}

/* ---- ERROR ---- */
[data-testid="stAlert"] {
    background: rgba(255, 77, 106, 0.08) !important;
    border: 1px solid rgba(255, 77, 106, 0.3) !important;
    border-radius: 4px !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.78rem !important;
    color: #FF4D6A !important;
}

/* ---- SCROLLBAR ---- */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: #080A0F; }
::-webkit-scrollbar-thumb { background: #1E2733; border-radius: 2px; }
::-webkit-scrollbar-thumb:hover { background: #00E5B4; }

/* ---- COLUMN GAPS ---- */
[data-testid="stHorizontalBlock"] {
    gap: 0.75rem !important;
}
</style>

<!-- Terminal header bar -->
<div style="
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.6rem 0 1.5rem 0;
    border-bottom: 1px solid #13181F;
    margin-bottom: 1.5rem;
">
    <div style="display:flex; align-items:center; gap: 1rem;">
        <span style="
            font-family: 'Space Mono', monospace;
            font-size: 1.1rem;
            font-weight: 700;
            color: #00E5B4;
            letter-spacing: 0.08em;
        ">QUANT/TERMINAL</span>
        <span style="
            background: rgba(0,229,180,0.08);
            border: 1px solid rgba(0,229,180,0.2);
            color: #00E5B4;
            font-family: 'Space Mono', monospace;
            font-size: 0.58rem;
            letter-spacing: 0.18em;
            padding: 2px 8px;
            border-radius: 2px;
            text-transform: uppercase;
        ">LIVE</span>
    </div>
    <span style="
        font-family: 'Space Mono', monospace;
        font-size: 0.6rem;
        color: #2A3344;
        letter-spacing: 0.1em;
    ">NSE · BSE · EQUITY</span>
</div>
""", unsafe_allow_html=True)

# ================= DATA =================
@st.cache_data(ttl=3600)
def fetch_data(ticker, period):
    df = yf.download(ticker, period=period, auto_adjust=False)

    if df.empty:
        return None

    df.columns = [col[0] if isinstance(col, tuple) else col for col in df.columns]
    df = df.reset_index()
    df['Date'] = pd.to_datetime(df['Date'])
    df['time'] = df['Date'].dt.strftime('%Y-%m-%d')

    df['MA20'] = df['Close'].rolling(20).mean()
    df['MA50'] = df['Close'].rolling(50).mean()

    return df

# ================= SIDEBAR =================
with st.sidebar:
    st.title("⬡ Controls")

    ticker = st.text_input("Symbol", "RELIANCE.NS").upper()

    period = st.selectbox(
        "Period",
        ["6mo", "1y", "2y", "5y"],
        index=1
    )

    st.divider()

    show_ma20 = st.checkbox("MA 20", True)
    show_ma50 = st.checkbox("MA 50", True)

    st.divider()

    if st.button("↺ Refresh Data"):
        st.cache_data.clear()
        st.rerun()

    # Sidebar footer
    st.markdown("""
    <div style="
        position: absolute;
        bottom: 2rem;
        left: 1.5rem;
        right: 1.5rem;
        font-family: 'Space Mono', monospace;
        font-size: 0.55rem;
        color: #1E2733;
        letter-spacing: 0.1em;
        line-height: 1.8;
        text-transform: uppercase;
    ">
        Data · Yahoo Finance<br>
        Charts · Lightweight Charts<br>
        Delayed · 15min
    </div>
    """, unsafe_allow_html=True)

# ================= MAIN =================
df = fetch_data(ticker, period)

if df is None:
    st.error("⚠  Invalid ticker or no data available.")
    st.stop()

# ================= METRICS =================
last = df.iloc[-1]
prev = df.iloc[-2]
change = ((last['Close'] - prev['Close']) / prev['Close']) * 100
change_abs = last['Close'] - prev['Close']

# Ticker label + date row
st.markdown(f"""
<div style="
    display: flex;
    align-items: baseline;
    gap: 1.2rem;
    margin-bottom: 1.2rem;
">
    <span style="
        font-family: 'Space Mono', monospace;
        font-size: 1.6rem;
        font-weight: 700;
        color: #E8EDF5;
        letter-spacing: 0.04em;
    ">{ticker}</span>
    <span style="
        font-family: 'Space Mono', monospace;
        font-size: 0.68rem;
        color: #2A3344;
        letter-spacing: 0.12em;
        text-transform: uppercase;
    ">{last['Date'].strftime('%d %b %Y') if hasattr(last['Date'], 'strftime') else ''}</span>
    <span style="
        font-family: 'Space Mono', monospace;
        font-size: 0.68rem;
        color: {'#00E5B4' if change >= 0 else '#FF4D6A'};
        letter-spacing: 0.06em;
    ">{'▲' if change >= 0 else '▼'} {abs(change):.2f}% ({'+' if change_abs >= 0 else ''}{change_abs:.2f})</span>
</div>
""", unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Last Price", f"₹{last['Close']:.2f}", f"{change:+.2f}%")
c2.metric("Day High", f"₹{last['High']:.2f}")
c3.metric("Day Low", f"₹{last['Low']:.2f}")
c4.metric("Volume", f"{int(last['Volume']):,}" if 'Volume' in df.columns else "—")

st.markdown("<div style='height:1.2rem'></div>", unsafe_allow_html=True)

# ================= CHART DATA =================
candles = df[['time', 'Open', 'High', 'Low', 'Close']].rename(columns={
    'Open': 'open', 'High': 'high', 'Low': 'low', 'Close': 'close'
}).to_dict('records')

for row in candles:
    row['open'] = float(row['open'])
    row['high'] = float(row['high'])
    row['low'] = float(row['low'])
    row['close'] = float(row['close'])

series = [
    {
        "type": "Candlestick",
        "data": candles,
        "options": {
            "upColor": "#00E5B4",
            "downColor": "#FF4D6A",
            "borderVisible": False,
            "wickUpColor": "#00E5B4",
            "wickDownColor": "#FF4D6A"
        }
    }
]

if show_ma20:
    ma20 = df[['time', 'MA20']].dropna()
    ma20 = [{"time": r['time'], "value": float(r['MA20'])} for _, r in ma20.iterrows()]
    if ma20:
        series.append({
            "type": "Line",
            "data": ma20,
            "options": {"color": "#F5A623", "lineWidth": 1, "lineStyle": 0}
        })

if show_ma50:
    ma50 = df[['time', 'MA50']].dropna()
    ma50 = [{"time": r['time'], "value": float(r['MA50'])} for _, r in ma50.iterrows()]
    if ma50:
        series.append({
            "type": "Line",
            "data": ma50,
            "options": {"color": "#4D9FFF", "lineWidth": 1, "lineStyle": 0}
        })

# ================= CHART OPTIONS =================
chart_options = {
    "layout": {
        "background": {"type": "solid", "color": "#0D1017"},
        "textColor": "#3A4459",
        "fontSize": 11,
        "fontFamily": "'Space Mono', monospace",
    },
    "grid": {
        "vertLines": {"color": "#0F1318", "style": 0},
        "horzLines": {"color": "#0F1318", "style": 0},
    },
    "crosshair": {
        "mode": 1,
        "vertLine": {
            "color": "rgba(0, 229, 180, 0.3)",
            "labelBackgroundColor": "#00E5B4"
        },
        "horzLine": {
            "color": "rgba(0, 229, 180, 0.3)",
            "labelBackgroundColor": "#00E5B4"
        }
    },
    "rightPriceScale": {
        "borderColor": "#13181F",
        "textColor": "#3A4459",
    },
    "timeScale": {
        "borderColor": "#13181F",
        "timeVisible": True,
        "secondsVisible": False,
        "tickMarkFormatter": None,
    },
    "watermark": {
        "visible": True,
        "fontSize": 48,
        "horzAlign": "center",
        "vertAlign": "center",
        "color": "rgba(255,255,255,0.02)",
        "text": ticker,
    }
}

chart = {"chart": chart_options, "series": series}

# Legend row
legend_html = f"""
<div style="
    display: flex;
    gap: 1.5rem;
    align-items: center;
    margin-bottom: 0.6rem;
    font-family: 'Space Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
">
    <span style="color:#3A4459">● Candles</span>
    {'<span style="color:#F5A623">— MA20</span>' if show_ma20 else ''}
    {'<span style="color:#4D9FFF">— MA50</span>' if show_ma50 else ''}
</div>
"""
st.markdown(legend_html, unsafe_allow_html=True)

try:
    renderLightweightCharts([chart], key="main_chart")
except TypeError:
    renderLightweightCharts([chart])

# ================= DATA TABLE =================
st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
with st.expander("▸  Raw Data  ·  Last 50 Sessions"):
    styled_df = df.tail(50)[['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'MA20', 'MA50']]
    st.dataframe(styled_df, use_container_width=True, hide_index=True)
