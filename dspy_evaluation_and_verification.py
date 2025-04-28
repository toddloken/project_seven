from dspy import Evaluate,SelfCritique, FactCheck, Metric
from typing import List, Dict, Any

class FinancialRAGEvaluator:
    def __init__(self, rag_pipeline, baseline_pipeline):
        self.rag_pipeline = rag_pipeline
        self.baseline_pipeline = baseline_pipeline
        self.evaluator = Evaluate()
        self.results = {}

    def _fact_check(self, response: str) -> bool:
        """Automated verification mechanism for factual accuracy."""
        return FactCheck().run(response)

    def _self_critique(self, response: str) -> str:
        """Allows the model to critique and improve its own response."""
        return SelfCritique().run(response)

    def _domain_metrics(self, response: str, reference: str) -> Dict[str, float]:
        """Custom domain-specific metrics."""
        return {
            "relevance": Metric.relevance(response, reference),
            "correctness": Metric.correctness(response, reference),
            "helpfulness": Metric.helpfulness(response, reference)
        }

    def evaluate_single(self, query: str, reference: str):
        """Evaluate a single query-response pair from both RAG and baseline pipelines."""
        rag_response = self.rag_pipeline(query)
        baseline_response = self.baseline_pipeline(query)

        rag_checked = self._fact_check(rag_response)
        rag_critique = self._self_critique(rag_response)
        rag_metrics = self._domain_metrics(rag_response, reference)

        baseline_metrics = self._domain_metrics(baseline_response, reference)

        return {
            "query": query,
            "reference": reference,
            "rag": {
                "response": rag_response,
                "factually_correct": rag_checked,
                "self_critique": rag_critique,
                "metrics": rag_metrics
            },
            "baseline": {
                "response": baseline_response,
                "metrics": baseline_metrics
            }
        }

    def batch_evaluate(self, queries_references: List[Dict[str, str]]):
        """Run evaluation on a batch of queries."""
        for qr in queries_references:
            result = self.evaluate_single(qr['query'], qr['reference'])
            self.results[qr['query']] = result

    def summarize_results(self) -> Dict[str, Any]:
        """Aggregate and summarize evaluation results."""
        summary = {"avg_metrics": {}, "comparison": []}
        total_metrics = {"relevance": 0, "correctness": 0, "helpfulness": 0}
        count = len(self.results)

        for data in self.results.values():
            for key in total_metrics:
                total_metrics[key] += data['rag']['metrics'][key]

            comparison_entry = {
                "query": data["query"],
                "rag_score": data['rag']['metrics'],
                "baseline_score": data['baseline']['metrics']
            }
            summary["comparison"].append(comparison_entry)

        if count > 0:
            for key in total_metrics:
                summary["avg_metrics"][key] = total_metrics[key] / count

        return summary