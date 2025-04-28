import math
from collections import Counter

class BM25Execution:
    def __init__(self, documents=None):
        # Initialize the documents
        self.documents = [
            "Good morning, and welcome to UnitedHealth Group Fourth Quarter and Full Year 2024 Earnings Conference",
            "Andrew Witty, Jennifer, thank you very much, and good morning, everyone. I'd like to start by expressing a sincere thank you from my colleagues and from me for the overwhelming expressions of condolence and support following the murder of our friend, Brian Thompson...",
            "Thank you, Andrew. And I'll add my deep gratitude for the enormous outpouring of support over the past few weeks. Brian helped build this company and forged deep trusted relationships...",
            "Tim Noel, Yeah, thanks for the question, Stephen. As you know, these rates are preliminary at this point in time and won't be finalized until April..."
        ]

        self.k1 = 1.5
        self.b = 0.75
        self.doc_lengths = [len(doc.split()) for doc in self.documents]
        self.avg_doc_length = sum(self.doc_lengths) / len(self.doc_lengths)
        self.doc_freqs = []
        self.inverted_index = {}
        self.N = len(self.documents)

        for idx, doc in enumerate(self.documents):
            terms = doc.lower().split()
            freqs = Counter(terms)
            self.doc_freqs.append(freqs)
            for term in freqs:
                if term not in self.inverted_index:
                    self.inverted_index[term] = set()
                self.inverted_index[term].add(idx)

    def idf(self, term):
        df = len(self.inverted_index.get(term, []))
        return math.log((self.N - df + 0.5) / (df + 0.5) + 1)

    def score(self, query, doc_id):
        score = 0.0
        doc_freq = self.doc_freqs[doc_id]
        doc_len = self.doc_lengths[doc_id]
        query_terms = query.lower().split()

        for term in query_terms:
            tf = doc_freq.get(term, 0)
            if tf == 0:
                continue
            idf = self.idf(term)
            denom = tf + self.k1 * (1 - self.b + self.b * (doc_len / self.avg_doc_length))
            score += idf * (tf * (self.k1 + 1)) / denom

        return score

    def search(self, query):
        scores = [(doc_id, self.score(query, doc_id)) for doc_id in range(self.N)]
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores

    def explain_score(self, query, doc_id):
        explanation = {}
        total_score = 0.0
        doc_freq = self.doc_freqs[doc_id]
        doc_len = self.doc_lengths[doc_id]
        query_terms = query.lower().split()

        for term in query_terms:
            tf = doc_freq.get(term, 0)
            idf = self.idf(term)
            doc_length_factor = self.k1 * (1 - self.b + self.b * (doc_len / self.avg_doc_length))
            denom = tf + doc_length_factor
            score_contribution = 0.0
            if tf > 0:
                score_contribution = idf * (tf * (self.k1 + 1)) / denom
                total_score += score_contribution
            explanation[term] = {
                "term_freq": tf,
                "idf": idf,
                "doc_length_factor": doc_length_factor,
                "score_contribution": score_contribution
            }

        explanation['total_score'] = total_score
        return explanation

    def get_document(self, doc_id):
        return self.documents[doc_id]

    def print_search_results(self, query):
        print(f"\nResults for query: '{query}'")
        results = self.search(query)
        for doc_id, score in results:
            print(f"\nScore: {score:.4f}")
            print(f"Document {doc_id}:\n{self.get_document(doc_id)}")

    def print_score_explanation(self, query, doc_id):
        explanation = self.explain_score(query, doc_id)
        print(f"\nScore explanation for document {doc_id} with query '{query}':")
        for term, details in explanation.items():
            if term != 'total_score':
                print(f"Term: '{term}'")
                print(f"  - Term frequency: {details['term_freq']}")
                print(f"  - IDF: {details['idf']:.4f}")
                print(f"  - Document length factor: {details['doc_length_factor']:.4f}")
                print(f"  - Score contribution: {details['score_contribution']:.4f}")
            else:
                print(f"Total score: {details:.4f}")


