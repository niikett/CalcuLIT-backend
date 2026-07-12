import random

from sqlalchemy.orm import Session

from fastapi import status, HTTPException, Depends, APIRouter, Body, Query

from app.schemas import *
from app.models import *
from app.schemas import *
from app.core.config_db import get_db

router = APIRouter(
    prefix="/multiplication", 
    tags=["multiplication"]
)


@router.post(
    "/", 
    response_model=MultiplicationServerResponse,
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
    }),
    db: Session = Depends(get_db),
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
                MultiplicationQuestionResponse(
                    question=f"{num1} * {num2}", 
                    answer=answer
                )
            )

        new_multiplication_practice = Multiplication(
            questions = [q.model_dump() for q in questions_list]
        )

        db.add(new_multiplication_practice)
        db.flush()

        response_model = {
            "multiplication_practice_id": new_multiplication_practice.multiplication_practice_id,
            "questions": questions_list,
            "created_at": new_multiplication_practice.created_at,
            "status_code": status.HTTP_201_CREATED,
        }

        db.commit()

        return MultiplicationServerResponse(**response_model)
    except Exception as e:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": str(e),
                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR
            }
        )


@router.put(
    "/",
    response_model=MultiplicationServerResponse,
    status_code=status.HTTP_201_CREATED
)
def multiplication_practice_response(
    multiplication_practice_response_details: MultiplicationResponse= Body(..., examples={
        "multiplication_practice_id": "123e4567-e89b-12d3-a456-426614174000",
        "questions": [
            {
                "question": "12 * 12",
                "answer": 144,
                "given_answer": 144,
                "time_taken": 3.5
            },
            {
                "question": "20 * 50",
                "answer": 1000,
                "given_answer": 100,
                "time_taken": 7.89
            }
        ],
        "total_time_taken": 15.75
    }),
    db: Session = Depends(get_db),
):
    try:    
        multiplication_practice_id = multiplication_practice_response_details.multiplication_practice_id
        questions = multiplication_practice_response_details.questions
        total_time_taken = multiplication_practice_response_details.total_time_taken

        multiplication_practice = db.query(Multiplication).filter(Multiplication.multiplication_practice_id == multiplication_practice_id).first()

        if not multiplication_practice:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "error": "No multiplication practice found with the given ID",
                    "status_code": status.HTTP_404_NOT_FOUND
                }
            )

        multiplication_practice.questions = []

        score = 0
        out_of = 0
        for question in questions:
            question.is_correct = question.answer == question.given_answer

            if question.is_correct:
                score += 1
            out_of += 1

        multiplication_practice.questions = [response.model_dump() for response in questions]
        multiplication_practice.score = f"{score}/{out_of}"
        multiplication_practice.total_time_taken = total_time_taken

        response_model = {
            "multiplication_practice_id": multiplication_practice_id,
            "questions": questions,
            "score": multiplication_practice.score,
            "total_time_taken": multiplication_practice.total_time_taken,
            "created_at": multiplication_practice.created_at,
            "status_code": status.HTTP_201_CREATED,   
        }

        db.commit()

        return MultiplicationServerResponse(**response_model)
    except Exception as e:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": str(e),
                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR
            }
        )
  

@router.get(
    "/",
    response_model=List[MultiplicationServerResponse],
)
def multiplication_practice_data(
    multiplication_practice_id: Optional[UUID] = Query(None),
    db: Session = Depends(get_db),
):
    if multiplication_practice_id is None:
        multiplication_practice = (
            db.query(Multiplication)
            .order_by(Multiplication.created_at.desc())
            .all()
        )
    else:
        multiplication_practice = [
            db.query(Multiplication)
            .filter(Multiplication.multiplication_practice_id == multiplication_practice_id)
            .first()
        ]

    if not multiplication_practice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": "No multiplication practice found with the given ID",
                "status_code": status.HTTP_404_NOT_FOUND
            }
        )
    
    response_model = []

    for practice in multiplication_practice:
        response_model.append(
            MultiplicationServerResponse(
                multiplication_practice_id = practice.multiplication_practice_id,
                questions = [MultiplicationQuestionResponse(**q) for q in practice.questions],
                score = practice.score,
                total_time_taken = practice.total_time_taken,
                created_at = practice.created_at,
                status_code = status.HTTP_200_OK,
            )
        )

    return response_model