# RAG PDF Chatbot

A simple retrieval-augmented generation (RAG) application for asking questions about uploaded PDF files. The project uses FastAPI for the API, Streamlit for the chat interface, Pinecone for vector search, and Groq to generate grounded answers.

## How it works

1. Upload a PDF through the Streamlit interface.
2. The API extracts its text and splits it into overlapping chunks.
3. Each chunk is embedded with `sentence-transformers/all-MiniLM-L6-v2` and stored in Pinecone.
4. When you ask a question, the app retrieves the three most relevant chunks and sends them with the question to Groq.

## Requirements

- Python 3.10+
- A [Pinecone](https://www.pinecone.io/) account and API key
- A [Groq](https://console.groq.com/) API key
- A Pinecone index named `raq-qa-whales`

The index must be compatible with the `all-MiniLM-L6-v2` embedding size (384 dimensions) and use the same distance metric expected by your Pinecone configuration.

## Setup

Clone the repository and create a virtual environment:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Install the runtime packages used directly by the application if they are not already present in your environment:

```powershell
pip install streamlit pinecone-client groq sentence-transformers langchain-community langchain-text-splitters
```

Create a `.env` file in the project root:

```env
PINECONE_API_KEY=your_pinecone_api_key
GROQ_API_KEY=your_groq_api_key
```

> `.env` is ignored by Git. Never commit API keys.

## Run the application

Start the API in one terminal:

```powershell
uvicorn app.main:app --reload
```

Then start the interface in another terminal:

```powershell
streamlit run ui.py
```

Open the Streamlit URL shown in the terminal (normally `http://localhost:8501`). The API runs at `http://127.0.0.1:8000` by default.

## API

| Endpoint | Method | Description |
| --- | --- | --- |
| `/` | `GET` | Confirms that the API is running. |
| `/upload` | `POST` | Accepts a PDF as multipart form field `file`, processes it, and stores its chunk embeddings. |
| `/ask?question=...` | `POST` | Retrieves relevant chunks and returns an answer based on their context. |

Example question request:

```powershell
Invoke-RestMethod -Method Post "http://127.0.0.1:8000/ask?question=What%20is%20this%20document%20about%3F"
```

## Project structure

```text
app/
  main.py           FastAPI routes and RAG workflow
  pdf_loader.py     PDF text extraction
  text_splitter.py  Chunking configuration
  embeddings.py     Sentence-transformer embeddings
  vector_store.py   Pinecone storage
  retriever.py      Similarity search
  llm.py            Groq answer generation
ui.py               Streamlit chat interface
uploads/            PDFs uploaded through the app
```

## Notes

- Uploaded PDFs are saved locally in `uploads/` and their vectors are added to the shared Pinecone index.
- The current implementation does not filter search results by filename, so questions can retrieve content from any PDF previously uploaded to the index.
- The application instructs the model to answer only from retrieved context; accuracy still depends on successful extraction and retrieval.
