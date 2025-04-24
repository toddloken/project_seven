from alpha_vantage_single_stock import AlphaVantageSingleStock
from earnings_transcript_extractor import TranscriptExtractor
from dspy_earnings_call import EarningsCallProcessor, SafeGetter, FinancialExtractorComponent
from bm25_retrieval import BM25
from bm25_execution import BM25Execution
from financial_analysis_swing_trading import  SwingTradeAnalyzer
# ======================================================
# Part 1 API
# get single stock
# stock_ticker = "UNH"
# stock = AlphaVantageSingleStock(stock_ticker)
# all_data = stock.get_all_data()
# ======================================================
# Part 1 to 2 Transcript Extractor
# extractor = TranscriptExtractor("data/earnings_transcript_data_current_quarter.json", debug=True)
# transcript = extractor.process()
# print(transcript)
# # ======================================================
# # Part 3 - Key Word RAG -
# call_processor = EarningsCallProcessor()
# financial_extractor = FinancialExtractorComponent()
#
# #variable set-up
# stock_context = {
#     "recent_performance": "The stock has been volatile, down 2% over the last 5 days.",
#     "analyst_expectations": "Analysts expected steady EPS growth and flat revenue."
# }
# #get stuff
# call_results = call_processor(transcript=transcript, stock_context=stock_context)
#
# revenue = SafeGetter.safe_get(call_results, "extraction", "financial_metrics")
# guidance = SafeGetter.safe_get(call_results, "extraction", "guidance")
# sentiment = SafeGetter.safe_get(call_results, "sentiment", "overall_sentiment")
# volatility = SafeGetter.safe_get(call_results, "impact", "impact_magnitude")
#
# financial_results = financial_extractor(transcript)
#
# financial_metrics = SafeGetter.safe_get(financial_results, "financial_metrics")
# challenges = SafeGetter.safe_get(financial_results, "challenges")
# opportunities = SafeGetter.safe_get(financial_results, "opportunities")
# management_tone = SafeGetter.safe_get(financial_results, "management_tone")

# #print for now
# print("Revenue:", revenue)
# print("Guidance:", guidance)
# print("Sentiment:", sentiment)
# print("Volatility:", volatility)
# print("Financial Metrics:", financial_metrics)
# print("Challenges:", challenges)
# print("Opportunities:", opportunities)
# print("Management Tone:", management_tone)
# # ======================================================
# # Part 3 - 4 Key Word RAG
# custom_documents = [ ]
# bm25 = BM25(documents=custom_documents)
# bm25 = BM25Execution()
# query = "support outpouring volatile unanticipated uncertainty weekly churn medicare advantage rates"
# bm25.print_search_results(query)
# bm25.print_score_explanation(query, doc_id=0)


analyzer = SwingTradeAnalyzer('data/daily_data.csv')

# Get the swing trade recommendation
fm_score, fm_swing_trade_recommendation = analyzer.get_swing_trade_recommendation()

# Print results
print("Swing Trade Rating Score:", fm_score)
print("Swing Trade Recommendation:", fm_swing_trade_recommendation)

# Optional: Print all indicators
fm_rsi, fm_atr_14, fm_atr_28, fm_atr_42, fm_vwap = analyzer.get_latest_indicators()
print("Latest RSI:", fm_rsi)
print("Latest 14Day ATR:", fm_atr_14)
print("Latest 28Day ATR:", fm_atr_28)
print("Latest 42Day ATR:", fm_atr_42)
print("Latest VWAP:", fm_vwap)
