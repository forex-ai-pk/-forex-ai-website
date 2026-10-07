import streamlit as st
import yfinance as yf
import pandas as pd
import ta

st.set_page_config(page_title="Pro Forex AI", layout="centered")
st.title("🚀 PRO Forex AI Signals")
st.caption("Powered by MT5 Logic - TP & SL ke saath")

pair_map = {
    "EUR/USD": "EURUSD=X",
    "GBP/USD": "GBPUSD=X",
    "USD/JPY": "USDJPY=X",
    "Gold (XAU/USD)": "GC=F",
    "BTC/USD": "BTC-USD"
}

choice = st.selectbox("Pair Select Karo", list(pair_map.keys()))
pair = pair_map[choice]

if st.button("🔍 PRO Analysis Karo", use_container_width=True):
    with st.spinner("AI Analysis kar raha hai..."):
        try:
            data = yf.download(pair, period="10d", interval="1h", auto_adjust=True)
            if data.empty:
                st.error("Data nahi mila, dobara try karo")
            else:
                close = data['Close']
                if isinstance(close, pd.DataFrame):
                    close = close.iloc[:,0]
                high = data['High']
                low = data['Low']
                if isinstance(high, pd.DataFrame):
                    high = high.iloc[:,0]
                if isinstance(low, pd.DataFrame):
                    low = low.iloc[:,0]

                close = close.dropna()
                ema20 = ta.trend.ema_indicator(close, window=20)
                ema50 = ta.trend.ema_indicator(close, window=50)
                rsi = ta.momentum.rsi(close, window=14)
                atr = ta.volatility.average_true_range(high, low, close, window=14)

                last_close = float(close.iloc[-1])
                last_ema20 = float(ema20.iloc[-1])
                last_ema50 = float(ema50.iloc[-1])
                last_rsi = float(rsi.iloc[-1])
                last_atr = float(atr.iloc[-1])

                # Logic
                is_buy = last_ema20 > last_ema50 and last_rsi > 52
                is_sell = last_ema20 < last_ema50 and last_rsi < 48

                st.divider()
                col1, col2, col3 = st.columns(3)
                col1.metric("Live Price", f"{last_close:.4f}")
                col2.metric("RSI (14)", f"{last_rsi:.1f}")
                col3.metric("Trend", "UP" if last_ema20 > last_ema50 else "DOWN")

                if is_buy:
                    st.success("### 🟢 STRONG BUY SIGNAL")
                    sl = last_close - (last_atr * 1.5)
                    tp1 = last_close + (last_atr * 1.5)
                    tp2 = last_close + (last_atr * 3)
                    conf = 85 if last_rsi > 60 else 72
                    st.write(f"**Confidence: {conf}%**")
                    st.write(f"**Entry:** {last_close:.4f}")
                    st.write(f"**Stop Loss:** {sl:.4f} 🔴")
                    st.write(f"**Take Profit 1:** {tp1:.4f} 🟢")
                    st.write(f"**Take Profit 2:** {tp2:.4f} 🟢🟢")
                    st.info("Tareeqa: TP1 pe 50% profit book karlo, baqi TP2 tak hold karo")

                elif is_sell:
                    st.error("### 🔴 STRONG SELL SIGNAL")
                    sl = last_close + (last_atr * 1.5)
                    tp1 = last_close - (last_atr * 1.5)
                    tp2 = last_close - (last_atr * 3)
                    conf = 85 if last_rsi < 40 else 72
                    st.write(f"**Confidence: {conf}%**")
                    st.write(f"**Entry:** {last_close:.4f}")
                    st.write(f"**Stop Loss:** {sl:.4f} 🔴")
                    st.write(f"**Take Profit 1:** {tp1:.4f} 🟢")
                    st.write(f"**Take Profit 2:** {tp2:.4f} 🟢🟢")
                    st.info("Tareeqa: TP1 pe 50% profit book karlo, baqi TP2 tak hold karo")
                else:
                    st.warning("### 🟡 WAIT - No Clear Trade")
                    st.write("Market sideways hai, thodi der baad check karo")

                st.divider()
                st.line_chart(close.tail(150))
                st.caption("Note: Ye AI analysis hai, 100% guarantee nahi. Apna risk management zaroor karo.")

        except Exception as e:
            st.error(f"Error: {e}")
