from fastapi import APIRouter
from ..schemas.user import User
api_router = APIRouter(prefix="/user",tags=["users"])

@api_router.get("/")

async def get_user() -> User:
    return User(id=1, name="John Doe", email="john.doe@example.com")