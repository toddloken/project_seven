import math
import re
from collections import Counter, defaultdict


class BM25:
    def __init__(self, documents, k1=1.5, b=0.75):
        """
        Initialize BM25 with a collection of documents

        """
        self.k1 = k1
        self.b = b
        self.documents = documents
        self.doc_count = len(documents)

        self.tokenized_docs = [self._tokenize(doc) for doc in documents]
        self.doc_lengths = [len(doc) for doc in self.tokenized_docs]
        self.avg_doc_length = sum(self.doc_lengths) / self.doc_count

        self.inverted_index = defaultdict(list)
        self.idf = {}
        self._build_index()

    def _tokenize(self, text):
        return re.findall(r'\w+', text.lower())

    def _build_index(self):
        df = defaultdict(int)
        for doc_id, doc in enumerate(self.tokenized_docs):
            term_frequencies = Counter(doc)

            for term, freq in term_frequencies.items():
                self.inverted_index[term].append((doc_id, freq))

            for term in term_frequencies:
                df[term] += 1

        for term, doc_freq in df.items():
            self.idf[term] = math.log((self.doc_count - doc_freq + 0.5) /
                                      (doc_freq + 0.5) + 1.0)

    def search(self, query, top_n=5):
        """
        Search the document collection with a query string
        """
        query_terms = self._tokenize(query)
        scores = [0] * self.doc_count

        for term in query_terms:
            if term not in self.inverted_index:
                continue

            idf_value = self.idf.get(term, 0)

            for doc_id, term_freq in self.inverted_index[term]:
                doc_length = self.doc_lengths[doc_id]

                # BM25 scoring formula
                numerator = idf_value * term_freq * (self.k1 + 1)
                denominator = term_freq + self.k1 * (1 - self.b + self.b * doc_length / self.avg_doc_length)
                scores[doc_id] += numerator / denominator

        results = [(doc_id, score) for doc_id, score in enumerate(scores) if score > 0]
        results.sort(key=lambda x: x[1], reverse=True)

        return results[:top_n]

    def get_document(self, doc_id):
        return self.documents[doc_id]

    def explain_score(self, query, doc_id):
        """
        Explain the score calculation for a document

        Args:
            query: Query string
            doc_id: Document ID

        Returns:
            Dictionary with term-by-term score contributions
        """
        query_terms = self._tokenize(query)
        explanation = {}
        total_score = 0

        for term in query_terms:
            # Initialize with a dictionary structure even when term isn't found
            if term not in self.inverted_index:
                explanation[term] = {
                    'term_freq': 0,
                    'idf': 0,
                    'doc_length_factor': 0,
                    'score_contribution': 0
                }
                continue

            idf_value = self.idf.get(term, 0)
            term_freq = 0

            for d_id, freq in self.inverted_index[term]:
                if d_id == doc_id:
                    term_freq = freq
                    break

            if term_freq == 0:
                explanation[term] = {
                    'term_freq': 0,
                    'idf': idf_value,
                    'doc_length_factor': 0,
                    'score_contribution': 0
                }
                continue

            doc_length = self.doc_lengths[doc_id]
            numerator = idf_value * term_freq * (self.k1 + 1)
            denominator = term_freq + self.k1 * (1 - self.b + self.b * doc_length / self.avg_doc_length)
            score_contribution = numerator / denominator

            explanation[term] = {
                'term_freq': term_freq,
                'idf': idf_value,
                'doc_length_factor': doc_length / self.avg_doc_length,
                'score_contribution': score_contribution
            }

            total_score += score_contribution

        explanation['total_score'] = total_score
        return explanation