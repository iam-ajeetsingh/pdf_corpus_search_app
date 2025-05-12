import streamlit as st
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import re

INDEX_PATH = "../vector_store/faiss_index.index"
META_PATH = "../vector_store/chunk_metadata.json"
CHUNKS_PATH = "../data/processed_text/chunks.json"

st.set_page_config(page_title="PDF Search App", layout="wide")

@st.cache_resource

def load_resources():
    model = SentenceTransformer("all-MiniLM-L6-v2")
    index = faiss.read_index(INDEX_PATH)
    with open(META_PATH, "r", encoding="utf-8") as f:
        metadata = json.load(f)
    with open(CHUNKS_PATH, "r", encoding="utf-8") as f:
        chunks = json.load(f)
    return model, index, metadata, chunks

model, index, metadata, chunks = load_resources()

st.title("📄 Keyword & Semantic Search Application")
st.markdown("""
Welcome to the **PDF Search Application**.  
Search across thousands of pdf documents using either:
- 🔎 **Keyword Search** for exact or partial text matches
- 🧠 **Semantic Search** for contextually relevant results
            
This tool is designed to help you quickly find relevant information from large collections of PDF documents. 
""")


#query = st.text_input("Enter your query:")
#search_type = st.radio("Search Mode", ["Semantic", "Keyword"])

col1, col2 = st.columns([1, 3])
with col1:
    search_type = st.radio("Select Search Mode", ["Keyword","Semantic"])
with col2:
    query = st.text_input("🔎 What are you looking for?", placeholder="e.g., Leave policy, Bonus notification")




def highlight_query(text, query):
    pattern = re.compile(re.escape(query), re.IGNORECASE)
    return pattern.sub(lambda m: f"<mark>{m.group(0)}</mark>", text)

if query:
    results = []
    if search_type == "Semantic":
        query_vec = model.encode([query], convert_to_numpy=True)
        D, I = index.search(query_vec, k=5)
        for i in I[0]:
            results.append(chunks[i])
    else:  # Keyword
        results = [c for c in chunks if query.lower() in c["text"].lower()][:5]

    st.subheader("🔍 Results")

    for r in results:
        st.markdown(f"**Source:** `{r['source_file']}`")
        #st.markdown(f"```text\n{r['text'][:1000]}\n```")
        highlighted = highlight_query(r['text'][:1000], query)
        st.markdown(f"<p><strong>Source:</strong> {r['source_file']}</p>", unsafe_allow_html=True)
        st.markdown(f"<div style='background:#f7f7f7; padding:10px;'>{highlighted}</div>", unsafe_allow_html=True)
        #st.markdown("<hr>")
        st.markdown("---")



