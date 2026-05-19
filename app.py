from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import shutil
import os

from utils.pdf_loader import load_pdf
from utils.text_splitter import split_documents
from utils.vector_store import create_vector_store

# Create uploads folder
os.makedirs("uploads", exist_ok=True)

app = FastAPI()

#  CORRECT CORS CONFIG
origins = [
    "https://docu-sense-ai-nine.vercel.app",
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 🔥 for now (demo purpose)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#  HANDLE PREFLIGHT REQUEST
@app.options("/{rest_of_path:path}")
async def preflight_handler(rest_of_path: str):
    return JSONResponse(content={})

# Global vector store
vectorstore = None

@app.get("/")
def home():
    return {"message": "DocuSenseAI is running"}

@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):

    global vectorstore

    file_path = f"uploads/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    documents = load_pdf(file_path)
    chunks = split_documents(documents)
    vectorstore = create_vector_store(chunks)

    return {
        "message": "PDF uploaded and processed successfully",
        "filename": file.filename,
        "total_chunks": len(chunks)
    }

@app.get("/ask")
def ask_question(query: str):

    global vectorstore

    if vectorstore is None:
        return {"error": "Please upload a PDF first"}

    results = vectorstore.similarity_search(query, k=5)

    #  pick best chunk manually
    best_text = ""
    for doc in results:
        text = doc.page_content.strip()

        # skip noisy chunks
        if len(text) < 100:
            continue
        if any(x in text for x in ["•", "1.", "2.", "202", "8/"]):
            continue

        best_text = text
        break

    if not best_text:
        best_text = results[0].page_content

    #  clean text
    best_text = best_text.replace("\n", " ")
    best_text = " ".join(best_text.split())

    #  remove dates/numbers junk
    import re
    best_text = re.sub(r"\d{1,2}/\d{1,2}/\d{2,4}", "", best_text)
    best_text = re.sub(r"\b\d+\b", "", best_text)

    #  split into sentences
    sentences = best_text.split(". ")

    # take only first clean sentence
    answer = sentences[0]

    # if too short, add second
    if len(answer) < 60 and len(sentences) > 1:
        answer += ". " + sentences[1]

    return {
        "query": query,
        "answer": answer.strip()
    }