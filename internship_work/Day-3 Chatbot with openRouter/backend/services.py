from config import OPENROUTER_API_KEY, OPENROUTER_URL, MODEL
import requests
import json
from pymongo import MongoClient
from config import MONGO_URI


mongo_client = MongoClient(MONGO_URI)

db = mongo_client["chatbot_db"]
checkpoints = db["checkpoints"]


def save_checkpoint(session_id: str, history: list):
    print("Saving checkpoint for session:", session_id)
    checkpoints.update_one(
        {"session_id": session_id},
        {"$set": {"history": history}},
        upsert=True
    )
print("Checkpoint saved for session:")

def load_checkpoint(session_id: str) -> list:
    checkpoint = checkpoints.find_one({"session_id": session_id})
  
    if checkpoint:
        return checkpoint["history"]
    return [{"role": "system", "content": "You are a helpful assistant."}]

def get_response_stream(message, history):
    history.append({"role": "user", "content": message})

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
    print("STATUS CODE:", response.status_code)  

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