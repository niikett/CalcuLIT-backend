from pydantic import BaseModel
from typing import List


class ExponentsCreate(BaseModel):
    exponent: int
    upto: int
    root: bool = False

class ExponentsQuestion(BaseModel):
    question: str
    answer: int

class ExponentsResponse(BaseModel):
    questions_list: List[ExponentsQuestion]
    status_code: int