from fastapi import APIRouter

from app.routes import question, option, vote, user

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(question.api_router)
api_router.include_router(option.api_router)
api_router.include_router(vote.api_router)
api_router.include_router(user.api_router)
