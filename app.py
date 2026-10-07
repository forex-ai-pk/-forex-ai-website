import streamlit as st
import yfinance as yf
import pandas as pd
import ta

st.set_page_config(page_title="Forex AI Signal")
st.title("AI Forex Analyzer - No Fees")

pair = st.selectbox("Pair Chuno", ["EURUSD=X", "GBPUSD=X", "USDJPY=X", "BTC-USD"])

if st.button("AI se Analysis Karo"):
    try:
        data = yf.download(pair, period="5d", interval="1h", auto_adjust=True)
        if data.empty:
            st.error("Data nahi mila")
        else:
            close = data['Close']
            if isinstance(close, pd.DataFrame):
                close = close.iloc[:,0]
            close = close.dropna()
            ema = ta.trend.ema_indicator(close, window=50)
            rsi = ta.momentum.rsi(close, window=14)
            last_close = float(close.iloc[-1])
            last_ema = float(ema.iloc[-1])
            last_rsi = float(rsi.iloc[-1])
            st.metric("Live Price", f"{last_close:.4f}")
            st.metric("RSI", f"{last_rsi:.2f}")
            if last_close < last_ema and last_rsi < 45:
                st.error("SELL Signal - Bearish")
            elif last_close > last_ema and last_rsi > 55:
                st.success("BUY Signal - Bullish")
            else:
                st.info("WAIT - No Clear Signal")
            st.line_chart(close.tail(100))
    except Exception as e:
        st.error(f"Error: {e}")
