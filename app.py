import streamlit as st
import yfinance as yf
import pandas as pd
from streamlit_lightweight_charts import renderLightweightCharts

st.set_page_config(layout="wide", page_title="Quant Terminal", page_icon="📈")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600&display=swap');
html, body, .stApp { background-color: #080A0F !important; color: #C8D0DC !important; font-family: 'DM Sans', sans-serif !important; }
.block-container { padding: 1.5rem 2.5rem 2rem 2.5rem !important; max-width: 100% !important; }
[data-testid="stSidebar"] { background: #0D1017 !important; border-right: 1px solid rgba(0,229,180,0.12) !important; }
[data-testid="stSidebar"] .block-container { padding: 2rem 1.5rem !important; }
[data-testid="stSidebar"] h1 { font-family: 'Space Mono', monospace !important; font-size: 1rem !important; letter-spacing: 0.18em !important; text-transform: uppercase !important; color: #00E5B4 !important; padding-bottom: 1.2rem !important; border-bottom: 1px solid rgba(0,229,180,0.2) !important; margin-bottom: 1.5rem !important; }
[data-testid="stSidebar"] label { font-family: 'Space Mono', monospace !important; font-size: 0.62rem !important; letter-spacing: 0.14em !important; text-transform: uppercase !important; color: #4A5568 !important; }
[data-testid="stSidebar"] input { background: #111520 !important; border: 1px solid rgba(0,229,180,0.18) !important; border-radius: 4px !important; color: #00E5B4 !important; font-family: 'Space Mono', monospace !important; font-size: 0.95rem !important; }
[data-testid="stSidebar"] input:focus { border-color: #00E5B4 !important; box-shadow: 0 0 0 2px rgba(0,229,180,0.1) !important; }
[data-testid="stSidebar"] .stSelectbox > div > div { background: #111520 !important; border: 1px solid rgba(0,229,180,0.18) !important; border-radius: 4px !important; color: #C8D0DC !important; }
[data-testid="stSidebar"] .stCheckbox label { font-family: 'Space Mono', monospace !important; font-size: 0.72rem !important; letter-spacing: 0.06em !important; text-transform: uppercase !important; color: #8892A4 !important; }
[data-testid="stSidebar"] hr { border-color: rgba(0,229,180,0.1) !important; margin: 1.2rem 0 !important; }
[data-testid="stSidebar"] .stButton button { width: 100% !important; background: transparent !important; border: 1px solid rgba(0,229,180,0.4) !important; border-radius: 4px !important; color: #00E5B4 !important; font-family: 'Space Mono', monospace !important; font-size: 0.7rem !important; letter-spacing: 0.14em !important; text-transform: uppercase !important; padding: 0.6rem !important; transition: all 0.2s !important; }
[data-testid="stSidebar"] .stButton button:hover { background: rgba(0,229,180,0.08) !important; border-color: #00E5B4 !important; box-shadow: 0 0 12px rgba(0,229,180,0.15) !important; }
h1, h2, h3 { font-family: 'Space Mono', monospace !important; }
[data-testid="stMetric"] { background: #0D1017 !important; border: 1px solid #161C27 !important; border-radius: 6px !important; padding: 0.85rem 1.1rem !important; position: relative !important; overflow: hidden !important; transition: border-color 0.2s !important; }
[data-testid="stMetric"]::before { content: ''; position: absolute; top: 0; left: 0; width: 3px; height: 100%; background: linear-gradient(180deg, #00E5B4, transparent); }
[data-testid="stMetric"]:hover { border-color: rgba(0,229,180,0.2) !important; }
[data-testid="stMetricLabel"] { font-family: 'Space Mono', monospace !important; font-size: 0.58rem !important; letter-spacing: 0.18em !important; text-transform: uppercase !important; color: #3A4459 !important; }
[data-testid="stMetricValue"] { font-family: 'Space Mono', monospace !important; font-size: 1.15rem !important; color: #E8EDF5 !important; font-weight: 700 !important; line-height: 1.3 !important; }
[data-testid="stMetricDelta"] { font-family: 'Space Mono', monospace !important; font-size: 0.65rem !important; }
[data-testid="stMetricDelta"] svg { display: none !important; }
[data-testid="stMetricDelta"][data-direction="up"] { color: #00E5B4 !important; }
[data-testid="stMetricDelta"][data-direction="down"] { color: #FF4D6A !important; }
[data-testid="stExpander"] { background: #0D1017 !important; border: 1px solid #161C27 !important; border-radius: 6px !important; margin-top: 0.75rem !important; }
[data-testid="stExpander"] summary { font-family: 'Space Mono', monospace !important; font-size: 0.65rem !important; letter-spacing: 0.14em !important; text-transform: uppercase !important; color: #3A4459 !important; padding: 0.75rem 1rem !important; }
[data-testid="stExpander"] summary:hover { color: #00E5B4 !important; }
.stDataFrame thead th { background: #080A0F !important; color: #3A4459 !important; font-family: 'Space Mono', monospace !important; font-size: 0.58rem !important; letter-spacing: 0.1em !important; text-transform: uppercase !important; }
.stDataFrame tbody td { font-family: 'Space Mono', monospace !important; font-size: 0.75rem !important; color: #8892A4 !important; }
.stDataFrame tbody tr:hover td { background: #111520 !important; color: #C8D0DC !important; }
[data-testid="stSpinner"] p { font-family: 'Space Mono', monospace !important; font-size: 0.7rem !important; letter-spacing: 0.1em !important; color: #3A4459 !important; }
[data-testid="stInfo"] { background: rgba(0,229,180,0.05) !important; border: 1px solid rgba(0,229,180,0.2) !important; border-radius: 4px !important; font-family: 'Space Mono', monospace !important; font-size: 0.72rem !important; color: #00E5B4 !important; }
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: #080A0F; }
::-webkit-scrollbar-thumb { background: #1E2733; border-radius: 2px; }
::-webkit-scrollbar-thumb:hover { background: #00E5B4; }
[data-testid="stHorizontalBlock"] { gap: 0.65rem !important; }
</style>
<div style="display:flex;align-items:center;justify-content:space-between;padding:0.6rem 0 1.4rem 0;border-bottom:1px solid #13181F;margin-bottom:1.4rem;">
  <div style="display:flex;align-items:center;gap:1rem;">
    <span style="font-family:'Space Mono',monospace;font-size:1.1rem;font-weight:700;color:#00E5B4;letter-spacing:0.08em;">QUANT/TERMINAL</span>
    <span style="background:rgba(0,229,180,0.08);border:1px solid rgba(0,229,180,0.2);color:#00E5B4;font-family:'Space Mono',monospace;font-size:0.56rem;letter-spacing:0.18em;padding:2px 8px;border-radius:2px;">LIVE</span>
  </div>
  <span style="font-family:'Space Mono',monospace;font-size:0.58rem;color:#2A3344;letter-spacing:0.1em;">NSE · BSE · EQUITY</span>
</div>
""", unsafe_allow_html=True)


def compute_rsi(series, period=14):
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.ewm(com=period - 1, min_periods=period).mean()
    avg_loss = loss.ewm(com=period - 1, min_periods=period).mean()
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))


@st.cache_data(ttl=3600)
def fetch_data(ticker, period):
    df = yf.download(ticker, period=period, auto_adjust=False)
    if df.empty:
        return None
    df.columns = [col[0] if isinstance(col, tuple) else col for col in df.columns]
    df = df.reset_index()
    df["Date"] = pd.to_datetime(df["Date"])
    df["time"] = df["Date"].dt.strftime("%Y-%m-%d")
    df["MA20"] = df["Close"].rolling(20).mean()
    df["MA50"] = df["Close"].rolling(50).mean()
    df["RSI"]  = compute_rsi(df["Close"])
    return df


with st.sidebar:
    st.title("⬡ Controls")
    ticker_raw = st.text_input("Symbol", "RELIANCE.NS", help="NSE: .NS  |  BSE: .BO")
    ticker = ticker_raw.strip().upper()
    st.markdown("""<div style="font-family:'Space Mono',monospace;font-size:0.53rem;color:#2A3344;letter-spacing:0.07em;margin-top:-0.4rem;margin-bottom:0.8rem;line-height:1.8;">e.g. INFY.NS · TCS.NS · HDFCBANK.NS<br>WIPRO.NS · ^NSEI · ^BSESN</div>""", unsafe_allow_html=True)
    period = st.selectbox("Period", ["3mo", "6mo", "1y", "2y", "5y"], index=2)
    chart_height = st.slider("Chart Height", 350, 700, 460, step=50)
    st.divider()
    st.markdown("""<div style="font-family:'Space Mono',monospace;font-size:0.6rem;color:#3A4459;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:0.4rem;">Overlays</div>""", unsafe_allow_html=True)
    show_ma20 = st.checkbox("MA 20", True)
    show_ma50 = st.checkbox("MA 50", True)
    st.divider()
    st.markdown("""<div style="font-family:'Space Mono',monospace;font-size:0.6rem;color:#3A4459;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:0.4rem;">Sub-Panels</div>""", unsafe_allow_html=True)
    show_volume = st.checkbox("Volume", True)
    show_rsi    = st.checkbox("RSI (14)", True)
    st.divider()
    if st.button("↺ Refresh Data"):
        st.cache_data.clear()
        st.rerun()
    st.markdown("""<div style="margin-top:2rem;font-family:'Space Mono',monospace;font-size:0.52rem;color:#1E2733;letter-spacing:0.1em;line-height:2;text-transform:uppercase;">Data · Yahoo Finance<br>Charts · Lightweight Charts<br>Prices delayed · 15 min</div>""", unsafe_allow_html=True)


with st.spinner(f"Fetching {ticker}  ·  {period} ..."):
    df = fetch_data(ticker, period)

if df is None:
    st.error(f"No data found for '{ticker}'")
    st.info("Try: RELIANCE.NS  ·  INFY.NS  ·  TCS.NS  ·  HDFCBANK.NS  ·  ^NSEI")
    st.stop()

if len(df) < 55:
    st.warning("Limited history — MA50 and RSI readings may be inaccurate. Try a longer period.")

last  = df.iloc[-1]
prev  = df.iloc[-2]
change     = float(((last["Close"] - prev["Close"]) / prev["Close"]) * 100)
change_abs = float(last["Close"] - prev["Close"])
w52_high      = float(df["High"].max())
w52_low       = float(df["Low"].min())
pct_from_high = float(((last["Close"] - w52_high) / w52_high) * 100)
last_ma20 = float(df["MA20"].dropna().iloc[-1]) if not df["MA20"].dropna().empty else None
last_ma50 = float(df["MA50"].dropna().iloc[-1]) if not df["MA50"].dropna().empty else None
last_rsi  = float(df["RSI"].dropna().iloc[-1])  if not df["RSI"].dropna().empty  else None
avg_vol20 = int(df["Volume"].tail(20).mean())    if "Volume" in df.columns else None

def rsi_label(v):
    if v is None: return ("—", "#3A4459")
    if v >= 70:   return (f"{v:.1f} OVERBOUGHT", "#FF4D6A")
    if v <= 30:   return (f"{v:.1f} OVERSOLD",   "#00E5B4")
    return (f"{v:.1f} NEUTRAL", "#8892A4")

rsi_txt, rsi_color = rsi_label(last_rsi)
date_str = last["Date"].strftime("%d %b %Y") if hasattr(last["Date"], "strftime") else ""

st.markdown(f"""
<div style="display:flex;align-items:baseline;gap:1.2rem;margin-bottom:1rem;flex-wrap:wrap;">
  <span style="font-family:'Space Mono',monospace;font-size:1.55rem;font-weight:700;color:#E8EDF5;letter-spacing:0.04em;">{ticker}</span>
  <span style="font-family:'Space Mono',monospace;font-size:0.65rem;color:#2A3344;letter-spacing:0.12em;text-transform:uppercase;">{date_str}</span>
  <span style="font-family:'Space Mono',monospace;font-size:0.7rem;letter-spacing:0.05em;color:{"#00E5B4" if change >= 0 else "#FF4D6A"};">
    {"▲" if change >= 0 else "▼"} {abs(change):.2f}% ({("+" if change_abs >= 0 else "")}{change_abs:.2f})
  </span>
  <span style="font-family:'Space Mono',monospace;font-size:0.65rem;letter-spacing:0.08em;color:{rsi_color};">RSI {rsi_txt}</span>
</div>
""", unsafe_allow_html=True)

c1, c2, c3, c4, c5, c6 = st.columns(6)
c1.metric("Last Price",  f"₹{float(last['Close']):.2f}", f"{change:+.2f}%")
c2.metric("Day High",    f"₹{float(last['High']):.2f}")
c3.metric("Day Low",     f"₹{float(last['Low']):.2f}")
c4.metric("Volume",      f"{int(last['Volume']):,}" if "Volume" in df.columns else "—")
c5.metric("52W High",    f"₹{w52_high:.2f}", f"{pct_from_high:+.1f}% off high")
c6.metric("52W Low",     f"₹{w52_low:.2f}")

st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

m1, m2, m3, m4 = st.columns(4)
if last_ma20:
    above20 = float(last["Close"]) > last_ma20
    m1.metric("MA 20", f"₹{last_ma20:.2f}", f"{"▲ Above" if above20 else "▼ Below"}")
else:
    m1.metric("MA 20", "—")
if last_ma50:
    above50 = float(last["Close"]) > last_ma50
    m2.metric("MA 50", f"₹{last_ma50:.2f}", f"{"▲ Above" if above50 else "▼ Below"}")
else:
    m2.metric("MA 50", "—")
m3.metric("RSI 14",      f"{last_rsi:.1f}" if last_rsi else "—")
m4.metric("Avg Vol 20d", f"{avg_vol20:,}"  if avg_vol20 else "—")

st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)


def base_opts(show_time=True):
    return {
        "layout": {"background": {"type": "solid", "color": "#0D1017"}, "textColor": "#3A4459", "fontSize": 11, "fontFamily": "'Space Mono', monospace"},
        "grid": {"vertLines": {"color": "#0F1318"}, "horzLines": {"color": "#0F1318"}},
        "crosshair": {"mode": 1, "vertLine": {"color": "rgba(0,229,180,0.3)", "labelBackgroundColor": "#00E5B4"}, "horzLine": {"color": "rgba(0,229,180,0.3)", "labelBackgroundColor": "#00E5B4"}},
        "rightPriceScale": {"borderColor": "#13181F", "textColor": "#3A4459", "autoScale": True, "minValue": 0},
        "timeScale": {"borderColor": "#13181F", "timeVisible": show_time, "secondsVisible": False, "visible": show_time},
    }


candles = df[["time","Open","High","Low","Close"]].rename(columns={"Open":"open","High":"high","Low":"low","Close":"close"}).to_dict("records")
for r in candles:
    r["open"] = float(r["open"]); r["high"] = float(r["high"]); r["low"] = float(r["low"]); r["close"] = float(r["close"])

price_series = [{"type": "Candlestick", "data": candles, "options": {"upColor": "#00E5B4", "downColor": "#FF4D6A", "borderVisible": False, "wickUpColor": "#00E5B4", "wickDownColor": "#FF4D6A"}}]

if show_ma20 and last_ma20:
    ma20d = df[["time","MA20"]].dropna()
    price_series.append({"type": "Line", "data": [{"time": r["time"], "value": float(r["MA20"])} for _, r in ma20d.iterrows()], "options": {"color": "#F5A623", "lineWidth": 1}})

if show_ma50 and last_ma50:
    ma50d = df[["time","MA50"]].dropna()
    price_series.append({"type": "Line", "data": [{"time": r["time"], "value": float(r["MA50"])} for _, r in ma50d.iterrows()], "options": {"color": "#4D9FFF", "lineWidth": 1}})

price_opts = base_opts(show_time=not (show_volume or show_rsi))
price_opts["watermark"] = {"visible": True, "fontSize": 52, "horzAlign": "center", "vertAlign": "center", "color": "rgba(255,255,255,0.018)", "text": ticker}

charts_to_render = [{"chart": price_opts, "series": price_series}]

if show_volume and "Volume" in df.columns:
    vol_data = []
    for _, row in df.iterrows():
        c = "#00E5B4" if float(row["Close"]) >= float(row["Open"]) else "#FF4D6A"
        vol_data.append({"time": row["time"], "value": float(row["Volume"]), "color": c + "88"})
    vol_opts = base_opts(show_time=not show_rsi)
    vol_opts["rightPriceScale"]["minValue"] = 0
    charts_to_render.append({"chart": vol_opts, "series": [{"type": "Histogram", "data": vol_data, "options": {"priceFormat": {"type": "volume"}, "priceScaleId": ""}}]})

if show_rsi:
    rsi_df   = df[["time","RSI"]].dropna()
    rsi_data = [{"time": r["time"], "value": float(r["RSI"])} for _, r in rsi_df.iterrows()]
    ob_line  = [{"time": r["time"], "value": 70.0} for _, r in rsi_df.iterrows()]
    os_line  = [{"time": r["time"], "value": 30.0} for _, r in rsi_df.iterrows()]
    rsi_opts = base_opts(show_time=True)
    rsi_opts["rightPriceScale"]["autoScale"] = False
    rsi_opts["rightPriceScale"]["minValue"]  = 0
    rsi_opts["rightPriceScale"]["maxValue"]  = 100
    charts_to_render.append({"chart": rsi_opts, "series": [
        {"type": "Line", "data": rsi_data, "options": {"color": "#A78BFA", "lineWidth": 1}},
        {"type": "Line", "data": ob_line,  "options": {"color": "rgba(255,77,106,0.4)", "lineWidth": 1, "lineStyle": 2}},
        {"type": "Line", "data": os_line,  "options": {"color": "rgba(0,229,180,0.4)",  "lineWidth": 1, "lineStyle": 2}},
    ]})

ma20_str = f" · ₹{last_ma20:.0f}" if last_ma20 else ""
ma50_str = f" · ₹{last_ma50:.0f}" if last_ma50 else ""
legend_parts = ["<span style='color:#3A4459'>● Candles</span>"]
if show_ma20: legend_parts.append(f"<span style='color:#F5A623'>— MA20{ma20_str}</span>")
if show_ma50: legend_parts.append(f"<span style='color:#4D9FFF'>— MA50{ma50_str}</span>")
if show_volume: legend_parts.append("<span style='color:#3A4459'>▪ Volume</span>")
if show_rsi:    legend_parts.append("<span style='color:#A78BFA'>▪ RSI 14</span>")

st.markdown(f"""<div style="display:flex;gap:1.4rem;align-items:center;margin-bottom:0.5rem;font-family:'Space Mono',monospace;font-size:0.6rem;letter-spacing:0.1em;text-transform:uppercase;">{"  ".join(legend_parts)}</div>""", unsafe_allow_html=True)

try:
    renderLightweightCharts(charts_to_render, key="quant_charts", height=chart_height)
except TypeError:
    try:
        renderLightweightCharts(charts_to_render, key="quant_charts")
    except Exception:
        renderLightweightCharts(charts_to_render)

st.markdown("<div style='height:0.4rem'></div>", unsafe_allow_html=True)
with st.expander("▸  Raw Data  ·  Last 60 Sessions"):
    show_cols = [c for c in ["Date","Open","High","Low","Close","Volume","MA20","MA50","RSI"] if c in df.columns]
    disp = df.tail(60)[show_cols].copy()
    for col in ["Open","High","Low","Close","MA20","MA50"]:
        if col in disp.columns:
            disp[col] = disp[col].apply(lambda x: f"₹{x:.2f}" if pd.notna(x) else "—")
    if "RSI" in disp.columns:
        disp["RSI"] = disp["RSI"].apply(lambda x: f"{x:.1f}" if pd.notna(x) else "—")
    if "Volume" in disp.columns:
        disp["Volume"] = disp["Volume"].apply(lambda x: f"{int(x):,}" if pd.notna(x) else "—")
    st.dataframe(disp, use_container_width=True, hide_index=True)
