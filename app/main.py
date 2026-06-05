from fastapi import FastAPI

app = FastAPI(
    title="RAG Q&A System",
    description="Document Question Answering API",
    version="1.0"
)

@app.get("/")
def home():
    return {
        "message": "RAG Q&A API Running"
    }