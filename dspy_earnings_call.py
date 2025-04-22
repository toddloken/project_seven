# DSPy for Earnings Call Analysis
# ==============================

import dspy
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta

# Configure DSPy with your preferred LLM
# For OpenAI
openai_api_key = "YOUR_API_KEY_HERE"
llm = dspy.OpenAI(model="gpt-4", api_key=openai_api_key)
# Or for Anthropic
# anthropic_api_key = "YOUR_API_KEY_HERE"
# llm = dspy.Anthropic(model="claude-3-opus-20240229", api_key=anthropic_api_key)

# Set the default LM for DSPy
dspy.settings.configure(lm=llm)


# ===== PART 1: Define Signatures for Earnings Call Analysis =====

class EarningsCallExtraction(dspy.Signature):
    """Extract structured information from earnings call transcripts."""
    transcript = dspy.InputField(desc="The earnings call transcript text")

    financial_metrics = dspy.OutputField(desc="Key financial metrics mentioned (revenue, EPS, etc.)")
    guidance = dspy.OutputField(desc="Forward-looking guidance provided")
    challenges = dspy.OutputField(desc="Challenges or risks mentioned")
    opportunities = dspy.OutputField(desc="Growth opportunities discussed")
    management_tone = dspy.OutputField(desc="Assessment of management's tone (confident, cautious, etc.)")


class EarningsSentimentAnalysis(dspy.Signature):
    """Analyze the sentiment of an earnings call transcript."""
    transcript = dspy.InputField(desc="The earnings call transcript text")

    overall_sentiment = dspy.OutputField(desc="Overall sentiment score (-1 to 1)")
    sentiment_breakdown = dspy.OutputField(desc="Sentiment breakdown by segments (intro, results, guidance, Q&A)")
    key_positive_points = dspy.OutputField(desc="Key positive points mentioned")
    key_negative_points = dspy.OutputField(desc="Key negative points or concerns mentioned")
    confidence_signals = dspy.OutputField(desc="Signals of management confidence or uncertainty")


class EarningsStockImpact(dspy.Signature):
    """Predict the potential stock price impact based on earnings call analysis."""
    financial_metrics = dspy.InputField(desc="Extracted financial metrics")
    sentiment_analysis = dspy.InputField(desc="Sentiment analysis results")
    stock_context = dspy.InputField(desc="Recent stock performance and analyst expectations")

    price_impact = dspy.OutputField(desc="Predicted price impact (positive, negative, neutral)")
    impact_magnitude = dspy.OutputField(desc="Estimated magnitude of impact (significant, moderate, minimal)")
    key_drivers = dspy.OutputField(desc="Key drivers of the predicted stock reaction")
    time_horizon = dspy.OutputField(desc="Expected time horizon for the impact (immediate, short-term, long-term)")


# ===== PART 2: Implement DSPy Modules =====

# Using ChainOfThought for better reasoning
EarningsExtractor = dspy.ChainOfThought(EarningsCallExtraction)
SentimentAnalyzer = dspy.ChainOfThought(EarningsSentimentAnalysis)
ImpactPredictor = dspy.ChainOfThought(EarningsStockImpact)


# ===== PART 3: Multi-stage Earnings Call Analysis Pipeline =====

# Split the earnings call pipeline into separate components

class FinancialExtractorComponent(dspy.Module):
    """Component for extracting financial metrics from earnings call transcripts."""

    def __init__(self):
        super().__init__()
        self.extractor = EarningsExtractor()

    def forward(self, transcript):
        """Extract financial information from transcript."""
        extraction = self.extractor(transcript=transcript)
        return extraction


class SentimentAnalysisComponent(dspy.Module):
    """Component for analyzing sentiment in earnings call transcripts."""

    def __init__(self):
        super().__init__()
        self.analyzer = SentimentAnalyzer()

    def forward(self, transcript):
        """Analyze sentiment in the transcript."""
        sentiment = self.analyzer(transcript=transcript)
        return sentiment


