import json
import os

import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.5-flash")


def get_question():
    question_generation_prompt = (
        "Generate an interview question for a Python backend developer "
        "(medium level). Just one sentence, no explanations."
    )
    fallback_question = (
        "Explain the difference between multithreading, multiprocessing, "
        "and asyncio in Python."
    )

    try:
        question = model.generate_content(question_generation_prompt)
        return question.text
    except Exception:
        return fallback_question


def _fallback_feedback(message: str):
    return {
        "score": 0.0,
        "feedback": message,
        "improvement": (
            "Review the answer for correctness, clarity, structure, and depth."
        ),
    }


def generate_feedback(answer: str, question: str):
    prompt = f"""
Return strict JSON with exactly these keys:
- score: number from 0 to 10
- feedback: short paragraph on strengths and weaknesses
- improvement: short paragraph with concrete suggestions

Do not wrap the JSON in markdown fences.

Question: {question}
Answer: {answer}
"""

    if not api_key:
        return _fallback_feedback(
            "Gemini API key is missing. Set GEMINI_API_KEY in .env and restart the backend."
        )

    try:
        response = model.generate_content(prompt)
        raw_text = response.text.strip() if response.text else ""
        parsed = json.loads(raw_text)

        score = parsed.get("score", 0)
        try:
            score = float(score)
        except (TypeError, ValueError):
            score = 0.0

        return {
            "score": score,
            "feedback": str(parsed.get("feedback", "")).strip(),
            "improvement": str(parsed.get("improvement", "")).strip(),
        }
    except Exception as exc:
        return _fallback_feedback(
            f"Feedback could not be generated from the AI service. Error: {exc}"
        )
