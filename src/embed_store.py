import os

import chromadb
from sentence_transformers import SentenceTransformer


CHUNKS_FILE = "data/chunks/chunks.txt"
CHROMA_PATH = "chroma_db"
COLLECTION_NAME = "mutual_fund_faq"


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


def main():
    print("Loading chunks...")

    chunks = load_chunks()

    print(f"Chunks loaded: {len(chunks)}")

    print("Loading embedding model...")

    model = SentenceTransformer("all-MiniLM-L6-v2")

    print("Creating embeddings...")

    embeddings = model.encode(
        chunks,
        show_progress_bar=True
    )

    print(
        f"Embedding dimensions: {len(embeddings[0])}"
    )

    print("Opening persistent ChromaDB...")

    client = chromadb.PersistentClient(
        path=CHROMA_PATH
    )

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME
    )

    ids = [
        f"chunk_{i + 1}"
        for i in range(len(chunks))
    ]

    metadatas = [
        {
            "source": extract_source(chunk)
        }
        for chunk in chunks
    ]

    collection.upsert(
        ids=ids,
        documents=chunks,
        embeddings=embeddings.tolist(),
        metadatas=metadatas
    )

    print(
        f"Documents stored in ChromaDB: {collection.count()}"
    )

    print("\nMetadata preview:")

    for i in range(min(5, len(chunks))):
        print(
            f"{ids[i]} -> "
            f"{metadatas[i]['source']}"
        )

    print("\nEmbedding preview:")

    print(
        "First 5 embeddings, first 10 dimensions:"
    )

    for i in range(min(5, len(embeddings))):
        preview = embeddings[i][:10]

        print(
            f"Embedding {i + 1}: {preview}"
        )


if __name__ == "__main__":
    main()