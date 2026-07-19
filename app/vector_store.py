from pinecone import Pinecone
from dotenv import load_dotenv
import os
import uuid

load_dotenv()

pc = Pinecone(
    api_key=os.getenv("PINECONE_API_KEY")
)

index = pc.Index("raq-qa-whales")


def store_embeddings(chunks, embeddings, filename):

    vectors = []

    for chunk, embedding in zip(chunks, embeddings):

        vectors.append({
            "id": str(uuid.uuid4()),
            "values": embedding.tolist(),
            "metadata": {
                "text": chunk,
                "source": filename
            }
        })

    index.upsert(vectors=vectors)

