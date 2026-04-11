import streamlit as st
import yfinance as yf
import pandas as pd
from streamlit_lightweight_charts import renderLightweightCharts

# ================= PAGE CONFIG =================
st.set_page_config(layout="wide", page_title="Quant Terminal", page_icon="📈")

st.markdown("""
    <style>
    [data-testid="stMetricValue"] { font-size: 24px; color: #00E5FF; }
    .stApp { background-color: #0b0e11; }
    </style>
    """, unsafe_allow_html=True)

# ================= DATA ENGINE =================
@st.cache_data(ttl=3600)
def fetch_and_clean_data(ticker, period="1y"):
    try:
        # Fetching with auto_adjust=True to avoid some common yfinance formatting issues
        df = yf.download(ticker, period=period, auto_adjust=True)
        if df.empty:
            return None
        
        # Flatten columns
        df.columns = [col[0] if isinstance(col, tuple) else col for col in df.columns]
        df = df.reset_index()
        
        # Format time to string (YYYY-MM-DD)
        df['time'] = df['Date'].dt.strftime('%Y-%m-%d')
        
        # Calculate Indicators
        df['MA20'] = df['Close'].rolling(20).mean()
        df['MA50'] = df['Close'].rolling(50).mean()
        
        delta = df['Close'].diff()
        gain = delta.clip(lower=0).rolling(14).mean()
        loss = (-delta.clip(upper=0)).rolling(14).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))
        
        return df
    except Exception as e:
        return None

# ================= SIDEBAR =================
with st.sidebar:
    st.title("📊 Terminal Settings")
    ticker = st.text_input("Symbol", value="RELIANCE.NS").upper()
    time_frame = st.selectbox("History", ["1y", "2y", "5y", "max"])
    
    st.divider()
    st.subheader("Overlays")
    show_ma20 = st.checkbox("20-Day MA (Yellow)", value=True)
    show_ma50 = st.checkbox("50-Day MA (Blue)", value=True)
    
    if st.button("Force Refresh"):
        st.cache_data.clear()
        st.rerun()

# ================= MAIN INTERFACE =================
df = fetch_and_clean_data(ticker, time_frame)

if df is not None:
    # 1. METRICS (Using the last valid index)
    last_idx = df['RSI'].last_valid_index()
    last_row = df.loc[last_idx]
    
    # Calculate price change
    prev_close = df['Close'].iloc[-2] if len(df) > 1 else last_row['Close']
    change = ((last_row['Close'] - prev_close) / prev_close) * 100

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Live Price", f"₹{last_row['Close']:,.2f}", f"{change:+.2f}%")
    col2.metric("RSI (14)", f"{last_row['RSI']:.2f}")
    col3.metric("MA 20", f"₹{last_row['MA20']:,.2f}" if not pd.isna(last_row['MA20']) else "N/A")
    col4.metric("MA 50", f"₹{last_row['MA50']:,.2f}" if not pd.isna(last_row['MA50']) else "N/A")

    # 2. PREPARE JSON DATA (The Fix: .dropna() here prevents the TypeError)
    # We drop any rows that don't have price data
    chart_data = df[['time', 'Open', 'High', 'Low', 'Close']].dropna().rename(
        columns={'Open': 'open', 'High': 'high', 'Low': 'low', 'Close': 'close'}
    ).to_dict('records')

    # Indicators (Ensuring no NaNs)
    ma20_list = df[['time', 'MA20']].dropna().rename(columns={'MA20': 'value'}).to_dict('records')
    ma50_list = df[['time', 'MA50']].dropna().rename(columns={'MA50': 'value'}).to_dict('records')

    # 3. CHART UI CONFIG
    chart_options = {
        "layout": {
            "background": {"type": "solid", "color": "#0b0e11"},
            "textColor": "#d1d4dc",
        },
        "grid": {
            "vertLines": {"color": "rgba(42, 46, 57, 0.1)"},
            "horzLines": {"color": "rgba(42, 46, 57, 0.1)"},
        },
        "priceScale": {"mode": 1, "autoScale": True},
        "timeScale": {"barSpacing": 10, "rightOffset": 5},
    }

    series_config = [
        {
            "type": "Candlestick", 
            "data": chart_data, 
            "options": {
                "upColor": "#26a69a", "downColor": "#ef5350",
                "borderVisible": False, "wickUpColor": "#26a69a", "wickDownColor": "#ef5350"
            }
        }
    ]

    if show_ma20 and ma20_list:
        series_config.append({"type": "Line", "data": ma20_list, "options": {"color": "#E3D231", "lineWidth": 1.5}})
    
    if show_ma50 and ma50_list:
        series_config.append({"type": "Line", "data": ma50_list, "options": {"color": "#2962FF", "lineWidth": 1.5}})

    # 4. RENDER
    st.subheader(f"Technical Chart: {ticker}")
    # Height fixed at 600 as per your previous error screenshot
    renderLightweightCharts(series_config, chart_options, height=600)

else:
    st.error("Invalid ticker or could not fetch data. Please try again.")
