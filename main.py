from alpha_vantage_single_stock import AlphaVantageSingleStock
from earnings_transcript_extractor import TranscriptExtractor

# ======================================================
# get single stock
# stock_ticker = "UNH"
# stock = AlphaVantageSingleStock(stock_ticker)
# all_data = stock.get_all_data()
# ======================================================
extractor = TranscriptExtractor("data/earnings_transcript_data_current_quarter.json", debug=True)
transcript = extractor.process()
print(transcript)
