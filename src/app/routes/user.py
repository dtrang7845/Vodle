from datetime import datetime
from fastapi import APIRouter
from ..schemas.user import UserOut

api_router = APIRouter(prefix="/user", tags=["users"])

@api_router.get("/")
async def get_user() -> UserOut:
    return UserOut(
        id=1,
        name="John Doe",
        email="john.doe@example.com",
        create_time=datetime.now(),
    )