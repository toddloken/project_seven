from mcp_financial_analysis_orchestrator import FinancialAnalysisClient as financial_client

"""These are prompts used in the compilation of metrics for """

ration_analysis_prompt = financial_client.mcp.ratio_analysis(
    company="COMPANY_SYMBOL",
    metrics=[
        "revenue",
        "operatingExpenses",
        "operatingIncome"
    ],
    start_year="2020",
    end_year="2024",
    custom_instructions="""
    Evaluate the company's operational efficiency over time.
    Address:
    1. How well the company manages its operating expenses
    2. Changes in operational efficiency ratios
    3. Comparison to industry standards if available
    4. Areas for potential improvement
    """
)

liquity_analysis_prompt = financial_client.mcp.ratio_analysis(
    company="COMPANY_SYMBOL",
    metrics=[
        "cashAndCashEquivalents",
        "totalCurrentAssets",
        "totalCurrentLiabilities"
    ],
    start_year="2020",
    end_year="2024",
    custom_instructions="""
    Analyze the company's liquidity position.
    Focus on:
    1. The company's ability to meet short-term obligations
    2. Changes in the current ratio over time
    3. Cash reserves adequacy
    4. Liquidity risk assessment
    """
)

trend_analysis_prompt = financial_client.mcp.trend_analysis(
    company="COMPANY_SYMBOL",
    metrics=[
        "revenue",
        "grossProfit",
        "netIncome"
    ],
    start_year="2018",
    end_year="2024",
    custom_instructions="""
    Analyze the company's growth trajectory.
    Include:
    1. Compound annual growth rate (CAGR) for revenue
    2. Year-over-year growth percentages
    3. Relationship between revenue growth and profit growth
    4. Sustainability of the growth trend
    5. Potential growth catalysts or concerns
    """
)

balance_sheet_prompt = financial_client.mcp.trend_analysis(
    company="COMPANY_SYMBOL",
    metrics=[
        "totalAssets",
        "totalLiabilities",
        "totalStockholdersEquity",
        "goodwill"
    ],
    start_year="2018",
    end_year="2024",
    custom_instructions="""
    Examine how the company's financial position has evolved.
    Focus on:
    1. Asset growth and composition changes
    2. Liability management
    3. Changes in equity structure
    4. Role of acquisitions (reflected in goodwill)
    5. Overall financial strength trajectory
    """
)

cash_flow_prompt = financial_client.mcp.trend_analysis(
    company="COMPANY_SYMBOL",
    metrics=[
        "operatingCashFlow",
        "capitalExpenditure",
        "freeCashFlow"
    ],
    start_year="2018",
    end_year="2024",
    custom_instructions="""
    Analyze the company's cash flow trends.
    Address:
    1. Cash generation capability
    2. Capital allocation strategy
    3. Free cash flow growth and sustainability
    4. Relationship between operating income and operating cash flow
    5. Cash flow quality assessment
    """
)

peer_prompt = financial_client.mcp.comparative_analysis(
    companies=["COMPANY1", "COMPANY2", "COMPANY3"],
    metrics=[
        "revenue",
        "netIncomeRatio",
        "operatingIncomeRatio"
    ],
    start_year="2021",
    end_year="2024",
    custom_instructions="""
    Compare the performance of these companies within their industry.
    Include:
    1. Relative size and growth rates
    2. Profitability differences
    3. Operational efficiency comparison
    4. Ranking of companies by key metrics
    5. Identification of best practices or competitive advantages
    """
)

financial_health_prompt = financial_client.mcp.comparative_analysis(
    companies=["COMPANY1", "COMPANY2", "COMPANY3"],
    metrics=[
        "totalDebt",
        "cashAndCashEquivalents",
        "totalAssets",
        "totalLiabilities",
        "totalStockholdersEquity"
    ],
    start_year="2021",
    end_year="2024",
    custom_instructions="""
    Compare the financial health and stability of these companies.
    Focus on:
    1. Debt levels and debt management
    2. Liquidity positions
    3. Asset utilization
    4. Financial leverage
    5. Overall financial risk assessment
    """
)

capital_health_prompt = financial_client.mcp.comparative_analysis(
    companies=["COMPANY1", "COMPANY2", "COMPANY3"],
    metrics=[
        "freeCashFlow",
        "capitalExpenditure",
        "commonStockRepurchased",
        "dividendsPaid"
    ],
    start_year="2021",
    end_year="2024",
    custom_instructions="""
    Compare how these companies allocate capital.
    Address:
    1. Investment in growth (CapEx)
    2. Shareholder returns (dividends and buybacks)
    3. Capital allocation efficiency
    4. Sustainability of shareholder returns
    5. Value creation assessment
    """
)

debt_structure_prompt = financial_client.mcp.custom_analysis(
    companies=["COMPANY_SYMBOL"],
    metrics=[
        "shortTermDebt",
        "longTermDebt",
        "totalDebt",
        "netDebt",
        "cashAndCashEquivalents",
        "operatingCashFlow"
    ],
    custom_instructions="""
    Conduct a comprehensive debt structure analysis.
    Include:
    1. Debt maturity profile assessment
    2. Interest coverage ratio calculation
    3. Debt service capability evaluation
    4. Debt-to-EBITDA and other relevant ratios
    5. Overall debt risk assessment
    6. Recommendations for debt management
    """
)

payor_prompt = financial_client.mcp.custom_analysis(
    companies=["UNH"],  # UnitedHealth Group
    metrics=[
        "revenue",
        "operatingIncomeRatio",
        "netIncomeRatio",
        "cashAndCashEquivalents",
        "totalDebt"
    ],
    start_year="2020",
    end_year="2024",
    custom_instructions="""
    Conduct a healthcare-focused financial analysis.
    Address:
    1. Revenue growth dynamics in the healthcare sector
    2. Margin trends specific to the healthcare industry
    3. Cash reserves adequacy for regulatory compliance
    4. Debt levels relative to industry norms
    5. Impact of healthcare policy changes on financial performance
    6. Recommendations for financial strategy in the evolving healthcare landscape
    """
)