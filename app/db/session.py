from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config.db_config import DBConfig

# for local connection

# SQLALCHEMY_DATABASE_URL = DBConfig.SQLALCHEMY_DATABASE_URL_LOCAL

# for docker connection

SQLALCHEMY_DATABASE_URL = DBConfig.SQLALCHEMY_DATABASE_URL

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_session() -> Generator:
    session = SessionLocal()
    try:
        yield session
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
