from typing import Generator

from app.db.session import SessionLocal


def get_db() -> Generator:
    db = SessionLocal()
    with db:
        try:
            yield db
        except:
            db.rollback()
        finally:
            db.close()
