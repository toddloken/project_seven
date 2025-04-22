from alpha_vantage_single_stock import AlphaVantageSingleStock
from earnings_transcript_extractor import TranscriptExtractor
from dspy_earnings_call import EarningsCallProcessor, SafeGetter, FinancialExtractorComponent

# ======================================================
# get single stock
# stock_ticker = "UNH"
# stock = AlphaVantageSingleStock(stock_ticker)
# all_data = stock.get_all_data()
# ======================================================
extractor = TranscriptExtractor("data/earnings_transcript_data_current_quarter.json", debug=True)
transcript = extractor.process()
print(transcript)
# ======================================================
# Get Objects from dspy_earnings
call_processor = EarningsCallProcessor()
financial_extractor = FinancialExtractorComponent()

#variable set-up
stock_context = {
    "recent_performance": "The stock has been volatile, down 2% over the last 5 days.",
    "analyst_expectations": "Analysts expected steady EPS growth and flat revenue."
}
#get stuff
call_results = call_processor(transcript=transcript, stock_context=stock_context)

revenue = SafeGetter.safe_get(call_results, "extraction", "financial_metrics")
guidance = SafeGetter.safe_get(call_results, "extraction", "guidance")
sentiment = SafeGetter.safe_get(call_results, "sentiment", "overall_sentiment")
volatility = SafeGetter.safe_get(call_results, "impact", "impact_magnitude")

financial_results = financial_extractor(transcript)

financial_metrics = SafeGetter.safe_get(financial_results, "financial_metrics")
challenges = SafeGetter.safe_get(financial_results, "challenges")
opportunities = SafeGetter.safe_get(financial_results, "opportunities")
management_tone = SafeGetter.safe_get(financial_results, "management_tone")

#print for now
print("Revenue:", revenue)
print("Guidance:", guidance)
print("Sentiment:", sentiment)
print("Volatility:", volatility)
print("Financial Metrics:", financial_metrics)
print("Challenges:", challenges)
print("Opportunities:", opportunities)
print("Management Tone:", management_tone)

