from fastapi import FastAPI, UploadFile, File
import os

from app.pdf_loader import extract_text
from app.text_splitter import split_text
from app.embeddings import create_embeddings
from app.vector_store import store_embeddings
from app.retriever import retrieve_chunks
from app.vector_store import store_embeddings
from app.retriever import retrieve_chunks
from app.llm import generate_answer

app = FastAPI()

UPLOAD_FOLDER = "uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.get("/")
def home():
    return {"message": "RAG API Running"}

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

    file_path = os.path.join(
        UPLOAD_FOLDER,
        file.filename
    )

    with open(file_path, "wb") as f:
        f.write(await file.read())

    extracted_text = extract_text(file_path)

    chunks = split_text(extracted_text)

    embeddings = create_embeddings(chunks)

    store_embeddings(
        chunks,
        embeddings,
        file.filename
    )

    return {
        "filename": file.filename,
        "total_chunks": len(chunks),
        "embedding_dimension": len(embeddings[0]),
        "stored_in_pinecone": True
    }

@app.post("/ask")
async def ask_question(question: str):

    chunks = retrieve_chunks(question)

    answer = generate_answer(
        question,
        chunks
    )

    return {
        "question": question,
        "answer": answer
    }