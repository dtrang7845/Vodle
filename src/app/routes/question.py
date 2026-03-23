from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.core.database import get_db
from app.schemas.question import QuestionCreate, QuestionOut
from app.services.question import question_service

api_router = APIRouter(prefix="/question", tags=["questions"])


@api_router.get("/", response_model=list[QuestionOut])
def get_questions(db: Session = Depends(get_db)):
    return question_service.get_all(db)


@api_router.get("/{question_id}", response_model=QuestionOut)
def get_question(question_id: int, db: Session = Depends(get_db)):
    question = question_service.get_by_id(db, question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return question


@api_router.post("/", response_model=QuestionOut, status_code=201)
def create_question(question: QuestionCreate, db: Session = Depends(get_db)):
    return question_service.create(db, question)