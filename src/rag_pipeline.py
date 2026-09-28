import os
import re

import chromadb
from dotenv import load_dotenv
from groq import Groq
from sentence_transformers import SentenceTransformer

from guardrails import check_guardrail


load_dotenv()


CHROMA_PATH = "chroma_db"
COLLECTION_NAME = "mutual_fund_faq"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
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
6. Do not add citation markers such as 【】, [106], or [104].
7. Do not add a Source or Last updated line. The application will add
   those automatically.
8. Answer only factual questions about the mutual funds covered
   by the knowledge base.
"""


def load_resources():
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError(
            "GROQ_API_KEY was not found. Check your .env file."
        )

    print("Loading embedding model...")
    model = SentenceTransformer(EMBEDDING_MODEL)

    print("Opening ChromaDB...")
    chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)
    collection = chroma_client.get_collection(
        name=COLLECTION_NAME
    )

    print("Connecting to Groq...")
    groq_client = Groq(api_key=api_key)

    return model, collection, groq_client


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


def retrieve_chunks(question, model, collection):
    question_embedding = model.encode([question])[0].tolist()

    source = identify_source(question)

    query_arguments = {
        "query_embeddings": [question_embedding],
        "n_results": TOP_K,
        "include": [
            "documents",
            "distances",
            "metadatas",
        ],
    }

    if source:
        query_arguments["where"] = {
            "source": source
        }

    results = collection.query(**query_arguments)

    documents = results["documents"][0]

    return documents


def extract_source_url(retrieved_chunks):
    url_pattern = r"Source URL:\s*(https?://\S+)"

    for chunk in retrieved_chunks:
        match = re.search(url_pattern, chunk)

        if match:
            return match.group(1).rstrip(").,]")

    return None


def clean_answer(answer):
    # Remove citation-style artifacts.
    answer = re.sub(r"【[^】]*】", "", answer)
    answer = re.sub(r"\[\d+\]", "", answer)

    # Remove accidental Source lines.
    answer = re.sub(
        r"(?im)^source:\s*https?://\S+\s*$",
        "",
        answer,
    )

    # Remove accidental Last updated lines.
    answer = re.sub(
        r"(?im)^last updated from sources:.*$",
        "",
        answer,
    )

    return answer.strip()


def ask_groq(question, retrieved_chunks, groq_client):
    context = "\n\n".join(retrieved_chunks)

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


def answer_question(
    question,
    model,
    collection,
    groq_client,
):
    guardrail_result = check_guardrail(question)

    if not guardrail_result["allowed"]:
        return {
            "answer": guardrail_result["message"],
            "source_url": None,
        }

    retrieved_chunks = retrieve_chunks(
        question,
        model,
        collection,
    )

    answer = ask_groq(
        question,
        retrieved_chunks,
        groq_client,
    )

    source_url = extract_source_url(
        retrieved_chunks
    )

    return {
        "answer": answer,
        "source_url": source_url,
    }


def main():
    print("Starting Mutual Fund RAG chatbot...")

    model, collection, groq_client = load_resources()

    print(
        f"ChromaDB contains {collection.count()} documents."
    )

    print("\nRAG chatbot is ready.")
    print("Type 'exit' to stop.\n")

    while True:
        question = input("You: ").strip()

        if question.lower() == "exit":
            print("Goodbye!")
            break

        if not question:
            continue

        result = answer_question(
            question,
            model,
            collection,
            groq_client,
        )

        print("\nAssistant:")
        print(result["answer"])

        if result["source_url"]:
            print(
                f"\nSource: {result['source_url']}"
            )

            print(
                "Last updated from sources: "
                "Source page content retrieved from "
                "the URL above."
            )

        print("\n" + "=" * 60)


if __name__ == "__main__":
    main()