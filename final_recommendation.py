class Recommendations:
    def day_trading_analysis(self, ticker_symbol):
        """
        Outputs a message indicating the ticker is suitable for day trading. criteria for later
        """
        print(
            f"Based on the analysis above the ticker {ticker_symbol} is suitable for day trading, due to its daily volatility. Please do so with caution")

    def swing_trading_analysis(self, ticker_symbol):
        """
        Outputs a message indicating the ticker is suitable for swing trading. - criteria for later
        """
        print(
            f"Based on the analysis above the ticker {ticker_symbol} is suitable for swing trading due to its volatility over a two week time period.")

    def backtest_summary(self, ticker_symbol):
        """
        Outputs a message summarizing the backtest results. - criteria for later
        """
        print(
            f"Backtesting complete for this run of {ticker_symbol}. The data seems reasonable. However, please evaluate on your own and remember market conditions are subject to change and volatility. Invest at your own risk.")