from typing import Generator

import pytest
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.api.api_enrollment import router
from app.config.db_config import DBConfig
from app.db.base import Base

engine = create_engine(DBConfig.SQLALCHEMY_DATABASE_URL_TEST)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session")
def app() -> FastAPI:
    app = FastAPI()
    app.include_router(router)
    return app


@pytest.fixture(scope="session")
def db() -> Generator:
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    yield TestingSessionLocal()




