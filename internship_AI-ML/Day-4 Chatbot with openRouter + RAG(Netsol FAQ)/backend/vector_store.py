import chromadb

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(name="netsol_faq")


def add_chunk(chunk_id: str, embedding: list, chunk_text: str, metadata: dict):
    collection.add(
        ids=[chunk_id],
        embeddings=[embedding],
        documents=[chunk_text],
        metadatas=[metadata]
    )


def search(query_embedding: list, k: int = 3):
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k
    )
    return results