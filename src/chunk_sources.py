import os


RAW_DIR = "data/raw"
OUTPUT_FILE = "data/chunks/chunks.txt"

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200


def chunk_text(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    chunks = []
    current_lines = []
    current_length = 0

    for line in lines:
        line_length = len(line) + 1

        if (
            current_lines
            and current_length + line_length > chunk_size
        ):
            chunks.append("\n".join(current_lines))

            overlap_lines = []
            overlap_length = 0

            for previous_line in reversed(current_lines):
                if overlap_length + len(previous_line) + 1 > overlap:
                    break

                overlap_lines.insert(0, previous_line)
                overlap_length += len(previous_line) + 1

            current_lines = overlap_lines
            current_length = overlap_length

        current_lines.append(line)
        current_length += line_length

    if current_lines:
        chunks.append("\n".join(current_lines))

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