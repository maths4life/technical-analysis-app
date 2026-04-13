import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime, time as dtime
import pytz
from streamlit_lightweight_charts import renderLightweightCharts

# ── PAGE CONFIG ───────────────────────────────────────────────────────────────
st.set_page_config(
    layout="wide",
    page_title="Terminal",
    page_icon="💴"
)

# ── STYLES ────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600&display=swap');

html, body, .stApp {
    background-color: #080A0F !important;
    color: #C8D0DC !important;
    font-family: 'DM Sans', sans-serif !important;
}
.block-container { padding: 1.5rem 2.5rem 2rem 2.5rem !important; max-width: 100% !important; }

/* ── SIDEBAR ── */
[data-testid="stSidebar"] { background: #0D1017 !important; border-right: 1px solid rgba(0,229,180,0.12) !important; }
[data-testid="stSidebar"] h1 {
    font-family: 'Space Mono', monospace !important; font-size: 1rem !important;
    letter-spacing: 0.18em !important; text-transform: uppercase !important; color: #00E5B4 !important;
    padding-bottom: 1.2rem !important; border-bottom: 1px solid rgba(0,229,180,0.2) !important; margin-bottom: 1.5rem !important;
}
[data-testid="stSidebar"] label {
    font-family: 'Space Mono', monospace !important; font-size: 0.62rem !important;
    letter-spacing: 0.14em !important; text-transform: uppercase !important; color: #4A5568 !important;
}
[data-testid="stSidebar"] input {
    background: #111520 !important; border: 1px solid rgba(0,229,180,0.18) !important;
    border-radius: 4px !important; color: #00E5B4 !important;
}

/* Metric Cards */
[data-testid="stMetric"] {
    background: #0D1017 !important; border: 1px solid #161C27 !important;
    border-radius: 6px !important; padding: 0.85rem 1.1rem !important;
}
[data-testid="stMetricLabel"] { font-family: 'Space Mono', monospace !important; font-size: 0.58rem !important; color: #3A4459 !important; }
[data-testid="stMetricValue"] { font-family: 'Space Mono', monospace !important; font-size: 1.15rem !important; color: #E8EDF5 !important; }
</style>
""", unsafe_allow_html=True)

# ── HELPERS ───────────────────────────────────────────────────────────────────

def compute_rsi(series, period=14):
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.ewm(com=period - 1, min_periods=period).mean()
    avg_loss = loss.ewm(com=period - 1, min_periods=period).mean()
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

def fmt_indian(n):
    if n is None: return "—"
    n = int(n)
    if n >= 10_000_000: return f"{n/10_000_000:.2f} Cr"
    if n >= 100_000: return f"{n/100_000:.2f} L"
    s = str(n)
    if len(s) <= 3: return s
    last3, rest = s[-3:], s[:-3]
    parts = []
    while len(rest) > 2:
        parts.append(rest[-2:])
        rest = rest[:-2]
    if rest: parts.append(rest)
    return ",".join(reversed(parts)) + "," + last3

def is_nse_open():
    ist = pytz.timezone("Asia/Kolkata")
    now = datetime.now(ist)
    market_open, market_close = dtime(9, 15), dtime(15, 30)
    if now.weekday() >= 5: return False, "CLOSED · Weekend"
    t = now.time()
    if market_open <= t <= market_close: return True, "OPEN"
    return False, "CLOSED"

# ── DATA FETCH ────────────────────────────────────────────────────────────────

@st.cache_data(ttl=3600)
def fetch_data(ticker, period, interval):
    df = yf.download(ticker, period=period, interval=interval, auto_adjust=False)
    if df.empty: return None
    df.columns = [col[0] if isinstance(col, tuple) else col for col in df.columns]
    df = df.reset_index()
    date_col = "Datetime" if "Datetime" in df.columns else "Date"
    df = df.rename(columns={date_col: "Date"})
    df["Date"] = pd.to_datetime(df["Date"])
    df["time"] = df["Date"].dt.strftime("%Y-%m-%d")
    df["MA20"] = df["Close"].rolling(20).mean()
    df["MA50"] = df["Close"].rolling(50).mean()
    df["RSI"] = compute_rsi(df["Close"])
    df["TP"] = (df["High"] + df["Low"] + df["Close"]) / 3
    df["VWAP"] = (df["TP"] * df["Volume"]).cumsum() / df["Volume"].cumsum()
    return df

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("⬡ Controls")
    ticker = st.text_input("Symbol", "RELIANCE.NS").strip().upper()
    period = st.radio("Period", ["1mo", "3mo", "6mo", "1y", "5y"], index=3)
    interval = st.radio("Interval", ["1d", "1wk", "1mo"], index=0)
    st.divider()
    show_ma20 = st.checkbox("MA 20", True)
    show_ma50 = st.checkbox("MA 50", True)
    show_volume = st.checkbox("Volume", True)
    show_rsi = st.checkbox("RSI (14)", True)

# ── HEADER & DATA ─────────────────────────────────────────────────────────────
df = fetch_data(ticker, period, interval)
if df is None:
    st.error(f"No data for {ticker}")
    st.stop()

last = df.iloc[-1]
prev_close = float(df.iloc[-2]["Close"])
close = float(last["Close"])
change = ((close - prev_close) / prev_close) * 100

st.subheader(f"{ticker} · ₹{close:,.2f} ({change:+.2f}%)")

# ── DYNAMIC HOVER RIBBON ──────────────────────────────────────────────────────
# This placeholder will update when the user hovers over the chart
hover_res = st.empty()

# ── CHART CONFIG ──────────────────────────────────────────────────────────────
def base_opts(show_time=True):
    return {
        "layout": {"background": {"type": "solid", "color": "#0D1017"}, "textColor": "#8892A4", "fontSize": 11},
        "grid": {"vertLines": {"color": "#161C27"}, "horzLines": {"color": "#161C27"}},
        "crosshair": {
            "mode": 0,
            "vertLine": {"labelBackgroundColor": "#00E5B4", "color": "rgba(0,229,180,0.2)"},
            "horzLine": {"labelBackgroundColor": "#00E5B4", "color": "rgba(0,229,180,0.2)"}
        },
        "rightPriceScale": {"borderColor": "#2A3344", "autoScale": True, "scaleMargins": {"top": 0.1, "bottom": 0.1}},
        "timeScale": {"borderColor": "#2A3344", "timeVisible": show_time}
    }

# ── SERIES PREP ───────────────────────────────────────────────────────────────
candles = df[["time","Open","High","Low","Close"]].rename(columns=lambda x: x.lower()).to_dict("records")
price_series = [{"type": "Candlestick", "data": candles, "options": {"upColor": "#00E5B4", "downColor": "#FF4D6A"}}]

if show_ma20:
    ma20_data = [{"time": r["time"], "value": float(r["MA20"])} for _, r in df.dropna(subset=["MA20"]).iterrows()]
    price_series.append({"type": "Line", "data": ma20_data, "options": {"color": "#F5A623", "lineWidth": 1}})

charts_to_render = [{"chart": base_opts(show_time=not (show_volume or show_rsi)), "series": price_series}]

if show_volume:
    vol_data = [{"time": r["time"], "value": float(r["Volume"]), "color": "#00E5B488" if r["Close"] >= r["Open"] else "#FF4D6A88"} for _, r in df.iterrows()]
    charts_to_render.append({"chart": base_opts(show_time=not show_rsi), "series": [{"type": "Histogram", "data": vol_data, "options": {"priceFormat": {"type": "volume"}}}]})

if show_rsi:
    rsi_data = [{"time": r["time"], "value": float(r["RSI"])} for _, r in df.dropna(subset=["RSI"]).iterrows()]
    charts_to_render.append({"chart": base_opts(show_time=True), "series": [{"type": "Line", "data": rsi_data, "options": {"color": "#A78BFA"}}]})

# ── RENDER & INTERACTION ──────────────────────────────────────────────────────
for c in charts_to_render: c["chart"]["height"] = 400 if len(charts_to_render) == 1 else 250

# Capture the interaction result
result = renderLightweightCharts(charts_to_render, key="main_chart")

# Update ribbon on hover
if result and "time" in result:
    match = df[df["time"] == result["time"]]
    if not match.empty:
        r = match.iloc[0]
        hover_res.markdown(
            f"""<div style="display:flex; gap:20px; font-family:'Space Mono'; font-size:0.9rem; color:#00E5B4; background:#111520; padding:10px; border-radius:5px;">
            <span><b>DATE:</b> {r['time']}</span>
            <span><b>O:</b> {r['Open']:,.2f}</span>
            <span><b>H:</b> {r['High']:,.2f}</span>
            <span><b>L:</b> {r['Low']:,.2f}</span>
            <span><b>C:</b> {r['Close']:,.2f}</span>
            <span><b>VOL:</b> {fmt_indian(r['Volume'])}</span>
            </div>""", unsafe_allow_html=True)
else:
    hover_res.info("Hover over the chart to see OHLCV data")
