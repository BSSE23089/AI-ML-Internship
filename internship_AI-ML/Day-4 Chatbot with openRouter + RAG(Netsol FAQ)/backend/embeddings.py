import requests
from config import OPENROUTER_API_KEY, EMBEDDINGS_URL, EMBEDDING_MODEL


def get_embedding(text: str):
    response = requests.post(
        EMBEDDINGS_URL,
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": EMBEDDING_MODEL,
            "input": text
        }
    )
    if response.status_code != 200:
        raise Exception(f"Embedding error {response.status_code}: {response.text}")
    data = response.json()
    return data["data"][0]["embedding"]