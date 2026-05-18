#  DocuSenseAI

An AI-powered document assistant that lets you upload PDFs and ask questions using Retrieval-Augmented Generation (RAG).

Built using FastAPI, React, FAISS, and a local LLM.

---

##  Features

-  Upload PDF documents
-  Semantic search using vector embeddings
-  Context-aware AI answers
-  Fast retrieval using FAISS
-  Local LLM integration (TinyLlama / Ollama)
-  Modern React UI

---

##  Tech Stack

**Frontend:**
- React (Vite)
- Tailwind CSS

**Backend:**
- FastAPI
- LangChain
- FAISS

**AI / LLM:**
- Ollama (TinyLlama)

---

##  How It Works

1. Upload a PDF
2. Text is split into chunks
3. Embeddings are created
4. Stored in FAISS vector DB
5. Query retrieves relevant chunks
6. LLM generates answer using context
