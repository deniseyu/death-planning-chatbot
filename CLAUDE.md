# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run the dev server
uvicorn app.main:app --reload

# Run all tests
pytest tests/

# Run a single test
pytest tests/test_documents.py::test_render_advance_directive_contains_name
```

## Architecture

This is a FastAPI chatbot that guides users through end-of-life planning via a multi-turn conversation with Claude, then generates an advance directive document from the collected information.

**Two-pass AI design:**
1. **Conversation pass** (`chat.py:chat`): Interactive multi-turn dialogue using `SYSTEM_PROMPT`. The prompt instructs Claude to cover five topics in order (personal info, healthcare wishes, funeral preferences, messages, assets) and emit a `[PLANNING_COMPLETE]` marker when done.
2. **Extraction pass** (`chat.py:extract_structured_data`): Takes the full conversation transcript and asks Claude to produce a structured JSON object matching a specific schema (defined in `EXTRACTION_PROMPT`). This JSON is then rendered into a Markdown document via a Jinja2 template (`app/templates/advance_directive.md`).

**Session state** is an in-memory dict (`chat.py:sessions`) mapping session IDs to message history lists. Sessions are lost on restart.

**Frontend** is a single vanilla HTML/JS page (`app/static/index.html`) served by FastAPI at `/`. It generates a UUID session ID on load, calls `/chat` for conversation turns, and calls `/document/{session_id}` to generate the final document. Markdown in responses is rendered with `marked.js` from CDN.

## Key conventions

- The Claude model used is `claude-sonnet-4-5-20250929` (set in `chat.py`)
- Completion detection relies on the magic string `[PLANNING_COMPLETE]` — this marker is stripped before displaying to the user
- Prompts are centralized in `prompts.py`; the extraction prompt defines the exact JSON schema the template expects
- The Jinja2 template handles null/missing values gracefully — the extraction prompt specifies null for unaddressed topics
