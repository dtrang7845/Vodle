from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.core.database import get_db
from app.models.question import Question
from app.schemas.question import QuestionOut, QuestionCreate

api_router = APIRouter(prefix="/question", tags=["questions"])


@api_router.get("/", response_model=list[QuestionOut])
def get_questions(db: Session = Depends(get_db)):
    statement = select(Question)
    questions = db.exec(statement).all()
    return questions


@api_router.get("/{question_id}", response_model=QuestionOut)
def get_question(question_id: int, db: Session = Depends(get_db)):
    question = db.get(Question, question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return question


@api_router.post("/", response_model=QuestionOut, status_code=201)
def create_question(question: QuestionCreate, db: Session = Depends(get_db)):
    db_question = Question(**question.model_dump())
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question