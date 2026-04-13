import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime, time as dtime
import pytz
from streamlit_lightweight_charts import renderLightweightCharts
import numpy as np
from io import StringIO

# ── PAGE CONFIG ───────────────────────────────────────────────────────────────
st.set_page_config(
    layout="wide",
    page_title="Quant Terminal",
    page_icon="💴",
    initial_sidebar_state="expanded"
)

# ── STYLES (Cached) ────────────────────────────────────────────────────────────
@st.cache_data
def get_styles():
    return """
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
[data-testid="stSidebar"] .block-container { padding: 2rem 1.5rem !important; }
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
    font-family: 'Space Mono', monospace !important; font-size: 0.95rem !important;
}
[data-testid="stSidebar"] input:focus {
    border-color: #00E5B4 !important; box-shadow: 0 0 0 2px rgba(0,229,180,0.1) !important;
}
[data-testid="stSidebar"] .stSelectbox > div > div {
    background: #111520 !important; border: 1px solid rgba(0,229,180,0.18) !important;
    border-radius: 4px !important; color: #C8D0DC !important;
}
[data-testid="stSidebar"] .stCheckbox label {
    font-family: 'Space Mono', monospace !important; font-size: 0.72rem !important;
    letter-spacing: 0.06em !important; text-transform: uppercase !important; color: #8892A4 !important;
}
[data-testid="stSidebar"] hr { border-color: rgba(0,229,180,0.1) !important; margin: 1.2rem 0 !important; }

/* Radio buttons styled as pill buttons */
[data-testid="stSidebar"] .stRadio > div {
    display: flex !important; flex-direction: column !important; gap: 0.3rem !important;
}
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label {
    background: #111520 !important; border: 1px solid #1A2030 !important;
    border-radius: 3px !important; padding: 0.35rem 0.75rem !important;
    font-family: 'Space Mono', monospace !important; font-size: 0.68rem !important;
    letter-spacing: 0.1em !important; color: #4A5568 !important;
    cursor: pointer !important; transition: all 0.15s !important;
    text-transform: uppercase !important; width: 100% !important;
}
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:hover {
    border-color: rgba(0,229,180,0.3) !important; color: #8892A4 !important;
}
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] [data-checked="true"] {
    border-color: rgba(0,229,180,0.5) !important; color: #00E5B4 !important; background: rgba(0,229,180,0.05) !important;
}

[data-testid="stSidebar"] .stButton button {
    width: 100% !important; background: transparent !important;
    border: 1px solid rgba(0,229,180,0.4) !important; border-radius: 4px !important;
    color: #00E5B4 !important; font-family: 'Space Mono', monospace !important;
    font-size: 0.7rem !important; letter-spacing: 0.14em !important;
    text-transform: uppercase !important; padding: 0.6rem !important; transition: all 0.2s !important;
}
[data-testid="stSidebar"] .stButton button:hover {
    background: rgba(0,229,180,0.08) !important; border-color: #00E5B4 !important;
    box-shadow: 0 0 12px rgba(0,229,180,0.15) !important;
}

/* ── TYPOGRAPHY ── */
h1, h2, h3 { font-family: 'Space Mono', monospace !important; }

/* ── METRIC CARDS ── */
[data-testid="stMetric"] {
    background: #0D1017 !important; border: 1px solid #161C27 !important;
    border-radius: 6px !important; padding: 0.85rem 1.1rem !important;
    position: relative !important; overflow: hidden !important; transition: border-color 0.2s !important;
}
[data-testid="stMetric"]::before {
    content: ''; position: absolute; top: 0; left: 0;
    width: 3px; height: 100%; background: linear-gradient(180deg, #00E5B4, transparent);
}
[data-testid="stMetric"]:hover { border-color: rgba(0,229,180,0.2) !important; }
[data-testid="stMetricLabel"] {
    font-family: 'Space Mono', monospace !important; font-size: 0.58rem !important;
    letter-spacing: 0.18em !important; text-transform: uppercase !important; color: #3A4459 !important;
}
[data-testid="stMetricValue"] {
    font-family: 'Space Mono', monospace !important; font-size: 1.15rem !important;
    color: #E8EDF5 !important; font-weight: 700 !important; line-height: 1.3 !important;
}
[data-testid="stMetricDelta"] { font-family: 'Space Mono', monospace !important; font-size: 0.65rem !important; }
[data-testid="stMetricDelta"] svg { display: none !important; }
[data-testid="stMetricDelta"][data-direction="up"]   { color: #00E5B4 !important; }
[data-testid="stMetricDelta"][data-direction="down"] { color: #FF4D6A !important; }

/* ── ALERTS ── */
[data-testid="stSpinner"] p {
    font-family: 'Space Mono', monospace !important; font-size: 0.7rem !important;
    letter-spacing: 0.1em !important; color: #3A4459 !important;
}
[data-testid="stInfo"] {
    background: rgba(0,229,180,0.05) !important; border: 1px solid rgba(0,229,180,0.2) !important;
    border-radius: 4px !important; font-family: 'Space Mono', monospace !important;
    font-size: 0.72rem !important; color: #00E5B4 !important;
}

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: #080A0F; }
::-webkit-scrollbar-thumb { background: #1E2733; border-radius: 2px; }
::-webkit-scrollbar-thumb:hover { background: #00E5B4; }
[data-testid="stHorizontalBlock"] { gap: 0.65rem !important; }

/* ── RESPONSIVE ── */
@media (max-width: 768px) {
    .block-container { padding: 1rem 1.5rem !important; }
    [data-testid="stSidebar"] .block-container { padding: 1.5rem 1rem !important; }
}
</style>
"""

