# services.py
from config import OPENROUTER_API_KEY, OPENROUTER_URL, MODEL
import requests
import json
import certifi
from pymongo import MongoClient
from config import MONGO_URI
from retrieve import get_context

mongo_client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())
db = mongo_client["chatbot_db"]
checkpoints = db["checkpoints"]


def save_checkpoint(session_id: str, history: list):
    checkpoints.update_one(
        {"session_id": session_id},
        {"$set": {"history": history}},
        upsert=True
    )


def load_checkpoint(session_id: str) -> list:
    checkpoint = checkpoints.find_one({"session_id": session_id})
    if checkpoint:
        return checkpoint["history"]
    return [{"role": "system", "content": "You are a helpful assistant for NetSol Technologies. Use the provided context to answer questions accurately."}]


def get_response_stream(message, history):
    context = get_context(message, k=3)

    if context:
        augmented_message = f"Context:\n{context}\n\nQuestion: {message}"
    else:
        augmented_message = message

    history.append({"role": "user", "content": augmented_message})

    response = requests.post(
        OPENROUTER_URL,
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": MODEL,
            "messages": history,
            "stream": True
        },
        stream=True
    )

    full_reply = ""
    for line in response.iter_lines():
        if not line:
            continue
        decoded = line.decode("utf-8")
        if decoded == "data: [DONE]":
            break
        if decoded.startswith("data: "):
            chunk = json.loads(decoded[6:])
            delta = chunk["choices"][0]["delta"].get("content", "")
            full_reply += delta
            yield delta

    history.append({"role": "assistant", "content": full_reply})