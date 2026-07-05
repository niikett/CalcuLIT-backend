import random

from fastapi import APIRouter, Depends, status, HTTPException, Query, Body
from app.schemas import *

router = APIRouter(
    prefix="/exponents", 
    tags=["exponents"]
)

@router.post(
    "/", 
    response_model=ExponentsResponse,
    status_code=status.HTTP_201_CREATED
)
def exponents_questions(
        exponents_create_details: ExponentsCreate = Body(..., examples={
        "exponent": 2,
        "upto": 30,
        "root": False
    })
):
    try:
        exponent = exponents_create_details.exponent
        upto = exponents_create_details.upto
        root = exponents_create_details.root

        numbers = list(range(1, upto + 1))
        random.shuffle(numbers)
        exponents = [num ** exponent for num in numbers]
        
        questions_list = []
        for i in range(upto):
            if root:
                questions_list.append(
                    ExponentsQuestion(
                        question=f"{exponents[i]}^(1/{exponent})", 
                        answer=numbers[i]
                    )
                )
            else:
                questions_list.append(
                    ExponentsQuestion(
                        question=f"{numbers[i]}^{exponent}", 
                        answer=exponents[i]
                    )
                )

        formatted_record = {
            "questions_list": questions_list,
            "status_code": status.HTTP_201_CREATED
        }

        response_data = ExponentsResponse(**formatted_record)

        return response_data
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": str(e),
                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR
            }
        )