import streamlit as st
import yfinance as yf
import pandas as pd
import ta

st.set_page_config(page_title="AI Forex Bot", layout="centered")
st.title("🤖 AI Forex Bot - Pro")
st.caption("Pair + Timeframe والا اصلی بوٹ")

# 1. Pair والا سسٹم
pair_map = {
    "EUR/USD": "EURUSD=X",
    "GBP/USD": "GBPUSD=X",
    "USD/JPY": "USDJPY=X",
    "USD/CHF": "CHF=X",
    "AUD/USD": "AUDUSD=X",
    "Gold (XAU/USD)": "GC=F",
    "BTC/USD": "BTC-USD",
    "ETH/USD": "ETH-USD"
}

# 2. Timeframe والا سسٹم - اب 1 Minute بھی شامل ہے
time_map = {
    "1 Minute": "1m",
    "5 Minute": "5m",
    "15 Minute": "15m",
    "30 Minute": "30m",
    "1 Hour": "1h",
    "4 Hour": "4h",
    "1 Day": "1d"
}

col1, col2 = st.columns(2)
with col1:
    choice_pair = st.selectbox("Pair منتخب کریں", list(pair_map.keys()))
with col2:
    choice_time = st.selectbox("Candle Timeframe", list(time_map.keys()))

pair = pair_map[choice_pair]
interval = time_map[choice_time]

# Period Logic
if interval == "1m":
    period = "1d"
elif interval in ["5m", "15m"]:
    period = "5d"
elif interval in ["30m", "1h"]:
    period = "20d"
else:
    period = "100d"

if st.button(f"🚀 {choice_pair} کا {choice_time} پر سگنل لو", use_container_width=True, type="primary"):
    with st.spinner(f"{choice_pair} کا {choice_time} پر تجزیہ ہو رہا ہے..."):
        try:
            data = yf.download(pair, period=period, interval=interval, auto_adjust=True)
            if data.empty or len(data) < 50:
                st.error("ڈیٹا کم ہے، دوسرا Timeframe ٹرائی کریں")
            else:
                close = data['Close']
                high = data['High']
                low = data['Low']
                if isinstance(close, pd.DataFrame):
                    close = close.iloc[:,0]
                    high = high.iloc[:,0]
                    low = low.iloc[:,0]

                close = close.dropna()
                ema9 = ta.trend.ema_indicator(close, window=9)
                ema21 = ta.trend.ema_indicator(close, window=21)
                ema50 = ta.trend.ema_indicator(close, window=50)
                rsi = ta.momentum.rsi(close, window=14)
                atr = ta.volatility.average_true_range(high, low, close, window=14)

                last_close = float(close.iloc[-1])
                last_ema9 = float(ema9.iloc[-1])
                last_ema21 = float(ema21.iloc[-1])
                last_ema50 = float(ema50.iloc[-1])
                last_rsi = float(rsi.iloc[-1])
                last_atr = float(atr.iloc[-1])

                buy_condition = last_ema9 > last_ema21 and last_ema21 > last_ema50 and last_rsi > 55
                sell_condition = last_ema9 < last_ema21 and last_ema21 < last_ema50 and last_rsi < 45

                st.divider()
                st.subheader(f"📊 {choice_pair} | {choice_time}")
                m1, m2, m3 = st.columns(3)
                m1.metric("قیمت", f"{last_close:.4f}")
                m2.metric("RSI", f"{last_rsi:.1f}")
                m3.metric("ATR", f"{last_atr:.4f}")

                if buy_condition:
                    sl = last_close - (last_atr * 1.8)
                    tp1 = last_close + (last_atr * 1.5)
                    tp2 = last_close + (last_atr * 3)
                    st.success(f"### 🟢 BUY - {choice_pair}")
                    st.markdown(f"**Entry:** `{last_close:.5f}`\n**SL:** `{sl:.5f}` 🔴\n**TP1:** `{tp1:.5f}`\n**TP2:** `{tp2:.5f}`")
                elif sell_condition:
                    sl = last_close + (last_atr * 1.8)
                    tp1 = last_close - (last_atr * 1.5)
                    tp2 = last_close - (last_atr * 3)
                    st.error(f"### 🔴 SELL - {choice_pair}")
                    st.markdown(f"**Entry:** `{last_close:.5f}`\n**SL:** `{sl:.5f}` 🔴\n**TP1:** `{tp1:.5f}`\n**TP2:** `{tp2:.5f}`")
                else:
                    st.warning(f"### 🟡 WAIT - {choice_pair} پر کوئی سگنل نہیں")
                
                st.line_chart(close.tail(100))
        except Exception as e:
            st.error(f"Error: {e}")
