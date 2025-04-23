import pandas as pd
import numpy as np

ticker = "UNH"

df = pd.read_csv('data/daily_data.csv')
print(df.head())


def average_daily_volume(df):
    return df['volume'].mean()

def average_true_range(df, window=14):
    """volatility measurment - helps to maintain constant risk exposure"""
    high_low = df['high'] - df['low']
    high_close = abs(df['high'] - df['close'].shift())
    low_close = abs(df['low'] - df['close'].shift())
    true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    atr = true_range.rolling(window=window).mean()
    return atr.iloc[-1]

def relative_volume(df):
    avg_vol = average_daily_volume(df)
    current_vol = df['volume'].iloc[-1]
    return current_vol / avg_vol if avg_vol > 0 else np.nan

def average_intraday_volatility(df):
    intraday_vol = ((df['high'] - df['low']) / df['open']) * 100
    return abs(intraday_vol.mean())

def five_day_momentum(df):
    return df['close'].pct_change(periods=5).iloc[-1] * 100

def evaluate_daily_metrics(volume, atr, relative_volume, volatility, momentum):
    score = 0
    day_trade_recommendation = False

    if volume >= 1000000:
        score += 1
    if atr >= 10:
        score += 1
    if relative_volume >= 0.25:
        score += 1
    if volatility >= 0.025:
        score += 1
    if momentum >= 2.5:
        score +=1
    print(score)
    if score >= 3:
        day_trade_recommendation = True
    return score, day_trade_recommendation


fm_daily_volume = average_daily_volume(df)
fm_true_range = average_true_range(df)
fm_relative_volume = relative_volume(df)
fm_intraday_volatility = average_intraday_volatility(df)
fm_five_day_momentum = five_day_momentum(df)

fm_score, fm_day_trade_recommendation = evaluate_daily_metrics(fm_daily_volume, fm_true_range, fm_relative_volume, fm_intraday_volatility, fm_five_day_momentum)

print(f"Metrics for {ticker}:")
print("Average Daily Volume:", fm_daily_volume)
print("Average True Range (ATR):", fm_true_range)
print("Relative Volume (RVOL):", fm_relative_volume)
print("Average Intraday Volatility (%):", fm_intraday_volatility)
print("5-Day Price Momentum (%):", fm_five_day_momentum)
print("Daily Rating Score:", fm_score)
print("Daily Recommendation:", fm_score)
