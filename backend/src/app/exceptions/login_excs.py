from fastapi import HTTPException, status

invalid_credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

email_already_exists_exception = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Email already registered",
)