st.markdown(get_styles(), unsafe_allow_html=True)


# ── HELPERS ───────────────────────────────────────────────────────────────────

def compute_rsi(series, period=14):
    """Compute RSI with safe division."""
    try:
        delta    = series.diff()
        gain     = delta.clip(lower=0)
        loss     = -delta.clip(upper=0)
        avg_gain = gain.ewm(com=period - 1, min_periods=period).mean()
        avg_loss = loss.ewm(com=period - 1, min_periods=period).mean()
        
        # Avoid division by zero
        avg_loss = avg_loss.replace(0, 1e-10)
        rs = avg_gain / avg_loss
        return 100 - (100 / (1 + rs))
    except Exception as e:
        st.warning(f"RSI calculation error: {str(e)}")
        return None


def compute_macd(series, fast=12, slow=26, signal=9):
    """Compute MACD."""
    try:
        ema_fast = series.ewm(span=fast).mean()
        ema_slow = series.ewm(span=slow).mean()
        macd = ema_fast - ema_slow
        signal_line = macd.ewm(span=signal).mean()
        histogram = macd - signal_line
        return macd, signal_line, histogram
    except Exception as e:
        st.warning(f"MACD calculation error: {str(e)}")
        return None, None, None


def compute_bollinger_bands(series, period=20, std_dev=2):
    """Compute Bollinger Bands."""
    try:
        sma = series.rolling(window=period).mean()
        std = series.rolling(window=period).std()
        upper_band = sma + (std * std_dev)
        lower_band = sma - (std * std_dev)
        return upper_band, sma, lower_band
    except Exception as e:
        st.warning(f"Bollinger Bands calculation error: {str(e)}")
        return None, None, None


def compute_atr(high, low, close, period=14):
    """Compute Average True Range."""
    try:
        tr1 = high - low
        tr2 = abs(high - close.shift())
        tr3 = abs(low - close.shift())
        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        atr = tr.rolling(window=period).mean()
        return atr
    except Exception as e:
        st.warning(f"ATR calculation error: {str(e)}")
        return None


def fmt_indian(n):
    """Format number in Indian system: 1,00,000 style."""
    if n is None or pd.isna(n):
        return "—"
    try:
        n = int(n)
        if n >= 10_000_000:
            return f"{n/10_000_000:.2f} Cr"
        if n >= 100_000:
            return f"{n/100_000:.2f} L"
        s = str(n)
        if len(s) <= 3:
            return s
        last3 = s[-3:]
        rest  = s[:-3]
        parts = []
        while len(rest) > 2:
            parts.append(rest[-2:])
            rest = rest[:-2]
        if rest:
            parts.append(rest)
        return ",".join(reversed(parts)) + "," + last3
    except:
        return "—"


def is_nse_open():
    """Returns (is_open: bool, status_str: str)."""
    try:
        ist = pytz.timezone("Asia/Kolkata")
        now = datetime.now(ist)
        market_open  = dtime(9, 15)
        market_close = dtime(15, 30)
        if now.weekday() >= 5:
            return False, "CLOSED · Weekend"
        t = now.time()
        if market_open <= t <= market_close:
            return True, "OPEN"
        if t < market_open:
            opens_in = datetime.combine(now.date(), market_open)
            opens_in = ist.localize(opens_in)
            diff = opens_in - now
            m = int(diff.seconds / 60)
            return False, f"PRE-MARKET · Opens in {m}m"
        return False, "CLOSED · After Hours"
    except Exception as e:
        return False, f"ERROR · {str(e)[:15]}"


def rsi_label(v):
    """Return RSI label and color."""
    if v is None or pd.isna(v): 
        return "—", "#3A4459"
    if v >= 70:   
        return f"{v:.1f} OVERBOUGHT", "#FF4D6A"
    if v <= 30:   
        return f"{v:.1f} OVERSOLD",   "#00E5B4"
    return f"{v:.1f} NEUTRAL", "#8892A4"