class ImpactPredictionComponent(dspy.Module):
    """Component for predicting stock impact based on earnings analysis."""

    def __init__(self):
        super().__init__()
        self.predictor = ImpactPredictor()

    def forward(self, financial_metrics, sentiment_analysis, stock_context):
        """Predict stock impact based on earnings analysis."""
        formatted_sentiment = f"Overall: {sentiment_analysis.overall_sentiment}\nPositives: {sentiment_analysis.key_positive_points}\nNegatives: {sentiment_analysis.key_negative_points}"

        impact = self.predictor(
            financial_metrics=financial_metrics,
            sentiment_analysis=formatted_sentiment,
            stock_context=stock_context
        )
        return impact


class EarningsCallPipeline(dspy.Module):
    """Modular pipeline for analyzing earnings calls and predicting stock impact."""

    def __init__(self):
        super().__init__()
        self.financial_extractor = FinancialExtractorComponent()
        self.sentiment_analyzer = SentimentAnalysisComponent()
        self.impact_predictor = ImpactPredictionComponent()

    def forward(self, transcript, stock_context):
        """Run the full earnings call analysis pipeline."""

        # Extract financial information
        extraction = self.financial_extractor(transcript=transcript)

        # Analyze sentiment
        sentiment = self.sentiment_analyzer(transcript=transcript)

        # Predict stock impact
        impact = self.impact_predictor(
            financial_metrics=extraction.financial_metrics,
            sentiment_analysis=sentiment,
            stock_context=stock_context
        )

        return {
            "extraction": extraction,
            "sentiment": sentiment,
            "impact": impact
        }


# ===== PART 4: Optimizing with Real Examples =====

def prepare_training_examples():
    """Prepare training examples for optimizing the earnings call pipeline."""

    examples = []

    # Example 1: Positive earnings call
    example1 = dspy.Example(
        transcript="We're pleased to report record quarterly revenue of $90.1 billion, up 8% year over year, and quarterly earnings per diluted share of $1.29, up 4%...",
        financial_metrics="Revenue: $90.1 billion (up 8% YoY)\nEPS: $1.29 (up 4% YoY)",
        guidance="Expects continued revenue growth in next quarter\nGross margin expected to be 43%",
        challenges="Supply chain constraints mentioned\nForeign exchange headwinds",
        opportunities="Services segment growing rapidly\nExpanding in emerging markets",
        management_tone="Confident and optimistic"
    )
    examples.append(example1)

    # Add more examples as needed

    return examples


def optimize_earnings_extractor():
    """Optimize the earnings call extractor using example data."""

    # Get training examples
    examples = prepare_training_examples()

    # Define evaluation metric
    def metric(example, prediction):
        # Simple metric based on content overlap
        score = 0
        if len(prediction.financial_metrics) > 20:
            score += 0.25
        if len(prediction.guidance) > 20:
            score += 0.25
        if len(prediction.challenges) > 10:
            score += 0.25
        if len(prediction.opportunities) > 10:
            score += 0.25
        return score

    # Use an optimizer (BootstrapFewShot is a simple approach)
    optimizer = dspy.BootstrapFewShot(metric=metric)

    # Compile the optimized module
    optimized_extractor = optimizer.compile(
        EarningsExtractor,
        trainset=examples
    )

    return optimized_extractor


# ===== PART 5: Using the Pipeline with Real Data =====

def analyze_real_earnings_call(ticker, transcript_text=None):
    """Analyze a real earnings call for a given ticker."""

    # If no transcript is provided, you would typically fetch it from a source
    if transcript_text is None:
        # This is a placeholder - in a real application, you would fetch the transcript
        transcript_text = f"This is a placeholder for {ticker}'s earnings call transcript."

    # Get stock context using yfinance
    stock = yf.Ticker(ticker)

    # Get recent stock performance
    history = stock.history(period="60d")
    recent_change = ((history['Close'].iloc[-1] / history['Close'].iloc[-20]) - 1) * 100

    # Get analyst recommendations if available
    try:
        recommendations = stock.recommendations
        recent_recommendations = recommendations.iloc[-5:] if len(recommendations) > 0 else "No recent recommendations"
    except:
        recent_recommendations = "Unable to fetch recommendations"

    # Format stock context
    stock_context = f"""
    Ticker: {ticker}
    Recent stock performance: {recent_change:.2f}% in last 20 trading days
    Current price: ${history['Close'].iloc[-1]:.2f}
    Recent analyst recommendations: {recent_recommendations}
    """

    # Create and run the pipeline
    pipeline = EarningsCallPipeline()
    results = pipeline(transcript=transcript_text, stock_context=stock_context)

    return results


