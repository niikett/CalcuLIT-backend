import random

from fastapi import APIRouter, Depends, status, HTTPException, Query, Body
from app.schemas import *

router = APIRouter(
    prefix="/subtraction", 
    tags=["subtraction"]
)

@router.post(
    "/", 
    response_model=SubtractionResponse,
    status_code=status.HTTP_201_CREATED
)
def subtraction_questions(
    subtraction_create_details: SubtractionCreate = Body(..., examples={
        "num1_digits": 2,
        "num2_digits": 2,
        "questions": 5,
        "negative_answers": False
    })
):
    try:    
        a = subtraction_create_details.num1_digits
        b = subtraction_create_details.num2_digits
        questions = subtraction_create_details.questions

        questions_list = []

        for _ in range(questions):
            num1 = random.randint(10**(a-1), 10**a-1)
            num2 = random.randint(10**(b-1), 10**b-1)

            if num1 < num2:
                if not subtraction_create_details.negative_answers:                
                    num1, num2 = num2, num1

            answer = num1 - num2

            questions_list.append(
                SubtractionQuestion(
                    question=f"{num1} - {num2}", 
                    answer=answer
                )
            )

        formatted_record = {
            "questions_list": questions_list,
            "status_code": status.HTTP_201_CREATED
        }

        response_data = SubtractionResponse(**formatted_record)

        return response_data
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": str(e),
                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR
            }
        )