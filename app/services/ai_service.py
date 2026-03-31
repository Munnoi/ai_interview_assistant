from .feedback import generate_feedback


def analyze_answer(answer: str, question: str):
    return generate_feedback(answer, question)