# ===== PART 6: Visualizing Results =====

def visualize_earnings_impact(ticker, earnings_date, results, days_before=30, days_after=30):
    """Visualize stock price movement around earnings date with analysis."""

    # Get stock data around earnings date
    if isinstance(earnings_date, str):
        earnings_date = datetime.strptime(earnings_date, '%Y-%m-%d')

    start_date = earnings_date - timedelta(days=days_before)
    end_date = earnings_date + timedelta(days=days_after)

    # Get stock data
    stock = yf.Ticker(ticker)
    df = stock.history(start=start_date, end=end_date)

    # Reset index for plotting
    df = df.reset_index()
    df['Date'] = pd.to_datetime(df['Date'])

    # Plot stock price
    plt.figure(figsize=(14, 8))

    # Plot price
    plt.subplot(2, 1, 1)
    plt.plot(df['Date'], df['Close'], label='Close Price')
    plt.axvline(x=earnings_date, color='r', linestyle='--', label='Earnings Date')
    plt.title(f'{ticker} Stock Price Around Earnings Call')
    plt.legend()

    # Plot volume
    plt.subplot(2, 1, 2)
    plt.bar(df['Date'], df['Volume'], alpha=0.5, label='Volume')
    plt.axvline(x=earnings_date, color='r', linestyle='--', label='Earnings Date')
    plt.title(f'{ticker} Trading Volume Around Earnings Call')
    plt.legend()

    plt.tight_layout()

    # Add annotation with analysis results
    plt.figtext(0.5, 0.01,
                f"Impact Analysis: {results['impact'].price_impact} ({results['impact'].impact_magnitude})\n" +
                f"Key Drivers: {results['impact'].key_drivers}\n" +
                f"Sentiment: {results['sentiment'].overall_sentiment}",
                ha="center", fontsize=10, bbox={"facecolor": "orange", "alpha": 0.2, "pad": 5})

    plt.show()


# ===== PART 7: Creating a Comparative Analysis Across Multiple Earnings Calls =====

def compare_earnings_calls(ticker, num_quarters=4):
    """Compare earnings calls across multiple quarters for trend analysis."""

    # This function would:
    # 1. Fetch multiple earnings call transcripts
    # 2. Analyze each using the pipeline
    # 3. Compare results to identify trends
    # 4. Visualize changes in key metrics and sentiment over time

    # For demonstration purposes, we'll simulate this with placeholder data
    results_over_time = []

    for i in range(num_quarters):
        quarter = f"Q{i + 1} 2022"  # Just example quarters

        # Simulate results for this quarter
        simulated_results = {
            "quarter": quarter,
            "extraction": {
                "financial_metrics": f"Revenue: ${85 + i * 5} billion",
                "guidance": f"Projected growth: {5 + i * 0.5}%"
            },
            "sentiment": {
                "overall_sentiment": 0.3 + (i * 0.1)  # Increasing sentiment
            },
            "impact": {
                "price_impact": "positive" if i % 2 == 0 else "neutral"
            }
        }

        results_over_time.append(simulated_results)

    # In a real implementation, you would fetch actual transcripts and analyze them

    return results_over_time


# ===== PART 8: Refining with Few-Shot Examples =====

def create_few_shot_examples():
    """Create examples for few-shot learning to improve earnings impact predictions."""

    examples = []

    # Example 1: Beat and raise scenario
    examples.append(dspy.Example(
        financial_metrics="Revenue: $15.3B (beat by $1.2B)\nEPS: $2.35 (beat by $0.40)",
        sentiment_analysis="Overall: 0.8 (very positive)\nPositives: Strong product demand, margin expansion, market share gains\nNegatives: Minor supply chain issues mentioned",
        stock_context="Stock up 5% YTD, analyst consensus was lower than actual results, high trading volume before earnings",
        price_impact="Positive",
        impact_magnitude="Significant",
        key_drivers="Beat on both top and bottom line, raised forward guidance, positive commentary on new product lines",
        time_horizon="Immediate positive reaction expected, with sustained momentum"
    ))

    # Example 2: Met expectations but weak guidance
    examples.append(dspy.Example(
        financial_metrics="Revenue: $8.7B (in-line)\nEPS: $1.75 (beat by $0.05)",
        sentiment_analysis="Overall: 0.1 (slightly positive)\nPositives: Cost-cutting measures working, cash flow improved\nNegatives: Cautious language about next quarter, mentioned competitive pressures",
        stock_context="Stock up 15% YTD, high expectations built in, analyst estimates recently raised",
        price_impact="Negative",
        impact_magnitude="Moderate",
        key_drivers="Met current quarter expectations but issued below-consensus guidance, management tone cautious",
        time_horizon="Initial negative reaction, reassessment after next earnings indicators"
    ))

    # Add more examples to cover different scenarios

    return examples


