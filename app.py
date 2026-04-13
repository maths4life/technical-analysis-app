import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime, time as dtime
import pytz
from streamlit_lightweight_charts import renderLightweightCharts

# ================= PAGE ================= #
st.set_page_config(layout="wide", page_title="Terminal", page_icon="💴")

# ================= HELPERS ================= #

def compute_rsi(series, period=14):
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.ewm(com=period - 1, min_periods=period).mean()
    avg_loss = loss.ewm(com=period - 1, min_periods=period).mean()
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))


def fmt_indian(n):
    if n is None:
        return "—"
    n = int(n)
    if n >= 10_000_000:
        return f"{n/10_000_000:.2f} Cr"
    if n >= 100_000:
        return f"{n/100_000:.2f} L"
    return f"{n:,}"


# ================= DATA ================= #

@st.cache_data(ttl=300)
def fetch_today_data(ticker):
    df = yf.download(ticker, period="5d", interval="1d", auto_adjust=False)
    if df.empty:
        return None
    df.columns = [col[0] if isinstance(col, tuple) else col for col in df.columns]
    return df.iloc[-1]


@st.cache_data(ttl=3600)
def fetch_data(ticker, period, interval):
    df = yf.download(ticker, period=period, interval=interval, auto_adjust=False)
    if df.empty:
        return None

    df.columns = [col[0] if isinstance(col, tuple) else col for col in df.columns]
    df = df.reset_index()

    date_col = "Datetime" if "Datetime" in df.columns else "Date"
    df = df.rename(columns={date_col: "Date"})
    df["Date"] = pd.to_datetime(df["Date"])
    df["time"] = df["Date"].dt.strftime("%Y-%m-%d")

    df["MA20"] = df["Close"].rolling(20).mean()
    df["MA50"] = df["Close"].rolling(50).mean()
    df["RSI"] = compute_rsi(df["Close"])

    return df


# ================= SIDEBAR ================= #

st.sidebar.title("Controls")

ticker = st.sidebar.text_input("Symbol", "RELIANCE.NS").upper()
period = st.sidebar.radio("Period", ["1mo", "3mo", "6mo", "1y"], index=3)
interval = "1d"

show_ma20 = st.sidebar.checkbox("MA 20", True)
show_ma50 = st.sidebar.checkbox("MA 50", True)
show_volume = st.sidebar.checkbox("Volume", True)
show_rsi = st.sidebar.checkbox("RSI", True)

# ================= FETCH ================= #

df = fetch_data(ticker, period, interval)
today = fetch_today_data(ticker)

if df is None:
    st.error("No data found")
    st.stop()

last = df.iloc[-1]
prev = df.iloc[-2]

close = float(last["Close"])
prev_close = float(prev["Close"])
change = ((close - prev_close) / prev_close) * 100
change_abs = close - prev_close

# ================= HEADER ================= #

st.markdown(f"## {ticker}")
st.markdown(f"### ₹{close:,.2f} ({change:+.2f}%)")

# ================= METRICS ================= #

c1, c2, c3, c4 = st.columns(4)

c1.metric("Last Price", f"₹{close:,.2f}", f"{change:+.2f}%")

if today is not None:
    c2.metric("Day High", f"₹{float(today['High']):,.2f}")
    c3.metric("Day Low", f"₹{float(today['Low']):,.2f}")
else:
    c2.metric("Day High", "—")
    c3.metric("Day Low", "—")

c4.metric("Volume", fmt_indian(last["Volume"]))

# ================= CHART ================= #

candles = (
    df[["time","Open","High","Low","Close"]]
    .rename(columns={"Open":"open","High":"high","Low":"low","Close":"close"})
    .to_dict("records")
)

for r in candles:
    r["open"]  = float(r["open"])
    r["high"]  = float(r["high"])
    r["low"]   = float(r["low"])
    r["close"] = float(r["close"])

series = [{
    "type": "Candlestick",
    "data": candles,
    "options": {
        "upColor": "#00E5B4",
        "downColor": "#FF4D6A",
        "borderVisible": False,
        "wickUpColor": "#00E5B4",
        "wickDownColor": "#FF4D6A",
        "priceFormat": {
            "type": "price",
            "precision": 2,
            "minMove": 0.01
        }
    }
}]

# MA lines (ONLY ON CHART)
if show_ma20:
    ma20 = df[["time","MA20"]].dropna()
    series.append({
        "type": "Line",
        "data": [{"time": r["time"], "value": float(r["MA20"])} for _, r in ma20.iterrows()],
        "options": {"color": "#F5A623"}
    })

if show_ma50:
    ma50 = df[["time","MA50"]].dropna()
    series.append({
        "type": "Line",
        "data": [{"time": r["time"], "value": float(r["MA50"])} for _, r in ma50.iterrows()],
        "options": {"color": "#4D9FFF"}
    })

# ================= CHART OPTIONS ================= #

chart_opts = {
    "layout": {
        "background": {"type": "solid", "color": "#0D1017"},
        "textColor": "#C8D0DC",
    },
    "crosshair": {
        "mode": 1,
        "vertLine": {"visible": True, "labelVisible": True},
        "horzLine": {"visible": True, "labelVisible": True},
    },
}

renderLightweightCharts([{
    "chart": chart_opts,
    "series": series
}], key="chart")

# ================= OHLC BAR ================= #

st.markdown(f"""
<div style="font-family:'Space Mono', monospace; font-size:0.7rem; color:#8892A4; margin-top:8px;">
O: ₹{last['Open']:.2f} |
H: ₹{last['High']:.2f} |
L: ₹{last['Low']:.2f} |
C: ₹{last['Close']:.2f} |
Vol: {fmt_indian(last['Volume'])}
</div>
""", unsafe_allow_html=True)
