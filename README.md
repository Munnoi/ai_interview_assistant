# AI Interview Assistant

AI Interview Assistant is a lightweight practice app for Python backend interview prep. It serves a static frontend for answering interview questions and a FastAPI backend that generates questions and returns AI-based feedback on your responses.

## What It Does

- Generates a backend-focused interview question
- Lets you submit a written answer in the browser
- Analyzes the answer and returns:
  - a score
  - short feedback
  - concrete improvement suggestions
- Falls back gracefully when the Gemini API key is missing or the model request fails

## Tech Stack

- Backend: FastAPI
- Frontend: HTML, CSS, vanilla JavaScript
- AI provider: Google Gemini via `google-generativeai`
- Environment loading: `python-dotenv`

## Project Structure

```text
ai_interview_assistant/
├── app/
│   ├── api/
│   ├── models/
│   ├── services/
│   └── main.py
├── frontend/
│   ├── index.html
│   ├── interview.html
│   ├── feedback.html
│   └── styles.css
└── requirements.txt
```

## Requirements

- Python 3.10+
- A browser
- Optional: a Gemini API key for AI-generated feedback

## Setup

1. Clone the repository and enter it.
2. Create a virtual environment.
3. Install dependencies.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file in the project root if you want live Gemini feedback:

```env
GEMINI_API_KEY=your_api_key_here
```

If `GEMINI_API_KEY` is not set, the app still works, but feedback will use a fallback response instead of Gemini.

## Running the App

You need to run the backend and frontend separately.

### 1. Start the FastAPI backend

Run this from the `app/` directory:

```bash
cd app
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

### 2. Start the frontend

The frontend fetches the API from a browser origin on port `5500`, so serve the `frontend/` directory on that port.

If you use VS Code Live Server, open `frontend/index.html` with Live Server so it runs at:

```text
http://127.0.0.1:5500
```

or

```text
http://localhost:5500
```

Those are the two origins currently allowed by the backend CORS configuration.

## How to Use

1. Open the frontend in your browser.
2. Click **Start Interview**.
3. Read the generated question.
4. Enter your answer and submit it.
5. Review the score, feedback, and improvement suggestions.

## API Endpoints

### `GET /`

Health-style root endpoint.

Response:

```json
{ "message": "Hello World" }
```

### `GET /question`

Returns a generated interview question.

Response:

```json
{ "question": "Explain the difference between multithreading, multiprocessing, and asyncio in Python." }
```

### `POST /answer`

Stores a submitted answer in memory.

Request body:

```json
{ "answer": "Your answer here" }
```

Response:

```json
{ "message": "Answer submitted" }
```

### `POST /analyze`

Returns structured feedback for a question-answer pair.

Request body:

```json
{
  "question": "What is dependency injection?",
  "answer": "Dependency injection is..."
}
```

Response:

```json
{
  "score": 8.5,
  "feedback": "Clear explanation with solid fundamentals.",
  "improvement": "Add tradeoffs and a practical backend example."
}
```

## Notes

- Submitted answers are stored only in an in-memory list and are not persisted.
- The `/answer` endpoint currently stores a newly generated question instead of the question shown in the UI.
- Feedback is saved in browser `localStorage` to power the feedback page.

## Troubleshooting

- `ModuleNotFoundError`: Make sure your virtual environment is activated and dependencies are installed.
- CORS errors in the browser: Serve the frontend from `http://127.0.0.1:5500` or `http://localhost:5500`.
- Missing AI feedback: Check that `.env` exists and `GEMINI_API_KEY` is set, then restart the backend.

## Future Improvements

- Persist interview history in a database
- Add question categories and difficulty levels
- Support voice answers and transcription
- Track progress across sessions
- Improve error handling and loading states in the frontend