def calculate_performance_metrics(df):
    """Calculate performance metrics."""
    try:
        if len(df) < 2:
            return {}, {}
        
        close = df["Close"].values
        returns = np.diff(close) / close[:-1]
        
        # Sharpe Ratio (annualized, assuming 252 trading days)
        sharpe = np.mean(returns) / (np.std(returns) + 1e-10) * np.sqrt(252) if len(returns) > 0 else 0
        
        # Max Drawdown
        cumulative = np.cumprod(1 + returns)
        running_max = np.maximum.accumulate(cumulative)
        drawdown = (cumulative - running_max) / running_max
        max_dd = np.min(drawdown) * 100 if len(drawdown) > 0 else 0
        
        # Win Rate
        win_rate = (np.sum(returns > 0) / len(returns) * 100) if len(returns) > 0 else 0
        
        # Return
        total_return = ((close[-1] - close[0]) / close[0]) * 100
        
        # Volatility (annualized)
        volatility = np.std(returns) * np.sqrt(252) * 100
        
        metrics = {
            "sharpe": sharpe,
            "max_dd": max_dd,
            "win_rate": win_rate,
            "total_return": total_return,
            "volatility": volatility
        }
        
        return metrics, {}
    except Exception as e:
        st.warning(f"Performance metrics error: {str(e)}")
        return {}, {}


# ── DATA FETCH ────────────────────────────────────────────────────────────────

@st.cache_data(ttl=300)
def fetch_data(ticker, period, interval):
    """Fetch OHLCV data with error handling."""
    try:
        df = yf.download(
            ticker, 
            period=period, 
            interval=interval, 
            auto_adjust=False,
            progress=False  # Suppress progress bar
        )
        
        if df.empty:
            return None
        
        # Handle column names
        df.columns = [col[0] if isinstance(col, tuple) else col for col in df.columns]
        df = df.reset_index()
        
        # Datetime column name varies by interval
        date_col = "Datetime" if "Datetime" in df.columns else "Date"
        df = df.rename(columns={date_col: "Date"})
        df["Date"] = pd.to_datetime(df["Date"])
        df["time"] = df["Date"].dt.strftime("%Y-%m-%d")
        
        # Technical indicators
        df["MA20"] = df["Close"].rolling(20).mean()
        df["MA50"] = df["Close"].rolling(50).mean()
        df["RSI"]  = compute_rsi(df["Close"])
        
        # VWAP (cumulative)
        df["TP"]   = (df["High"] + df["Low"] + df["Close"]) / 3
        df["VWAP"] = (df["TP"] * df["Volume"]).cumsum() / df["Volume"].cumsum()
        
        # MACD
        df["MACD"], df["Signal"], df["Histogram"] = compute_macd(df["Close"])
        
        # Bollinger Bands
        df["BB_Upper"], df["BB_Middle"], df["BB_Lower"] = compute_bollinger_bands(df["Close"])
        
        # ATR
        df["ATR"] = compute_atr(df["High"], df["Low"], df["Close"])
        
        return df
    except Exception as e:
        st.error(f"Error fetching {ticker}: {str(e)}")
        return None


@st.cache_data(ttl=86400)
def fetch_52w(ticker):
    """Fetch true 52-week data."""
    try:
        df = yf.download(ticker, period="1y", interval="1d", auto_adjust=False, progress=False)
        if df.empty:
            return None, None
        df.columns = [col[0] if isinstance(col, tuple) else col for col in df.columns]
        return float(df["High"].max()), float(df["Low"].min())
    except Exception as e:
        st.warning(f"Could not fetch 52W data for {ticker}")
        return None, None


@st.cache_data(ttl=86400)
def fetch_avg_vol(ticker):
    """Fetch true 20-day average volume."""
    try:
        df = yf.download(ticker, period="2mo", interval="1d", auto_adjust=False, progress=False)
        if df.empty:
            return None
        df.columns = [col[0] if isinstance(col, tuple) else col for col in df.columns]
        return int(df["Volume"].tail(20).mean())
    except Exception as e:
        st.warning(f"Could not fetch avg volume for {ticker}")
        return None


# ── SESSION STATE ─────────────────────────────────────────────────────────────
if "recent" not in st.session_state:
    st.session_state.recent = []

if "alerts" not in st.session_state:
    st.session_state.alerts = []


def add_recent(t):
    """Add ticker to recent list (max 5)."""
    if t not in st.session_state.recent:
        st.session_state.recent.insert(0, t)
    st.session_state.recent = st.session_state.recent[:5]


def add_alert(alert_type, message):
    """Add alert to session state."""
    st.session_state.alerts.append({
        "type": alert_type,
        "message": message,
        "timestamp": datetime.now()
    })
    # Keep only last 10 alerts
    st.session_state.alerts = st.session_state.alerts[-10:]


# ── SIDEBAR ───────────────────────────────────────────────────────────────────
market_open, market_status = is_nse_open()
dot_color = "#00E5B4" if market_open else "#FF4D6A"

