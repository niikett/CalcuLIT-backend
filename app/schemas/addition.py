from pydantic import BaseModel
from typing import List


class AdditionCreate(BaseModel):
    num1_digits: int
    num2_digits: int
    questions: int

class AdditionQuestion(BaseModel):
    question: str
    answer: int

class AdditionResponse(BaseModel):
    questions_list: List[AdditionQuestion]
    status_code: int