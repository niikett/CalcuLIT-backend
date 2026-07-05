import random

from fastapi import APIRouter, Depends, status, HTTPException, Query, Body
from app.schemas import *

router = APIRouter(
    prefix="/multiplication", 
    tags=["multiplication"]
)

@router.post(
    "/", 
    response_model=MultiplicationResponse,
    status_code=status.HTTP_201_CREATED
)
def multiplication_questions(
    multiplication_create_details: MultiplicationCreate = Body(..., examples={
        "num1_digits": 2,
        "num2_digits": 2,
        "questions": 5,
        "special_number": 12,
        "special_number_range_min": 10,
        "special_number_range_max": 20
    })
):
    try:    
        a = multiplication_create_details.num1_digits
        b = multiplication_create_details.num2_digits
        questions = multiplication_create_details.questions
        special_number = multiplication_create_details.special_number
        special_number_range_min = multiplication_create_details.special_number_range_min
        special_number_range_max = multiplication_create_details.special_number_range_max

        questions_list = []

        for _ in range(questions):
            num1 = random.randint(10**(a-1), 10**a-1)

            if special_number != 0:
                num2 = special_number
            elif special_number_range_max != 0 and special_number_range_min != 0:
                num2 = random.randint(special_number_range_min, special_number_range_max)
            else:
                num2 = random.randint(10**(b-1), 10**b-1)

            answer = num1 * num2

            questions_list.append(
                MultiplicationQuestion(
                    question=f"{num1} * {num2}", 
                    answer=answer
                )
            )

        formatted_record = {
            "questions_list": questions_list,
            "status_code": status.HTTP_201_CREATED
        }

        response_data = MultiplicationResponse(**formatted_record)

        return response_data
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": str(e),
                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR
            }
        )