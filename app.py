import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# ================= FETCH =================
def fetch_data(stock, period="5y"):
    data = yf.download(stock, period=period, auto_adjust=False)

    # Fix column format
    data.columns = [col[0] if isinstance(col, tuple) else col for col in data.columns]

    # Ensure datetime index
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
def create_chart(data, stock):

    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03,
        row_width=[0.25, 0.75]
    )

    # ----- CANDLE -----
    fig.add_trace(go.Candlestick(
        x=data.index,
        open=data['Open'],
        high=data['High'],
        low=data['Low'],
        close=data['Close'],
        increasing_line_color='#00C853',
        decreasing_line_color='#D50000',
        name="Price"
    ), row=1, col=1)

    # ----- MOVING AVERAGES -----
    fig.add_trace(go.Scatter(
        x=data.index, y=data['MA20'],
        name="MA20",
        line=dict(color='#FFD600', width=1.5)
    ), row=1, col=1)

    fig.add_trace(go.Scatter(
        x=data.index, y=data['MA50'],
        name="MA50",
        line=dict(color='#2962FF', width=1.5)
    ), row=1, col=1)

    # ----- RSI -----
    fig.add_trace(go.Scatter(
        x=data.index, y=data['RSI'],
        name="RSI",
        line=dict(color='#00E5FF')
    ), row=2, col=1)

    fig.add_hline(y=70, line=dict(color='red', dash='dash'), row=2, col=1)
    fig.add_hline(y=30, line=dict(color='green', dash='dash'), row=2, col=1)

    # ----- DEFAULT 6 MONTH VIEW (FIXED) -----
    end_date = data.index.max()
    start_date = end_date - pd.Timedelta(days=180)

    recent = data.loc[start_date:end_date]

    if not recent.empty:
        fig.update_xaxes(range=[recent.index[0], recent.index[-1]])

        fig.update_yaxes(
            range=[recent['Low'].min()*0.98, recent['High'].max()*1.02],
            row=1, col=1
        )

    fig.update_yaxes(range=[0, 100], row=2, col=1)

    # ----- STYLE -----
    fig.update_layout(
        title=stock,
        template='plotly_dark',
        height=800,
        dragmode='pan',
        hovermode='x unified'
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


# ================= STREAMLIT APP =================
st.set_page_config(layout="wide")
st.title("📈 Live Stock Chart")

stock = st.text_input("Enter Stock Ticker", "RELIANCE.NS")

# Fetch data
data = fetch_data(stock)

if data.empty:
    st.error("Invalid stock ticker or no data found")
    st.stop()

# Indicators
data = add_indicators(data)

# Chart
fig = create_chart(data, stock)

st.plotly_chart(fig, use_container_width=True)

# Refresh option
if st.checkbox("🔄 Auto Refresh"):
    st.rerun()
