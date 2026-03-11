from fastapi import APIRouter
from datetime import datetime
from ..schemas.question import Question
api_router = APIRouter(prefix="/question",tags=["questions"])

@api_router.get("/")
async def get_question() -> Question:
    return Question(
        id=1,
        title="did I do this right",
        description="please be 200",
        create_time=datetime.now(),
    )