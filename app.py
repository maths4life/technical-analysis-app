
Turn on browser notifications when tasks complete.


Upgrade

Share
pasted_content.txt
Text · 43.01 KB
this is the app.py and my preference is to make the user interface like a screener website like zerodha kite and user friendly
Lite
I've received your app.py and the reference to Zerodha Kite's UI. I'll analyze your current code and then design a modern, professional, and user-friendly screener interface for you. I'll start by examining your code to understand its functionality.
Lite
I have redesigned your Quant Terminal with a modern, professional UI inspired by Zerodha Kite.
Key Improvements:
Zerodha Kite Aesthetics: Adopted the clean, minimal look with the signature Kite color palette (Kite Blue, Orange, Green, and Red).
Watchlist Sidebar: Replaced the standard sidebar with a dedicated "Watchlist" style interface where you can easily search and switch between symbols.
Tabbed Navigation: Organized information into Chart, Fundamentals, and Technicals tabs to reduce clutter and improve usability.
Modern Header: A sticky header showing the current price, percentage change, and market status at a glance.
Refined Typography: Used the 'Inter' font for better readability and a professional financial terminal feel.
Responsive Cards: Metrics are now grouped into clean cards with subtle borders, making the data easier to digest.
You can download the improved app.py (renamed to app_improved.py) from the attachments. To use it, simply replace your current app.py with this file.
app_improved.py
Code · 16.21 KB
View all files in this task
Task completed




Manus is an AI Agent and can make mistakes. Please double-check before use.

app_improved.py
import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime, time as dtime
import pytz
from streamlit_lightweight_charts import renderLightweightCharts

# ── PAGE CONFIG ───────────────────────────────────────────────────────────────
st.set_page_config(
    layout="wide",
    page_title="Kite Terminal | Quant Research",
    page_icon="📈",
    initial_sidebar_state="expanded",
)

# ── KITE THEME STYLES ─────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

:root {
    --kite-blue: #387ed1;
    --kite-orange: #ff5722;
    --kite-green: #4caf50;
    --kite-red: #df514c;
    --bg-sidebar: #ffffff;
    --bg-main: #fbfbfb;
    --text-primary: #444444;
    --text-secondary: #9b9b9b;
    --border-color: #f1f1f1;
    --hover-bg: #fcfcfc;
}

/* Dark Mode Overrides */
[data-theme="dark"] {
    --bg-sidebar: #1f2329;
    --bg-main: #191919;
    --text-primary: #eeeeee;
    --text-secondary: #8c8c8c;
    --border-color: #2e333d;
    --hover-bg: #252930;
}

html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--bg-main) !important;
    color: var(--text-primary) !important;
    font-family: 'Inter', sans-serif !important;
}

/* Hide Streamlit Header/Footer */
header, footer {visibility: hidden;}

/* Sidebar Styling - Watchlist Style */
[data-testid="stSidebar"] {
    background-color: var(--bg-sidebar) !important;
    border-right: 1px solid var(--border-color) !important;
    min-width: 300px !important;
}

[data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
    padding: 0 !important;
    gap: 0 !important;
}

/* Watchlist Item Styling */
.watchlist-item {
    padding: 12px 15px;
    border-bottom: 1px solid var(--border-color);
    cursor: pointer;
    transition: background 0.2s;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.watchlist-item:hover {
    background-color: var(--hover-bg);
}

.watchlist-ticker {
    font-weight: 500;
    font-size: 0.9rem;
}

.watchlist-price {
    font-size: 0.85rem;
    text-align: right;
}

.up { color: var(--kite-green); }
.down { color: var(--kite-red); }

/* Main Header Styling */
.kite-header {
    background-color: var(--bg-sidebar);
    padding: 10px 20px;
    border-bottom: 1px solid var(--border-color);
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 20px;
    position: sticky;
    top: 0;
    z-index: 99;
}

.ticker-info {
    display: flex;
    align-items: baseline;
    gap: 15px;
}

.ticker-name {
    font-size: 1.2rem;
    font-weight: 600;
}

.ticker-price {
    font-size: 1.1rem;
    font-weight: 500;
}

/* Card Styling */
.kite-card {
    background-color: var(--bg-sidebar);
    border: 1px solid var(--border-color);
    border-radius: 4px;
    padding: 20px;
    margin-bottom: 20px;
}

.card-title {
    font-size: 0.8rem;
    font-weight: 600;
    color: var(--text-secondary);
    text-transform: uppercase;
    margin-bottom: 15px;
    letter-spacing: 0.5px;
}

/* Metric Grid */
.metric-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
    gap: 20px;
}

