from alpha_vantage_single_stock import AlphaVantageSingleStock
from earnings_transcript_extractor import TranscriptExtractor
from dspy_earnings_call import EarningsCallProcessor, SafeGetter, FinancialExtractorComponent
from bm25_retrieval import BM25
from bm25_execution import BM25Execution
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
