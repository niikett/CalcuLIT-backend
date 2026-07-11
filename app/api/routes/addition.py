import random

from sqlalchemy.orm import Session

from fastapi import status, HTTPException, Depends, APIRouter, Body, Query

from app.schemas import *
from app.models import *
from app.schemas import *
from app.core.config_db import get_db

router = APIRouter(
    prefix="/addition", 
    tags=["addition"]
)


@router.post(
    "/", 
    response_model=AdditionServerResponse,
    status_code=status.HTTP_201_CREATED
)
def addition_questions(
    addition_create_details: AdditionCreate = Body(..., examples={
        "num1_digits": 2,
        "num2_digits": 2,
        "questions": 5
    }),
    db: Session = Depends(get_db),
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
                AdditionQuestionResponse(
                    question = f"{num1} + {num2}", 
                    answer = answer
                )
            )

        new_addition_practice = Addition(
            questions = [q.model_dump() for q in questions_list]
        )

        db.add(new_addition_practice)
        db.flush()

        response_model = {
            "addition_practice_id": new_addition_practice.addition_practice_id,
            "questions": questions_list,
            "created_at": new_addition_practice.created_at,
            "status_code": status.HTTP_201_CREATED,
        }

        db.commit()

        return AdditionServerResponse(**response_model)
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
    "/practice-response",
    response_model=AdditionServerResponse,
    status_code=status.HTTP_201_CREATED
)
def addition_practice_response(
    addition_practice_response_details: AdditionResponse= Body(..., examples={
        "addition_practice_id": "123e4567-e89b-12d3-a456-426614174000",
        "questions": [
            {
                "question": "12 + 34",
                "answer": 46,
                "given_answer": 46,
                "time_taken": 3.5
            },
            {
                "question": "56 + 78",
                "answer": 134,
                "given_answer": 130,
                "time_taken": 7.89
            }
        ],
        "total_time_taken": 15.75
    }),
    db: Session = Depends(get_db),
):
    try:    
        addition_practice_id = addition_practice_response_details.addition_practice_id
        questions = addition_practice_response_details.questions
        total_time_taken = addition_practice_response_details.total_time_taken

        addition_practice = db.query(Addition).filter(Addition.addition_practice_id == addition_practice_id).first()

        if not addition_practice:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "error": "No addition practice found with the given ID",
                    "status_code": status.HTTP_404_NOT_FOUND
                }
            )

        addition_practice.questions = []

        score = 0
        out_of = 0
        for question in questions:
            question.is_correct = question.answer == question.given_answer

            if question.is_correct:
                score += 1
            out_of += 1

        addition_practice.questions = [response.model_dump() for response in questions]
        addition_practice.score = f"{score}/{out_of}"
        addition_practice.total_time_taken = total_time_taken

        response_model = {
            "addition_practice_id": addition_practice_id,
            "questions": questions,
            "score": addition_practice.score,
            "total_time_taken": addition_practice.total_time_taken,
            "created_at": addition_practice.created_at,
            "status_code": status.HTTP_201_CREATED,   
        }

        db.commit()

        return AdditionServerResponse(**response_model)
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
    response_model=List[AdditionServerResponse],
)
def addition_practice_data(
    addition_practice_id: Optional[UUID] = Query(None),
    db: Session = Depends(get_db),
):
    if addition_practice_id is None:
        addition_practice = (
            db.query(Addition)
            .order_by(Addition.created_at.desc())
            .all()
        )
    else:
        addition_practice = [
            db.query(Addition)
            .filter(Addition.addition_practice_id == addition_practice_id)
            .first()
        ]

    if not addition_practice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": "No addition practice found with the given ID",
                "status_code": status.HTTP_404_NOT_FOUND
            }
        )
    
    response_model = []

    for practice in addition_practice:
        response_model.append(
            AdditionServerResponse(
                addition_practice_id = practice.addition_practice_id,
                questions = [AdditionQuestionResponse(**q) for q in practice.questions],
                score = practice.score,
                total_time_taken = practice.total_time_taken,
                created_at = practice.created_at,
                status_code = status.HTTP_200_OK,
            )
        )

    return response_model