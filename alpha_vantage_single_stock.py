from alpha_vantage import AlphaVantage
import json
import os


class AlphaVantageSingleStock:
    def __init__(self, ticker_symbol, data_dir='data'):
        """
        Initialize the class with a ticker symbol and optional data directory.
        """
        self.ticker_symbol = ticker_symbol
        self.av = AlphaVantage()
        self.data_dir = data_dir

        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

    def get_market_data(self):
        """Get and save various market data for the stock - saving to file now due to limit on API calls per day"""
        weekly_data = self.av.get_weekly_time_series(self.ticker_symbol)
        weekly_data.to_csv(f'{self.data_dir}/weekly_data.csv', index=False)

        daily_data = self.av.get_daily_time_series(self.ticker_symbol)
        daily_data.to_csv(f'{self.data_dir}/daily_data.csv', index=False)

        insider_data = self.av.get_insider_transactions(self.ticker_symbol)
        insider_data.to_csv(f'{self.data_dir}/insider_data.csv', index=False)

        return {
            'weekly_data': weekly_data,
            'daily_data': daily_data,
            'insider_data': insider_data
        }

    def get_earnings_transcripts(self, quarters):
        """
        Get and save earnings call transcripts for specified quarters.
        """
        results = {}

        for quarter in quarters:
            transcript_data = self.av.get_earnings_call_transcript(self.ticker_symbol, quarter)

            # Save to JSON file
            filename = f'{self.data_dir}/earnings_transcript_data_{quarter}.json'
            with open(filename, 'w') as f:
                json.dump(transcript_data, f, indent=4)

            # Store in results dictionary
            results[quarter] = transcript_data

        return results

    def get_all_data(self, quarters=None):
        """
        Get all available data (market data and transcripts)
        """
        if quarters is None:
            quarters = ["2025Q1", "2024Q4", "2024Q3", "2024Q2"]

        market_data = self.get_market_data()

        transcript_data = self.get_earnings_transcripts(quarters)

        return {
            'market_data': market_data,
            'transcript_data': transcript_data
        }


