import streamlit as st
import yfinance as yf
import pandas as pd
import ta
import random

st.set_page_config(page_title="😎 ALONE BOAT 😎", layout="centered")

st.markdown("""
<style>
.big-board { 
    background: linear-gradient(90deg, #000000, #1a1a1a, #000000); 
    border: 2px solid #00ff88; 
    padding: 20px; 
    border-radius: 15px; 
    text-align: center; 
    color: white;
    box-shadow: 0 0 20px #00ff88;
}
.signal-buy { background-color: #00ff66; color: black; padding: 18px; border-radius: 12px; font-size: 26px; font-weight: bold; text-align: center; }
.signal-sell { background-color: #ff1744; color: white; padding: 18px; border-radius: 12px; font-size: 26px; font-weight: bold; text-align: center; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="big-board"><h1>😎 ALONE BOAT 😎</h1><p>MT5 | QUOTEX | POCKET OPTION | PRO VERSION</p></div>', unsafe_allow_html=True)
st.write("")

BROKERS = ["MT5", "QUOTEX", "Pocket Option"]
PAIRS = {
    "EUR/USD": "EURUSD=X",
    "GBP/USD": "GBPUSD=X",
    "AUD/CHF": "AUDCHF=X",
    "EUR/JPY": "EURJPY=X",
    "GBP/JPY": "GBPJPY=X",
    "USD/JPY": "USDJPY=X"
}
TIMES = ["30 Second", "1 Minute", "2 Minute", "5 Minute", "15 Minute", "30 Minute (Half Hour)"]

def detect_candle_pattern(df):
    try:
        last = df.iloc[-1]
        o = float(last['Open']); h = float(last['High'])
        l = float(last['Low']); c = float(last['Close'])
        prev = df.iloc[-2]
        po = float(prev['Open']); pc = float(prev['Close'])
        body = abs(c - o)
        total_range = h - l
        if total_range == 0: return "Normal", 0
        upper_shadow = h - max(c, o)
        lower_shadow = min(c, o) - l
        pattern = "Normal Market"; signal = 0
        if body < total_range * 0.4 and lower_shadow > body * 2:
            pattern = "Hammer (Bullish)"; signal = 1
        elif body < total_range * 0.4 and upper_shadow > body * 2:
            pattern = "Shooting Star (Bearish)"; signal = -1
        elif pc < po and c > o and o < pc and c > po:
            pattern = "Bullish Engulfing"; signal = 1
        elif
