from fastapi import APIRouter
api_router = APIRouter(prefix="/user",tags=["users"])

@api_router.get("/")

async def get_user() ->dict:
    return { "test": "number"}