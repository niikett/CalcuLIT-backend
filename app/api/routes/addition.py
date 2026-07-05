import random

from fastapi import APIRouter, Depends, status, HTTPException, Query, Body
from app.schemas import *

router = APIRouter(
    prefix="/addition", 
    tags=["addition"]
)

@router.post(
    "/", 
    response_model=AdditionResponse,
    status_code=status.HTTP_201_CREATED
)
def addition_questions(
    addition_create_details: AdditionCreate = Body(..., examples={
        "num1_digits": 2,
        "num2_digits": 2,
        "questions": 5
    })
):
    try:    
        a = addition_create_details.num1_digits
        b = addition_create_details.num2_digits
        questions = addition_create_details.questions

        questions_list = []

        for _ in range(questions):
            num1 = random.randint(10**(a-1), 10**a-1)
            num2 = random.randint(10**(b-1), 10**b-1)
            answer = num1 + num2

            questions_list.append(
                AdditionQuestion(
                    question=f"{num1} + {num2}", 
                    answer=answer
                )
            )

        formatted_record = {
            "questions_list": questions_list,
            "status_code": status.HTTP_201_CREATED
        }

        response_data = AdditionResponse(**formatted_record)

        return response_data
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": str(e),
                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR
            }
        )