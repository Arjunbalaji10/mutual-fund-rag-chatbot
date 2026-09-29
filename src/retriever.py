import re

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
        text = text.lower()

        text = re.sub(
            r"[^a-z0-9₹.%]+",
            " ",
            text
        )

        return text.split()

    def retrieve(self, question, top_k=10):
        question_lower = question.lower()

        tokenized_question = self.tokenize(question)

        scores = self.bm25.get_scores(
            tokenized_question
        )

        # Boost exact phrase matches.
        important_phrases = [
            "expense ratio",
            "minimum investment",
            "minimum sip investment",
            "minimum lumpsum investment",
            "exit load",
            "fund size",
            "aum",
            "nav",
        ]

        for index, chunk in enumerate(self.chunks):
            chunk_lower = chunk.lower()

            for phrase in important_phrases:
                if phrase in question_lower and phrase in chunk_lower:
                    scores[index] += 5.0

        # Boost the exact fund name when it appears
        # in both the question and the chunk.
        fund_names = [
            "hdfc large cap fund direct growth",
            "hdfc equity fund direct growth",
            "hdfc elss tax saver fund direct plan growth",
            "hdfc small cap fund direct growth",
            "hdfc balanced advantage fund direct growth",
        ]

        for index, chunk in enumerate(self.chunks):
            chunk_lower = chunk.lower()

            for fund_name in fund_names:
                if (
                    fund_name in question_lower
                    and fund_name in chunk_lower
                ):
                    scores[index] += 10.0

        ranked_indexes = sorted(
            range(len(scores)),
            key=lambda i: scores[i],
            reverse=True
        )[:top_k]

        results = []

        for index in ranked_indexes:
            results.append({
                "document": self.chunks[index],
                "score": float(scores[index]),
            })

        return results