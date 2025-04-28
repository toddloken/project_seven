from pprint import pprint
from typing import List, Dict

class FinancialRAGTestRunner:
    def __init__(self, evaluator_class):
        self.evaluator_class = evaluator_class
        self.evaluator = None
        self.test_queries = self._load_test_queries()

    def _mock_rag_pipeline(self, query: str) -> str:
        """Simulated RAG system response."""
        return f"RAG response to: {query}. The net profit is $10 million."

    def _mock_baseline_pipeline(self, query: str) -> str:
        """Simulated baseline system response."""
        return f"Baseline response to: {query}. Profit is estimated."

    def _load_test_queries(self) -> List[Dict[str, str]]:
        """Sample queries with ground truth references."""
        return [
            {
                "query": "What is the net profit for Q4 2024?",
                "reference": "The net profit for Q4 2024 was $10 million."
            },
            {
                "query": "What were the revenue and expenses for 2023?",
                "reference": "Revenue was $100 million, expenses were $90 million."
            }
        ]

    def run(self):
        """Execute evaluation process and print results."""
        self.evaluator = self.evaluator_class(
            rag_pipeline=self._mock_rag_pipeline,
            baseline_pipeline=self._mock_baseline_pipeline
        )

        self.evaluator.batch_evaluate(self.test_queries)

        print("\n--- Detailed Results ---")
        pprint(self.evaluator.results)

        print("\n--- Summary ---")
        summary = self.evaluator.summarize_results()
        pprint(summary)