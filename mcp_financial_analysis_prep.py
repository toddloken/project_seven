import json
import os
import re
from dotenv import load_dotenv
import xml.etree.ElementTree as ET
from typing import Dict, List, Optional, Union, Any
from enum import Enum
from lxml import etree

class QueryType(Enum):
    RATIO_ANALYSIS = "ratio_analysis"
    TREND_ANALYSIS = "trend_analysis"
    COMPARATIVE_ANALYSIS = "comparative_analysis"
    CUSTOM_ANALYSIS = "custom_analysis"


class FinancialStatement(Enum):
    INCOME_STATEMENT = "income_statement"
    BALANCE_SHEET = "balance_sheet"
    CASH_FLOW = "cash_flow"


class FinancialMetric:
    """Class representing a financial metric with its value and metadata"""

    def __init__(
            self,
            name: str,
            value: Union[float, int],
            statement: FinancialStatement,
            year: str,
            symbol: str
    ):
        self.name = name
        self.value = value
        self.statement = statement
        self.year = year
        self.symbol = symbol

    def __str__(self):
        return f"{self.name}: {self.value} ({self.year})"


class FinancialAnalysisMCP:
    """
    Model Context Protocol implementation for financial analysis using Claude API
    """

    SYSTEM_PROMPT = """
    You are a financial analyst assistant that analyzes company financial statements.

    The user will provide financial data and analysis requests in XML format following this schema:

    <analysis>
        <type>{query_type}</type>
        <companies>
            <company>{company_symbol}</company>
            <!-- Additional companies for comparative analysis -->
        </companies>
        <metrics>
            <metric>{metric_name}</metric>
            <!-- Additional metrics to analyze -->
        </metrics>
        <timeframe>
            <start_year>{start_year}</start_year>
            <end_year>{end_year}</end_year>
        </timeframe>
        <custom_instructions>{custom_instructions}</custom_instructions>
    </analysis>

    You MUST respond using the following XML schema:

    <financial_analysis>
        <summary>
            <!-- High-level summary of the analysis -->
        </summary>
        <metrics>
            <metric>
                <name>{metric_name}</name>
                <values>
                    <value year="{year}" company="{company_symbol}">{value}</value>
                    <!-- Additional values for different years/companies -->
                </values>
                <insights>
                    <!-- Specific insights about this metric -->
                </insights>
            </metric>
            <!-- Additional metrics as requested -->
        </metrics>
        <trends>
            <!-- Overall trends identified in the data -->
        </trends>
        <recommendations>
            <!-- Actionable recommendations based on the analysis -->
        </recommendations>
    </financial_analysis>

    Always ensure your analysis is data-driven, clear, and actionable.
    """

    def __init__(self, data_dir: str = "data"):
        """Initialize with the directory containing financial statement JSON files"""
        load_dotenv()
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("API key not found. Please add ANTHROPIC_API_KEY to your .env file.")

        self.data_dir = data_dir
        self.income_statements = {}
        self.balance_sheets = {}
        self.cash_flows = {}
        self._load_financial_data()

    def _load_financial_data(self):
        """Load all financial data from JSON files in the 'data' subdirectory."""
        try:
            data_subdir = os.path.join(self.data_dir, "data")

            # Load income statements
            with open(os.path.join(data_subdir, "income_statement.json"), "r") as f:
                self.income_statements = json.load(f)

            # Load balance sheets
            with open(os.path.join(data_subdir, "balance_sheet_statement.json"), "r") as f:
                self.balance_sheets = json.load(f)

            # Load cash flow statements
            with open(os.path.join(data_subdir, "cash_flow_statement.json"), "r") as f:
                self.cash_flows = json.load(f)

        except FileNotFoundError as e:
            raise Exception(f"Financial data file not found: {e}")
        except json.JSONDecodeError as e:
            raise Exception(f"Error parsing financial data: {e}")

    def _get_statement_data(self, statement_type: FinancialStatement) -> List[Dict]:
        """Get data for a specific financial statement type"""
        if statement_type == FinancialStatement.INCOME_STATEMENT:
            return self.income_statements
        elif statement_type == FinancialStatement.BALANCE_SHEET:
            return self.balance_sheets
        elif statement_type == FinancialStatement.CASH_FLOW:
            return self.cash_flows
        else:
            raise ValueError(f"Unknown statement type: {statement_type}")

    def get_available_metrics(self, statement_type: FinancialStatement) -> List[str]:
        """Get a list of available metrics for a specific statement type"""
        data = self._get_statement_data(statement_type)
        if not data:
            return []

        # Get keys from the first entry, excluding metadata fields
        all_fields = data[0].keys()
        excluded_fields = [
            "date", "symbol", "reportedCurrency", "cik", "fillingDate",
            "acceptedDate", "calendarYear", "period", "link", "finalLink"
        ]
        return [field for field in all_fields if field not in excluded_fields]

    def get_metric_values(
            self,
            metric_name: str,
            symbol: str,
            start_year: str = None,
            end_year: str = None
    ) -> List[FinancialMetric]:
        """Get values for a specific metric across financial statements"""
        results = []

        # Determine which statement contains this metric
        for statement_type in FinancialStatement:
            data = self._get_statement_data(statement_type)

            # Filter by company symbol
            company_data = [entry for entry in data if entry.get("symbol") == symbol]

            for entry in company_data:
                if metric_name in entry:
                    # Filter by year range if specified
                    year = entry.get("calendarYear")
                    if start_year and year < start_year:
                        continue
                    if end_year and year > end_year:
                        continue

                    results.append(FinancialMetric(
                        name=metric_name,
                        value=entry[metric_name],
                        statement=statement_type,
                        year=year,
                        symbol=symbol
                    ))

        # Sort by year
        results.sort(key=lambda x: x.year)
        return results

    def create_analysis_prompt(
            self,
            query_type: QueryType,
            companies: List[str],
            metrics: List[str],
            start_year: str = None,
            end_year: str = None,
            custom_instructions: str = ""
    ) -> str:
        """Create an XML-formatted analysis request following the schema"""

        # Build the XML analysis request
        analysis_xml = f"""
        <analysis>
            <type>{query_type.value}</type>
            <companies>
                {"".join(f'<company>{company}</company>' for company in companies)}
            </companies>
            <metrics>
                {"".join(f'<metric>{metric}</metric>' for metric in metrics)}
            </metrics>
            <timeframe>
                <start_year>{start_year or ""}</start_year>
                <end_year>{end_year or ""}</end_year>
            </timeframe>
            <custom_instructions>{custom_instructions}</custom_instructions>
        </analysis>
        """

        # Combine with the financial data for context
        data_context = self._prepare_data_context(companies, metrics, start_year, end_year)

        # Create the complete prompt
        prompt = f"{self.SYSTEM_PROMPT}\n\nHere is the financial data for analysis:\n\n{data_context}\n\nAnalysis request:\n{analysis_xml}"

        return prompt

    def _prepare_data_context(
            self,
            companies: List[str],
            metrics: List[str],
            start_year: str = None,
            end_year: str = None
    ) -> str:
        """Prepare relevant financial data as context for the analysis"""

        data_context = "<financial_data>\n"

        # Add relevant data for each company and metric
        for company in companies:
            data_context += f"  <company symbol='{company}'>\n"

            for metric in metrics:
                metric_values = self.get_metric_values(metric, company, start_year, end_year)

                if metric_values:
                    data_context += f"    <metric name='{metric}'>\n"

                    for val in metric_values:
                        data_context += f"      <value year='{val.year}'>{val.value}</value>\n"

                    data_context += "    </metric>\n"

            data_context += "  </company>\n"

        data_context += "</financial_data>"

        return data_context

    def parse_analysis_response(self, response: str) -> Dict:
        """Parse the XML response from Claude into a structured format with improved error handling"""
        try:
            # Extract the XML portion using regex
            xml_pattern = r"<financial_analysis>(.*?)</financial_analysis>"
            match = re.search(xml_pattern, response, re.DOTALL)

            if not match:
                # If XML tags aren't found, try to parse the response as JSON or return a structured error
                try:
                    # Check if it's a JSON response
                    json_data = json.loads(response)
                    return self._convert_json_to_standard_format(json_data)
                except json.JSONDecodeError:
                    # If not JSON either, return a minimal valid structure with error info
                    return {
                        "summary": "Error: Could not parse response",
                        "metrics": [],
                        "trends": "No valid data found",
                        "recommendations": "Please check the API response format"
                    }

            # Get the full XML string
            full_xml = f"<financial_analysis>{match.group(1)}</financial_analysis>"

            # Pre-process the XML to fix common issues
            processed_xml = self._preprocess_xml(full_xml)

            try:
                # Try using the standard ElementTree parser first
                root = ET.fromstring(processed_xml)
            except ET.ParseError:
                # If standard parser fails, try using lxml with recovery mode
                try:
                    import lxml.etree as lxml_ET
                    parser = lxml_ET.XMLParser(recover=True)
                    root = lxml_ET.fromstring(processed_xml.encode('utf-8'), parser)
                except ImportError:
                    # If lxml isn't available, try a more aggressive cleanup
                    processed_xml = self._aggressive_xml_cleanup(processed_xml)
                    root = ET.fromstring(processed_xml)

            # Extract summary
            summary = root.find("summary").text.strip() if root.find("summary") is not None else ""

            # Extract metrics
            metrics = []
            for metric_elem in root.findall("metrics/metric"):
                metric = {
                    "name": metric_elem.find("name").text.strip() if metric_elem.find("name") is not None else "",
                    "values": [],
                    "insights": metric_elem.find("insights").text.strip() if metric_elem.find(
                        "insights") is not None else ""
                }

                for value_elem in metric_elem.findall("values/value"):
                    metric["values"].append({
                        "year": value_elem.get("year"),
                        "company": value_elem.get("company"),
                        "value": value_elem.text.strip() if value_elem.text else ""
                    })

                metrics.append(metric)

            # Extract trends
            trends = root.find("trends").text.strip() if root.find("trends") is not None else ""

            # Extract recommendations
            recommendations = root.find("recommendations").text.strip() if root.find(
                "recommendations") is not None else ""

            return {
                "summary": summary,
                "metrics": metrics,
                "trends": trends,
                "recommendations": recommendations
            }

        except Exception as e:
            # Log the error and include part of the problematic response
            error_snippet = response[:100] + "..." if len(response) > 100 else response
            print(f"Error parsing response: {e}")
            print(f"Response snippet: {error_snippet}")

            # Return a minimal valid structure rather than raising an exception
            return {
                "summary": f"Error parsing response: {e}",
                "metrics": [],
                "trends": "Error in parsing",
                "recommendations": "Please check the response format"
            }

    def _preprocess_xml(self, xml_str: str) -> str:
        """Pre-process XML to handle common issues"""
        # Replace problematic characters
        xml_str = xml_str.replace('&', '&amp;')

        # Fix unclosed tags (this is a simple approach and might need enhancement)
        open_tags = re.findall(r'<(\w+)[^/>]*>', xml_str)
        closed_tags = re.findall(r'</(\w+)>', xml_str)

        for tag in open_tags:
            if tag not in closed_tags:
                xml_str += f"</{tag}>"

        return xml_str

    def _aggressive_xml_cleanup(self, xml_str: str) -> str:
        """More aggressive XML cleanup for problematic responses"""
        # Remove any XML declaration
        xml_str = re.sub(r'<\?xml[^>]+\?>', '', xml_str)

        # Escape all special characters in text content
        xml_str = re.sub(r'(?<=>)([^<]+)(?=<)',
                         lambda m: m.group(1)
                         .replace('&', '&amp;')
                         .replace('<', '&lt;')
                         .replace('>', '&gt;')
                         .replace('"', '&quot;')
                         .replace("'", '&apos;'),
                         xml_str)

        return xml_str

    def _convert_json_to_standard_format(self, json_data: Dict) -> Dict:
        """Convert JSON response to the standard format expected by the application"""
        # Implement conversion logic based on your JSON structure
        # This is a placeholder - you'll need to adjust based on your actual JSON format
        return {
            "summary": json_data.get("summary", ""),
            "metrics": json_data.get("metrics", []),
            "trends": json_data.get("trends", ""),
            "recommendations": json_data.get("recommendations", "")
        }

    def ratio_analysis(
            self,
            company: str,
            metrics: List[str],
            start_year: str = None,
            end_year: str = None,
            custom_instructions: str = ""
    ) -> str:
        """Create a prompt for ratio analysis"""
        return self.create_analysis_prompt(
            query_type=QueryType.RATIO_ANALYSIS,
            companies=[company],
            metrics=metrics,
            start_year=start_year,
            end_year=end_year,
            custom_instructions=custom_instructions
        )

    def trend_analysis(
            self,
            company: str,
            metrics: List[str],
            start_year: str = None,
            end_year: str = None,
            custom_instructions: str = ""
    ) -> str:
        """Create a prompt for trend analysis"""
        return self.create_analysis_prompt(
            query_type=QueryType.TREND_ANALYSIS,
            companies=[company],
            metrics=metrics,
            start_year=start_year,
            end_year=end_year,
            custom_instructions=custom_instructions
        )

    def comparative_analysis(
            self,
            companies: List[str],
            metrics: List[str],
            start_year: str = None,
            end_year: str = None,
            custom_instructions: str = ""
    ) -> str:
        """Create a prompt for comparative analysis between companies"""
        return self.create_analysis_prompt(
            query_type=QueryType.COMPARATIVE_ANALYSIS,
            companies=companies,
            metrics=metrics,
            start_year=start_year,
            end_year=end_year,
            custom_instructions=custom_instructions
        )

    def custom_analysis(
            self,
            companies: List[str],
            metrics: List[str],
            custom_instructions: str,
            start_year: str = None,
            end_year: str = None
    ) -> str:
        """Create a prompt for custom analysis"""
        return self.create_analysis_prompt(
            query_type=QueryType.CUSTOM_ANALYSIS,
            companies=companies,
            metrics=metrics,
            start_year=start_year,
            end_year=end_year,
            custom_instructions=custom_instructions
        )