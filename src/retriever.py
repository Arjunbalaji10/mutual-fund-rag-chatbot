from rank_bm25 import BM25Okapi


class BM25Retriever:
    def __init__(self, chunks):
        self.chunks = chunks
        self.tokenized_chunks = [
            self.tokenize(chunk)
            for chunk in chunks
        ]
        self.bm25 = BM25Okapi(self.tokenized_chunks)

    @staticmethod
    def tokenize(text):
        return text.lower().split()

    def retrieve(self, question, top_k=10):
        tokenized_question = self.tokenize(question)

        scores = self.bm25.get_scores(
            tokenized_question
        )

        ranked_indexes = sorted(
            range(len(scores)),
            key=lambda i: scores[i],
            reverse=True
        )[:top_k]

        results = []

        for index in ranked_indexes:
            results.append({
                "document": self.chunks[index],
                "score": float(scores[index])
            })

        return results