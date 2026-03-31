from fastapi import APIRouter

from services.ai_service import analyze_answer
from services.feedback import get_question as generate_question
from models.schemas import AnswerRequest, FeedbackRequest, FeedbackResponse

router = APIRouter()

answers_db = []

@router.get("/")
def root():
    return {"message": "Hello World"}

@router.get("/question")
def get_question_route():
    question = generate_question()
    return {"question": question}

@router.post("/answer")
def submit_answer(data: AnswerRequest):
    record = {
        "question": generate_question(),
        "answer": data.answer
    }

    answers_db.append(record)
    return {"message": "Answer submitted"}

@router.post("/analyze", response_model=FeedbackResponse)
def analyze(data: FeedbackRequest):
    return analyze_answer(data.answer, data.question)
