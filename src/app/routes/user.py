from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from app.core.database import get_db
from app.schemas.user import UserCreate, UserOut, UserLogin
from app.schemas.token import Token
from app.services.user import user_service
from app.core.authentication import create_access_token, get_current_user
from app.models.user import User

api_router = APIRouter(prefix="/user", tags=["users"])


@api_router.get("/", response_model=list[UserOut])
def get_users(db: Session = Depends(get_db)):
    return user_service.get_all(db)

@api_router.get("/me", response_model=UserOut)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user

@api_router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = user_service.get_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@api_router.post("/", response_model=UserOut, status_code=201)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return user_service.create(db, user)

@api_router.post("/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = user_service.authenticate(db, user.email, user.password)

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    access_token = create_access_token(data={"sub": str(user.id)})

    return Token(access_token=access_token, token_type="bearer")

