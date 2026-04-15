import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, time as dtime
import pytz
from streamlit_lightweight_charts import renderLightweightCharts

# ── PAGE CONFIG ───────────────────────────────────────────────────────────────
st.set_page_config(
    layout="wide",
    page_title="Quant Terminal",
    page_icon="📈"
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

h1, h2, h3 { font-family: 'Space Mono', monospace !important; }

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

[data-testid="stSpinner"] p {
    font-family: 'Space Mono', monospace !important; font-size: 0.7rem !important;
    letter-spacing: 0.1em !important; color: #3A4459 !important;
}
[data-testid="stInfo"] {
    background: rgba(0,229,180,0.05) !important; border: 1px solid rgba(0,229,180,0.2) !important;
    border-radius: 4px !important; font-family: 'Space Mono', monospace !important;
    font-size: 0.72rem !important; color: #00E5B4 !important;
}

/* Tabs styling */
.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 1px solid #161C27 !important;
    gap: 0 !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: #3A4459 !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.65rem !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    border: none !important;
    padding: 0.5rem 1.2rem !important;
}
.stTabs [aria-selected="true"] {
    color: #00E5B4 !important;
    border-bottom: 2px solid #00E5B4 !important;
}
.stTabs [data-baseweb="tab-panel"] { padding: 1rem 0 0 0 !important; }

