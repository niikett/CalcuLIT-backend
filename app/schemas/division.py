from uuid import UUID
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Union
from datetime import datetime

class DivisionQuestionResponse(BaseModel):
    question: str
    answer: Union[int, float]
    given_answer: Optional[Union[int, float]] = None
    is_correct: Optional[bool] = None
    time_taken: Optional[float] = None

    @field_validator("time_taken")
    @classmethod
    def round_time(cls, value):
        if value is None:
            return value
        return round(value, 2)

class DivisionCreate(BaseModel):
    questions: int
    perfect_division: bool = False
    special_number: int = 0
    special_number_range_min: int = 0
    special_number_range_max: int = 0

class DivisionResponse(BaseModel):
    division_practice_id: UUID
    questions: List[DivisionQuestionResponse]
    total_time_taken: float

    @field_validator("total_time_taken")
    @classmethod
    def round_time(cls, value):
        if value is None:
            return value
        return round(value, 2)

class DivisionServerResponse(BaseModel):
    division_practice_id: UUID
    questions: List[DivisionQuestionResponse]
    score: Optional[str] = None
    total_time_taken: Optional[float] = None
    created_at: Optional[datetime] = None
    status_code: int

    class Config:
        from_attributes = True