with st.sidebar:
    st.title("⬡ Controls")

    ticker_raw = st.text_input("Symbol", "RELIANCE.NS", help="NSE: .NS  |  BSE: .BO")
    ticker = ticker_raw.strip().upper()

    st.markdown(
        f"""<div style="font-family:'Space Mono',monospace;font-size:0.53rem;color:#2A3344;
        letter-spacing:0.07em;margin-top:-0.4rem;margin-bottom:0.8rem;line-height:1.8;">
        e.g. INFY.NS · TCS.NS · HDFCBANK.NS<br>WIPRO.NS · ^NSEI · ^BSESN
        </div>""",
        unsafe_allow_html=True
    )

    # Recent tickers
    if st.session_state.recent:
        st.markdown(
            """<div style="font-family:'Space Mono',monospace;font-size:0.58rem;color:#3A4459;
            letter-spacing:0.1em;text-transform:uppercase;margin-bottom:0.3rem;">Recents</div>""",
            unsafe_allow_html=True
        )
        cols = st.columns(len(st.session_state.recent))
        for i, sym in enumerate(st.session_state.recent):
            if cols[i].button(sym, key=f"rec_{sym}"):
                st.session_state["_jump"] = sym
                st.rerun()

    # Jump to recent ticker
    if "_jump" in st.session_state:
        ticker = st.session_state.pop("_jump")

    st.divider()

    # Period
    st.markdown(
        """<div style="font-family:'Space Mono',monospace;font-size:0.6rem;color:#3A4459;
        letter-spacing:0.1em;text-transform:uppercase;margin-bottom:0.5rem;">Period</div>""",
        unsafe_allow_html=True
    )
    period = st.radio(
        "Period",
        ["1mo", "3mo", "6mo", "1y", "2y", "5y", "max"],
        index=3,
        label_visibility="collapsed"
    )

    st.markdown("<div style='height:0.3rem'></div>", unsafe_allow_html=True)

    # Interval
    st.markdown(
        """<div style="font-family:'Space Mono',monospace;font-size:0.6rem;color:#3A4459;
        letter-spacing:0.1em;text-transform:uppercase;margin-bottom:0.5rem;">Interval</div>""",
        unsafe_allow_html=True
    )
    interval_map = {"Daily": "1d", "Weekly": "1wk", "Monthly": "1mo"}
    interval_label = st.radio(
        "Interval",
        list(interval_map.keys()),
        index=0,
        label_visibility="collapsed"
    )
    interval = interval_map[interval_label]

    st.divider()

    st.markdown(
        """<div style="font-family:'Space Mono',monospace;font-size:0.6rem;color:#3A4459;
        letter-spacing:0.1em;text-transform:uppercase;margin-bottom:0.4rem;">Overlays</div>""",
        unsafe_allow_html=True
    )
    show_ma20  = st.checkbox("MA 20",  True)
    show_ma50  = st.checkbox("MA 50",  True)
    show_vwap  = st.checkbox("VWAP",   False)
    show_prevc = st.checkbox("Prev Close", True)
    show_bb    = st.checkbox("Bollinger Bands", False)

    st.divider()

    st.markdown(
        """<div style="font-family:'Space Mono',monospace;font-size:0.6rem;color:#3A4459;
        letter-spacing:0.1em;text-transform:uppercase;margin-bottom:0.4rem;">Sub-Panels</div>""",
        unsafe_allow_html=True
    )
    show_volume = st.checkbox("Volume",   True)
    show_rsi    = st.checkbox("RSI (14)", True)
    show_macd   = st.checkbox("MACD",     False)

    st.divider()

    # Alerts Section
    st.markdown(
        """<div style="font-family:'Space Mono',monospace;font-size:0.6rem;color:#3A4459;
        letter-spacing:0.1em;text-transform:uppercase;margin-bottom:0.4rem;">Alerts</div>""",
        unsafe_allow_html=True
    )
    
    col_alert1, col_alert2 = st.columns(2)
    with col_alert1:
        alert_rsi_overbought = st.checkbox("RSI > 70", False, key="alert_rsi_ob")
    with col_alert2:
        alert_rsi_oversold = st.checkbox("RSI < 30", False, key="alert_rsi_os")
    
    enable_price_alert = st.checkbox("Price Alert", False, key="alert_price_en")
    if enable_price_alert:
        price_alert_value = st.number_input("Alert Price (₹)", value=0.0, step=1.0)
    else:
        price_alert_value = None

    st.divider()

    if st.button("↺ Refresh Data"):
        st.cache_data.clear()
        st.toast("Cache cleared!", icon="✅")
        st.rerun()

    # Market status
    st.markdown(
        f"""<div style="margin-top:1.5rem;font-family:'Space Mono',monospace;font-size:0.58rem;
        letter-spacing:0.1em;text-transform:uppercase;line-height:2;">
        <span style="color:{dot_color};">●</span>
        <span style="color:#2A3344;"> NSE {market_status}</span><br>
        <span style="color:#1E2733;">Data · Yahoo Finance</span><br>
        <span style="color:#1E2733;">Delayed · 15 min</span>
        </div>""",
        unsafe_allow_html=True
    )


