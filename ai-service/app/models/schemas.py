from pydantic import BaseModel
from typing import List

class GenerateQuestionRequest(BaseModel):
    interview_type: str
    difficulty: str = "medium"

class GenerateQuestionResponse(BaseModel):
    question: str

class EvaluateAnswerRequest(BaseModel):
    question: str
    answer: str
    interview_type: str

class EvaluateAnswerResponse(BaseModel):
    score: int
    feedback: str
    missed_points: List[str]