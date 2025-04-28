import os


class FinancialAnalysisResults:
    def __init__(self, score, swing_trade_recommendation, rsi, atr_14, atr_28, atr_42, vwap):
        # Store variables with fm_ prefix in the class
        self.fm_score = score
        self.fm_swing_trade_recommendation = swing_trade_recommendation
        self.fm_rsi = rsi
        self.fm_atr_14 = atr_14
        self.fm_atr_28 = atr_28
        self.fm_atr_42 = atr_42
        self.fm_vwap = vwap

    def save_to_file(self):
        # Create data directory if it doesn't exist
        if not os.path.exists('data'):
            os.makedirs('data')

        # Path for the output file
        filepath = os.path.join('data', 'financial_analysis_key_metrics.txt')

        # Write to file - removing fm_ prefix as requested
        with open(filepath, 'w') as f:
            f.write(f"score: {self.fm_score}\n")
            f.write(f"swing_trade_recommendation: {self.fm_swing_trade_recommendation}\n")
            f.write(f"rsi: {self.fm_rsi}\n")
            f.write(f"atr_14: {self.fm_atr_14}\n")
            f.write(f"atr_28: {self.fm_atr_28}\n")
            f.write(f"atr_42: {self.fm_atr_42}\n")
            f.write(f"vwap: {self.fm_vwap}\n")

        return filepath