# ── DYNAMIC PAGE TITLE ────────────────────────────────────────────────────────
st.markdown(
    f"""<div style="display:flex;align-items:center;justify-content:space-between;
    padding:0.6rem 0 1.4rem 0;border-bottom:1px solid #13181F;margin-bottom:1.4rem;">
  <div style="display:flex;align-items:center;gap:1rem;flex-wrap:wrap;">
    <span style="font-family:'Space Mono',monospace;font-size:1.1rem;font-weight:700;
        color:#00E5B4;letter-spacing:0.08em;">QUANT/TERMINAL</span>
    <span style="background:rgba(0,229,180,0.08);border:1px solid rgba(0,229,180,0.2);
        color:#00E5B4;font-family:'Space Mono',monospace;font-size:0.56rem;
        letter-spacing:0.18em;padding:2px 8px;border-radius:2px;">LIVE</span>
    <span style="background:rgba({('0,229,180' if market_open else '255,77,106')},0.08);
        border:1px solid rgba({('0,229,180' if market_open else '255,77,106')},0.2);
        color:{dot_color};font-family:'Space Mono',monospace;font-size:0.56rem;
        letter-spacing:0.14em;padding:2px 8px;border-radius:2px;">
      ● NSE {market_status}
    </span>
  </div>
  <span style="font-family:'Space Mono',monospace;font-size:0.58rem;color:#2A3344;
      letter-spacing:0.1em;">NSE · BSE · EQUITY</span>
</div>""",
    unsafe_allow_html=True
)

# Update browser tab title dynamically
st.markdown(f"<title>{ticker} | Quant Terminal</title>", unsafe_allow_html=True)


# ── FETCH DATA ────────────────────────────────────────────────────────────────
with st.spinner(f"Fetching {ticker}  ·  {period}  ·  {interval_label} ..."):
    df         = fetch_data(ticker, period, interval)
    w52_h, w52_l = fetch_52w(ticker)
    true_avg_vol = fetch_avg_vol(ticker)

if df is None or len(df) == 0:
    st.error(f"❌ No data found for '{ticker}'")
    st.info("💡 Try: RELIANCE.NS  ·  INFY.NS  ·  TCS.NS  ·  HDFCBANK.NS  ·  ^NSEI")
    st.stop()

if len(df) < 55:
    st.warning("⚠️ Limited history — MA50 / RSI readings may be inaccurate. Try a longer period.")

add_recent(ticker)

last  = df.iloc[-1]
prev  = df.iloc[-2]
close      = float(last["Close"])
prev_close = float(prev["Close"])
change     = ((close - prev_close) / prev_close) * 100
change_abs = close - prev_close

# Use true 52W data if available, fallback to period data
if w52_h is None:
    w52_h = float(df["High"].max())
if w52_l is None:
    w52_l = float(df["Low"].min())

pct_from_high = ((close - w52_h) / w52_h) * 100
pct_from_low  = ((close - w52_l) / w52_l) * 100

last_ma20  = float(df["MA20"].dropna().iloc[-1])  if not df["MA20"].dropna().empty  else None
last_ma50  = float(df["MA50"].dropna().iloc[-1])  if not df["MA50"].dropna().empty  else None
last_rsi   = float(df["RSI"].dropna().iloc[-1])   if not df["RSI"].dropna().empty   else None
last_vwap  = float(df["VWAP"].dropna().iloc[-1])  if not df["VWAP"].dropna().empty  else None
avg_vol20  = true_avg_vol if true_avg_vol else (int(df["Volume"].tail(20).mean()) if "Volume" in df.columns else None)

rsi_txt, rsi_color = rsi_label(last_rsi)
date_str = last["Date"].strftime("%d %b %Y") if hasattr(last["Date"], "strftime") else ""

# Calculate performance metrics
perf_metrics, _ = calculate_performance_metrics(df)

# Alert Logic
alerts_to_show = []

if alert_rsi_overbought and last_rsi and last_rsi > 70:
    alerts_to_show.append(("⚠️ RSI OVERBOUGHT", f"RSI at {last_rsi:.1f}", "warning"))
    add_alert("rsi_overbought", f"{ticker}: RSI {last_rsi:.1f}")

if alert_rsi_oversold and last_rsi and last_rsi < 30:
    alerts_to_show.append(("⚠️ RSI OVERSOLD", f"RSI at {last_rsi:.1f}", "info"))
    add_alert("rsi_oversold", f"{ticker}: RSI {last_rsi:.1f}")

if price_alert_value and price_alert_value > 0:
    if close > price_alert_value * 1.01:  # 1% above alert price
        alerts_to_show.append(("📈 PRICE ABOVE", f"₹{close:,.2f} vs Alert ₹{price_alert_value:,.2f}", "warning"))
    elif close < price_alert_value * 0.99:  # 1% below alert price
        alerts_to_show.append(("📉 PRICE BELOW", f"₹{close:,.2f} vs Alert ₹{price_alert_value:,.2f}", "error"))

# Display active alerts
if alerts_to_show:
    for alert_title, alert_msg, alert_type in alerts_to_show:
        if alert_type == "warning":
            st.warning(f"{alert_title}: {alert_msg}")
        elif alert_type == "error":
            st.error(f"{alert_title}: {alert_msg}")
        else:
            st.info(f"{alert_title}: {alert_msg}")


