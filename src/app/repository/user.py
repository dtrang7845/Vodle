from typing import TYPE_CHECKING

from app.models.user import User

if TYPE_CHECKING:
    from sqlmodel.orm import Session

    from app.schemas.user import UserDb


class UserRepository:
    @staticmethod
    def get_by_mail(db: Session, email: str) -> User | None:

        # select * from user where email = email limit 1
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def get_by_id(db: Session, user_id: int) -> User | None:

        # select * from user where id = user_id limit 1
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def create(
        db: Session,
        user_db: UserDb,
    ) -> User:

        db_user = User(
            email=user_db.email,
            hashed_password=user_db.hashed_password,
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def update(db: Session, db_user: User) -> User:
        """
        Update user.

        Args:
            db: Database session
            db_user: User instance to update

        Returns:
            User: Updated user
        """
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def delete(db: Session, db_user: User) -> None:
        """
        Delete user.

        Args:
            db: Database session
            db_user: User instance to delete
        """
        db.delete(db_user)
        db.commit()