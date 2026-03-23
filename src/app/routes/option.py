from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.core.database import get_db
from app.schemas.option import OptionCreate, OptionOut
from app.services.option import option_service

api_router = APIRouter(prefix="/option", tags=["options"])


@api_router.get("/", response_model=list[OptionOut])
def get_options(db: Session = Depends(get_db)):
    return option_service.get_all(db)


@api_router.get("/question/{question_id}", response_model=list[OptionOut])
def get_options_by_question(question_id: int, db: Session = Depends(get_db)):
    return option_service.get_by_question_id(db, question_id)


@api_router.get("/{option_id}", response_model=OptionOut)
def get_option(option_id: int, db: Session = Depends(get_db)):
    option = option_service.get_by_id(db, option_id)
    if not option:
        raise HTTPException(status_code=404, detail="Option not found")
    return option


@api_router.post("/", response_model=OptionOut, status_code=201)
def create_option(option: OptionCreate, db: Session = Depends(get_db)):
    return option_service.create(db, option)