# ── TICKER HEADER ─────────────────────────────────────────────────────────────
st.markdown(
    f"""<div style="display:flex;align-items:baseline;gap:1.2rem;margin-bottom:1rem;flex-wrap:wrap;">
  <span style="font-family:'Space Mono',monospace;font-size:1.55rem;font-weight:700;
      color:#E8EDF5;letter-spacing:0.04em;">{ticker}</span>
  <span style="font-family:'Space Mono',monospace;font-size:0.65rem;color:#2A3344;
      letter-spacing:0.12em;text-transform:uppercase;">{date_str}</span>
  <span style="font-family:'Space Mono',monospace;font-size:0.7rem;letter-spacing:0.05em;
      color:{"#00E5B4" if change >= 0 else "#FF4D6A"};">
    {"▲" if change >= 0 else "▼"} {abs(change):.2f}%
    ({("+" if change_abs >= 0 else "")}{change_abs:.2f})
  </span>
  <span style="font-family:'Space Mono',monospace;font-size:0.65rem;
      letter-spacing:0.08em;color:{rsi_color};">RSI {rsi_txt}</span>
  <span style="font-family:'Space Mono',monospace;font-size:0.62rem;
      color:#2A3344;letter-spacing:0.08em;">{interval_label} · {period}</span>
</div>""",
    unsafe_allow_html=True
)

# ── METRIC ROW 1 ──────────────────────────────────────────────────────────────
c1, c2, c3, c4, c5, c6 = st.columns(6)
c1.metric("Last Price", f"₹{close:,.2f}",        f"{change:+.2f}%")
c2.metric("Day High",   f"₹{float(last['High']):,.2f}")
c3.metric("Day Low",    f"₹{float(last['Low']):,.2f}")
c4.metric("Volume",     fmt_indian(float(last["Volume"])) if "Volume" in df.columns else "—")
c5.metric("52W High",   f"₹{w52_h:,.2f}",         f"{abs(pct_from_high):.1f}% below ATH")
c6.metric("52W Low",    f"₹{w52_l:,.2f}",          f"{pct_from_low:.1f}% above")

st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

# ── METRIC ROW 2 ──────────────────────────────────────────────────────────────
m1, m2, m3, m4 = st.columns(4)

if last_ma20:
    above20 = close > last_ma20
    m1.metric("MA 20", f"₹{last_ma20:,.2f}", "▲ Above" if above20 else "▼ Below")
else:
    m1.metric("MA 20", "—")

if last_ma50:
    above50 = close > last_ma50
    m2.metric("MA 50", f"₹{last_ma50:,.2f}", "▲ Above" if above50 else "▼ Below")
else:
    m2.metric("MA 50", "—")

m3.metric("RSI 14",      f"{last_rsi:.1f}" if last_rsi else "—")
m4.metric("Avg Vol 20d", fmt_indian(avg_vol20))

st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)

# ── PERFORMANCE METRICS ROW ───────────────────────────────────────────────────
if perf_metrics:
    st.markdown(
        """<div style="font-family:'Space Mono',monospace;font-size:0.6rem;color:#3A4459;
        letter-spacing:0.1em;text-transform:uppercase;margin-bottom:0.5rem;">Performance Metrics</div>""",
        unsafe_allow_html=True
    )
    
    p1, p2, p3, p4, p5 = st.columns(5)
    
    p1.metric(
        "Sharpe Ratio",
        f"{perf_metrics.get('sharpe', 0):.2f}",
        f"{perf_metrics.get('sharpe', 0):+.2f}"
    )
    
    p2.metric(
        "Max Drawdown",
        f"{perf_metrics.get('max_dd', 0):.2f}%",
        f"{perf_metrics.get('max_dd', 0):+.2f}%"
    )
    
    p3.metric(
        "Win Rate",
        f"{perf_metrics.get('win_rate', 0):.1f}%",
        f"{perf_metrics.get('win_rate', 0):+.1f}%"
    )
    
    p4.metric(
        "Total Return",
        f"{perf_metrics.get('total_return', 0):.2f}%",
        f"{perf_metrics.get('total_return', 0):+.2f}%"
    )
    
    p5.metric(
        "Volatility (Annual)",
        f"{perf_metrics.get('volatility', 0):.2f}%",
        f"{perf_metrics.get('volatility', 0):+.2f}%"
    )
    
    st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)


# ── CHART HELPERS ─────────────────────────────────────────────────────────────
def base_opts(show_time=True):
    return {
        "layout": {
            "background": {"type": "solid", "color": "#0D1017"},
            "textColor": "#3A4459", "fontSize": 11,
            "fontFamily": "'Space Mono', monospace",
        },
        "grid": {
            "vertLines": {"color": "#0F1318"},
            "horzLines": {"color": "#0F1318"},
        },
        "crosshair": {
            "mode": 1,
            "vertLine": {"color": "rgba(0,229,180,0.3)", "labelBackgroundColor": "#00E5B4"},
            "horzLine": {"color": "rgba(0,229,180,0.3)", "labelBackgroundColor": "#00E5B4"},
        },
        "rightPriceScale": {
            "borderColor": "#13181F", "textColor": "#3A4459",
            "autoScale": True, "minValue": 0,
        },
        "timeScale": {
            "borderColor": "#13181F", "timeVisible": show_time,
            "secondsVisible": False, "visible": show_time,
        },
    }


