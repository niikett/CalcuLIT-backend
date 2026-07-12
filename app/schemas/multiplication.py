from uuid import UUID
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from datetime import datetime

class MultiplicationQuestionResponse(BaseModel):
    question: str
    answer: int
    given_answer: Optional[int] = None
    is_correct: Optional[bool] = None
    time_taken: Optional[float] = None

    @field_validator("time_taken")
    @classmethod
    def round_time(cls, value):
        if value is None:
            return value
        return round(value, 2)

class MultiplicationCreate(BaseModel):
    num1_digits: int
    num2_digits: int
    questions: int
    special_number: int = 0
    special_number_range_min: int = 0
    special_number_range_max: int = 0

class MultiplicationResponse(BaseModel):
    multiplication_practice_id: UUID
    questions: List[MultiplicationQuestionResponse]
    total_time_taken: float

    @field_validator("total_time_taken")
    @classmethod
    def round_time(cls, value):
        if value is None:
            return value
        return round(value, 2)

class MultiplicationServerResponse(BaseModel):
    multiplication_practice_id: UUID
    questions: List[MultiplicationQuestionResponse]
    score: Optional[str] = None
    total_time_taken: Optional[float] = None
    created_at: Optional[datetime] = None
    status_code: int

    class Config:
        from_attributes = True
