import random

from sqlalchemy.orm import Session

from fastapi import status, HTTPException, Depends, APIRouter, Body, Query

from app.schemas import *
from app.models import *
from app.schemas import *
from app.core.config_db import get_db

router = APIRouter(
    prefix="/exponent", 
    tags=["exponent"]
)


@router.post(
    "/", 
    response_model=ExponentServerResponse,
    status_code=status.HTTP_201_CREATED
)
def exponent_questions(
    exponent_create_details: ExponentCreate = Body(..., examples={
        "exponent": 2,
        "upto": 30,
        "root": False
    }),
    db: Session = Depends(get_db),
):   
    try:
        exponent = exponent_create_details.exponent
        upto = exponent_create_details.upto
        root = exponent_create_details.root

        numbers = list(range(1, upto + 1))
        random.shuffle(numbers)
        
        answers = [num ** exponent for num in numbers]
        
        questions_list = []

        if root:
            for i in range(upto):
                questions_list.append(
                    ExponentQuestionResponse(
                        question=f"{answers[i]} ** (1/{exponent})",
                        answer=numbers[i]
                    )
                )
        else:
            for i in range(upto):
                questions_list.append(
                    ExponentQuestionResponse(
                        question=f"{numbers[i]} ** {exponent}",
                        answer=answers[i]
                    )
                )

        new_exponent_practice = Exponent(
            questions = [q.model_dump() for q in questions_list]
        )

        db.add(new_exponent_practice)
        db.flush()

        response_model = {
            "exponent_practice_id": new_exponent_practice.exponent_practice_id,
            "questions": questions_list,
            "created_at": new_exponent_practice.created_at,
            "status_code": status.HTTP_201_CREATED,
        }

        db.commit()

        return ExponentServerResponse(**response_model)
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
    response_model=ExponentServerResponse,
    status_code=status.HTTP_201_CREATED
)
def exponent_practice_response(
    exponent_practice_response_details: ExponentResponse= Body(..., examples={
        "exponent_practice_id": "123e4567-e89b-12d3-a456-426614174000",
        "questions": [
            {
                "question": "12 ** 2",
                "answer": 144,
                "given_answer": 144,
                "time_taken": 3.5
            },
            {
                "question": "21 ** 2",
                "answer": 441,
                "given_answer": 441,
                "time_taken": 7.89
            }
        ],
        "total_time_taken": 15.75
    }),
    db: Session = Depends(get_db),
):
    try:    
        exponent_practice_id = exponent_practice_response_details.exponent_practice_id
        questions = exponent_practice_response_details.questions
        total_time_taken = exponent_practice_response_details.total_time_taken

        exponent_practice = db.query(Exponent).filter(Exponent.exponent_practice_id == exponent_practice_id).first()

        if not exponent_practice:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "error": "No exponent practice found with the given ID",
                    "status_code": status.HTTP_404_NOT_FOUND
                }
            )

        exponent_practice.questions = []

        score = 0
        out_of = 0
        for question in questions:
            question.is_correct = question.answer == question.given_answer

            if question.is_correct:
                score += 1
            out_of += 1

        exponent_practice.questions = [response.model_dump() for response in questions]
        exponent_practice.score = f"{score}/{out_of}"
        exponent_practice.total_time_taken = total_time_taken

        response_model = {
            "exponent_practice_id": exponent_practice_id,
            "questions": questions,
            "score": exponent_practice.score,
            "total_time_taken": exponent_practice.total_time_taken,
            "created_at": exponent_practice.created_at,
            "status_code": status.HTTP_201_CREATED,   
        }

        db.commit()

        return ExponentServerResponse(**response_model)
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
    response_model=List[ExponentServerResponse],
)
def exponent_practice_data(
    exponent_practice_id: Optional[UUID] = Query(None),
    db: Session = Depends(get_db),
):
    if exponent_practice_id is None:
        exponent_practice = (
            db.query(Exponent)
            .order_by(Exponent.created_at.desc())
            .all()
        )
    else:
        exponent_practice = [
            db.query(Exponent)
            .filter(Exponent.exponent_practice_id == exponent_practice_id)
            .first()
        ]

    if not exponent_practice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": "No exponent practice found with the given ID",
                "status_code": status.HTTP_404_NOT_FOUND
            }
        )
    
    response_model = []

    for practice in exponent_practice:
        response_model.append(
            ExponentServerResponse(
                exponent_practice_id = practice.exponent_practice_id,
                questions = [ExponentQuestionResponse(**q) for q in practice.questions],
                score = practice.score,
                total_time_taken = practice.total_time_taken,
                created_at = practice.created_at,
                status_code = status.HTTP_200_OK,
            )
        )

    return response_model