import streamlit as st
import yfinance as yf
import pandas as pd
from streamlit_lightweight_charts import renderLightweightCharts

# ================= PAGE CONFIG =================
st.set_page_config(layout="wide", page_title="Quant Terminal", page_icon="📈")

# ================= UI STYLE =================
st.markdown("""
<style>
.stApp { background-color: #0b0e11; }
[data-testid="stMetricValue"] { font-size: 22px; color: #00E5FF; }
.block-container { padding: 1rem 2rem; }
</style>
""", unsafe_allow_html=True)

# ================= DATA =================
@st.cache_data(ttl=3600)
def fetch_data(ticker, period):
    df = yf.download(ticker, period=period, auto_adjust=False)

    if df.empty:
        return None

    # Fix columns
    df.columns = [col[0] if isinstance(col, tuple) else col for col in df.columns]

    df = df.reset_index()
    df['Date'] = pd.to_datetime(df['Date'])

    # REQUIRED FORMAT for lightweight charts
    df['time'] = df['Date'].dt.strftime('%Y-%m-%d')

    # Indicators
    df['MA20'] = df['Close'].rolling(20).mean()
    df['MA50'] = df['Close'].rolling(50).mean()

    return df

# ================= SIDEBAR =================
with st.sidebar:
    st.title("📊 Terminal Settings")

    ticker = st.text_input("Symbol", "RELIANCE.NS").upper()

    period = st.selectbox(
        "History",
        ["6mo", "1y", "2y", "5y"],
        index=1
    )

    st.divider()
    st.subheader("Indicators")

    show_ma20 = st.checkbox("MA20", True)
    show_ma50 = st.checkbox("MA50", True)

    if st.button("Refresh"):
        st.cache_data.clear()
        st.rerun()

# ================= MAIN =================
df = fetch_data(ticker, period)

if df is None:
    st.error("Invalid ticker or no data")
    st.stop()

# ================= METRICS =================
last = df.iloc[-1]
prev = df.iloc[-2]

change = ((last['Close'] - prev['Close']) / prev['Close']) * 100

c1, c2, c3, c4 = st.columns(4)

c1.metric("Price", f"₹ {last['Close']:.2f}", f"{change:.2f}%")
c2.metric("High", f"₹ {last['High']:.2f}")
c3.metric("Low", f"₹ {last['Low']:.2f}")
c4.metric("Volume", f"{int(last['Volume']):,}" if 'Volume' in df else "N/A")

# ================= CHART DATA =================
candles = df[['time', 'Open', 'High', 'Low', 'Close']].rename(columns={
    'Open': 'open',
    'High': 'high',
    'Low': 'low',
    'Close': 'close'
}).to_dict('records')

series = [
    {
        "type": "Candlestick",
        "data": candles,
        "options": {
            "upColor": "#22c55e",
            "downColor": "#ef4444",
            "borderVisible": False,
            "wickUpColor": "#22c55e",
            "wickDownColor": "#ef4444"
        }
    }
]

# Add indicators safely (NO NaNs)
if show_ma20:
    ma20 = df[['time', 'MA20']].dropna().rename(columns={'MA20': 'value'}).to_dict('records')
    series.append({
        "type": "Line",
        "data": ma20,
        "options": {"color": "#facc15", "lineWidth": 1}
    })

if show_ma50:
    ma50 = df[['time', 'MA50']].dropna().rename(columns={'MA50': 'value'}).to_dict('records')
    series.append({
        "type": "Line",
        "data": ma50,
        "options": {"color": "#3b82f6", "lineWidth": 1}
    })

# ================= CHART OPTIONS =================
chart_options = {
    "layout": {
        "background": {"type": "solid", "color": "#0b0e11"},
        "textColor": "#d1d4dc",
    },
    "grid": {
        "vertLines": {"color": "rgba(255,255,255,0.05)"},
        "horzLines": {"color": "rgba(255,255,255,0.05)"},
    },
    "crosshair": {"mode": 1},
    "timeScale": {
        "timeVisible": True,
        "secondsVisible": False
    }
}

# ================= FIXED RENDER =================
chart = {
    "chart": chart_options,
    "series": series
}

st.subheader(f"📈 {ticker} Chart")

renderLightweightCharts([chart], height=600)

# ================= DATA TABLE =================
with st.expander("📋 View Raw Data"):
    st.dataframe(df.tail(50), use_container_width=True)