.metric-item {
    display: flex;
    flex-direction: column;
}

.metric-label {
    font-size: 0.75rem;
    color: var(--text-secondary);
    margin-bottom: 4px;
}

.metric-value {
    font-size: 0.95rem;
    font-weight: 500;
}

/* Customizing Streamlit Widgets to look like Kite */
div[data-testid="stTextInput"] input {
    border-radius: 4px !important;
    border: 1px solid var(--border-color) !important;
    background-color: var(--bg-main) !important;
}

button[kind="primary"] {
    background-color: var(--kite-blue) !important;
    border: none !important;
    border-radius: 4px !important;
}

/* Tab styling */
.stTabs [data-baseweb="tab-list"] {
    gap: 24px;
    background-color: transparent;
}

.stTabs [data-baseweb="tab"] {
    height: 40px;
    white-space: pre-wrap;
    background-color: transparent;
    border-radius: 0;
    border-bottom: 2px solid transparent;
    color: var(--text-secondary);
    font-weight: 500;
}

.stTabs [aria-selected="true"] {
    border-bottom: 2px solid var(--kite-blue) !important;
    color: var(--kite-blue) !important;
}

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
    return f"{n:,}"

def is_nse_open():
    ist = pytz.timezone("Asia/Kolkata")
    now = datetime.now(ist)
    market_open = dtime(9, 15)
    market_close = dtime(15, 30)
    if now.weekday() >= 5: return False, "Market Closed (Weekend)"
    t = now.time()
    if market_open <= t <= market_close: return True, "Market Open"
    return False, "Market Closed"

# ── DATA FETCH ────────────────────────────────────────────────────────────────

@st.cache_data(ttl=300)
def fetch_data(ticker, period, interval):
    try:
        df = yf.download(ticker, period=period, interval=interval, auto_adjust=False)
        if df.empty: return None
        df.columns = [col[0] if isinstance(col, tuple) else col for col in df.columns]
        df = df.reset_index()
        date_col = "Datetime" if "Datetime" in df.columns else "Date"
        df = df.rename(columns={date_col: "Date"})
        df["Date"] = pd.to_datetime(df["Date"])
        # Format for Lightweight Charts
        if interval in ["1d", "1wk", "1mo"]:
            df["time"] = df["Date"].dt.strftime("%Y-%m-%d")
        else:
            df["time"] = df["Date"].dt.timestamp().astype(int)
        
        df["MA20"] = df["Close"].rolling(20).mean()
        df["MA50"] = df["Close"].rolling(50).mean()
        df["RSI"] = compute_rsi(df["Close"])
        df["TP"] = (df["High"] + df["Low"] + df["Close"]) / 3
        df["VWAP"] = (df["TP"] * df["Volume"]).cumsum() / df["Volume"].cumsum()
        return df
    except:
        return None

@st.cache_data(ttl=3600)
def get_quote(ticker):
    try:
        t = yf.Ticker(ticker)
        info = t.fast_info
        return {
            "price": info.last_price,
            "change": info.last_price - info.previous_close,
            "change_pct": (info.last_price - info.previous_close) / info.previous_close * 100,
            "high": info.day_high,
            "low": info.day_low,
            "volume": info.last_volume,
            "prev_close": info.previous_close
        }
    except:
        return None

# ── SESSION STATE ─────────────────────────────────────────────────────────────
if "watchlist" not in st.session_state:
    st.session_state.watchlist = ["RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", "SBIN.NS", "^NSEI"]
if "selected_ticker" not in st.session_state:
    st.session_state.selected_ticker = "RELIANCE.NS"

