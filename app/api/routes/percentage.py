import random

from fastapi import APIRouter, Depends, status, HTTPException, Query, Body
from app.schemas import *

router = APIRouter(
    prefix="/percentage", 
    tags=["percentage"]
)

@router.post(
    "/", 
    response_model=PercentageResponse,
    status_code=status.HTTP_201_CREATED
)
def percentage_questions(
    percentage_create_details: PercentageCreate = Body(..., examples={
        "num1_digits": 2,
        "num2_digits": 2,
        "questions": 5,
    })
):
    try:    
        a = percentage_create_details.num1_digits
        b = percentage_create_details.num2_digits
        questions = percentage_create_details.questions

        questions_list = []

        for _ in range(questions):
            num1 = random.randint(10**(a-1), 10**a-1)
            num2 = random.randint(10**(b-1), 10**b-1)
            answer = (num1 * num2) / 100

            if type(answer) == float:
                answer = round(answer, 2)

            questions_list.append(
                PercentageQuestion(
                    question=f"{num1}% of {num2}", 
                    answer=answer
                )
            )

        formatted_record = {
            "questions_list": questions_list,
            "status_code": status.HTTP_201_CREATED
        }

        response_data = PercentageResponse(**formatted_record)

        return response_data
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": str(e),
                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR
            }
        )