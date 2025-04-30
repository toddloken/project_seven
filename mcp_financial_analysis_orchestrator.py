import os
import json
from pprint import pprint
from mcp_financial_analysis_prep import FinancialAnalysisMCP, QueryType, FinancialStatement
from mcp_financial_client_claude import FinancialAnalysisClient


class FinancialAnalysisRunner:
    def __init__(self, api_key=None, data_dir="./"):
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY", "your_api_key_here")
        self.data_dir = data_dir
        self.client = FinancialAnalysisClient(self.api_key, self.data_dir)

    def show_available_metrics(self):
        print("Available Financial Metrics:")
        metrics = self.client.get_available_metrics()
        print("\nIncome Statement Metrics:")
        print(", ".join(metrics["income_statement"][:5]) + "...")
        print("\nBalance Sheet Metrics:")
        print(", ".join(metrics["balance_sheet"][:5]) + "...")
        print("\nCash Flow Metrics:")
        print(", ".join(metrics["cash_flow"][:5]) + "...")
        return metrics

    def run_ratio_analysis(self):
        print("\n\n=== RATIO ANALYSIS EXAMPLE ===")
        result = self.client.perform_ratio_analysis(
            company="UNH",
            metrics=["grossProfitRatio", "operatingIncomeRatio", "netIncomeRatio"],
            start_year="2021",
            end_year="2024",
            custom_instructions="Focus on profitability trends and what they indicate about the company's operational efficiency."
        )
        pprint(result)
        return result

    def run_trend_analysis(self):
        print("\n\n=== TREND ANALYSIS EXAMPLE ===")
        result = self.client.perform_trend_analysis(
            company="UNH",
            metrics=["revenue", "netIncome"],
            start_year="2020",
            end_year="2024",
            custom_instructions="Evaluate the company's growth trajectory and highlight any significant changes year-over-year."
        )
        pprint(result)
        return result

    def run_comparative_analysis(self):
        print("\n\n=== COMPARATIVE ANALYSIS EXAMPLE ===")
        result = self.client.perform_comparative_analysis(
            companies=["UNH", "AAPL"],
            metrics=["netIncomeRatio", "totalAssets"],
            start_year="2021",
            end_year="2023",
            custom_instructions="Compare financial performance and efficiency across these companies."
        )
        pprint(result)
        return result

    def run_custom_analysis(self):
        print("\n\n=== CUSTOM ANALYSIS EXAMPLE ===")
        result = self.client.perform_custom_analysis(
            companies=["UNH"],
            metrics=["cashAndCashEquivalents", "totalDebt", "netDebt"],
            custom_instructions="Analyze the debt situation and liquidity position. Calculate the debt-to-cash ratio and evaluate if the company has sufficient liquidity to cover short-term obligations.",
            start_year="2020",
            end_year="2024"
        )
        pprint(result)
        return result
