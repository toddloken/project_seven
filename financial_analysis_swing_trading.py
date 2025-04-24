import pandas as pd
import numpy as np

df = pd.read_csv('data/daily_data.csv')
print(df.head())

def calculate_rsi(data, period=14):
    """Relative Strenght index - RSI > 70: Overbought → potential sell
       RSI < 30: Oversold → potential buy
    """
    delta = data['close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_atr(data, period=14):
    high_low = data['high'] - data['low']
    high_close = np.abs(data['high'] - data['close'].shift())
    low_close = np.abs(data['low'] - data['close'].shift())
    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    atr = tr.rolling(period).mean()
    return atr

def calculate_vwap(data):
    """trading intensity and price relationship"""
    cum_price_vol = (data['close'] * data['volume']).cumsum()
    cum_vol = data['volume'].cumsum()
    vwap = cum_price_vol / cum_vol
    return vwap

def evaluate_swing_trading(rsi, atr_14, atr_28, atr_42, vwap):
    score = 0
    swing_trade_recommendation = False

    if rsi >= 70:
        score += 1
    elif rsi <=30:
        score +=1

    if atr_14 >15:
        score += 1

    if atr_28 >10:
        score += 1

    if atr_42 >10:
        score += 1

    if vwap >100:
        score += 1

    if score >= 3:
        swing_trade_recommendation = True

    return score, swing_trade_recommendation

rsi = calculate_rsi(df)
fm_rsi = rsi.dropna().iloc[-1]
atr_14 = calculate_atr(df, period=14)
fm_atr_14 = atr_14.dropna().iloc[-1]
atr_28 = calculate_atr(df, period=28)
fm_atr_28 = atr_28.dropna().iloc[-1]
atr_42 = calculate_atr(df, period=42)
fm_atr_42= atr_42.dropna().iloc[-1]
vwap = calculate_vwap(df)
fm_vwap = vwap.dropna().iloc[-1]

fm_swing_score, fm_swing_trade_recommendation = evaluate_swing_trading(fm_rsi, fm_atr_14, fm_atr_28, fm_atr_42, fm_vwap)


# vwap = calculate_vwap(data)
#
# # Print sample outputs
print("Latest RSI:",fm_rsi)
print("Latest 14Day ATR:",fm_atr_14)
print("Latest 28Day ATR:",fm_atr_28)
print("Latest 42Day ATR:",fm_atr_42)
print("Latest VWAP:", fm_vwap)

print("Swing Trade Rating Score:", fm_swing_score)
print("Swing Trade Recommendation:", fm_swing_trade_recommendation)
