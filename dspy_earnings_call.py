import dspy
from dspy_config import DSPyConfigurator


class SafeGetter:
    @staticmethod
    def safe_get(obj, *keys, default="N/A"):
        try:
            for key in keys:
                obj = getattr(obj, key) if not isinstance(obj, dict) else obj[key]
            return obj
        except (KeyError, AttributeError, TypeError):
            return default


# Define a simple DSPy signature
class EarningsInsightSignature(dspy.Signature):
    """Extract insights from an earnings call transcript."""
    transcript = dspy.InputField(desc="Full earnings call transcript")
    revenue = dspy.OutputField(desc="Revenue figures mentioned")
    guidance = dspy.OutputField(desc="Future guidance provided")
    volatility = dspy.OutputField(desc="Market Volatility (volatile/stable)")
    sentiment = dspy.OutputField(desc="Overall sentiment (positive/neutral/negative)")


class EarningsCallProcessor(dspy.Module):
    def __init__(self):
        super().__init__()
        # Configure the language model
        configurator = DSPyConfigurator()
        configurator.configure()

        # Initialize Chain of Thought models
        self.extractor = dspy.ChainOfThought(EarningsCallExtraction)
        self.sentiment_analyzer = dspy.ChainOfThought(EarningsSentimentAnalysis)
        self.impact_predictor = dspy.ChainOfThought(EarningsStockImpact)

    def forward(self, transcript, stock_context):
        # Step 1: Extract structured info from transcript
        extracted = self.extractor(transcript=transcript)

        # Step 2: Perform sentiment analysis on transcript
        sentiment = self.sentiment_analyzer(transcript=transcript)

        # Step 3: Predict stock impact using extracted + sentiment + external context
        impact = self.impact_predictor(
            financial_metrics=extracted.financial_metrics,
            sentiment_analysis=sentiment,
            stock_context=stock_context
        )

        # Combine and return results
        return {
            "extraction": extracted,
            "sentiment": sentiment,
            "impact": impact
        }

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


class FinancialExtractorComponent(dspy.Module):
    """Component for extracting financial metrics from earnings call transcripts."""

    def __init__(self):
        super().__init__()
        self.extractor = dspy.ChainOfThought(EarningsCallExtraction)

    def forward(self, transcript):
        """Extract financial information from transcript."""
        extraction = self.extractor(transcript=transcript)
        return extraction
#
#
# class SentimentAnalysisComponent(dspy.Module):
#     """Component for analyzing sentiment in earnings call transcripts."""
#
#     def __init__(self):
#         super().__init__()
#         self.analyzer = SentimentAnalyzer()
#
#     def forward(self, transcript):
#         """Analyze sentiment in the transcript."""
#         sentiment = self.analyzer(transcript=transcript)
#         return sentiment
#
# class ImpactPredictionComponent(dspy.Module):
#         """Component for predicting stock impact based on earnings analysis."""
#
#         def __init__(self):
#             super().__init__()
#             self.predictor = ImpactPredictor()
#
#         def forward(self, financial_metrics, sentiment_analysis, stock_context):
#             """Predict stock impact based on earnings analysis."""
#             formatted_sentiment = f"Overall: {sentiment_analysis.overall_sentiment}\nPositives: {sentiment_analysis.key_positive_points}\nNegatives: {sentiment_analysis.key_negative_points}"
#
#             impact = self.predictor(
#                 financial_metrics=financial_metrics,
#                 sentiment_analysis=formatted_sentiment,
#                 stock_context=stock_context
#             )
#             return impact
#
#
# class ImpactPredictionComponent(dspy.Module):
#     """Component for predicting stock impact based on earnings analysis."""
#
#     def __init__(self):
#         super().__init__()
#         self.predictor = ImpactPredictor()
#
#     def forward(self, financial_metrics, sentiment_analysis, stock_context):
#         """Predict stock impact based on earnings analysis."""
#         formatted_sentiment = f"Overall: {sentiment_analysis.overall_sentiment}\nPositives: {sentiment_analysis.key_positive_points}\nNegatives: {sentiment_analysis.key_negative_points}"
#
#         impact = self.predictor(
#             financial_metrics=financial_metrics,
#             sentiment_analysis=formatted_sentiment,
#             stock_context=stock_context
#         )
#         return impact
#
#     class EarningsCallPipeline(dspy.Module):
#         """Modular pipeline for analyzing earnings calls and predicting stock impact."""
#
#         def __init__(self):
#             super().__init__()
#             self.financial_extractor = FinancialExtractorComponent()
#             self.sentiment_analyzer = SentimentAnalysisComponent()
#             self.impact_predictor = ImpactPredictionComponent()
#
#         def forward(self, transcript, stock_context):
#             """Run the full earnings call analysis pipeline."""
#
#             # Extract financial information
#             extraction = self.financial_extractor(transcript=transcript)
#
#             # Analyze sentiment
#             sentiment = self.sentiment_analyzer(transcript=transcript)
#
#             # Predict stock impact
#             impact = self.impact_predictor(
#                 financial_metrics=extraction.financial_metrics,
#                 sentiment_analysis=sentiment,
#                 stock_context=stock_context
#             )
#
#             return {
#                 "extraction": extraction,
#                 "sentiment": sentiment,
#                 "impact": impact
#             }