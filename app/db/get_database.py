from typing import Generator

from app.db.session import SessionLocal


def get_db() -> Generator:
    db = SessionLocal()
    with db:
        yield db