# ── CANDLE DATA ───────────────────────────────────────────────────────────────
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

price_series = [{
    "type": "Candlestick", "data": candles,
    "options": {
        "upColor": "#00E5B4", "downColor": "#FF4D6A",
        "borderVisible": False,
        "wickUpColor": "#00E5B4", "wickDownColor": "#FF4D6A",
    }
}]

# MA20
if show_ma20 and last_ma20:
    ma20d = df[["time","MA20"]].dropna()
    price_series.append({
        "type": "Line",
        "data": [{"time": r["time"], "value": float(r["MA20"])} for _, r in ma20d.iterrows()],
        "options": {"color": "#F5A623", "lineWidth": 1}
    })

# MA50
if show_ma50 and last_ma50:
    ma50d = df[["time","MA50"]].dropna()
    price_series.append({
        "type": "Line",
        "data": [{"time": r["time"], "value": float(r["MA50"])} for _, r in ma50d.iterrows()],
        "options": {"color": "#4D9FFF", "lineWidth": 1}
    })

# VWAP
if show_vwap and last_vwap:
    vwapd = df[["time","VWAP"]].dropna()
    price_series.append({
        "type": "Line",
        "data": [{"time": r["time"], "value": float(r["VWAP"])} for _, r in vwapd.iterrows()],
        "options": {"color": "#E879F9", "lineWidth": 1, "lineStyle": 2}
    })

# Bollinger Bands
if show_bb:
    bb_upper = df[["time","BB_Upper"]].dropna()
    bb_lower = df[["time","BB_Lower"]].dropna()
    price_series.append({
        "type": "Line",
        "data": [{"time": r["time"], "value": float(r["BB_Upper"])} for _, r in bb_upper.iterrows()],
        "options": {"color": "rgba(200,150,255,0.4)", "lineWidth": 1, "lineStyle": 2}
    })
    price_series.append({
        "type": "Line",
        "data": [{"time": r["time"], "value": float(r["BB_Lower"])} for _, r in bb_lower.iterrows()],
        "options": {"color": "rgba(200,150,255,0.4)", "lineWidth": 1, "lineStyle": 2}
    })

# Previous close line
if show_prevc:
    price_series.append({
        "type": "Line",
        "data": [{"time": r["time"], "value": prev_close} for r in candles],
        "options": {"color": "rgba(200,208,220,0.25)", "lineWidth": 1, "lineStyle": 2}
    })

price_opts = base_opts(show_time=not (show_volume or show_rsi or show_macd))
price_opts["watermark"] = {
    "visible": True, "fontSize": 52,
    "horzAlign": "center", "vertAlign": "center",
    "color": "rgba(255,255,255,0.018)", "text": ticker,
}

charts_to_render = [{"chart": price_opts, "series": price_series}]


# ── VOLUME PANEL ──────────────────────────────────────────────────────────────
if show_volume and "Volume" in df.columns:
    vol_data = []
    for _, row in df.iterrows():
        c = "#00E5B4" if float(row["Close"]) >= float(row["Open"]) else "#FF4D6A"
        vol_data.append({"time": row["time"], "value": float(row["Volume"]), "color": c + "88"})
    vol_opts = base_opts(show_time=not (show_rsi or show_macd))
    vol_opts["rightPriceScale"]["minValue"] = 0
    charts_to_render.append({
        "chart": vol_opts,
        "series": [{"type": "Histogram", "data": vol_data,
                    "options": {"priceFormat": {"type": "volume"}, "priceScaleId": ""}}]
    })


# ── RSI PANEL ─────────────────────────────────────────────────────────────────
if show_rsi:
    rsi_df   = df[["time","RSI"]].dropna()
    rsi_data = [{"time": r["time"], "value": float(r["RSI"])} for _, r in rsi_df.iterrows()]
    ob_line  = [{"time": r["time"], "value": 70.0} for _, r in rsi_df.iterrows()]
    os_line  = [{"time": r["time"], "value": 30.0} for _, r in rsi_df.iterrows()]
    rsi_opts = base_opts(show_time=not show_macd)
    rsi_opts["rightPriceScale"]["autoScale"] = False
    rsi_opts["rightPriceScale"]["minValue"]  = 0
    rsi_opts["rightPriceScale"]["maxValue"]  = 100
    charts_to_render.append({
        "chart": rsi_opts,
        "series": [
            {"type": "Line", "data": rsi_data, "options": {"color": "#A78BFA", "lineWidth": 1}},
            {"type": "Line", "data": ob_line,  "options": {"color": "rgba(255,77,106,0.4)",  "lineWidth": 1, "lineStyle": 2}},
            {"type": "Line", "data": os_line,  "options": {"color": "rgba(0,229,180,0.4)",   "lineWidth": 1, "lineStyle": 2}},
        ]
    })