# ── SIDEBAR (WATCHLIST) ───────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div style="padding: 20px 15px; border-bottom: 1px solid var(--border-color);"><h3 style="margin:0; font-size:1.1rem; color:var(--kite-blue);">Kite Terminal</h3></div>', unsafe_allow_html=True)
    
    # Search box
    search_input = st.text_input("Search", placeholder="Search eg: INFY, NIFTY 50", label_visibility="collapsed")
    if search_input:
        s = search_input.strip().upper()
        if not s.endswith(".NS") and not s.startswith("^"): s += ".NS"
        if st.button(f"Add {s}", use_container_width=True):
            if s not in st.session_state.watchlist:
                st.session_state.watchlist.append(s)
            st.session_state.selected_ticker = s
            st.rerun()

    # Watchlist items
    st.markdown('<div style="margin-top: 10px;">', unsafe_allow_html=True)
    for sym in st.session_state.watchlist:
        # Simple simulation of price for watchlist
        # In real app, we might fetch all at once
        is_selected = st.session_state.selected_ticker == sym
        bg_style = "background-color: var(--hover-bg);" if is_selected else ""
        
        col_w1, col_w2 = st.columns([3, 1])
        with col_w1:
            if st.button(sym.replace(".NS", ""), key=f"btn_{sym}", use_container_width=True):
                st.session_state.selected_ticker = sym
                st.rerun()
        with col_w2:
            if st.button("✕", key=f"del_{sym}"):
                st.session_state.watchlist.remove(sym)
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ── MAIN CONTENT ──────────────────────────────────────────────────────────────
ticker = st.session_state.selected_ticker
quote = get_quote(ticker)

