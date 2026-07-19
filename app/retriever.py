from app.embeddings import model
from app.vector_store import index

def retrieve_chunks(query, top_k=3):

    query_embedding = model.encode(query)

    results = index.query(
        vector=query_embedding.tolist(),
        top_k=top_k,
        include_metadata=True
    )

    chunks = []

    for match in results["matches"]:
        chunks.append(
            match["metadata"]["text"]
        )

    return chunks