def optimize_impact_predictor():
    """Optimize the impact predictor using few-shot examples."""

    examples = create_few_shot_examples()

    # Define metric
    def accuracy_metric(example, prediction):
        # Check if impact direction matches
        direction_correct = example.price_impact.lower() == prediction.price_impact.lower()
        # Check if magnitude is reasonable
        magnitude_correct = example.impact_magnitude.lower() == prediction.impact_magnitude.lower()

        score = 0
        if direction_correct:
            score += 0.6
        if magnitude_correct:
            score += 0.4

        return score

    # Use the FewShot optimizer
    optimizer = dspy.FewShot(metric=accuracy_metric)

    # Compile the optimized module
    optimized_predictor = optimizer.compile(
        ImpactPredictor,
        trainset=examples
    )

    return optimized_predictor


# ===== PART 9: Complete Example Workflow =====

def process_earnings_call_example():
    """Complete example workflow for analyzing an earnings call and its impact."""

    # 1. Select a company to analyze
    ticker = "AAPL"

    # 2. Define a sample earnings call transcript (in practice, you would fetch this)
    transcript = """
    Good afternoon, and welcome to Apple's fiscal year 2023 first quarter earnings conference call. 

    I'm pleased to report Apple's revenue for the December quarter was $117.2 billion, down 5% year over year. 
    However, on a constant currency basis, we grew year over year, and would have grown in the vast majority of the markets we track.

    We set an all-time revenue record of $20.8 billion in our Services category. Our installed base of active devices has now surpassed 2 billion, with double-digit growth in several emerging markets. Despite the challenging macroeconomic environment, we continue to invest significantly in our long-term growth plans.

    While iPhone revenue declined by 8%, this was largely due to supply constraints and foreign exchange headwinds. Mac revenue was down 29%, primarily due to challenging comparisons to last year's launch of M1 MacBooks and ongoing supply chain issues.

    Looking ahead to the March quarter, we expect revenue to be similar to last year, with some improvement in foreign exchange impact. We expect Services to continue strong double-digit growth. Gross margins should be between 43% and 44%.

    We remain committed to our product innovation roadmap and are excited about the opportunities ahead, particularly in artificial intelligence and augmented reality.

    With that, I'll turn it over to the operator for questions.
    """

    # 3. Define recent stock context
    earnings_date = "2023-02-02"  # Date of the earnings call
    stock_context = """
    Ticker: AAPL
    Recent stock performance: -2.5% in last 20 trading days
    Current price: $150.82
    Market cap: $2.39T
    Average analyst target: $170
    Recent analyst recommendations: 25 Buy, 5 Hold, 1 Sell
    Expected EPS: $1.94
    Expected Revenue: $121.1B
    """

    # 4. Create the earnings pipeline
    pipeline = EarningsCallPipeline()

    # 5. Run the full analysis
    results = pipeline(transcript=transcript, stock_context=stock_context)

    # 6. Display results
    print("\n===== EARNINGS CALL ANALYSIS RESULTS =====")
    print("\nKEY FINANCIAL METRICS:")
    print(results["extraction"].financial_metrics)

    print("\nFORWARD GUIDANCE:")
    print(results["extraction"].guidance)

    print("\nCHALLENGES IDENTIFIED:")
    print(results["extraction"].challenges)

    print("\nOPPORTUNITIES IDENTIFIED:")
    print(results["extraction"].opportunities)

    print("\nMANAGEMENT TONE:")
    print(results["extraction"].management_tone)

    print("\nSENTIMENT ANALYSIS:")
    print(f"Overall sentiment: {results['sentiment'].overall_sentiment}")
    print(f"Key positive points: {results['sentiment'].key_positive_points}")
    print(f"Key negative points: {results['sentiment'].key_negative_points}")

    print("\nPREDICTED STOCK IMPACT:")
    print(f"Price impact: {results['impact'].price_impact}")
    print(f"Impact magnitude: {results['impact'].impact_magnitude}")
    print(f"Key drivers: {results['impact'].key_drivers}")
    print(f"Time horizon: {results['impact'].time_horizon}")

    # 7. Visualize stock impact
    visualize_earnings_impact(ticker, earnings_date, results)

    return results