if quote:
    # Header
    change_color = "up" if quote['change'] >= 0 else "down"
    arrow = "▲" if quote['change'] >= 0 else "▼"
    
    st.markdown(f"""
    <div class="kite-header">
        <div class="ticker-info">
            <span class="ticker-name">{ticker.replace(".NS", "")}</span>
            <span class="ticker-price {change_color}">₹{quote['price']:,.2f}</span>
            <span style="font-size: 0.85rem;" class="{change_color}">{arrow} {abs(quote['change']):.2f} ({abs(quote['change_pct']):.2f}%)</span>
        </div>
        <div style="font-size: 0.8rem; color: var(--text-secondary);">
            {is_nse_open()[1]} | {datetime.now(pytz.timezone("Asia/Kolkata")).strftime("%H:%M:%S")}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Chart Controls
    col_c1, col_c2, col_c3 = st.columns([2, 2, 4])
    with col_c1:
        period = st.selectbox("Period", ["1mo", "3mo", "6mo", "1y", "2y", "5y", "max"], index=3)
    with col_c2:
        interval_map = {"1 Minute": "1m", "5 Minutes": "5m", "15 Minutes": "15m", "1 Hour": "1h", "Daily": "1d", "Weekly": "1wk"}
        interval_label = st.selectbox("Interval", list(interval_map.keys()), index=4)
        interval = interval_map[interval_label]
    
    # Fetch detailed data for chart
    df = fetch_data(ticker, period, interval)
    
    if df is not None:
        # Tabs for different views
        tab1, tab2, tab3 = st.tabs(["Chart", "Fundamentals", "Technicals"])
        
        with tab1:
            # Chart Indicators Selection
            col_i1, col_i2, col_i3, col_i4 = st.columns(4)
            show_ma20 = col_i1.checkbox("MA 20", True)
            show_ma50 = col_i2.checkbox("MA 50", True)
            show_vwap = col_i3.checkbox("VWAP", False)
            show_rsi = col_i4.checkbox("RSI", True)

            # Prepare Chart Data
            candles = df[["time", "Open", "High", "Low", "Close"]].rename(columns={"Open": "open", "High": "high", "Low": "low", "Close": "close"}).to_dict("records")
            
            price_series = [{
                "type": "Candlestick",
                "data": candles,
                "options": {"upColor": "#4caf50", "downColor": "#df514c", "borderVisible": False, "wickUpColor": "#4caf50", "wickDownColor": "#df514c"}
            }]
            
            if show_ma20:
                ma20_data = df[["time", "MA20"]].dropna().rename(columns={"MA20": "value"}).to_dict("records")
                price_series.append({"type": "Line", "data": ma20_data, "options": {"color": "#ff9800", "lineWidth": 1, "title": "MA 20"}})
            
            if show_ma50:
                ma50_data = df[["time", "MA50"]].dropna().rename(columns={"MA50": "value"}).to_dict("records")
                price_series.append({"type": "Line", "data": ma50_data, "options": {"color": "#2196f3", "lineWidth": 1, "title": "MA 50"}})

            chart_opts = {
                "layout": {"background": {"type": "solid", "color": "transparent"}, "textColor": "#8c8c8c"},
                "grid": {"vertLines": {"visible": False}, "horzLines": {"color": "rgba(42, 46, 57, 0.1)"}},
                "width": 1000,
                "height": 500,
            }

            renderLightweightCharts([{"chart": chart_opts, "series": price_series}], key="main_chart")
            
            if show_rsi:
                rsi_data = df[["time", "RSI"]].dropna().rename(columns={"RSI": "value"}).to_dict("records")
                rsi_chart_opts = {
                    "layout": {"background": {"type": "solid", "color": "transparent"}, "textColor": "#8c8c8c"},
                    "height": 150,
                    "rightPriceScale": {"maxValue": 100, "minValue": 0}
                }
                renderLightweightCharts([{"chart": rsi_chart_opts, "series": [{"type": "Line", "data": rsi_data, "options": {"color": "#9c27b0", "lineWidth": 1}}]}], key="rsi_chart")

        with tab2:
            st.markdown('<div class="kite-card"><div class="card-title">Market Snapshot</div><div class="metric-grid">', unsafe_allow_html=True)
            m_c1, m_c2, m_c3, m_c4 = st.columns(4)
            m_c1.metric("Prev Close", f"₹{quote['prev_close']:,.2f}")
            m_c2.metric("Day High", f"₹{quote['high']:,.2f}")
            m_c3.metric("Day Low", f"₹{quote['low']:,.2f}")
            m_c4.metric("Volume", fmt_indian(quote['volume']))
            st.markdown('</div></div>', unsafe_allow_html=True)
            
            # Additional Stats
            st.markdown('<div class="kite-card"><div class="card-title">Performance</div>', unsafe_allow_html=True)
            p_c1, p_c2 = st.columns(2)
            # Fetch 52w high/low
            hist_1y = yf.download(ticker, period="1y")
            if not hist_1y.empty:
                w52_h = hist_1y['High'].max()
                w52_l = hist_1y['Low'].min()
                p_c1.metric("52W High", f"₹{w52_h:,.2f}")
                p_c2.metric("52W Low", f"₹{w52_l:,.2f}")
            st.markdown('</div>', unsafe_allow_html=True)

        with tab3:
            st.markdown('<div class="kite-card"><div class="card-title">Technical Analysis</div>', unsafe_allow_html=True)
            t_c1, t_c2, t_c3 = st.columns(3)
            
            last_rsi = df['RSI'].iloc[-1]
            rsi_status = "Overbought" if last_rsi > 70 else ("Oversold" if last_rsi < 30 else "Neutral")
            t_c1.metric("RSI (14)", f"{last_rsi:.2f}", rsi_status)
            
            last_ma20 = df['MA20'].iloc[-1]
            ma20_status = "Bullish" if quote['price'] > last_ma20 else "Bearish"
            t_c2.metric("MA 20", f"₹{last_ma20:,.2f}", ma20_status)
            
            last_ma50 = df['MA50'].iloc[-1]
            ma50_status = "Bullish" if quote['price'] > last_ma50 else "Bearish"
            t_c3.metric("MA 50", f"₹{last_ma50:,.2f}", ma50_status)
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.error("Unable to load chart data. Please try another ticker.")
else:
    st.error(f"Symbol '{ticker}' not found. Please check the ticker name.")

# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align: center; padding: 40px; color: var(--text-secondary); font-size: 0.75rem; border-top: 1px solid var(--border-color); margin-top: 40px;">
    Kite Terminal &copy; 2026 | Quant Equity Research | Data by Yahoo Finance
</div>
""", unsafe_allow_html=True)
Improve UI Design for Better Usability and Appeal - Manus
