import os
import json
from anthropic import Anthropic
from app.prompts import SYSTEM_PROMPT, EXTRACTION_PROMPT

COMPLETION_MARKER = "[PLANNING_COMPLETE]"

client = Anthropic()  # uses ANTHROPIC_API_KEY env var

# In-memory session store: session_id -> list of message dicts
sessions: dict[str, list[dict]] = {}


def get_or_create_session(session_id: str) -> list[dict]:
    if session_id not in sessions:
        sessions[session_id] = []
    return sessions[session_id]


def chat(session_id: str, user_message: str) -> dict:
    """Send a user message and return the assistant reply plus completion flag."""
    history = get_or_create_session(session_id)
    history.append({"role": "user", "content": user_message})

    response = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=history,
    )

    assistant_text = response.content[0].text
    complete = COMPLETION_MARKER in assistant_text

    # Strip the marker from the text shown to the user
    display_text = assistant_text.replace(COMPLETION_MARKER, "").strip()

    history.append({"role": "assistant", "content": assistant_text})

    return {"response": display_text, "complete": complete}


def extract_structured_data(session_id: str) -> dict:
    """Use Claude to extract structured JSON from the conversation transcript."""
    history = sessions.get(session_id, [])
    if not history:
        raise ValueError(f"No conversation found for session {session_id}")

    transcript = "\n".join(
        f"{msg['role'].upper()}: {msg['content']}" for msg in history
    )

    response = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=2048,
        messages=[
            {
                "role": "user",
                "content": EXTRACTION_PROMPT + transcript,
            }
        ],
    )

    raw = response.content[0].text
    return json.loads(raw)
