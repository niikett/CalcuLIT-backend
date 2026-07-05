from pydantic import BaseModel
from typing import List


class SubtractionCreate(BaseModel):
    num1_digits: int
    num2_digits: int
    questions: int
    negative_answers: bool = False

class SubtractionQuestion(BaseModel):
    question: str
    answer: int

class SubtractionResponse(BaseModel):
    questions_list: List[SubtractionQuestion]
    status_code: int
    