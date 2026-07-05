from pydantic import BaseModel
from typing import List, Union


class DivisionCreate(BaseModel):
    questions: int
    perfect_division: bool = False
    special_number: int = 0
    special_number_range_min: int = 0
    special_number_range_max: int = 0

class DivisionQuestion(BaseModel):
    question: str
    answer: Union[int, float]

class DivisionResponse(BaseModel):
    questions_list: List[DivisionQuestion]
    status_code: int
    