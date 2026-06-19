from embeddings import get_embedding
from vector_store import search


def get_context(user_message: str, k: int = 3) -> str:
    query_embedding = get_embedding(user_message)
    results = search(query_embedding, k=k)

    documents = results.get("documents", [[]])[0]
    if not documents:
        return ""

    context = "\n\n".join(documents)
    return context