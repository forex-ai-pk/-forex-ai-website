import streamlit as st
import yfinance as yf
import ta
st.set_page_config(page_title="AI Forex Analyzer")
st.title("AI Forex Analyzer - No Fees")
pair = st.selectbox("Pair Chuno", ["EURUSD=X", "GBPUSD=X", "GC=F", "BTC-USD"])
if st.button("AI se Analysis Karo"):
    data = yf.download(pair, period="1d", interval="5m")
    data['EMA_50'] = ta.trend.ema_indicator(data['Close'], window=50)
    data['RSI'] = ta.momentum.rsi(data['Close'], window=14)
    last_close = float(data['Close'].iloc[-1])
    last_ema = float(data['EMA_50'].iloc[-1])
    last_rsi = float(data['RSI'].iloc[-1])
    st.metric("Live Price", last_close)
    if last_close < last_ema and last_rsi > 60:
        st.error("SELL Signal - Bearish Candle")
    elif last_close > last_ema and last_rsi < 40:
        st.success("BUY Signal - Bullish Candle")
    else:
        st.warning("WAIT - No Clear Signal")
    st.line_chart(data['Close'])
