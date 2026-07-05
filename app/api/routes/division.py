import random

from fastapi import APIRouter, Depends, status, HTTPException, Query, Body
from app.schemas import *

router = APIRouter(
    prefix="/division", 
    tags=["division"]
)


@router.post(
    "/", 
    response_model=DivisionResponse,
    status_code=status.HTTP_201_CREATED
)
def division_questions(
    division_create_details: DivisionCreate = Body(..., examples={
        "questions": 5,
        "perfect_division": False,
        "special_number": 12,
        "special_number_range_min": 10,
        "special_number_range_max": 20
    })
):
    try:    
        questions = division_create_details.questions
        perfect_division = division_create_details.perfect_division
        special_number = division_create_details.special_number
        special_number_range_min = division_create_details.special_number_range_min
        special_number_range_max = division_create_details.special_number_range_max

        questions_list = []

        for _ in range(questions):
            if special_number != 0:
                num2 = special_number
                num1 = random.randint(1, 100) * num2
            elif special_number_range_max != 0 and special_number_range_min != 0:
                num2 = random.randint(special_number_range_min, special_number_range_max)
                num1 = random.randint(1, 100) * num2
            else:
                num2 = random.randint(1, 100)
                num1 = random.randint(1, 100) * num2

            if perfect_division:
                answer = num1 // num2
            else:
                num1 = num1 + random.randint(1, num2 - 1)
                answer = round(num1 / num2, 2)

            questions_list.append(
                DivisionQuestion(
                    question=f"{num1} / {num2}", 
                    answer=answer
                )
            )

        formatted_record = {
            "questions_list": questions_list,
            "status_code": status.HTTP_201_CREATED
        }

        response_data = DivisionResponse(**formatted_record)

        return response_data
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": str(e),
                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR
            }
        )