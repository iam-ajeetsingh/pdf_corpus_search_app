# 📄 Keyword & Semantic Search Application

A secure, local, and AI-powered application for searching through large volumes of internal PDFs using **semantic** and **keyword** search. 

---

## 🚀 Features

- 🔍 Semantic Search (via MiniLM embeddings)
- 🧾 Keyword Search fallback
- 📑 Structured + OCR text extraction from PDFs
- 📚 Intelligent chunking (heading-based or fixed size)
- 💾 Fast local vector search with FAISS
- 🧠 Simple UI built with Streamlit
- 🔐 100% offline — no data leaves your machine

---

## 🧱 Tech Stack

| Layer               | Technology                                      |
|------------------  |--------------------------------------------------|
| PDF Text Extraction | `pdfplumber`, `pytesseract`, `pdf2image`        |
| Text Chunking      | `regex`, `langchain`                             |
| Embeddings         | `sentence-transformers` with `all-MiniLM-L6-v2`  |
| Vector Search      | `FAISS`                                          |
| UI                 | `Streamlit`                                      |
| Environment        | `Python 3.9`, `Conda`                            |

---


## 📁 Project Structure

```

pdf_corpus_search_app 
├── data/
│   ├── raw_pdfs/              # Original PDFs
│   ├── processed_text/        # Extracted .txt and chunks.json
│   └── ocr_images/            # Images for OCR fallback
├── vector_store/              # FAISS index + metadata
├── scripts/
│   ├── extract_text.py        # PDF and OCR text extraction
│   ├── chunk_text.py          # Intelligent text chunking
│   └── embed_store.py         # Embeddings + FAISS indexing
├── ui/
│   └── gui.py                 # Streamlit Search interface
├── requirements.txt
└── README.md

````

---

## ⚙️ Setup Instructions

### 1. Clone the Repo

```bash
git clone https://github.com/yourusername/pdf_corpus_search_app.git
cd pdf_corpus_search_app
````

### 2. Set Up Environment

```bash
conda create -n venv python=3.9
conda activate venv
pip install -r requirements.txt
```

### 3. Install System Dependencies

```bash
sudo apt install poppler-utils tesseract-ocr
```

On Windows:

* Install [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
* Install [Poppler](http://blog.alivate.com.au/poppler-windows/) and add it to your PATH

---

## 🧪 Usage

### 1. Place Your PDFs

Put all PDFs inside the following directory:

```
data/raw_pdfs/
```

### 2. Run Processing Scripts

```bash
python scripts/extract_text.py
python scripts/chunk_text.py
python scripts/embed_store.py
```

### 3. Launch the App

```bash
streamlit run ui/gui.py
```

---

## 🧠 How It Works

| Component       | Description                                       |
| --------------- | ------------------------------------------------- |
| Keyword Search  | Exact string match using Python’s `in` operator   |
| Semantic Search | Meaning-based match using MiniLM + FAISS          |
| Text Extraction | From text-based PDFs or via OCR for scanned files |
| Chunking        | Based on headings or fixed char length fallback   |

---

## 📊 Limitations

* No LLM-based response generation yet
* No multi-turn conversations or summaries
* Chunking is static, not dynamically optimized
* Manual pipeline for adding new PDFs
* No PDF preview or page-level navigation

---

## 🔮 Future Enhancements

*  Integrate a local LLM (e.g., GPT4All or Mistral)
*  Add PDF preview with page highlights
*  Enable filters (by department, date, etc.)
*  Role-based access or user login
*  Incremental indexing of new PDFs
*  Download/export search results
*  Chat-style UI with context memory

---

## 🔐 Data Privacy

> This app is fully offline. No data is sent to external APIs or cloud services. It is ideal for sensitive, internal document use in government and enterprise settings.

---

## 📎 Use Cases

* Government Docuements search
* Internal HR policy lookup
* SOP or compliance document exploration
* Research paper/document retrieval
* Legal or procurement circular indexing

---

