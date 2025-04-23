import pandas as pd
import numpy as np

df = pd.read_csv('data/daily_data.csv')
print(df.head())

def calculate_rsi(data, period=14):
    delta = data['close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_sma(data, window=20):
    return data['close'].rolling(window=window).mean()

def calculate_ema(data, window=20):
    return data['Adj Close'].ewm(span=window, adjust=False).mean()

def calculate_macd(data, fast=12, slow=26, signal=9):
    ema_fast = data['Adj Close'].ewm(span=fast, adjust=False).mean()
    ema_slow = data['Adj Close'].ewm(span=slow, adjust=False).mean()
    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    histogram = macd_line - signal_line
    return macd_line, signal_line, histogram

def calculate_atr(data, period=14):
    high_low = data['High'] - data['Low']
    high_close = np.abs(data['High'] - data['Close'].shift())
    low_close = np.abs(data['Low'] - data['Close'].shift())
    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    atr = tr.rolling(period).mean()
    return atr

def calculate_bollinger_bands(data, window=20, num_std=2):
    sma = data['Adj Close'].rolling(window).mean()
    std = data['Adj Close'].rolling(window).std()
    upper_band = sma + (num_std * std)
    lower_band = sma - (num_std * std)
    return upper_band, sma, lower_band

def calculate_fibonacci_levels(data):
    max_price = data['Adj Close'].max()
    min_price = data['Adj Close'].min()
    diff = max_price - min_price
    levels = {
        "0.0%": max_price,
        "23.6%": max_price - 0.236 * diff,
        "38.2%": max_price - 0.382 * diff,
        "50.0%": max_price - 0.5 * diff,
        "61.8%": max_price - 0.618 * diff,
        "100.0%": min_price
    }
    return levels

def calculate_vwap(data):
    cum_price_vol = (data['Close'] * data['Volume']).cumsum()
    cum_vol = data['Volume'].cumsum()
    vwap = cum_price_vol / cum_vol
    return vwap

rsi = calculate_rsi(df)
# sma20 = calculate_sma(data, 20)
# ema20 = calculate_ema(data, 20)
# macd_line, signal_line, macd_hist = calculate_macd(data)
# atr = calculate_atr(data)
# upper_bb, mid_bb, lower_bb = calculate_bollinger_bands(data)
# fib_levels = calculate_fibonacci_levels(data)
# vwap = calculate_vwap(data)
#
# # Print sample outputs
print("Latest RSI:", rsi.dropna().iloc[-1])
# print("Latest 20-day SMA:", sma20.dropna().iloc[-1])
# print("Latest ATR:", atr.dropna().iloc[-1])
# print("Fibonacci levels:", fib_levels)
# print("Latest VWAP:", vwap.dropna().iloc[-1])

"""RSI > 70: Overbought → potential sell
RSI < 30: Oversold → potential buy"""