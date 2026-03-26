from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session

from app.core.database import get_db
from app.schemas.user import UserCreate, UserOut, UserUpdate
from app.schemas.token import Token
from app.services.user import user_service
from app.core.authentication import create_access_token, get_current_user
from app.models.user import User, UserRole

from app.exceptions.notfound_excs import user_not_found_exception
from app.exceptions.login_excs import invalid_credentials_exception
from app.exceptions.other_excs import user_unauthorized_exception

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
    if user is None:
        raise user_not_found_exception
    return user


@api_router.post("/", response_model=UserOut, status_code=201)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return user_service.create(db, user)


@api_router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    db_user = user_service.authenticate(db, form_data.username, form_data.password)

    if not db_user:
        raise invalid_credentials_exception

    access_token = create_access_token(data={"sub": str(db_user.id)})

    return Token(access_token=access_token, token_type="bearer")


@api_router.put("/{user_id}", response_model=UserOut)
def update_user(
    user_id: int,
    user: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.id != user_id and current_user.role != UserRole.ADMIN:
        raise user_unauthorized_exception
    return user_service.update(db, user_id, user)


@api_router.delete("/{user_id}", status_code=204)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.id != user_id and current_user.role != UserRole.ADMIN:
        raise user_unauthorized_exception
    return user_service.delete(db, user_id)