/* Expander */
[data-testid="stExpander"] {
    background: #0D1017 !important;
    border: 1px solid #161C27 !important;
    border-radius: 6px !important;
}
[data-testid="stExpander"] summary {
    font-family: 'Space Mono', monospace !important;
    font-size: 0.68rem !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    color: #3A4459 !important;
}
[data-testid="stExpander"] summary:hover { color: #00E5B4 !important; }

/* Comparison table */
.comp-table { width: 100%; border-collapse: collapse; font-family: 'Space Mono', monospace; font-size: 0.68rem; }
.comp-table th {
    color: #3A4459; letter-spacing: 0.1em; text-transform: uppercase;
    padding: 0.5rem 0.8rem; border-bottom: 1px solid #161C27; text-align: right;
}
.comp-table th:first-child { text-align: left; }
.comp-table td { padding: 0.45rem 0.8rem; border-bottom: 1px solid #0F1318; text-align: right; color: #8892A4; }
.comp-table td:first-child { text-align: left; color: #3A4459; }
.comp-table tr:last-child td { border-bottom: none; }
.comp-table tr:hover td { background: rgba(0,229,180,0.03); }
.up { color: #00E5B4 !important; }
.dn { color: #FF4D6A !important; }

/* Fundamental grid */
.fund-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 0.6rem; margin-bottom: 1rem; }
.fund-card {
    background: #0D1017; border: 1px solid #161C27;
    border-radius: 5px; padding: 0.7rem 0.85rem;
}
.fund-label { font-family: 'Space Mono', monospace; font-size: 0.52rem; letter-spacing: 0.15em; text-transform: uppercase; color: #2A3344; margin-bottom: 0.25rem; }
.fund-value { font-family: 'Space Mono', monospace; font-size: 0.88rem; color: #E8EDF5; font-weight: 700; }
.fund-sub   { font-family: 'Space Mono', monospace; font-size: 0.55rem; color: #3A4459; margin-top: 0.15rem; }

::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: #080A0F; }
::-webkit-scrollbar-thumb { background: #1E2733; border-radius: 2px; }
::-webkit-scrollbar-thumb:hover { background: #00E5B4; }
[data-testid="stHorizontalBlock"] { gap: 0.65rem !important; }
</style>
""", unsafe_allow_html=True)


# ── HELPERS ───────────────────────────────────────────────────────────────────

def compute_rsi(series, period=14):
    delta    = series.diff()
    gain     = delta.clip(lower=0)
    loss     = -delta.clip(upper=0)
    avg_gain = gain.ewm(com=period - 1, min_periods=period).mean()
    avg_loss = loss.ewm(com=period - 1, min_periods=period).mean()
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))


def compute_bollinger(series, period=20, std_dev=2):
    sma   = series.rolling(period).mean()
    std   = series.rolling(period).std()
    upper = sma + std_dev * std
    lower = sma - std_dev * std
    return upper, sma, lower


def compute_macd(series, fast=12, slow=26, signal=9):
    ema_fast   = series.ewm(span=fast, adjust=False).mean()
    ema_slow   = series.ewm(span=slow, adjust=False).mean()
    macd_line  = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    histogram  = macd_line - signal_line
    return macd_line, signal_line, histogram


def fmt_indian(n):
    if n is None:
        return "—"
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


def fmt_large(n):
    """Format large numbers (market cap etc.) in Cr/L."""
    if n is None or (isinstance(n, float) and np.isnan(n)):
        return "—"
    if n >= 1e12:
        return f"₹{n/1e7:.0f} Cr"
    if n >= 1e9:
        return f"₹{n/1e7:.0f} Cr"
    if n >= 1e7:
        return f"₹{n/1e7:.2f} Cr"
    return f"₹{n:,.0f}"


def safe(d, key, fmt=None, default="—"):
    v = d.get(key)
    if v is None or v == "N/A" or (isinstance(v, float) and np.isnan(v)):
        return default
    if fmt:
        try:
            return fmt(v)
        except Exception:
            return default
    return str(v)


def is_nse_open():
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


def rsi_label(v):
    if v is None: return "—", "#3A4459"
    if v >= 70:   return f"{v:.1f} OVERBOUGHT", "#FF4D6A"
    if v <= 30:   return f"{v:.1f} OVERSOLD",   "#00E5B4"
    return f"{v:.1f} NEUTRAL", "#8892A4"


# ── DATA FETCH ────────────────────────────────────────────────────────────────

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
    df["RSI"]  = compute_rsi(df["Close"])
    df["TP"]   = (df["High"] + df["Low"] + df["Close"]) / 3
    df["VWAP"] = (df["TP"] * df["Volume"]).cumsum() / df["Volume"].cumsum()
    # Bollinger Bands
    df["BB_upper"], df["BB_mid"], df["BB_lower"] = compute_bollinger(df["Close"])
    # MACD
    df["MACD"], df["MACD_signal"], df["MACD_hist"] = compute_macd(df["Close"])
    return df


@st.cache_data(ttl=86400)
def fetch_52w(ticker):
    df = yf.download(ticker, period="1y", interval="1d", auto_adjust=False)
    if df.empty:
        return None, None
    df.columns = [col[0] if isinstance(col, tuple) else col for col in df.columns]
    return float(df["High"].max()), float(df["Low"].min())


@st.cache_data(ttl=86400)
def fetch_avg_vol(ticker):
    df = yf.download(ticker, period="2mo", interval="1d", auto_adjust=False)
    if df.empty:
        return None
    df.columns = [col[0] if isinstance(col, tuple) else col for col in df.columns]
    return int(df["Volume"].tail(20).mean())


@st.cache_data(ttl=3600)
def fetch_fundamentals(ticker):
    try:
        t    = yf.Ticker(ticker)
        info = t.info
        return info
    except Exception:
        return {}


@st.cache_data(ttl=3600)
def fetch_comparison_data(tickers_tuple, period, interval):
    """Fetch normalized % return data for multiple tickers."""
    result = {}
    for tk in tickers_tuple:
        df = yf.download(tk, period=period, interval=interval, auto_adjust=False)
        if df.empty:
            continue
        df.columns = [col[0] if isinstance(col, tuple) else col for col in df.columns]
        df = df.reset_index()
        date_col = "Datetime" if "Datetime" in df.columns else "Date"
        df = df.rename(columns={date_col: "Date"})
        df["Date"] = pd.to_datetime(df["Date"])
        df["time"] = df["Date"].dt.strftime("%Y-%m-%d")
        df = df.dropna(subset=["Close"])
        first = float(df["Close"].iloc[0])
        df["pct_return"] = ((df["Close"].astype(float) - first) / first) * 100
        result[tk] = df
    return result


# ── SESSION STATE ─────────────────────────────────────────────────────────────
if "recent" not in st.session_state:
    st.session_state.recent = []


def add_recent(t):
    if t not in st.session_state.recent:
        st.session_state.recent.insert(0, t)
        st.session_state.recent = st.session_state.recent[:5]


# ── SIDEBAR ───────────────────────────────────────────────────────────────────
market_open, market_status = is_nse_open()
dot_color = "#00E5B4" if market_open else "#FF4D6A"

with st.sidebar:
    st.title("⬡ Controls")

    ticker_raw = st.text_input("Symbol", "RELIANCE.NS", help="NSE: .NS  |  BSE: .BO")
    ticker = ticker_raw.strip().upper()

    st.markdown(
        """<div style="font-family:'Space Mono',monospace;font-size:0.53rem;color:#2A3344;
        letter-spacing:0.07em;margin-top:-0.4rem;margin-bottom:0.8rem;line-height:1.8;">
        e.g. INFY.NS · TCS.NS · HDFCBANK.NS<br>WIPRO.NS · ^NSEI · ^BSESN
        </div>""",
        unsafe_allow_html=True
    )

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

    if "_jump" in st.session_state:
        ticker = st.session_state.pop("_jump")

    st.divider()

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
    show_bb    = st.checkbox("Bollinger Bands", True)
    show_vwap  = st.checkbox("VWAP",   False)
    show_prevc = st.checkbox("Prev Close", True)

    st.divider()

    st.markdown(
        """<div style="font-family:'Space Mono',monospace;font-size:0.6rem;color:#3A4459;
        letter-spacing:0.1em;text-transform:uppercase;margin-bottom:0.4rem;">Sub-Panels</div>""",
        unsafe_allow_html=True
    )
    show_volume = st.checkbox("Volume",   True)
    show_macd   = st.checkbox("MACD",     True)
    show_rsi    = st.checkbox("RSI (14)", True)

    st.divider()

    if st.button("↺ Refresh Data"):
        st.cache_data.clear()
        st.rerun()

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
  <div style="display:flex;align-items:center;gap:1rem;">
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

st.markdown(f"<title>{ticker} | Quant Terminal</title>", unsafe_allow_html=True)


# ── FETCH DATA ────────────────────────────────────────────────────────────────
with st.spinner(f"Fetching {ticker}  ·  {period}  ·  {interval_label} ..."):
    df           = fetch_data(ticker, period, interval)
    w52_h, w52_l = fetch_52w(ticker)
    true_avg_vol = fetch_avg_vol(ticker)

if df is None:
    st.error(f"No data found for '{ticker}'")
    st.info("Try: RELIANCE.NS  ·  INFY.NS  ·  TCS.NS  ·  HDFCBANK.NS  ·  ^NSEI")
    st.stop()

if len(df) < 55:
    st.warning("Limited history — MA50 / RSI readings may be inaccurate. Try a longer period.")

add_recent(ticker)

last       = df.iloc[-1]
prev       = df.iloc[-2]
close      = float(last["Close"])
prev_close = float(prev["Close"])
change     = ((close - prev_close) / prev_close) * 100
change_abs = close - prev_close

if w52_h is None:
    w52_h = float(df["High"].max())
if w52_l is None:
    w52_l = float(df["Low"].min())

pct_from_high = ((close - w52_h) / w52_h) * 100
pct_from_low  = ((close - w52_l) / w52_l) * 100

last_ma20   = float(df["MA20"].dropna().iloc[-1])  if not df["MA20"].dropna().empty  else None
last_ma50   = float(df["MA50"].dropna().iloc[-1])  if not df["MA50"].dropna().empty  else None
last_rsi    = float(df["RSI"].dropna().iloc[-1])   if not df["RSI"].dropna().empty   else None
last_vwap   = float(df["VWAP"].dropna().iloc[-1])  if not df["VWAP"].dropna().empty  else None
last_bb_u   = float(df["BB_upper"].dropna().iloc[-1]) if not df["BB_upper"].dropna().empty else None
last_bb_l   = float(df["BB_lower"].dropna().iloc[-1]) if not df["BB_lower"].dropna().empty else None
last_macd   = float(df["MACD"].dropna().iloc[-1])  if not df["MACD"].dropna().empty  else None
last_msig   = float(df["MACD_signal"].dropna().iloc[-1]) if not df["MACD_signal"].dropna().empty else None
avg_vol20   = true_avg_vol if true_avg_vol else (int(df["Volume"].tail(20).mean()) if "Volume" in df.columns else None)

rsi_txt, rsi_color = rsi_label(last_rsi)
date_str = last["Date"].strftime("%d %b %Y") if hasattr(last["Date"], "strftime") else ""

# MACD signal badge
if last_macd is not None and last_msig is not None:
    macd_signal_str   = "BULLISH CROSS" if last_macd > last_msig else "BEARISH CROSS"
    macd_signal_color = "#00E5B4" if last_macd > last_msig else "#FF4D6A"
else:
    macd_signal_str   = "—"
    macd_signal_color = "#3A4459"

# BB signal badge
if last_bb_u and last_bb_l:
    if close > last_bb_u:
        bb_signal = "ABOVE UPPER BAND"
        bb_color  = "#FF4D6A"
    elif close < last_bb_l:
        bb_signal = "BELOW LOWER BAND"
        bb_color  = "#00E5B4"
    else:
        bb_signal = "INSIDE BANDS"
        bb_color  = "#8892A4"
else:
    bb_signal = "—"
    bb_color  = "#3A4459"


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
  <span style="font-family:'Space Mono',monospace;font-size:0.65rem;
      letter-spacing:0.08em;color:{macd_signal_color};">MACD {macd_signal_str}</span>
  <span style="font-family:'Space Mono',monospace;font-size:0.65rem;
      letter-spacing:0.08em;color:{bb_color};">BB {bb_signal}</span>
  <span style="font-family:'Space Mono',monospace;font-size:0.62rem;
      color:#2A3344;letter-spacing:0.08em;">{interval_label} · {period}</span>
</div>""",
    unsafe_allow_html=True
)

# ── TABS ──────────────────────────────────────────────────────────────────────
tab_chart, tab_compare, tab_fundamental = st.tabs([
    "📈  Chart",
    "⚖  Compare",
    "🏦  Fundamentals"
])


# ════════════════════════════════════════════════════════════════════════════
# TAB 1 — CHART
# ════════════════════════════════════════════════════════════════════════════
with tab_chart:

    # ── METRIC ROW 1 ──────────────────────────────────────────────────────
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.metric("Last Price", f"₹{close:,.2f}",        f"{change:+.2f}%")
    c2.metric("Day High",   f"₹{float(last['High']):,.2f}")
    c3.metric("Day Low",    f"₹{float(last['Low']):,.2f}")
    c4.metric("Volume",     fmt_indian(float(last["Volume"])) if "Volume" in df.columns else "—")
    c5.metric("52W High",   f"₹{w52_h:,.2f}",         f"{abs(pct_from_high):.1f}% below ATH")
    c6.metric("52W Low",    f"₹{w52_l:,.2f}",          f"{pct_from_low:.1f}% above")

    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

    # ── METRIC ROW 2 ──────────────────────────────────────────────────────
    m1, m2, m3, m4, m5, m6 = st.columns(6)

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
    m4.metric("MACD",        f"{last_macd:.2f}" if last_macd else "—",
              f"Signal {last_msig:.2f}" if last_msig else None)
    m5.metric("BB Upper",    f"₹{last_bb_u:,.2f}" if last_bb_u else "—")
    m6.metric("Avg Vol 20d", fmt_indian(avg_vol20))

    st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)

    # ── CHART HELPERS ─────────────────────────────────────────────────────
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

    # ── CANDLE DATA ───────────────────────────────────────────────────────
# Clean data
df = df.replace([np.inf, -np.inf], np.nan)
df = df.dropna(subset=["Open", "High", "Low", "Close"])

# Select + rename
candles_df = df[["time", "Open", "High", "Low", "Close"]].rename(columns={
    "Open": "open",
    "High": "high",
    "Low": "low",
    "Close": "close"
})

# FINAL SAFETY (very important)
candles_df = candles_df.dropna()

# Convert to float explicitly
for col in ["open", "high", "low", "close"]:
    candles_df[col] = candles_df[col].astype(float)

# Convert to dict
candles = candles_df.to_dict("records")
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

    # Bollinger Bands
    if show_bb:
        bb_df = df[["time","BB_upper","BB_mid","BB_lower"]].dropna()
        price_series.append({
            "type": "Line",
            "data": [{"time": r["time"], "value": float(r["BB_upper"])} for _, r in bb_df.iterrows()],
            "options": {"color": "rgba(147,112,219,0.7)", "lineWidth": 1, "lineStyle": 2}
        })
        price_series.append({
            "type": "Line",
            "data": [{"time": r["time"], "value": float(r["BB_mid"])} for _, r in bb_df.iterrows()],
            "options": {"color": "rgba(147,112,219,0.35)", "lineWidth": 1, "lineStyle": 2}
        })
        price_series.append({
            "type": "Line",
            "data": [{"time": r["time"], "value": float(r["BB_lower"])} for _, r in bb_df.iterrows()],
            "options": {"color": "rgba(147,112,219,0.7)", "lineWidth": 1, "lineStyle": 2}
        })

    # VWAP
    if show_vwap and last_vwap:
        vwapd = df[["time","VWAP"]].dropna()
        price_series.append({
            "type": "Line",
            "data": [{"time": r["time"], "value": float(r["VWAP"])} for _, r in vwapd.iterrows()],
            "options": {"color": "#E879F9", "lineWidth": 1, "lineStyle": 2}
        })

    # Previous close
    if show_prevc:
        price_series.append({
            "type": "Line",
            "data": [{"time": r["time"], "value": prev_close} for r in candles],
            "options": {"color": "rgba(200,208,220,0.25)", "lineWidth": 1, "lineStyle": 2}
        })

    price_opts = base_opts(show_time=not (show_volume or show_macd or show_rsi))
    price_opts["watermark"] = {
        "visible": True, "fontSize": 52,
        "horzAlign": "center", "vertAlign": "center",
        "color": "rgba(255,255,255,0.018)", "text": ticker,
    }

    charts_to_render = [{"chart": price_opts, "series": price_series}]

    # ── VOLUME PANEL ──────────────────────────────────────────────────────
    if show_volume and "Volume" in df.columns:
        vol_data = []
        for _, row in df.iterrows():
            c = "#00E5B4" if float(row["Close"]) >= float(row["Open"]) else "#FF4D6A"
            vol_data.append({"time": row["time"], "value": float(row["Volume"]), "color": c + "88"})
        vol_opts = base_opts(show_time=not (show_macd or show_rsi))
        vol_opts["rightPriceScale"]["minValue"] = 0
        charts_to_render.append({
            "chart": vol_opts,
            "series": [{"type": "Histogram", "data": vol_data,
                        "options": {"priceFormat": {"type": "volume"}, "priceScaleId": ""}}]
        })

    # ── MACD PANEL ────────────────────────────────────────────────────────
    if show_macd:
        macd_df = df[["time","MACD","MACD_signal","MACD_hist"]].dropna()
        macd_line_data   = [{"time": r["time"], "value": float(r["MACD"])}        for _, r in macd_df.iterrows()]
        signal_line_data = [{"time": r["time"], "value": float(r["MACD_signal"])} for _, r in macd_df.iterrows()]
        hist_data = []
        for _, r in macd_df.iterrows():
            h = float(r["MACD_hist"])
            hist_data.append({"time": r["time"], "value": h, "color": "#00E5B488" if h >= 0 else "#FF4D6A88"})
        macd_opts = base_opts(show_time=not show_rsi)
        macd_opts["rightPriceScale"]["autoScale"] = True
        charts_to_render.append({
            "chart": macd_opts,
            "series": [
                {"type": "Histogram", "data": hist_data,
                 "options": {"priceScaleId": ""}},
                {"type": "Line", "data": macd_line_data,
                 "options": {"color": "#00E5B4", "lineWidth": 1}},
                {"type": "Line", "data": signal_line_data,
                 "options": {"color": "#FF4D6A", "lineWidth": 1}},
            ]
        })

    # ── RSI PANEL ─────────────────────────────────────────────────────────
    if show_rsi:
        rsi_df   = df[["time","RSI"]].dropna()
        rsi_data = [{"time": r["time"], "value": float(r["RSI"])} for _, r in rsi_df.iterrows()]
        ob_line  = [{"time": r["time"], "value": 70.0} for _, r in rsi_df.iterrows()]
        os_line  = [{"time": r["time"], "value": 30.0} for _, r in rsi_df.iterrows()]
        rsi_opts = base_opts(show_time=True)
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

    # ── HEIGHTS ───────────────────────────────────────────────────────────
    total_h    = 640
    num_panels = len(charts_to_render)
    if num_panels == 1:
        heights = [total_h]
    elif num_panels == 2:
        heights = [int(total_h * 0.62), int(total_h * 0.38)]
    elif num_panels == 3:
        heights = [int(total_h * 0.52), int(total_h * 0.22), int(total_h * 0.26)]
    else:  # 4 panels
        heights = [int(total_h * 0.44), int(total_h * 0.18), int(total_h * 0.18), int(total_h * 0.20)]

    for i, h in enumerate(heights):
        charts_to_render[i]["chart"]["height"] = h

    # ── LEGEND ────────────────────────────────────────────────────────────
    ma20_str = f" · ₹{last_ma20:,.0f}" if last_ma20 else ""
    ma50_str = f" · ₹{last_ma50:,.0f}" if last_ma50 else ""
    bb_u_str = f" · ₹{last_bb_u:,.0f}" if last_bb_u else ""
    vwap_str = f" · ₹{last_vwap:,.0f}" if last_vwap else ""
    legend_parts = ["<span style='color:#3A4459'>● Candles</span>"]
    if show_ma20:   legend_parts.append(f"<span style='color:#F5A623'>— MA20{ma20_str}</span>")
    if show_ma50:   legend_parts.append(f"<span style='color:#4D9FFF'>— MA50{ma50_str}</span>")
    if show_bb:     legend_parts.append(f"<span style='color:rgba(147,112,219,0.8)'>-- BB(20,2){bb_u_str}</span>")
    if show_vwap:   legend_parts.append(f"<span style='color:#E879F9'>-- VWAP{vwap_str}</span>")
    if show_prevc:  legend_parts.append(f"<span style='color:rgba(200,208,220,0.4)'>-- Prev Close ₹{prev_close:,.2f}</span>")
    if show_volume: legend_parts.append("<span style='color:#3A4459'>▪ Volume</span>")
    if show_macd:   legend_parts.append("<span style='color:#00E5B4'>▪ MACD</span> <span style='color:#FF4D6A'>▪ Signal</span>")
    if show_rsi:    legend_parts.append("<span style='color:#A78BFA'>▪ RSI 14</span>")

    st.markdown(
        f"""<div style="display:flex;gap:1.4rem;align-items:center;flex-wrap:wrap;margin-bottom:0.5rem;
        font-family:'Space Mono',monospace;font-size:0.6rem;letter-spacing:0.1em;text-transform:uppercase;">
        {"  ".join(legend_parts)}</div>""",
        unsafe_allow_html=True
    )

    # ── RENDER ────────────────────────────────────────────────────────────
    try:
        renderLightweightCharts(charts_to_render, key="quant_charts")
    except Exception:
        renderLightweightCharts(charts_to_render)


# ════════════════════════════════════════════════════════════════════════════
# TAB 2 — MULTI-TICKER COMPARE
# ════════════════════════════════════════════════════════════════════════════
with tab_compare:

    st.markdown(
        """<div style="font-family:'Space Mono',monospace;font-size:0.62rem;color:#3A4459;
        letter-spacing:0.1em;text-transform:uppercase;margin-bottom:0.8rem;">
        Compare up to 5 symbols · normalized % return from period start
        </div>""",
        unsafe_allow_html=True
    )

    comp_col1, comp_col2 = st.columns([3, 1])
    with comp_col1:
        compare_input = st.text_input(
            "Symbols (comma-separated)",
            f"{ticker}, NIFTY50.NS, TCS.NS",
            key="compare_input",
            label_visibility="collapsed",
            placeholder="RELIANCE.NS, TCS.NS, INFY.NS"
        )
    with comp_col2:
        compare_period = st.selectbox(
            "Period",
            ["1mo", "3mo", "6mo", "1y", "2y"],
            index=2,
            key="compare_period",
            label_visibility="collapsed"
        )

    tickers_raw    = [t.strip().upper() for t in compare_input.split(",") if t.strip()]
    tickers_to_cmp = tickers_raw[:5]  # max 5

    COMP_COLORS = ["#00E5B4", "#4D9FFF", "#F5A623", "#E879F9", "#FF4D6A"]

    if tickers_to_cmp:
        with st.spinner("Loading comparison data..."):
            cmp_data = fetch_comparison_data(tuple(tickers_to_cmp), compare_period, "1d")

        if not cmp_data:
            st.error("Could not load any comparison data. Check symbols.")
        else:
            # ── NORMALIZED RETURN CHART ───────────────────────────────────
            cmp_series = []
            for i, tk in enumerate(tickers_to_cmp):
                if tk not in cmp_data:
                    continue
                d = cmp_data[tk]
                color = COMP_COLORS[i % len(COMP_COLORS)]
                series_data = [
                    {"time": r["time"], "value": round(float(r["pct_return"]), 4)}
                    for _, r in d.iterrows()
                ]
                cmp_series.append({
                    "type": "Line",
                    "data": series_data,
                    "options": {"color": color, "lineWidth": 2, "title": tk}
                })

            # Zero baseline
            if cmp_series:
                all_times = list(cmp_data.values())[0]["time"].tolist()
                cmp_series.append({
                    "type": "Line",
                    "data": [{"time": t, "value": 0.0} for t in all_times],
                    "options": {"color": "rgba(200,208,220,0.12)", "lineWidth": 1, "lineStyle": 2}
                })

            cmp_chart_opts = {
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
                "rightPriceScale": {"borderColor": "#13181F", "textColor": "#3A4459"},
                "timeScale": {"borderColor": "#13181F", "timeVisible": True, "secondsVisible": False},
                "height": 420,
            }

            # Legend for comparison
            legend_html = "  ".join([
                f"<span style='color:{COMP_COLORS[i]};'>— {tk}</span>"
                for i, tk in enumerate(tickers_to_cmp)
                if tk in cmp_data
            ])
            st.markdown(
                f"""<div style="font-family:'Space Mono',monospace;font-size:0.6rem;
                letter-spacing:0.1em;text-transform:uppercase;margin-bottom:0.4rem;
                display:flex;gap:1.4rem;flex-wrap:wrap;">
                {legend_html}
                </div>""",
                unsafe_allow_html=True
            )

            try:
                renderLightweightCharts(
                    [{"chart": cmp_chart_opts, "series": cmp_series}],
                    key="compare_charts"
                )
            except Exception:
                renderLightweightCharts([{"chart": cmp_chart_opts, "series": cmp_series}])

            # ── STATS TABLE ───────────────────────────────────────────────
            st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
            st.markdown(
                """<div style="font-family:'Space Mono',monospace;font-size:0.6rem;color:#3A4459;
                letter-spacing:0.12em;text-transform:uppercase;margin-bottom:0.5rem;">
                Performance Summary
                </div>""",
                unsafe_allow_html=True
            )

            rows_html = ""
            for i, tk in enumerate(tickers_to_cmp):
                if tk not in cmp_data:
                    rows_html += f"<tr><td style='color:{COMP_COLORS[i]}'>{tk}</td><td colspan='5' style='color:#3A4459'>No data</td></tr>"
                    continue
                d     = cmp_data[tk]
                ret   = float(d["pct_return"].iloc[-1])
                hi    = float(d["pct_return"].max())
                lo    = float(d["pct_return"].min())
                start = float(d["Close"].iloc[0])
                end   = float(d["Close"].iloc[-1])
                vol   = float(d["Close"].pct_change().std() * np.sqrt(252) * 100)
                ret_cls = "up" if ret >= 0 else "dn"
                rows_html += f"""
                <tr>
                  <td style="color:{COMP_COLORS[i % len(COMP_COLORS)]}">{tk}</td>
                  <td class="{ret_cls}">{"+" if ret >= 0 else ""}{ret:.2f}%</td>
                  <td class="up">+{hi:.2f}%</td>
                  <td class="dn">{lo:.2f}%</td>
                  <td>₹{end:,.2f}</td>
                  <td>{vol:.1f}%</td>
                </tr>"""

            st.markdown(
                f"""<table class="comp-table">
                <thead>
                  <tr>
                    <th>Symbol</th>
                    <th>Return</th>
                    <th>Period High</th>
                    <th>Period Low</th>
                    <th>Last Price</th>
                    <th>Ann. Vol</th>
                  </tr>
                </thead>
                <tbody>{rows_html}</tbody>
                </table>""",
                unsafe_allow_html=True
            )


# ════════════════════════════════════════════════════════════════════════════
# TAB 3 — FUNDAMENTALS
# ════════════════════════════════════════════════════════════════════════════
with tab_fundamental:

    with st.spinner(f"Loading fundamentals for {ticker} ..."):
        info = fetch_fundamentals(ticker)

    if not info:
        st.warning("No fundamental data available for this symbol.")
    else:
        long_name  = info.get("longName") or info.get("shortName") or ticker
        sector     = info.get("sector", "—")
        industry   = info.get("industry", "—")
        exchange   = info.get("exchange", "—")
        currency   = info.get("currency", "INR")
        country    = info.get("country", "—")
        website    = info.get("website", "")
        summary    = info.get("longBusinessSummary", "")

        # ── COMPANY HEADER ────────────────────────────────────────────────
        st.markdown(
            f"""<div style="margin-bottom:1.2rem;">
            <div style="font-family:'Space Mono',monospace;font-size:1.1rem;font-weight:700;
                color:#E8EDF5;margin-bottom:0.2rem;">{long_name}</div>
            <div style="font-family:'Space Mono',monospace;font-size:0.6rem;color:#3A4459;
                letter-spacing:0.1em;text-transform:uppercase;display:flex;gap:1.2rem;flex-wrap:wrap;">
              <span>{sector}</span>
              <span style="color:#1E2733">·</span>
              <span>{industry}</span>
              <span style="color:#1E2733">·</span>
              <span>{exchange}</span>
              <span style="color:#1E2733">·</span>
              <span>{country}</span>
              {"<span style='color:#1E2733'>·</span><a href='" + website + "' style='color:#00E5B4;text-decoration:none;'>" + website.replace("https://","").replace("http://","").rstrip("/") + "</a>" if website else ""}
            </div>
            </div>""",
            unsafe_allow_html=True
        )

        # ── VALUATION ─────────────────────────────────────────────────────
        st.markdown(
            """<div style="font-family:'Space Mono',monospace;font-size:0.6rem;color:#3A4459;
            letter-spacing:0.12em;text-transform:uppercase;margin-bottom:0.5rem;">
            Valuation
            </div>""",
            unsafe_allow_html=True
        )

        market_cap = info.get("marketCap")
        ev         = info.get("enterpriseValue")
        pe_trail   = info.get("trailingPE")
        pe_fwd     = info.get("forwardPE")
        pb         = info.get("priceToBook")
        ps         = info.get("priceToSalesTrailing12Months")
        ev_ebitda  = info.get("enterpriseToEbitda")
        ev_rev     = info.get("enterpriseToRevenue")

        def fc(v, fmt_fn=lambda x: f"{x:.2f}"):
            if v is None or (isinstance(v, float) and np.isnan(v)):
                return "—"
            try:
                return fmt_fn(v)
            except Exception:
                return "—"

        fund_cards = [
            ("Market Cap",       fmt_large(market_cap)          if market_cap else "—", ""),
            ("Enterprise Value", fmt_large(ev)                  if ev else "—",         ""),
            ("P/E (Trailing)",   fc(pe_trail),                  "ttm"),
            ("P/E (Forward)",    fc(pe_fwd),                    "fwd"),
            ("Price / Book",     fc(pb),                        "x"),
            ("Price / Sales",    fc(ps),                        "ttm"),
            ("EV / EBITDA",      fc(ev_ebitda),                 "x"),
            ("EV / Revenue",     fc(ev_rev),                    "x"),
        ]

        cols = st.columns(4)
        for idx, (label, val, sub) in enumerate(fund_cards):
            with cols[idx % 4]:
                st.markdown(
                    f"""<div class="fund-card">
                    <div class="fund-label">{label}</div>
                    <div class="fund-value">{val}</div>
                    {"<div class='fund-sub'>" + sub + "</div>" if sub else ""}
                    </div>""",
                    unsafe_allow_html=True
                )
            if idx % 4 == 3 and idx < len(fund_cards) - 1:
                st.markdown("<div style='height:0.2rem'></div>", unsafe_allow_html=True)
                cols = st.columns(4)

        st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

        # ── INCOME / GROWTH ───────────────────────────────────────────────
        st.markdown(
            """<div style="font-family:'Space Mono',monospace;font-size:0.6rem;color:#3A4459;
            letter-spacing:0.12em;text-transform:uppercase;margin-bottom:0.5rem;">
            Income & Growth
            </div>""",
            unsafe_allow_html=True
        )

        rev          = info.get("totalRevenue")
        gross_margin = info.get("grossMargins")
        op_margin    = info.get("operatingMargins")
        profit_mg    = info.get("profitMargins")
        rev_growth   = info.get("revenueGrowth")
        earn_growth  = info.get("earningsGrowth")
        eps_trail    = info.get("trailingEps")
        eps_fwd      = info.get("forwardEps")

        def pct(v):
            if v is None or (isinstance(v, float) and np.isnan(v)):
                return "—"
            return f"{v*100:.1f}%"

        income_cards = [
            ("Total Revenue",    fmt_large(rev) if rev else "—", "ttm"),
            ("Gross Margin",     pct(gross_margin),              "ttm"),
            ("Operating Margin", pct(op_margin),                 "ttm"),
            ("Profit Margin",    pct(profit_mg),                 "ttm"),
            ("Revenue Growth",   pct(rev_growth),                "yoy"),
            ("Earnings Growth",  pct(earn_growth),               "yoy"),
            ("EPS (Trailing)",   fc(eps_trail, lambda x: f"₹{x:.2f}"), "ttm"),
            ("EPS (Forward)",    fc(eps_fwd,   lambda x: f"₹{x:.2f}"), "fwd"),
        ]

        cols2 = st.columns(4)
        for idx, (label, val, sub) in enumerate(income_cards):
            with cols2[idx % 4]:
                st.markdown(
                    f"""<div class="fund-card">
                    <div class="fund-label">{label}</div>
                    <div class="fund-value">{val}</div>
                    {"<div class='fund-sub'>" + sub + "</div>" if sub else ""}
                    </div>""",
                    unsafe_allow_html=True
                )
            if idx % 4 == 3 and idx < len(income_cards) - 1:
                st.markdown("<div style='height:0.2rem'></div>", unsafe_allow_html=True)
                cols2 = st.columns(4)

        st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

        # ── BALANCE SHEET / HEALTH ────────────────────────────────────────
        st.markdown(
            """<div style="font-family:'Space Mono',monospace;font-size:0.6rem;color:#3A4459;
            letter-spacing:0.12em;text-transform:uppercase;margin-bottom:0.5rem;">
            Balance Sheet & Health
            </div>""",
            unsafe_allow_html=True
        )

        total_cash   = info.get("totalCash")
        total_debt   = info.get("totalDebt")
        de_ratio     = info.get("debtToEquity")
        current_r    = info.get("currentRatio")
        quick_r      = info.get("quickRatio")
        roe          = info.get("returnOnEquity")
        roa          = info.get("returnOnAssets")
        fcf          = info.get("freeCashflow")

        balance_cards = [
            ("Total Cash",     fmt_large(total_cash) if total_cash else "—", ""),
            ("Total Debt",     fmt_large(total_debt) if total_debt else "—", ""),
            ("Debt / Equity",  fc(de_ratio, lambda x: f"{x:.1f}"),           "ratio"),
            ("Current Ratio",  fc(current_r),                                "x"),
            ("Quick Ratio",    fc(quick_r),                                  "x"),
            ("ROE",            pct(roe),                                     "ttm"),
            ("ROA",            pct(roa),                                     "ttm"),
            ("Free Cash Flow", fmt_large(fcf) if fcf else "—",               "ttm"),
        ]

        cols3 = st.columns(4)
        for idx, (label, val, sub) in enumerate(balance_cards):
            with cols3[idx % 4]:
                st.markdown(
                    f"""<div class="fund-card">
                    <div class="fund-label">{label}</div>
                    <div class="fund-value">{val}</div>
                    {"<div class='fund-sub'>" + sub + "</div>" if sub else ""}
                    </div>""",
                    unsafe_allow_html=True
                )
            if idx % 4 == 3 and idx < len(balance_cards) - 1:
                st.markdown("<div style='height:0.2rem'></div>", unsafe_allow_html=True)
                cols3 = st.columns(4)

        st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

        # ── DIVIDENDS & OWNERSHIP ─────────────────────────────────────────
        st.markdown(
            """<div style="font-family:'Space Mono',monospace;font-size:0.6rem;color:#3A4459;
            letter-spacing:0.12em;text-transform:uppercase;margin-bottom:0.5rem;">
            Dividends & Ownership
            </div>""",
            unsafe_allow_html=True
        )

        div_yield    = info.get("dividendYield")
        div_rate     = info.get("dividendRate")
        payout_r     = info.get("payoutRatio")
        beta         = info.get("beta")
        shares_out   = info.get("sharesOutstanding")
        inst_hold    = info.get("heldPercentInstitutions")
        insider_hold = info.get("heldPercentInsiders")
        short_float  = info.get("shortPercentOfFloat")

        div_cards = [
            ("Dividend Yield", pct(div_yield),                               ""),
            ("Dividend Rate",  fc(div_rate, lambda x: f"₹{x:.2f}"),         "annual"),
            ("Payout Ratio",   pct(payout_r),                                ""),
            ("Beta",           fc(beta),                                     "5y monthly"),
            ("Shares Out",     fmt_indian(shares_out) if shares_out else "—",""),
            ("Inst. Holding",  pct(inst_hold),                               ""),
            ("Insider Hold.",  pct(insider_hold),                            ""),
            ("Short Float",    pct(short_float),                             ""),
        ]

        cols4 = st.columns(4)
        for idx, (label, val, sub) in enumerate(div_cards):
            with cols4[idx % 4]:
                st.markdown(
                    f"""<div class="fund-card">
                    <div class="fund-label">{label}</div>
                    <div class="fund-value">{val}</div>
                    {"<div class='fund-sub'>" + sub + "</div>" if sub else ""}
                    </div>""",
                    unsafe_allow_html=True
                )
            if idx % 4 == 3 and idx < len(div_cards) - 1:
                st.markdown("<div style='height:0.2rem'></div>", unsafe_allow_html=True)
                cols4 = st.columns(4)

        # ── ANALYST TARGETS ───────────────────────────────────────────────
        target_mean = info.get("targetMeanPrice")
        target_high = info.get("targetHighPrice")
        target_low  = info.get("targetLowPrice")
        rec_mean    = info.get("recommendationMean")
        num_analyst = info.get("numberOfAnalystOpinions")
        rec_key     = info.get("recommendationKey", "").upper()

        if target_mean:
            st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)
            st.markdown(
                """<div style="font-family:'Space Mono',monospace;font-size:0.6rem;color:#3A4459;
                letter-spacing:0.12em;text-transform:uppercase;margin-bottom:0.5rem;">
                Analyst Consensus
                </div>""",
                unsafe_allow_html=True
            )
            upside = ((target_mean - close) / close) * 100 if target_mean else None
            upside_str   = f"{upside:+.1f}%" if upside is not None else "—"
            upside_color = "#00E5B4" if (upside or 0) >= 0 else "#FF4D6A"

            rec_color_map = {
                "STRONG_BUY": "#00E5B4", "BUY": "#00E5B4",
                "HOLD": "#F5A623", "NEUTRAL": "#F5A623",
                "SELL": "#FF4D6A", "STRONG_SELL": "#FF4D6A"
            }
            rec_color = rec_color_map.get(rec_key.replace(" ","_"), "#8892A4")

            analyst_cards = [
                ("Target (Mean)",  f"₹{target_mean:,.2f}" if target_mean else "—",  ""),
                ("Target (High)",  f"₹{target_high:,.2f}" if target_high else "—",  ""),
                ("Target (Low)",   f"₹{target_low:,.2f}"  if target_low  else "—",  ""),
                ("Upside / Down",  upside_str,                                       "vs last price"),
            ]

            cols5 = st.columns(4)
            for idx, (label, val, sub) in enumerate(analyst_cards):
                with cols5[idx]:
                    color_override = upside_color if label == "Upside / Down" else "#E8EDF5"
                    st.markdown(
                        f"""<div class="fund-card">
                        <div class="fund-label">{label}</div>
                        <div class="fund-value" style="color:{color_override};">{val}</div>
                        {"<div class='fund-sub'>" + sub + "</div>" if sub else ""}
                        </div>""",
                        unsafe_allow_html=True
                    )

            st.markdown(
                f"""<div style="margin-top:0.6rem;font-family:'Space Mono',monospace;
                font-size:0.65rem;letter-spacing:0.1em;">
                <span style="color:#3A4459;">Recommendation: </span>
                <span style="color:{rec_color};font-weight:700;">{rec_key or "—"}</span>
                <span style="color:#2A3344;margin-left:1rem;">{num_analyst or "—"} analysts</span>
                <span style="color:#2A3344;margin-left:0.5rem;">· Score {rec_mean:.1f}/5</span>
                </div>""" if rec_mean else "",
                unsafe_allow_html=True
            )

        # ── BUSINESS SUMMARY ──────────────────────────────────────────────
        if summary:
            st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)
            with st.expander("Business Summary"):
                st.markdown(
                    f"""<div style="font-family:'DM Sans',sans-serif;font-size:0.82rem;
                    color:#8892A4;line-height:1.7;padding:0.3rem 0;">{summary}</div>""",
                    unsafe_allow_html=True
                )
