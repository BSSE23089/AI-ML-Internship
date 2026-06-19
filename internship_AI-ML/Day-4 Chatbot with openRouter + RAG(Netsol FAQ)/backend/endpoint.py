# endpoint.py
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from model import ChatRequest
from services import get_response_stream, load_checkpoint, save_checkpoint
import uuid

app = FastAPI()

@app.post("/chat")
def chat(request: ChatRequest):
    if not request.session_id:
        request.session_id = str(uuid.uuid4())

    history = load_checkpoint(request.session_id)

    def event_generator():
        for chunk in get_response_stream(request.message, history):
            yield chunk
        save_checkpoint(request.session_id, history)

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={"X-Session-Id": request.session_id}
    )