from datetime import datetime
from typing import Generator, Dict

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session as SQLAlchemySession

from app.api.api_enrollment import router
from app.api.dependencies import get_session
from app.config.db_config import DBConfig
from app.constansts.constants_session import ConstantSessionStatus
from app.crud.crud_role import CRUDRole
from app.crud.crud_session import CRUDSession
from app.db.base import Base
from app.db.models import Role, Session
from app.manager.manager_role import RoleManager
from app.schemas.session import SessionCreate
from app.tests.utils.base import get_su_token_headers

engine = create_engine(DBConfig.SQLALCHEMY_DATABASE_URL_TEST)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session")
def app() -> FastAPI:
    app = FastAPI()
    app.include_router(router)
    return app


@pytest.fixture(scope="module")
def db() -> Generator:
    Base.metadata.create_all(engine)
    yield TestingSessionLocal()
    Base.metadata.drop_all(engine)


@pytest.fixture(scope="module")
def get_test_session(override_crud_session):
    session = override_crud_session.create(
        SessionCreate(
            token="token",
            creation_date=datetime.utcnow(),
            status=ConstantSessionStatus.logged_in,
        )
    )
    yield session


@pytest.fixture(scope="module")
def client(app: FastAPI, db: SQLAlchemySession) -> Generator:
    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_test_session
        yield client


@pytest.fixture(scope="module")
def su_token_headers(client: TestClient) -> Dict[str, str]:
    return get_su_token_headers(client)


@pytest.fixture(scope="module")
def override_crud_role(db: SQLAlchemySession):
    return CRUDRole(Role, db)


@pytest.fixture(scope="module")
def override_manager_role(override_crud_role):
    return RoleManager(Role, override_crud_role)


@pytest.fixture(scope="module")
def override_crud_session(db: SQLAlchemySession):
    return CRUDSession(Session, db)