# ===== PART 10: Building a Comparative Analysis Dashboard =====

def create_earnings_performance_tracker(ticker, num_quarters=6):
    """Create a historical tracker of earnings performance and sentiment."""

    # In a real application, you would:
    # 1. Fetch actual earnings call dates
    # 2. Get transcripts for each date
    # 3. Run the analysis pipeline on each transcript
    # 4. Create a consolidated view of performance over time

    # For this example, we'll create simulated data
    quarters = []
    revenue = []
    eps = []
    sentiment = []
    stock_impact = []  # % change 1 day after earnings

    # Simulated data for demonstration
    base_revenue = 90.0  # in billions
    base_eps = 1.20

    for i in range(num_quarters):
        # Quarter label
        quarter_num = (i % 4) + 1
        year = 2022 + (i // 4)
        quarters.append(f"Q{quarter_num} {year}")

        # Revenue with some variation
        rev_growth = np.random.uniform(-0.05, 0.08)  # -5% to +8%
        curr_revenue = base_revenue * (1 + rev_growth)
        revenue.append(curr_revenue)
        base_revenue = curr_revenue  # For next quarter

        # EPS with some variation
        eps_growth = np.random.uniform(-0.07, 0.10)  # -7% to +10%
        curr_eps = base_eps * (1 + eps_growth)
        eps.append(curr_eps)
        base_eps = curr_eps  # For next quarter

        # Sentiment - partly correlated with revenue growth
        curr_sentiment = 0.3 + (rev_growth * 2) + np.random.uniform(-0.2, 0.2)
        # Bound between -1 and 1
        curr_sentiment = max(-1, min(1, curr_sentiment))
        sentiment.append(curr_sentiment)

        # Stock impact - correlated with both revenue surprise and sentiment
        impact = rev_growth * 10 + eps_growth * 15 + curr_sentiment * 5 + np.random.uniform(-3, 3)
        stock_impact.append(impact)

    # Create a DataFrame for visualization
    df = pd.DataFrame({
        'Quarter': quarters,
        'Revenue (B)': revenue,
        'EPS': eps,
        'Sentiment': sentiment,
        'Stock Impact (%)': stock_impact
    })

    # Plot the results
    plt.figure(figsize=(15, 10))

    # Revenue subplot
    plt.subplot(2, 2, 1)
    plt.plot(df['Quarter'], df['Revenue (B)'], marker='o', linestyle='-', color='blue')
    plt.title(f'{ticker} Quarterly Revenue')
    plt.ylabel('Revenue (Billions $)')
    plt.xticks(rotation=45)
    plt.grid(True, alpha=0.3)

    # EPS subplot
    plt.subplot(2, 2, 2)
    plt.plot(df['Quarter'], df['EPS'], marker='o', linestyle='-', color='green')
    plt.title(f'{ticker} Earnings Per Share')
    plt.ylabel('EPS ($)')
    plt.xticks(rotation=45)
    plt.grid(True, alpha=0.3)

    # Sentiment subplot
    plt.subplot(2, 2, 3)
    bars = plt.bar(df['Quarter'], df['Sentiment'], color=[
        'green' if x > 0.3 else 'blue' if x > 0 else 'orange' if x > -0.3 else 'red'
        for x in df['Sentiment']
    ])
    plt.title(f'{ticker} Earnings Call Sentiment')
    plt.ylabel('Sentiment Score (-1 to 1)')
    plt.xticks(rotation=45)
    plt.grid(True, alpha=0.3)

    # Stock impact subplot
    plt.subplot(2, 2, 4)
    bars = plt.bar(df['Quarter'], df['Stock Impact (%)'], color=[
        'green' if x > 0 else 'red' for x in df['Stock Impact (%)']
    ])
    plt.title(f'{ticker} Post-Earnings Stock Impact')
    plt.ylabel('1-Day % Change')
    plt.xticks(rotation=45)
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.suptitle(f'{ticker} Earnings Performance Tracker', fontsize=16, y=1.02)
    plt.subplots_adjust(top=0.9)

    plt.show()

    return df


# ===== PART 11: Integrating with Other Financial Data =====

def integrate_with_technical_analysis(ticker, earnings_date, earnings_results):
    """Integrate earnings call analysis with technical analysis for a comprehensive view."""

    # Convert date string to datetime if needed
    if isinstance(earnings_date, str):
        earnings_date = datetime.strptime(earnings_date, '%Y-%m-%d')

    # Get data around earnings date
    start_date = earnings_date - timedelta(days=60)
    end_date = earnings_date + timedelta(days=30)

    # Fetch stock data
    stock = yf.Ticker(ticker)
    history = stock.history(start=start_date, end=end_date)

    # Calculate technical indicators
    # 1. Moving Averages
    history['MA20'] = history['Close'].rolling(window=20).mean()
    history['MA50'] = history['Close'].rolling(window=50).mean()

    # 2. Relative Strength Index (RSI)
    delta = history['Close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()
    rs = avg_gain / avg_loss
    history['RSI'] = 100 - (100 / (1 + rs))

    # 3. MACD
    history['EMA12'] = history['Close'].ewm(span=12, adjust=False).mean()
    history['EMA26'] = history['Close'].ewm(span=26, adjust=False).mean()
    history['MACD'] = history['EMA12'] - history['EMA26']
    history['Signal'] = history['MACD'].ewm(span=9, adjust=False).mean()

    # Create visualization with both earnings and technical analysis
    plt.figure(figsize=(15, 12))

    # Plot price and MAs
    plt.subplot(3, 1, 1)
    plt.plot(history.index, history['Close'], label='Close Price')
    plt.plot(history.index, history['MA20'], label='20-Day MA', alpha=0.7)
    plt.plot(history.index, history['MA50'], label='50-Day MA', alpha=0.7)
    plt.axvline(x=earnings_date, color='r', linestyle='--', label='Earnings Date')
    plt.title(f'{ticker} Price with Earnings Call Impact')
    plt.ylabel('Price ($)')
    plt.legend()
    plt.grid(True, alpha=0.3)

    # Add annotation with earnings analysis
    earnings_idx = history.index[history.index >= earnings_date][0]
    plt.annotate(
        f"Earnings: {earnings_results['impact'].price_impact}",
        xy=(earnings_idx, history.loc[earnings_idx, 'Close']),
        xytext=(30, 30),
        textcoords='offset points',
        arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=.2')
    )

    # Plot RSI
    plt.subplot(3, 1, 2)
    plt.plot(history.index, history['RSI'], color='purple')
    plt.axhline(y=70, color='r', linestyle='--', alpha=0.5)
    plt.axhline(y=30, color='g', linestyle='--', alpha=0.5)
    plt.axvline(x=earnings_date, color='r', linestyle='--')
    plt.title(f'{ticker} RSI')
    plt.ylabel('RSI')
    plt.grid(True, alpha=0.3)

    # Plot MACD
    plt.subplot(3, 1, 3)
    plt.plot(history.index, history['MACD'], label='MACD', color='blue')
    plt.plot(history.index, history['Signal'], label='Signal Line', color='red')
    plt.bar(history.index, history['MACD'] - history['Signal'], color=[
        'green' if x > 0 else 'red' for x in (history['MACD'] - history['Signal'])
    ], alpha=0.5)
    plt.axvline(x=earnings_date, color='r', linestyle='--')
    plt.title(f'{ticker} MACD')
    plt.ylabel('MACD')
    plt.legend()
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()

    # Return the enhanced technical analysis data
    return history

#
# # Run the complete example
# if __name__ == "__main__":
#     print("Running earnings call analysis example...")
#
#     # Process a single earnings call
#     results = process_earnings_call_example()
#
#     # Show historical earnings performance
#     earnings_df = create_earnings_performance_tracker("AAPL")
#
#     # Integrate with technical analysis
#     tech_analysis = integrate_with_technical_analysis("AAPL", "2023-02-02", results)
#
#     print("Analysis complete!")