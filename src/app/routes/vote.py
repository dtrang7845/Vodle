from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.core.database import get_db
from app.models.user import User
from app.schemas.vote import VoteCreate, VoteOut, VoteUpdate
from app.services.vote import vote_service
from app.core.authentication import get_current_user

from app.exceptions.notfound_excs import vote_not_found_exception


api_router = APIRouter(prefix="/vote", tags=["votes"])


@api_router.get("/", response_model=list[VoteOut])
def get_votes(db: Session = Depends(get_db)):
    return vote_service.get_all(db)


@api_router.get("/question/{question_id}", response_model=list[VoteOut])
def get_votes_by_question(question_id: int, db: Session = Depends(get_db)):
    return vote_service.get_by_question_id(db, question_id)


@api_router.get("/{vote_id}", response_model=VoteOut)
def get_vote(vote_id: int, db: Session = Depends(get_db)):
    vote = vote_service.get_by_id(db, vote_id)

    if vote is None:
        raise vote_not_found_exception
    return vote


@api_router.post("/", response_model=VoteOut, status_code=201)
def create_vote(
    vote: VoteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return vote_service.create(db, vote, current_user.id)


@api_router.put("/{vote_id}", response_model=VoteOut)
def update_vote(
    vote_id: int,
    vote: VoteUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return vote_service.update(db, vote_id, vote, current_user.id)


@api_router.delete("/{vote_id}", status_code=204)
def delete_vote(
    vote_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    vote_service.delete(db, vote_id, current_user.id)
