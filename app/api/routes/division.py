import random

from sqlalchemy.orm import Session

from fastapi import status, HTTPException, Depends, APIRouter, Body, Query

from app.schemas import *
from app.models import *
from app.schemas import *
from app.core.config_db import get_db

router = APIRouter(
    prefix="/division", 
    tags=["division"]
)


@router.post(
    "/", 
    response_model=DivisionServerResponse,
    status_code=status.HTTP_201_CREATED
)
def division_questions(
    division_create_details: DivisionCreate = Body(..., examples={
        "questions": 5,
        "perfect_division": False,
        "special_number": 12,
        "special_number_range_min": 10,
        "special_number_range_max": 20
    }),
    db: Session = Depends(get_db),
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
                DivisionQuestionResponse(
                    question=f"{num1} / {num2}", 
                    answer=answer
                )
            )

        new_division_practice = Division(
            questions = [q.model_dump() for q in questions_list]
        )

        db.add(new_division_practice)
        db.flush()

        response_model = {
            "division_practice_id": new_division_practice.division_practice_id,
            "questions": questions_list,
            "created_at": new_division_practice.created_at,
            "status_code": status.HTTP_201_CREATED,
        }

        db.commit()

        return DivisionServerResponse(**response_model)
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
    response_model=DivisionServerResponse,
    status_code=status.HTTP_201_CREATED
)
def division_practice_response(
    division_practice_response_details: DivisionResponse= Body(..., examples={
        "division_practice_id": "123e4567-e89b-12d3-a456-426614174000",
        "questions": [
            {
                "question": "36 / 6",
                "answer": 6,
                "given_answer": 6,
                "time_taken": 3.5
            },
            {
                "question": "70 / 7",
                "answer": 10,
                "given_answer": 10,
                "time_taken": 7.89
            }
        ],
        "total_time_taken": 15.75
    }),
    db: Session = Depends(get_db),
):
    try:    
        division_practice_id = division_practice_response_details.division_practice_id
        questions = division_practice_response_details.questions
        total_time_taken = division_practice_response_details.total_time_taken

        division_practice = db.query(Division).filter(Division.division_practice_id == division_practice_id).first()

        if not division_practice:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "error": "No division practice found with the given ID",
                    "status_code": status.HTTP_404_NOT_FOUND
                }
            )

        division_practice.questions = []

        score = 0
        out_of = 0
        for question in questions:
            question.is_correct = question.answer == question.given_answer

            if question.is_correct:
                score += 1
            out_of += 1

        division_practice.questions = [response.model_dump() for response in questions]
        division_practice.score = f"{score}/{out_of}"
        division_practice.total_time_taken = total_time_taken

        response_model = {
            "division_practice_id": division_practice_id,
            "questions": questions,
            "score": division_practice.score,
            "total_time_taken": division_practice.total_time_taken,
            "created_at": division_practice.created_at,
            "status_code": status.HTTP_201_CREATED,   
        }

        db.commit()

        return DivisionServerResponse(**response_model)
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
    response_model=List[DivisionServerResponse],
)
def division_practice_data(
    division_practice_id: Optional[UUID] = Query(None),
    db: Session = Depends(get_db),
):
    if division_practice_id is None:
        division_practice = (
            db.query(Division)
            .order_by(Division.created_at.desc())
            .all()
        )
    else:
        division_practice = [
            db.query(Division)
            .filter(Division.division_practice_id == division_practice_id)
            .first()
        ]

    if not division_practice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": "No division practice found with the given ID",
                "status_code": status.HTTP_404_NOT_FOUND
            }
        )
    
    response_model = []

    for practice in division_practice:
        response_model.append(
            DivisionServerResponse(
                division_practice_id = practice.division_practice_id,
                questions = [DivisionQuestionResponse(**q) for q in practice.questions],
                score = practice.score,
                total_time_taken = practice.total_time_taken,
                created_at = practice.created_at,
                status_code = status.HTTP_200_OK,
            )
        )

    return response_model