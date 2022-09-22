from typing import Generator

import pytest
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from fastapi.testclient import TestClient

from app.api.api_enrollment import router
from app.config.db_config import DBConfig
from app.crud.crud_role import CRUDRole
from app.db.base import Base
from app.db.models import Role
from app.manager.manager_role import RoleManager

engine = create_engine(DBConfig.SQLALCHEMY_DATABASE_URL_TEST)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session")
def app() -> FastAPI:
    app = FastAPI()
    app.include_router(router)
    return app


@pytest.fixture(scope="session")
def db() -> Generator:
    Base.metadata.create_all(engine)
    yield TestingSessionLocal()
    Base.metadata.drop_all(engine)


@pytest.fixture(scope="module")
def client(app) -> Generator:
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="module")
def override_crud_role(db: Session):
    return CRUDRole(Role, db)


@pytest.fixture(scope="module")
def override_manager_role(override_crud_role):
    return RoleManager(Role, override_crud_role)




