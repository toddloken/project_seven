import pandas as pd
import numpy as np


class SwingTradeAnalyzer:
    def __init__(self, data_path):
        self.df = pd.read_csv(data_path)

    def calculate_rsi(self, period=14):
        """Relative Strength Index - RSI > 70: Overbought → potential sell
           RSI < 30: Oversold → potential buy
        """
        delta = self.df['close'].diff()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)
        avg_gain = gain.rolling(period).mean()
        avg_loss = loss.rolling(period).mean()
        rs = avg_gain / avg_loss
        return 100 - (100 / (1 + rs))

    def calculate_atr(self, period=14):
        high_low = self.df['high'] - self.df['low']
        high_close = np.abs(self.df['high'] - self.df['close'].shift())
        low_close = np.abs(self.df['low'] - self.df['close'].shift())
        tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
        return tr.rolling(period).mean()

    def calculate_vwap(self):
        """Trading intensity and price relationship"""
        cum_price_vol = (self.df['close'] * self.df['volume']).cumsum()
        cum_vol = self.df['volume'].cumsum()
        return cum_price_vol / cum_vol

    def evaluate_swing_trading(self, rsi, atr_14, atr_28, atr_42, vwap):
        score = 0
        swing_trade_recommendation = False

        if rsi >= 70 or rsi <= 30:
            score += 1

        if atr_14 > 15:
            score += 1

        if atr_28 > 10:
            score += 1

        if atr_42 > 10:
            score += 1

        if vwap > 100:
            score += 1

        if score >= 3:
            swing_trade_recommendation = True

        return score, swing_trade_recommendation

    def get_latest_indicators(self):
        # Calculate all indicators
        rsi = self.calculate_rsi()
        atr_14 = self.calculate_atr(period=14)
        atr_28 = self.calculate_atr(period=28)
        atr_42 = self.calculate_atr(period=42)
        vwap = self.calculate_vwap()

        # Get latest values
        fm_rsi = rsi.dropna().iloc[-1]
        fm_atr_14 = atr_14.dropna().iloc[-1]
        fm_atr_28 = atr_28.dropna().iloc[-1]
        fm_atr_42 = atr_42.dropna().iloc[-1]
        fm_vwap = vwap.dropna().iloc[-1]

        return fm_rsi, fm_atr_14, fm_atr_28, fm_atr_42, fm_vwap

    def get_swing_trade_recommendation(self):
        fm_rsi, fm_atr_14, fm_atr_28, fm_atr_42, fm_vwap = self.get_latest_indicators()
        fm_score, fm_recommendation = self.evaluate_swing_trading(
            fm_rsi, fm_atr_14, fm_atr_28, fm_atr_42, fm_vwap
        )
        return fm_score, fm_recommendation