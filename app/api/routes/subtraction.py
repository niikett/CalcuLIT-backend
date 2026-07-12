import random

from sqlalchemy.orm import Session

from fastapi import status, HTTPException, Depends, APIRouter, Body, Query

from app.schemas import *
from app.models import *
from app.schemas import *
from app.core.config_db import get_db

router = APIRouter(
    prefix="/subtraction", 
    tags=["subtraction"]
)


@router.post(
    "/", 
    response_model=SubtractionServerResponse,
    status_code=status.HTTP_201_CREATED
)
def subtraction_questions(
    subtraction_create_details: SubtractionCreate = Body(..., examples={
        "num1_digits": 2,
        "num2_digits": 2,
        "questions": 5
    }),
    db: Session = Depends(get_db),
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
                SubtractionQuestionResponse(
                    question = f"{num1} - {num2}", 
                    answer = answer
                )
            )

        new_subtraction_practice = Subtraction(
            questions = [q.model_dump() for q in questions_list]
        )

        db.add(new_subtraction_practice)
        db.flush()

        response_model = {
            "subtraction_practice_id": new_subtraction_practice.subtraction_practice_id,
            "questions": questions_list,
            "created_at": new_subtraction_practice.created_at,
            "status_code": status.HTTP_201_CREATED,
        }

        db.commit()

        return SubtractionServerResponse(**response_model)
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
    response_model=SubtractionServerResponse,
    status_code=status.HTTP_201_CREATED
)
def subtraction_practice_response(
    subtraction_practice_response_details: SubtractionResponse= Body(..., examples={
        "subtraction_practice_id": "123e4567-e89b-12d3-a456-426614174000",
        "questions": [
            {
                "question": "12 - 34",
                "answer": -22,
                "given_answer": 46,
                "time_taken": 3.5
            },
            {
                "question": "78 - 56",
                "answer": 22,
                "given_answer": 13,
                "time_taken": 7.89
            }
        ],
        "total_time_taken": 15.75
    }),
    db: Session = Depends(get_db),
):
    try:    
        subtraction_practice_id = subtraction_practice_response_details.subtraction_practice_id
        questions = subtraction_practice_response_details.questions
        total_time_taken = subtraction_practice_response_details.total_time_taken

        subtraction_practice = db.query(Subtraction).filter(Subtraction.subtraction_practice_id == subtraction_practice_id).first()

        if not subtraction_practice:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "error": "No subtraction practice found with the given ID",
                    "status_code": status.HTTP_404_NOT_FOUND
                }
            )

        subtraction_practice.questions = []

        score = 0
        out_of = 0
        for question in questions:
            question.is_correct = question.answer == question.given_answer

            if question.is_correct:
                score += 1
            out_of += 1

        subtraction_practice.questions = [response.model_dump() for response in questions]
        subtraction_practice.score = f"{score}/{out_of}"
        subtraction_practice.total_time_taken = total_time_taken

        response_model = {
            "subtraction_practice_id": subtraction_practice_id,
            "questions": questions,
            "score": subtraction_practice.score,
            "total_time_taken": subtraction_practice.total_time_taken,
            "created_at": subtraction_practice.created_at,
            "status_code": status.HTTP_201_CREATED,   
        }

        db.commit()

        return SubtractionServerResponse(**response_model)
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
    response_model=List[SubtractionServerResponse],
)
def subtraction_practice_data(
    subtraction_practice_id: Optional[UUID] = Query(None),
    db: Session = Depends(get_db),
):
    if subtraction_practice_id is None:
        subtraction_practice = (
            db.query(Subtraction)
            .order_by(Subtraction.created_at.desc())
            .all()
        )
    else:
        subtraction_practice = [
            db.query(Subtraction)
            .filter(Subtraction.subtraction_practice_id == subtraction_practice_id)
            .first()
        ]

    if not subtraction_practice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": "No subtraction practice found with the given ID",
                "status_code": status.HTTP_404_NOT_FOUND
            }
        )
    
    response_model = []

    for practice in subtraction_practice:
        response_model.append(
            SubtractionServerResponse(
                subtraction_practice_id = practice.subtraction_practice_id,
                questions = [SubtractionQuestionResponse(**q) for q in practice.questions],
                score = practice.score,
                total_time_taken = practice.total_time_taken,
                created_at = practice.created_at,
                status_code = status.HTTP_200_OK,
            )
        )

    return response_model