import os
import re
import json
from pathlib import Path
from tqdm import tqdm

from langchain.text_splitter import RecursiveCharacterTextSplitter

TEXT_DIR = "../data/processed_text"
CHUNK_OUTPUT = "../data/processed_text/chunks.json"

# Regex patterns to detect headings (tune as needed)
HEADING_PATTERNS = [
    r"^\s*[A-Z][A-Z0-9\s\-:]{5,}$",              # ALL CAPS HEADINGS
    r"^\s*\d+\.\s+.*",                          # Numbered headings
    r"^\s*[IVXLC]+\.\s+.*"                       # Roman numerals
]

# Fallback splitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=700,
    chunk_overlap=100
)

def split_by_headings(text):
    lines = text.split("\n")
    chunks = []
    buffer = []
    for line in lines:
        if any(re.match(p, line.strip()) for p in HEADING_PATTERNS):
            if buffer:
                chunks.append("\n".join(buffer))
                buffer = []
        buffer.append(line)
    if buffer:
        chunks.append("\n".join(buffer))
    return chunks

if __name__ == "__main__":
    chunked_docs = []
    txt_files = list(Path(TEXT_DIR).glob("*.txt"))

    for txt_path in tqdm(txt_files, desc="Chunking Text Files"):
        with open(txt_path, "r", encoding="utf-8") as f:
            full_text = f.read()

        # Try to chunk by headings
        chunks = split_by_headings(full_text)

        # Fallback if not enough chunks
        if len(chunks) < 2:
            chunks = text_splitter.split_text(full_text)

        for idx, chunk in enumerate(chunks):
            chunked_docs.append({
                "chunk_id": f"{txt_path.stem}_{idx}",
                "text": chunk.strip(),
                "source_file": txt_path.name
            })

    with open(CHUNK_OUTPUT, "w", encoding="utf-8") as f:
        json.dump(chunked_docs, f, indent=2)

    print(f"Saved {len(chunked_docs)} chunks to {CHUNK_OUTPUT}")
