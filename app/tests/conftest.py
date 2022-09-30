from datetime import datetime
from typing import Dict, Generator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session as SQLAlchemySession
from sqlalchemy.orm import sessionmaker

from app.api.api_enrollment import router
from app.api.dependencies import get_session
from app.config.db_config import DBConfig
from app.constansts.constants_session import ConstantSessionStatus
from app.crud.crud_employer import CRUDEmployer
from app.crud.crud_employer_type import CRUDEmployerType
from app.crud.crud_role import CRUDRole
from app.crud.crud_session import CRUDSession
from app.crud.crud_status_type import CRUDStatusType
from app.crud.crud_user import CRUDUser
from app.db.base import Base
from app.db.models import Role, Session, Employer, User, EmployerType, StatusType
from app.schemas.employer_type import EmployerTypeCreate
from app.schemas.role import RoleCreate
from app.schemas.session import SessionCreate
from app.schemas.status_type import StatusTypeCreate
from app.tests.utils.base import get_su_token_headers, random_string, random_email, random_password, random_phone

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
def override_crud_session(db: SQLAlchemySession):
    return CRUDSession(Session, db)


@pytest.fixture(scope="module")
def override_crud_user(db: SQLAlchemySession):
    return CRUDUser(User, db)


@pytest.fixture(scope="module")
def override_crud_status_type(db: SQLAlchemySession):
    return CRUDStatusType(StatusType, db)


@pytest.fixture(scope="module")
def override_crud_employer(db: SQLAlchemySession):
    return CRUDEmployer(Employer, db)


@pytest.fixture(scope="module")
def override_crud_employer_type(db: SQLAlchemySession):
    return CRUDEmployerType(EmployerType, db)


@pytest.fixture
def create_random_role(override_crud_role: CRUDRole):
    return override_crud_role.create(RoleCreate(name=random_string()))


@pytest.fixture
def create_random_status_type(override_crud_status_type: CRUDStatusType):
    return override_crud_status_type.create(StatusTypeCreate(name=random_string()))


@pytest.fixture
def create_random_employer_type(override_crud_employer_type: CRUDEmployerType):
    return override_crud_employer_type.create(EmployerTypeCreate(name=random_string()))


@pytest.fixture
def create_random_user(override_crud_user: CRUDUser, create_random_role, create_random_status_type):
    return override_crud_user.create(
        {
            "email": random_email(),
            "password": random_password(),
            "phone": random_phone(),
            "creation_date": datetime.utcnow(),
            "activation_date": datetime.utcnow(),
            "role_id": create_random_role.id,
            "status_type_id": create_random_status_type.id,
        }
    )
