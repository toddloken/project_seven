import os
import requests
import json
from typing import Dict, List, Optional, Any
from mcp_financial_analysis_prep import FinancialAnalysisMCP, QueryType, FinancialStatement


class ClaudeAPIClient:
    """
    Client for interacting with Claude API using the Financial Analysis MCP
    """

    API_URL = "https://api.anthropic.com/v1/messages"

    def __init__(self, api_key: str, model: str = "claude-3-7-sonnet-20250219"):
        """Initialize the API client with authentication"""
        self.api_key = api_key
        self.model = model
        self.headers = {
            "Content-Type": "application/json",
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01"
        }

    def send_message(self, prompt: str, max_tokens: int = 4000) -> Dict[str, Any]:
        """Send a message to Claude API and return the response"""
        payload = {
            "model": self.model,
            "max_tokens": max_tokens,
            "messages": [{"role": "user", "content": prompt}]
        }

        try:
            response = requests.post(
                self.API_URL,
                headers=self.headers,
                json=payload
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"API request failed: {e}")

    def extract_content(self, response: Dict[str, Any]) -> str:
        """Extract the content from Claude's response"""
        try:
            return response["content"][0]["text"]
        except (KeyError, IndexError) as e:
            raise Exception(f"Failed to extract content from API response: {e}")


class FinancialAnalysisClient:
    """
    Client for performing financial analysis using Claude API with MCP
    """

    def __init__(self, api_key: str, data_dir: str = "./"):
        """Initialize with API key and data directory"""
        self.api_client = ClaudeAPIClient(api_key)
        self.mcp = FinancialAnalysisMCP(data_dir)

    def get_available_metrics(self) -> Dict[str, List[str]]:
        """Get all available metrics organized by statement type"""
        return {
            "income_statement": self.mcp.get_available_metrics(FinancialStatement.INCOME_STATEMENT),
            "balance_sheet": self.mcp.get_available_metrics(FinancialStatement.BALANCE_SHEET),
            "cash_flow": self.mcp.get_available_metrics(FinancialStatement.CASH_FLOW)
        }

    def perform_ratio_analysis(
            self,
            company: str,
            metrics: List[str],
            start_year: str = None,
            end_year: str = None,
            custom_instructions: str = ""
    ) -> Dict[str, Any]:
        """Perform financial ratio analysis for a company"""
        prompt = self.mcp.ratio_analysis(
            company=company,
            metrics=metrics,
            start_year=start_year,
            end_year=end_year,
            custom_instructions=custom_instructions
        )

        response = self.api_client.send_message(prompt)
        content = self.api_client.extract_content(response)
        return self.mcp.parse_analysis_response(content)

    def perform_trend_analysis(
            self,
            company: str,
            metrics: List[str],
            start_year: str = None,
            end_year: str = None,
            custom_instructions: str = ""
    ) -> Dict[str, Any]:
        """Perform trend analysis for financial metrics"""
        prompt = self.mcp.trend_analysis(
            company=company,
            metrics=metrics,
            start_year=start_year,
            end_year=end_year,
            custom_instructions=custom_instructions
        )

        response = self.api_client.send_message(prompt)
        content = self.api_client.extract_content(response)
        return self.mcp.parse_analysis_response(content)

    def perform_comparative_analysis(
            self,
            companies: List[str],
            metrics: List[str],
            start_year: str = None,
            end_year: str = None,
            custom_instructions: str = ""
    ) -> Dict[str, Any]:
        """Perform comparative analysis between companies"""
        prompt = self.mcp.comparative_analysis(
            companies=companies,
            metrics=metrics,
            start_year=start_year,
            end_year=end_year,
            custom_instructions=custom_instructions
        )

        response = self.api_client.send_message(prompt)
        content = self.api_client.extract_content(response)
        return self.mcp.parse_analysis_response(content)

    def perform_custom_analysis(
            self,
            companies: List[str],
            metrics: List[str],
            custom_instructions: str,
            start_year: str = None,
            end_year: str = None
    ) -> Dict[str, Any]:
        """Perform custom financial analysis"""
        prompt = self.mcp.custom_analysis(
            companies=companies,
            metrics=metrics,
            custom_instructions=custom_instructions,
            start_year=start_year,
            end_year=end_year
        )

        response = self.api_client.send_message(prompt)
        content = self.api_client.extract_content(response)
        return self.mcp.parse_analysis_response(content)