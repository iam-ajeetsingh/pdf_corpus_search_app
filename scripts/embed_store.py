import json
import os
import faiss
import numpy as np
from tqdm import tqdm
from sentence_transformers import SentenceTransformer

CHUNKS_PATH = "../data/processed_text/chunks.json"
INDEX_SAVE_PATH = "../vector_store/faiss_index.index"
META_SAVE_PATH = "../vector_store/chunk_metadata.json"

model = SentenceTransformer("all-MiniLM-L6-v2")

# Load chunk data
with open(CHUNKS_PATH, "r", encoding="utf-8") as f:
    chunks = json.load(f)

texts = [chunk["text"] for chunk in chunks]
metadata = [{"chunk_id": chunk["chunk_id"], "source_file": chunk["source_file"]} for chunk in chunks]

print("Embedding text chunks...")
embeddings = model.encode(texts, show_progress_bar=True, convert_to_numpy=True)

# Create FAISS index
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

# Save index and metadata
faiss.write_index(index, INDEX_SAVE_PATH)

with open(META_SAVE_PATH, "w", encoding="utf-8") as f:
    json.dump(metadata, f, indent=2)

print(f"\n✅ Stored {len(texts)} chunks in FAISS index at: {INDEX_SAVE_PATH}")
