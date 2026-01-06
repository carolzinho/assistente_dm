from fastapi import FastAPI
from pydantic import BaseModel
from router import route_message

app = FastAPI(title="dm_assistant API")


class MessageInput(BaseModel):
    message: str


class MessageOutput(BaseModel):
    reply: str


@app.post("/message", response_model=MessageOutput)
def message_endpoint(payload: MessageInput):
    reply = route_message(payload.message)
    return {"reply": reply}
