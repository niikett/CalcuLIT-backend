from pydantic import BaseModel
from typing import List


class MultiplicationCreate(BaseModel):
    num1_digits: int
    num2_digits: int
    questions: int
    special_number: int = 0
    special_number_range_min: int = 0
    special_number_range_max: int = 0

class MultiplicationQuestion(BaseModel):
    question: str
    answer: int

class MultiplicationResponse(BaseModel):
    questions_list: List[MultiplicationQuestion]
    status_code: int
    