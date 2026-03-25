from fastapi import HTTPException, status

user_not_found_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="User not found",
)

question_not_found_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Question not found",
)

option_not_found_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Option not found",
)

vote_not_found_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Vote not found",
)