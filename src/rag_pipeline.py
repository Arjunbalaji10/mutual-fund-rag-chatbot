import os
import re

from dotenv import load_dotenv
from groq import Groq

from guardrails import check_guardrail
from retriever import BM25Retriever


load_dotenv()


CHUNKS_FILE = "data/chunks/chunks.txt"
TOP_K = 10
GROQ_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")


SYSTEM_PROMPT = """
You are a factual Mutual Fund FAQ assistant.

Your job is to answer questions using ONLY the provided retrieved
knowledge-base chunks.

Rules:
1. Do not provide investment advice or recommendations.
2. Do not make claims about future returns or performance.
3. If the retrieved chunks do not contain enough information to answer
   the question, say:
   "I don't know based on the available sources."
4. Do not invent facts.
5. Keep the answer to a maximum of 3 sentences.
6. Do not add citation markers such as [106] or [104].
7. Do not add a Source or Last updated line.
8. Answer only factual questions about the mutual funds covered
   by the knowledge base.
"""


SOURCE_URLS = {
    "hdfc_large_cap": (
        "https://groww.in/mutual-funds/"
        "hdfc-large-cap-fund-direct-growth"
    ),
    "hdfc_equity": (
        "https://groww.in/mutual-funds/"
        "hdfc-equity-fund-direct-growth"
    ),
    "hdfc_elss": (
        "https://groww.in/mutual-funds/"
        "hdfc-elss-tax-saver-fund-direct-plan-growth"
    ),
    "hdfc_small_cap": (
        "https://groww.in/mutual-funds/"
        "hdfc-small-cap-fund-direct-growth"
    ),
    "hdfc_balanced_advantage": (
        "https://groww.in/mutual-funds/"
        "hdfc-balanced-advantage-fund-direct-growth"
    ),
}


def load_chunks():
    with open(CHUNKS_FILE, "r", encoding="utf-8") as file:
        text = file.read()

    raw_chunks = text.split("--- Chunk ")

    chunks = []

    for raw_chunk in raw_chunks:
        raw_chunk = raw_chunk.strip()

        if not raw_chunk:
            continue

        chunks.append("--- Chunk " + raw_chunk)

    return chunks


def extract_source(chunk):
    for line in chunk.splitlines():
        if line.startswith("Source:"):
            return line.replace("Source:", "").strip()

    return "unknown"


def identify_source(question):
    question_lower = question.lower()

    source_map = {
        "hdfc_large_cap": [
            "hdfc large cap",
            "large cap fund",
        ],
        "hdfc_equity": [
            "hdfc equity fund",
            "hdfc equity",
        ],
        "hdfc_elss": [
            "hdfc elss",
            "elss tax saver",
        ],
        "hdfc_small_cap": [
            "hdfc small cap",
            "small cap fund",
        ],
        "hdfc_balanced_advantage": [
            "hdfc balanced advantage",
            "balanced advantage fund",
        ],
    }

    for source, keywords in source_map.items():
        for keyword in keywords:
            if keyword in question_lower:
                return source

    return None


def clean_answer(answer):
    answer = re.sub(
        r"\[[0-9]+\]",
        "",
        answer,
    )

    answer = re.sub(
        r"(?im)^source:\s*https?://\S+\s*$",
        "",
        answer,
    )

    answer = re.sub(
        r"(?im)^last updated from sources:.*$",
        "",
        answer,
    )

    return answer.strip()


def ask_groq(
    question,
    retrieved_chunks,
    groq_client,
):
    context = "\n\n".join(
        retrieved_chunks
    )
print("\n--- RAG DEBUG ---")
print(f"Question: {question}")
print(f"Retrieved chunks: {len(retrieved_chunks)}")
print(f"Contains 1.03%: {'1.03%' in context}")
print(context[:1500])
print("--- END RAG DEBUG ---")

    user_prompt = f"""
Retrieved knowledge-base chunks:

{context}

User question:

{question}
"""

    response = groq_client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ],
        temperature=0,
    )

    answer = response.choices[0].message.content

    return clean_answer(answer)


def load_resources():
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError(
            "GROQ_API_KEY was not found. Check your .env file."
        )

    print("Loading knowledge base...")

    chunks = load_chunks()

    print(f"Loaded {len(chunks)} chunks.")

    retriever = BM25Retriever(chunks)

    print("Connecting to Groq...")

    groq_client = Groq(api_key=api_key)

    return chunks, retriever, groq_client


def answer_question(
    question,
    chunks,
    retriever,
    groq_client,
):
    guardrail_result = check_guardrail(question)

    if not guardrail_result["allowed"]:
        return {
            "answer": guardrail_result["message"],
            "source_url": None,
        }

    results = retriever.retrieve(
        question,
        top_k=TOP_K,
    )

    retrieved_chunks = [
        result["document"]
        for result in results
    ]

    answer = ask_groq(
        question,
        retrieved_chunks,
        groq_client,
    )

    source = identify_source(question)

    if not source and results:
        source = extract_source(
            results[0]["document"]
        )

    source_url = SOURCE_URLS.get(source)

    return {
        "answer": answer,
        "source_url": source_url,
    }


def main():
    print(
        "Starting Mutual Fund RAG chatbot..."
    )

    chunks, retriever, groq_client = load_resources()

    print(
        f"Knowledge base contains "
        f"{len(chunks)} chunks."
    )

    print("\nRAG chatbot is ready.")
    print("Type 'exit' to stop.\n")

    while True:
        question = input(
            "You: "
        ).strip()

        if question.lower() == "exit":
            print("Goodbye!")
            break

        if not question:
            continue

        result = answer_question(
            question,
            chunks,
            retriever,
            groq_client,
        )

        print("\nAssistant:")
        print(result["answer"])

        if result["source_url"]:
            print(
                f"\nSource: "
                f"{result['source_url']}"
            )

        print(
            "\n" + "=" * 60
        )


if __name__ == "__main__":
    main()