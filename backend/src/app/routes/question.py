from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.core.authentication import require_admin
from app.core.database import get_db
from app.models.user import User
from app.schemas.question import (
    QuestionCreate,
    QuestionCreateWithOptions,
    QuestionOut,
    QuestionWithOptions,
    QuestionWithResults,
    QuestionUpdate,
)
from app.services.question import question_service

from app.exceptions.notfound_excs import question_not_found_exception

api_router = APIRouter(prefix="/question", tags=["questions"])


@api_router.get("/", response_model=list[QuestionOut])
def get_questions(db: Session = Depends(get_db)):
    return question_service.get_all(db)


@api_router.get("/today", response_model=QuestionWithOptions)
def get_today_question(db: Session = Depends(get_db)):
    return question_service.get_today(db)


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
def create_question(
    question: QuestionCreate,
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_admin),
):
    return question_service.create(db, question)


@api_router.post("/with-options", response_model=QuestionWithOptions, status_code=201)
def create_question_with_options(
    question: QuestionCreateWithOptions,
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_admin),
):
    return question_service.create_with_options(db, question)


@api_router.put("/{question_id}", response_model=QuestionOut)
def update_question(
    question_id: int,
    question: QuestionUpdate,
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_admin),
):
    return question_service.update(db, question_id, question)


@api_router.delete("/{question_id}", status_code=204)
def delete_question(
    question_id: int,
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_admin),
):
    question_service.delete(db, question_id)
