from uuid import UUID
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from datetime import datetime

class ExponentQuestionResponse(BaseModel):
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

class ExponentCreate(BaseModel):
    exponent: int
    upto: int
    root: bool = False

class ExponentResponse(BaseModel):
    exponent_practice_id: UUID
    questions: List[ExponentQuestionResponse]
    total_time_taken: float

    @field_validator("total_time_taken")
    @classmethod
    def round_time(cls, value):
        if value is None:
            return value
        return round(value, 2)

class ExponentServerResponse(BaseModel):
    exponent_practice_id: UUID
    questions: List[ExponentQuestionResponse]
    score: Optional[str] = None
    total_time_taken: Optional[float] = None
    created_at: Optional[datetime] = None
    status_code: int

    class Config:
        from_attributes = True
