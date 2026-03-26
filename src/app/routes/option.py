from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.core.database import get_db
from app.core.authentication import require_admin
from app.models.user import User
from app.schemas.option import OptionCreate, OptionOut
from app.services.option import option_service

from app.exceptions.notfound_excs import option_not_found_exception

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

    if option is None:
        raise option_not_found_exception

    return option


@api_router.post("/", response_model=OptionOut, status_code=201)
def create_option(
    option: OptionCreate,
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_admin),
):
    return option_service.create(db, option)
