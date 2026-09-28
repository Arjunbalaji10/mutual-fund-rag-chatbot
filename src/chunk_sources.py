import os


RAW_DIR = "data/raw"
OUTPUT_FILE = "data/chunks/chunks.txt"

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200


def chunk_text(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    chunks = []

    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


def main():
    os.makedirs("data/chunks", exist_ok=True)

    all_chunks = []
    chunk_number = 1

    for filename in sorted(os.listdir(RAW_DIR)):

        if not filename.endswith(".txt"):
            continue

        filepath = os.path.join(RAW_DIR, filename)

        with open(filepath, "r", encoding="utf-8") as file:
            text = file.read()

        source_name = filename.replace(".txt", "")

        chunks = chunk_text(text)

        for chunk in chunks:
            formatted_chunk = (
                f"--- Chunk {chunk_number} ---\n"
                f"Source: {source_name}\n"
                f"Character count: {len(chunk)}\n\n"
                f"{chunk}\n"
            )

            all_chunks.append(formatted_chunk)
            chunk_number += 1

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        file.write("\n".join(all_chunks))

    print(f"Total chunks created: {len(all_chunks)}")
    print(f"Saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()