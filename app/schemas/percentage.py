from pydantic import BaseModel
from typing import List, Union


class PercentageCreate(BaseModel):
    num1_digits: int
    num2_digits: int
    questions: int

class PercentageQuestion(BaseModel):
    question: str
    answer: Union[int, float]

class PercentageResponse(BaseModel):
    questions_list: List[PercentageQuestion]
    status_code: int