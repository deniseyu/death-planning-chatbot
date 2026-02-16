from dotenv import load_dotenv

load_dotenv()

import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

from app.chat import chat, extract_structured_data
from app.documents import render_advance_directive

app = FastAPI(title="End-of-Life Planning Chatbot")

_static_dir = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=_static_dir), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    session_id: str
    message: str


class ChatResponse(BaseModel):
    response: str
    complete: bool


@app.get("/")
def root():
    return FileResponse(os.path.join(_static_dir, "index.html"))


@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(req: ChatRequest):
    result = chat(req.session_id, req.message)
    return result


@app.post("/document/{session_id}")
def generate_document(session_id: str):
    try:
        data = extract_structured_data(session_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    markdown = render_advance_directive(data)
    return {"document": markdown}
