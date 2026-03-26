from fastapi import HTTPException, status

bad_option_exception = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Option does not belong to this question",
)

user_already_voted_exception = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="User has already voted on this question",
)

admin_required_exception = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Admin privileges required",
)

user_vote_deletion_exception = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="User is not authorized to delete this vote",
)

user_unauthorized_exception = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="User is authoried for this action",
)