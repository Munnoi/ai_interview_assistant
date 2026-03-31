from pydantic import BaseModel


class AnswerRequest(BaseModel):
    answer: str


class FeedbackResponse(BaseModel):
    score: float
    feedback: str
    improvement: str


class FeedbackRequest(BaseModel):
    question: str
    answer: str
