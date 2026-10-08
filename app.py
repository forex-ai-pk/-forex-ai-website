import streamlit as st
import yfinance as yf
import pandas as pd
import ta
import random

st.set_page_config(page_title="😎 ALONE BOAT 😎", layout="centered")

st.markdown("""
<style>
.big-board { background: linear-gradient(90deg, #000000, #1a1a1a, #000000); border: 2px solid #00ff88; padding: 20px; border-radius: 15px; text-align: center; color: white; box-shadow: 0 0 20px #00ff88; }
.signal-buy { background-color: #00ff66; color: black; padding: 18px; border-radius: 12px; font-size: 26px; font-weight: bold; text-align: center; }
.signal-sell { background-color: #ff1744; color: white; padding: 18px; border-radius: 12px; font-size: 26px; font-weight: bold; text-align: center; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="big-board"><h1>😎 ALONE BOAT 😎</h1><p>MT5 | QUOTEX | POCKET OPTION | 16 PATTERNS</p></div>', unsafe_allow_html=True)

BROKERS = ["MT5", "QUOTEX", "Pocket Option"]
PAIRS = {
    "EUR/USD": "EURUSD=X", "GBP/USD": "GBPUSD=X", "AUD/CHF": "AUDCHF=X",
    "EUR/JPY": "EURJPY=X", "GBP/JPY": "GBPJPY=X", "USD/JPY": "USDJPY=X"
}
TIMES = ["30 Second", "1 Minute", "2 Minute", "5 Minute", "15 Minute", "30 Minute"]

def detect_candle_pattern(df):
    try:
        df_last = df.tail(5)
        c1 = df_last.iloc[-3]
        c2 = df_last.iloc[-2]
        c3 = df_last.iloc[-1]

        o1, h1, l1, cl1 = float(c1['Open']), float(c1['High']), float(c1['Low']), float(c1['Close'])
        o2, h2, l2, cl2 = float(c2['Open']), float(c2['High']), float(c2['Low']), float(c2['Close'])
        o3, h3, l3, cl3 = float(c3['Open']), float(c3['High']), float(c3['Low']), float(c3['Close'])

        body3 = abs(cl3 - o3)
        range3 = h3 - l3 if (h3 - l3) != 0 else 0.001
        upper3 = h3 - max(cl3, o3)
        lower3 = min(cl3, o3) - l3

        # Default
        pattern = "Normal Market"
        signal = 0

        # 1 & 2 Engulfing
        if cl2 < o2 and cl3 > o3 and o3 < cl2 and cl3 > o2:
            pattern = "Bullish Engulfing"; signal = 1
        elif cl2 > o2 and cl3 < o3 and o3 > cl2 and cl3 < o2:
            pattern = "Bearish Engulfing"; signal = -1
        # 3 Hammer
        elif body3 < range3 * 0.35 and lower3 > body3 * 2:
            pattern = "Hammer (Bullish)"; signal = 1
        # 4 Shooting Star
        elif body3 < range3 * 0.35 and upper3 > body3 * 2:
            pattern = "Shooting Star (Bearish)"; signal = -1
        # 5 Morning Star
        elif cl1 < o1 and abs(cl2 - o2) < abs(cl1 - o1) * 0.4 and cl3 > o3 and cl3 > (o1 + cl1)/2:
            pattern = "Morning Star"; signal = 1
        # 6 Evening Star
        elif cl1 > o1 and abs(cl2 - o2) < abs(cl1 - o1) * 0.4 and cl3 < o3 and cl3 < (o1 + cl1)/2:
            pattern = "Evening Star"; signal = -1
        # 7 Bullish Harami
        elif cl2 < o2 and cl3 > o3 and o3 > cl2 and cl3 < o2:
            pattern = "Bullish Harami"; signal = 1
        # 8 Bearish Harami
        elif cl2 > o2 and cl3 < o3 and o3 < cl2 and cl3 > o2:
            pattern = "Bearish Harami"; signal = -1
        # 9 Spinning Top/Bottom
        elif body3 < range3 * 0.3 and upper3 > body3 and lower3 > body3:
            pattern = "Spinning Bottom"; signal = 0
        # 10 Doji
        elif body3 < range3 * 0.1:
            pattern = "Doji"; signal = 0
        # 11 Inverted Hammer
        elif cl2 < o2 and body3 < range3 * 0.4 and upper3 > body3 * 2 and cl3 > o3:
            pattern = "Inverted Hammer"; signal = 1
        # 12 Hanging Man
        elif cl1 > o1 and body3 < range3 * 0.4 and lower3 > body3 * 2 and cl3 < o3:
            pattern = "Hanging Man"; signal = -1
        # 13 Piercing Line
        elif cl2 < o2 and cl3 > o3 and o3 < l2 and cl3 > (o2 + cl2)/2:
            pattern = "Piercing Line"; signal = 1
        # 14 Dark Cloud
        elif cl2 > o2 and cl3 < o3 and o3 > h2 and cl3 < (o2 + cl2)/2:
            pattern = "Dark Cloud Cover"; signal = -1
       
