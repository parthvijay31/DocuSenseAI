from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
#import ollama

from utils.pdf_loader import load_pdf
from utils.text_splitter import split_documents
from utils.vector_store import create_vector_store

#  CREATE uploads folder
os.makedirs("uploads", exist_ok=True)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global vector store
vectorstore = None

@app.get("/")
def home():
    return {"message": "DocuSenseAI is running"}

@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):

    global vectorstore

    # Save uploaded PDF
    file_path = f"uploads/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Load PDF
    documents = load_pdf(file_path)

    # Split chunks
    chunks = split_documents(documents)

    # Create vector DB
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
        return {
            "error": "Please upload a PDF first"
        }

    # Retrieve relevant chunks
    results = vectorstore.similarity_search(query, k=2)

    context = "\n\n".join(
        [result.page_content for result in results]
    )

    # Return only relevant context (no LLM)
    answer = context.strip()

    if len(answer) > 800:
        answer = answer[:800] + "..."

    return {
        "query": query,
        "answer": answer
    }


    #prompt = prompt = f"""
#Answer the question based only on the context below.

##Context:
#{context}

#Question:
#{query}

#Answer:
#"""

    #response = ollama.chat(
        #model='tinyllama',
        #messages=[
            #{
                #'role': 'user',
                #'content': prompt
           # }
    #    ]
  #  )

   # answer = response['message']['content']
   
