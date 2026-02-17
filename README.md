# End-of-Life Planning Chatbot

A conversational chatbot that guides users through end-of-life planning and generates a personalized advance directive document. Built with FastAPI and Claude.

## Prerequisites

- Python 3.11+
- An [Anthropic API key](https://console.anthropic.com/)

## Setup

1. Clone the repository and install dependencies:

   ```bash
   git clone <repo-url>
   cd eol-planning-chatbot
   pip install -r requirements.txt
   ```

2. Set your Anthropic API key:

   ```bash
   export ANTHROPIC_API_KEY=your-key-here
   ```

   Or create a `.env` file in the project root:

   ```
   ANTHROPIC_API_KEY=your-key-here
   ```

## Running the app

Start the development server:

```bash
uvicorn app.main:app --reload
```

Then open [http://localhost:8000](http://localhost:8000) in your browser.

## Running tests

```bash
# Run all tests
pytest tests/

# Run a single test
pytest tests/test_documents.py::test_render_advance_directive_contains_name
```
