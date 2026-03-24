from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.core.database import get_db
from app.models.user import User
from app.schemas.vote import VoteCreate, VoteOut
from app.services.vote import vote_service
from app.core.authentication import get_current_user


api_router = APIRouter(prefix="/vote", tags=["votes"])


@api_router.get("/", response_model=list[VoteOut])
def get_votes(db: Session = Depends(get_db)):
    return vote_service.get_all(db)


@api_router.get("/{vote_id}", response_model=VoteOut)
def get_vote(vote_id: int, db: Session = Depends(get_db)):
    vote = vote_service.get_by_id(db, vote_id)
    if not vote:
        raise HTTPException(status_code=404, detail="Vote not found")
    return vote


@api_router.get("/question/{question_id}", response_model=list[VoteOut])
def get_votes_by_question(question_id: int, db: Session = Depends(get_db)):
    return vote_service.get_by_question_id(db, question_id)


@api_router.post("/", response_model=VoteOut, status_code=201)
def create_vote(vote: VoteCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return vote_service.create(db, vote, current_user.id)