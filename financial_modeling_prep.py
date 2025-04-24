import os
import json
import ssl
import certifi
from urllib.request import urlopen
from dotenv import load_dotenv

class FinancialStatementsFetcher:
    BASE_URL = "https://financialmodelingprep.com/api/v3"

    def __init__(self, ticker):
        load_dotenv()
        self.ticker = ticker
        self.api_key = os.getenv("FMP_API_KEY")
        if not self.api_key:
            raise ValueError("API key not found. Please add FMP_API_KEY to your .env file.")

        self.context = ssl.create_default_context(cafile=certifi.where())

    def get_jsonparsed_data(self, endpoint):
        url = f"{self.BASE_URL}/{endpoint}/{self.ticker}?period=annual&apikey={self.api_key}"
        response = urlopen(url, context=self.context)
        data = response.read().decode("utf-8")
        return json.loads(data)

    def fetch_and_save(self):
        statements = {
            "income-statement": "income_statement.json",
            "balance-sheet-statement": "balance_sheet_statement.json",
            "cash-flow-statement": "cash_flow_statement.json"
        }

        # Ensure the 'data' subdirectory exists
        os.makedirs("data", exist_ok=True)

        for endpoint, filename in statements.items():
            data = self.get_jsonparsed_data(endpoint)
            filepath = os.path.join("data", filename)
            with open(filepath, "w") as f:
                json.dump(data, f, indent=4)
            print(f"Data saved to {filepath}")