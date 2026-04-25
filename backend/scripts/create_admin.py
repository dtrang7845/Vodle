from __future__ import annotations

import argparse

from sqlmodel import Session

from app.core.authentication import get_password_hash
from app.core.database import create_db_and_tables, engine
from app.models import option  # noqa: F401
from app.models import question  # noqa: F401
from app.models import vote  # noqa: F401
from app.models.user import User, UserRole
from app.repository.user import UserRepository


def create_or_update_admin(username: str, email: str, password: str) -> None:
    create_db_and_tables()
    repository = UserRepository()

    with Session(engine) as session:
        existing_by_email = repository.get_by_email(session, email)
        existing_by_username = repository.get_by_username(session, username)

        if existing_by_email and existing_by_username:
            if existing_by_email.id != existing_by_username.id:
                raise ValueError(
                    "The provided username and email belong to different users. "
                    "Choose a matching pair or unused values."
                )

            existing_by_email.username = username
            existing_by_email.password_hash = get_password_hash(password)
            existing_by_email.role = UserRole.ADMIN
            repository.update(session, existing_by_email)
            print(
                f"Updated existing user {existing_by_email.email} "
                "and granted admin access."
            )
            return

        if existing_by_email:
            existing_by_email.username = username
            existing_by_email.password_hash = get_password_hash(password)
            existing_by_email.role = UserRole.ADMIN
            repository.update(session, existing_by_email)
            print(
                f"Promoted existing email {existing_by_email.email} to admin "
                "and updated the username/password."
            )
            return

        if existing_by_username:
            existing_by_username.email = email
            existing_by_username.password_hash = get_password_hash(password)
            existing_by_username.role = UserRole.ADMIN
            repository.update(session, existing_by_username)
            print(
                f"Promoted existing username {existing_by_username.username} to admin "
                "and updated the email/password."
            )
            return

        admin = User(
            username=username,
            email=email,
            password_hash=get_password_hash(password),
            role=UserRole.ADMIN,
        )
        repository.create(session, admin)
        print(f"Created admin user {admin.email}.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Create or promote an admin user in the local Vodle database."
    )
    parser.add_argument("--username", required=True, help="Admin username")
    parser.add_argument("--email", required=True, help="Admin email address")
    parser.add_argument("--password", required=True, help="Admin password")
    args = parser.parse_args()

    create_or_update_admin(
        username=args.username,
        email=args.email,
        password=args.password,
    )
