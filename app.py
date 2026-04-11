import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# ================= PAGE CONFIG =================
st.set_page_config(layout="wide", page_title="MJ Trading Terminal")


# ================= CLEAN UI STYLE =================
st.markdown("""
<style>
.block-container {
    padding-top: 1rem;
    padding-bottom: 0rem;
}

[data-testid="stMetric"] {
    background-color: #111;
    padding: 15px;
    border-radius: 12px;
    text-align: center;
}

.css-1d391kg {
    background-color: #0e1117;
}
</style>
""", unsafe_allow_html=True)


# ================= SIDEBAR =================
with st.sidebar:
    st.title("⚙️ Controls")

    stock = st.text_input("Ticker", "RELIANCE.NS")

    period = st.selectbox(
        "Timeframe",
        ["1mo", "3mo", "6mo", "1y", "5y"],
        index=2
    )

    indicators = st.multiselect(
        "Indicators",
        ["MA20", "MA50", "RSI"],
        default=["MA20", "MA50"]
    )

    auto_refresh = st.checkbox("🔄 Auto Refresh")


# ================= FETCH =================
@st.cache_data
def fetch_data(stock, period):
    data = yf.download(stock, period=period, auto_adjust=False)

    data.columns = [col[0] if isinstance(col, tuple) else col for col in data.columns]
    data.index = pd.to_datetime(data.index)

    return data[['Open', 'High', 'Low', 'Close']].astype(float).dropna()


# ================= INDICATORS =================
def add_indicators(data):
    data['MA20'] = data['Close'].rolling(20).mean()
    data['MA50'] = data['Close'].rolling(50).mean()

    delta = data['Close'].diff()
    gain = delta.clip(lower=0).rolling(14).mean()
    loss = (-delta.clip(upper=0)).rolling(14).mean()
    rs = gain / loss
    data['RSI'] = 100 - (100 / (1 + rs))

    return data


# ================= CHART =================
def create_chart(data):

    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03,
        row_width=[0.25, 0.75]
    )

    # CANDLE
    fig.add_trace(go.Candlestick(
        x=data.index,
        open=data['Open'],
        high=data['High'],
        low=data['Low'],
        close=data['Close'],
        increasing_line_color='#22c55e',
        decreasing_line_color='#ef4444',
        name="Price"
    ), row=1, col=1)

    # MOVING AVERAGES
    if "MA20" in indicators:
        fig.add_trace(go.Scatter(
            x=data.index, y=data['MA20'],
            name="MA20",
            line=dict(color='#facc15', width=1.5)
        ), row=1, col=1)

    if "MA50" in indicators:
        fig.add_trace(go.Scatter(
            x=data.index, y=data['MA50'],
            name="MA50",
            line=dict(color='#3b82f6', width=1.5)
        ), row=1, col=1)

    # RSI
    if "RSI" in indicators:
        fig.add_trace(go.Scatter(
            x=data.index, y=data['RSI'],
            name="RSI",
            line=dict(color='#22d3ee')
        ), row=2, col=1)

        fig.add_hline(y=70, line=dict(color='red', dash='dash'), row=2, col=1)
        fig.add_hline(y=30, line=dict(color='green', dash='dash'), row=2, col=1)

    # STYLE
    fig.update_layout(
        template='plotly_dark',
        height=700,
        dragmode='pan',
        hovermode='x unified',
        margin=dict(l=10, r=10, t=40, b=10),
        title=stock
    )

    fig.update_xaxes(
        rangeslider_visible=False,
        showgrid=True,
        gridcolor='rgba(255,255,255,0.05)'
    )

    fig.update_yaxes(
        showgrid=True,
        gridcolor='rgba(255,255,255,0.05)'
    )

    return fig


# ================= MAIN =================
st.title("📈 MJ Trading Terminal")


data = fetch_data(stock, period)

if data.empty:
    st.error("Invalid stock ticker or no data found")
    st.stop()

data = add_indicators(data)


# ================= TOP METRICS =================
col1, col2, col3, col4 = st.columns(4)

latest_price = data['Close'].iloc[-1]
prev_price = data['Close'].iloc[-2]
change_pct = ((latest_price - prev_price) / prev_price) * 100

col1.metric("Price", round(latest_price, 2))
col2.metric("Change %", f"{round(change_pct,2)}%")
col3.metric("High", round(data['High'].iloc[-1], 2))
col4.metric("Low", round(data['Low'].iloc[-1], 2))


# ================= TABS =================
tab1, tab2, tab3 = st.tabs(["📊 Chart", "📈 Indicators", "📋 Data"])

with tab1:
    fig = create_chart(data)
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("Indicators Data")
    st.dataframe(data[['MA20', 'MA50', 'RSI']].tail(50))

with tab3:
    st.subheader("Raw Data")
    st.dataframe(data.tail(100))


# ================= AUTO REFRESH =================
if auto_refresh:
    st.rerun()
