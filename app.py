import MetaTrader5 as mt5
import yfinance as yf
import ta
import time

# 1. MT5 سے کنیکٹ کرو
mt5.initialize(login=YOUR_MT5_LOGIN, password="YOUR_PASSWORD", server="YOUR_SERVER")

symbol = "EURUSD"
lot = 0.01

while True:
    # مارکیٹ کا ڈیٹا لو
    data = yf.download("EURUSD=X", period="5d", interval="5m")
    close = data['Close'].iloc[:,0]
    rsi = ta.momentum.rsi(close, 14).iloc[-1]
    ema9 = ta.trend.ema_indicator(close, 9).iloc[-1]
    ema21 = ta.trend.ema_indicator(close, 21).iloc[-1]
    
    price = mt5.symbol_info_tick(symbol).ask
    
    # BUY کی شرط
    if ema9 > ema21 and rsi > 55:
        sl = price - 0.0020  # 20 pips SL
        tp = price + 0.0030  # 30 pips TP
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": lot,
            "type": mt5.ORDER_TYPE_BUY,
            "price": price,
            "sl": sl,
            "tp": tp,
            "magic": 12345,
        }
        mt5.order_send(request)
        print(f"AUTO BUY TRADE LE LI - Price {price}")
        time.sleep(300) # 5 منٹ بعد دوبارہ چیک کرے گا

    # SELL کی شرط
    elif ema9 < ema21 and rsi < 45:
        sl = price + 0.0020
        tp = price - 0.0030
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": lot,
            "type": mt5.ORDER_TYPE_SELL,
            "price": price,
            "sl": sl,
            "tp": tp,
            "magic": 12345,
        }
        mt5.order_send(request)
        print(f"AUTO SELL TRADE LE LI - Price {price}")
        time.sleep(300)
