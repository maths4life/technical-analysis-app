import streamlit as st
import yfinance as yf
import pandas as pd
from streamlit_lightweight_charts import renderLightweightCharts

# ================= PAGE CONFIG =================
st.set_page_config(layout="wide", page_title="Pro-Quant Terminal", page_icon="📈")

# Custom CSS for a cleaner "SaaS" look
st.markdown("""
    <style>
    [data-testid="stMetricValue"] { font-size: 22px; color: #00E5FF; }
    .stApp { background-color: #0b0e11; }
    </style>
    """, unsafe_allow_html=True)

# ================= DATA FETCHING =================
@st.cache_data(ttl=3600)
def fetch_data(ticker, period="1y"):
    data = yf.download(ticker, period=period, auto_adjust=False)
    data.columns = [col[0] if isinstance(col, tuple) else col for col in data.columns]
    data = data.reset_index()
    data['time'] = data['Date'].dt.strftime('%Y-%m-%d')
    return data

def add_indicators(df):
    # Moving Averages
    df['MA20'] = df['Close'].rolling(20).mean()
    df['MA50'] = df['Close'].rolling(50).mean()
    
    # RSI
    delta = df['Close'].diff()
    gain = delta.clip(lower=0).rolling(14).mean()
    loss = (-delta.clip(upper=0)).rolling(14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    return df

# ================= SIDEBAR UI =================
with st.sidebar:
    st.title("⚙️ Parameters")
    ticker = st.text_input("Stock Ticker", value="MSFT").upper()
    time_frame = st.selectbox("Timeframe", ["1y", "2y", "5y", "max"], index=0)
    
    st.divider()
    st.subheader("Indicators")
    show_ma20 = st.checkbox("MA 20 (Yellow)", value=True)
    show_ma50 = st.checkbox("MA 50 (Blue)", value=True)
    
    if st.button("Refresh Data"):
        st.rerun()

# ================= MAIN UI =================
df = fetch_data(ticker, time_frame)
df = add_indicators(df)

if not df.empty:
    # 1. TOP METRICS ROW
    last_price = df['Close'].iloc[-1]
    prev_price = df['Close'].iloc[-2]
    delta_price = ((last_price - prev_price) / prev_price) * 100
    current_rsi = df['RSI'].iloc[-1]

    m1, m2, m3, m4 = st.columns(4)
    m1.metric(f"{ticker} Price", f"${last_price:,.2f}", f"{delta_price:+.2f}%")
    m2.metric("RSI (14)", f"{current_rsi:.2f}", "Overbought" if current_rsi > 70 else "Oversold" if current_rsi < 30 else "Neutral")
    m3.metric("MA 20", f"${df['MA20'].iloc[-1]:,.2f}")
    m4.metric("MA 50", f"${df['MA50'].iloc[-1]:,.2f}")

    # 2. PREPARE CHART DATA
    # Lightweight charts expects specific keys: time, open, high, low, close
    chart_data = df[['time', 'Open', 'High', 'Low', 'Close']].rename(columns={
        'Open': 'open', 'High': 'high', 'Low': 'low', 'Close': 'close'
    }).to_dict('records')

    ma20_data = df[['time', 'MA20']].rename(columns={'MA20': 'value'}).dropna().to_dict('records')
    ma50_data = df[['time', 'MA50']].rename(columns={'MA50': 'value'}).dropna().to_dict('records')

    # 3. CHART CONFIGURATION
    chart_options = {
        "layout": {
            "background": {"type": "solid", "color": "#0b0e11"},
            "textColor": "#d1d4dc",
        },
        "grid": {
            "vertLines": {"color": "rgba(42, 46, 57, 0.5)"},
            "horzLines": {"color": "rgba(42, 46, 57, 0.5)"},
        },
        "crosshair": {"mode": 0},
        "priceScale": {"borderColor": "rgba(197, 203, 206, 0.8)"},
        "timeScale": {"borderColor": "rgba(197, 203, 206, 0.8)", "barSpacing": 10},
    }

    # Render the Chart
    st.subheader(f"Technical Analysis: {ticker}")
    
    series_config = [
        {"type": "Candlestick", "data": chart_data, "options": {
            "upColor": "#26a69a", "downColor": "#ef5350", 
            "borderVisible": False, "wickUpColor": "#26a69a", "wickDownColor": "#ef5350"
        }}
    ]
    
    if show_ma20:
        series_config.append({"type": "Line", "data": ma20_data, "options": {"color": "#E3D231", "lineWidth": 2}})
    if show_ma50:
        series_config.append({"type": "Line", "data": ma50_data, "options": {"color": "#2962FF", "lineWidth": 2}})

    renderLightweightCharts(series_config, chart_options, height=500)

    # 4. DATA TABLE (Collapsed)
    with st.expander("View Raw Data"):
        st.dataframe(df.tail(20), use_container_width=True)

else:
    st.error("No data found for the given ticker.")
