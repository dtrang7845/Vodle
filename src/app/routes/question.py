from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.core.database import get_db
from app.schemas.question import QuestionCreate, QuestionOut, QuestionWithResults
from app.services.question import question_service

from app.exceptions.notfound_excs import question_not_found_exception

api_router = APIRouter(prefix="/question", tags=["questions"])


@api_router.get("/", response_model=list[QuestionOut])
def get_questions(db: Session = Depends(get_db)):
    return question_service.get_all(db)


@api_router.get("/{question_id}", response_model=QuestionOut)
def get_question(question_id: int, db: Session = Depends(get_db)):
    question = question_service.get_by_id(db, question_id)

    if question is None:
        raise question_not_found_exception
    return question


@api_router.get("/{question_id}/results", response_model=QuestionWithResults)
def get_question_with_results(question_id: int, db: Session = Depends(get_db)):
    return question_service.get_with_results(db, question_id)


@api_router.post("/", response_model=QuestionOut, status_code=201)
def create_question(question: QuestionCreate, db: Session = Depends(get_db)):
    return question_service.create(db, question)
