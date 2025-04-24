import pandas as pd
import numpy as np


class DailyMetricsAnalyzer:
    def __init__(self, csv_path):
        """Initialize the analyzer with data from a CSV file."""
        self.df = pd.read_csv(csv_path)

    def average_daily_volume(self):
        """Calculate the average daily trading volume."""
        return self.df['volume'].mean()

    def average_true_range(self, window=14):
        """Calculate volatility measurement (ATR) - helps to maintain constant risk exposure."""
        high_low = self.df['high'] - self.df['low']
        high_close = abs(self.df['high'] - self.df['close'].shift())
        low_close = abs(self.df['low'] - self.df['close'].shift())
        true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
        atr = true_range.rolling(window=window).mean()
        return atr.iloc[-1]

    def relative_volume(self):
        """Calculate current volume relative to average volume."""
        avg_vol = self.average_daily_volume()
        current_vol = self.df['volume'].iloc[-1]
        return current_vol / avg_vol if avg_vol > 0 else np.nan

    def average_intraday_volatility(self):
        """Calculate average intraday volatility as a percentage."""
        intraday_vol = ((self.df['high'] - self.df['low']) / self.df['open']) * 100
        return abs(intraday_vol.mean())

    def five_day_momentum(self):
        """Calculate 5-day price momentum as a percentage."""
        return self.df['close'].pct_change(periods=5).iloc[-1] * 100

    def evaluate_daily_metrics(self):
        """Evaluate all metrics and generate a trading recommendation."""
        volume = self.average_daily_volume()
        atr = self.average_true_range()
        rel_volume = self.relative_volume()
        volatility = self.average_intraday_volatility()
        momentum = self.five_day_momentum()

        score = 0
        day_trade_recommendation = False

        if volume >= 1000000:
            score += 1
        if atr >= 10:
            score += 1
        if rel_volume >= 0.25:
            score += 1
        if volatility >= 0.025:
            score += 1
        if momentum >= 2.5:
            score += 1

        if score >= 3:
            day_trade_recommendation = True

        return {
            'volume': volume,
            'atr': atr,
            'relative_volume': rel_volume,
            'volatility': volatility,
            'momentum': momentum,
            'score': score,
            'recommendation': day_trade_recommendation
        }

    def print_summary(self):
        """Print a summary of all metrics and recommendations."""
        results = self.evaluate_daily_metrics()

        print("Average Daily Volume:", results['volume'])
        print("Average True Range (ATR):", results['atr'])
        print("Relative Volume (RVOL):", results['relative_volume'])
        print("Average Intraday Volatility (%):", results['volatility'])
        print("5-Day Price Momentum (%):", results['momentum'])
        print("Daily Rating Score:", results['score'])
        print("Daily Recommendation:", results['recommendation'])