# ── MACD PANEL ─────────��──────────────────────────────────────────────────────
if show_macd:
    macd_df = df[["time","MACD","Signal","Histogram"]].dropna()
    
    macd_data = [{"time": r["time"], "value": float(r["MACD"])} for _, r in macd_df.iterrows()]
    signal_data = [{"time": r["time"], "value": float(r["Signal"])} for _, r in macd_df.iterrows()]
    
    histogram_data = []
    for _, row in macd_df.iterrows():
        hist_val = float(row["Histogram"])
        color = "#00E5B4" if hist_val >= 0 else "#FF4D6A"
        histogram_data.append({"time": row["time"], "value": hist_val, "color": color + "88"})
    
    macd_opts = base_opts(show_time=True)
    macd_opts["rightPriceScale"]["autoScale"] = True
    
    charts_to_render.append({
        "chart": macd_opts,
        "series": [
            {"type": "Line", "data": macd_data, "options": {"color": "#4D9FFF", "lineWidth": 1}},
            {"type": "Line", "data": signal_data, "options": {"color": "#F5A623", "lineWidth": 1}},
            {"type": "Histogram", "data": histogram_data, "options": {"priceScaleId": ""}},
        ]
    })


# ── HEIGHTS ───────────────────────────────────────────────────────────────────
total_h = 600
num_panels = len(charts_to_render)
if num_panels == 1:
    heights = [total_h]
elif num_panels == 2:
    heights = [int(total_h * 0.65), int(total_h * 0.35)]
elif num_panels == 3:
    heights = [int(total_h * 0.50), int(total_h * 0.25), int(total_h * 0.25)]
else:
    heights = [int(total_h * 0.45), int(total_h * 0.18), int(total_h * 0.18), int(total_h * 0.19)]

for i, h in enumerate(heights):
    charts_to_render[i]["chart"]["height"] = h


# ── LEGEND ────────────────────────────────────────────────────────────────────
ma20_str = f" · ₹{last_ma20:,.0f}" if last_ma20 else ""
ma50_str = f" · ₹{last_ma50:,.0f}" if last_ma50 else ""
vwap_str = f" · ₹{last_vwap:,.0f}" if last_vwap else ""
legend_parts = ["<span style='color:#3A4459'>● Candles</span>"]
if show_ma20:   legend_parts.append(f"<span style='color:#F5A623'>— MA20{ma20_str}</span>")
if show_ma50:   legend_parts.append(f"<span style='color:#4D9FFF'>— MA50{ma50_str}</span>")
if show_vwap:   legend_parts.append(f"<span style='color:#E879F9'>-- VWAP{vwap_str}</span>")
if show_bb:     legend_parts.append(f"<span style='color:rgba(200,150,255,0.6)'>-- BB Bands</span>")
if show_prevc:  legend_parts.append(f"<span style='color:rgba(200,208,220,0.4)'>-- Prev Close ₹{prev_close:,.2f}</span>")
if show_volume: legend_parts.append("<span style='color:#3A4459'>▪ Volume</span>")
if show_rsi:    legend_parts.append("<span style='color:#A78BFA'>▪ RSI 14</span>")
if show_macd:   legend_parts.append("<span style='color:#4D9FFF'>▪ MACD</span>")

st.markdown(
    f"""<div style="display:flex;gap:1.4rem;align-items:center;margin-bottom:0.5rem;
    font-family:'Space Mono',monospace;font-size:0.6rem;letter-spacing:0.1em;text-transform:uppercase;flex-wrap:wrap;">
    {"  ·  ".join(legend_parts)}</div>""",
    unsafe_allow_html=True
)


# ── RENDER CHARTS ─��───────────────────────────────────────────────────────────
try:
    renderLightweightCharts(charts_to_render, key="quant_charts")
except Exception as e:
    st.error(f"Chart rendering error: {str(e)}")
    st.info("Try selecting different indicators or refreshing the page.")


# ── EXPORT SECTION ────────────────────────────────────────────────────────────
st.divider()
st.markdown(
    """<div style="font-family:'Space Mono',monospace;font-size:0.6rem;color:#3A4459;
    letter-spacing:0.1em;text-transform:uppercase;margin-bottom:0.5rem;">Export Data</div>""",
    unsafe_allow_html=True
)

col_exp1, col_exp2 = st.columns(2)

# Export as CSV
csv_data = df[[col for col in df.columns if col not in ["Date", "time"]]].to_csv(index=False)
col_exp1.download_button(
    label="📥 Download CSV",
    data=csv_data,
    file_name=f"{ticker}_{period}_{interval_label}.csv",
    mime="text/csv"
)

# Export as JSON
json_data = df[[col for col in df.columns if col not in ["Date", "time"]]].to_json(orient="records")
col_exp2.download_button(
    label="📥 Download JSON",
    data=json_data,
    file_name=f"{ticker}_{period}_{interval_label}.json",
    mime="application/json"
)


# ── FOOTER ────────────────────────────────────────────────────────────────────
st.divider()
st.markdown(
    """<div style="font-family:'Space Mono',monospace;font-size:0.55rem;color:#1E2733;
    letter-spacing:0.08em;text-align:center;margin-top:2rem;">
    Data sourced from Yahoo Finance · 15-minute delayed · Not investment advice · For educational purposes only
    </div>""",
    unsafe_allow_html=True
)
