import os
import requests
import pandas as pd
import json
from io import StringIO
from dotenv import load_dotenv


class AlphaVantage:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("ALPHA_VANTAGE_KEY")
        self.base_url = "https://www.alphavantage.co/query"

        if not self.api_key:
            raise ValueError("ALPHA_VANTAGE_KEY not found in environment variables")

    def get_weekly_time_series(self, symbol):
        url = f"{self.base_url}?function=TIME_SERIES_WEEKLY&symbol={symbol}&apikey={self.api_key}&datatype=csv"

        try:
            response = requests.get(url)
            response.raise_for_status()

            df = pd.read_csv(StringIO(response.text))
            return df

        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return None

    def get_insider_transactions(self, symbol):
        url = f"{self.base_url}?function=INSIDER_TRANSACTIONS&symbol={symbol}&apikey={self.api_key}"

        try:
            response = requests.get(url)
            response.raise_for_status()

            data = response.json()

            if 'data' not in data:
                print(f"Error: 'data' key not found in API response for {symbol}")
                return None

            df = pd.DataFrame(data['data'])

            if df.empty:
                print(f"No insider transactions found for {symbol}")
                return pd.DataFrame()


            df['shares'] = pd.to_numeric(df['shares'], errors='coerce')
            df['share_price'] = pd.to_numeric(df['share_price'], errors='coerce')


            df['transaction_date'] = pd.to_datetime(df['transaction_date'], errors='coerce')


            df = df.fillna({
                'shares': 0.0,
                'share_price': 0.0
            })


            date_na_count = df['transaction_date'].isna().sum()
            if date_na_count > 0:
                print(f"Warning: {date_na_count} invalid date entries found and set to NaT")

            return df

        except requests.exceptions.RequestException as e:
            print(f"Request error fetching data for {symbol}: {e}")
            return None
        except KeyError as e:
            print(f"Key error processing data for {symbol}: {e}")
            return None
        except ValueError as e:
            print(f"Value error processing data for {symbol}: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error processing data for {symbol}: {e}")
            return None

    def get_daily_time_series(self, symbol):
        url = f"{self.base_url}?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={self.api_key}&datatype=csv"

        try:
            response = requests.get(url)
            response.raise_for_status()

            df = pd.read_csv(StringIO(response.text))
            return df

        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return None

    def get_earnings_call_transcript(self, symbol, quarter):
        url = f"{self.base_url}?function=EARNINGS_CALL_TRANSCRIPT&symbol={symbol}&quarter={quarter}&apikey={self.api_key}"

        try:
            response = requests.get(url)
            response.raise_for_status()

            data = response.json()
            return data

        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return None
