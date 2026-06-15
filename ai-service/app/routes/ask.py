from fastapi import APIRouter, HTTPException
from app.models.schemas import (
    GenerateQuestionRequest, GenerateQuestionResponse,
    EvaluateAnswerRequest, EvaluateAnswerResponse
)
from app.services.llm import generate_question, evaluate_answer

router = APIRouter()

@router.post("/generate-question", response_model=GenerateQuestionResponse)
def generate_question_route(req: GenerateQuestionRequest):
    try:
        question = generate_question(req.interview_type, req.difficulty)
        return GenerateQuestionResponse(question=question)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/evaluate-answer", response_model=EvaluateAnswerResponse)
def evaluate_answer_route(req: EvaluateAnswerRequest):
    result = evaluate_answer(req.question, req.answer, req.interview_type)
    return EvaluateAnswerResponse(**result)