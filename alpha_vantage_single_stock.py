from alpha_vantage import AlphaVantage
import json
import os


class AlphaVantageSingleStock:
    def __init__(self, ticker_symbol, data_dir='data'):
        """
        Initialize the class with a ticker symbol and optional data directory.

        Args:
            ticker_symbol (str): The stock ticker symbol (e.g., 'UNH')
            data_dir (str): Directory to save data files (defaults to 'data')
        """
        self.ticker_symbol = ticker_symbol
        self.av = AlphaVantage()
        self.data_dir = data_dir

        # Create data directory if it doesn't exist
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

    def get_market_data(self):
        """Get and save various market data for the stock"""
        # Get and save weekly data
        weekly_data = self.av.get_weekly_time_series(self.ticker_symbol)
        weekly_data.to_csv(f'{self.data_dir}/weekly_data.csv', index=False)

        # Get and save daily data
        daily_data = self.av.get_daily_time_series(self.ticker_symbol)
        daily_data.to_csv(f'{self.data_dir}/daily_data.csv', index=False)

        # Get and save insider transactions
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

        Args:
            quarters (list): List of quarter codes (e.g., ['2025Q1', '2024Q4'])

        Returns:
            dict: Dictionary with quarter codes as keys and transcript data as values
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
        Get all available data (market data and transcripts).

        Args:
            quarters (list): Optional list of quarters for transcripts.
                            Defaults to current quarter and three previous quarters.

        Returns:
            dict: Dictionary containing all retrieved data
        """
        # Set default quarters if not provided
        if quarters is None:
            # This is just an example - in production you might want to calculate these dynamically
            quarters = ["2025Q1", "2024Q4", "2024Q3", "2024Q2"]

        # Get market data
        market_data = self.get_market_data()

        # Get transcript data
        transcript_data = self.get_earnings_transcripts(quarters)

        return {
            'market_data': market_data,
            'transcript_data': transcript_data
        }


# Example usage:
if __name__ == "__main__":
    # Create an instance for UNH stock
    unh_stock = AlphaVantageSingleStock("UNH")

    # Get all data with default quarters
    all_data = unh_stock.get_all_data()

    # Or specify particular quarters
    custom_quarters = ["2025Q1", "2024Q4"]
    transcript_data = unh_stock.get_earnings_transcripts(custom_quarters)