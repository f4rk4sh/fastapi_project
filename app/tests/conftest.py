from datetime import datetime
from typing import Dict, Generator, List, Any

import pytest
from fastapi import FastAPI, Response, status
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
from app.db.models import (Employer, EmployerType, Role, Session, StatusType,
                           User)
from app.schemas.schema_employer_type import EmployerTypeCreate
from app.schemas.schema_role import RoleCreate
from app.schemas.schema_session import SessionCreate
from app.schemas.schema_status_type import StatusTypeCreate
from app.tests.utils.base import (get_su_token_headers, random_date,
                                  random_email, random_integer,
                                  random_password, random_phone, random_string)

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
def session(crud_session) -> Session:
    session = crud_session.create(
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
        app.dependency_overrides[get_session] = session
        yield client


@pytest.fixture(scope="module")
def su_token_headers(client: TestClient) -> Dict[str, str]:
    return get_su_token_headers(client)


@pytest.fixture(scope="module")
def crud_role(db: SQLAlchemySession) -> CRUDRole:
    return CRUDRole(Role, db)


@pytest.fixture(scope="module")
def crud_session(db: SQLAlchemySession) -> CRUDSession:
    return CRUDSession(Session, db)


@pytest.fixture(scope="module")
def crud_user(db: SQLAlchemySession) -> CRUDUser:
    return CRUDUser(User, db)


@pytest.fixture(scope="module")
def crud_status_type(db: SQLAlchemySession) -> CRUDStatusType:
    return CRUDStatusType(StatusType, db)


@pytest.fixture(scope="module")
def crud_employer(db: SQLAlchemySession) -> CRUDEmployer:
    return CRUDEmployer(Employer, db)


@pytest.fixture(scope="module")
def crud_employer_type(db: SQLAlchemySession) -> CRUDEmployerType:
    return CRUDEmployerType(EmployerType, db)


@pytest.fixture
def random_role(crud_role) -> Role:
    return crud_role.create(RoleCreate(name=random_string()))


@pytest.fixture
def random_roles(crud_role) -> List[Role]:
    return [
        crud_role.create(RoleCreate(name=random_string())) for _ in range(3)
    ]


@pytest.fixture
def expected_role() -> Role:
    return Role(id=random_integer(), name=random_string())


@pytest.fixture
def expected_roles() -> List[Role]:
    return [Role(id=random_integer(), name=random_string()) for _ in range(3)]


@pytest.fixture
def random_status_type(crud_status_type) -> StatusType:
    return crud_status_type.create(StatusTypeCreate(name=random_string()))


@pytest.fixture
def random_status_types(crud_status_type) -> List[StatusType]:
    return [
        crud_status_type.create(
            StatusTypeCreate(name=random_string())
        ) for _ in range(3)
    ]


@pytest.fixture
def expected_status_type() -> StatusType:
    return StatusType(id=random_integer(), name=random_string())


@pytest.fixture
def expected_status_types() -> List[StatusType]:
    return [
        StatusType(
            id=random_integer(), name=random_string()
        ) for _ in range(3)
    ]


@pytest.fixture
def random_employer_type(
    crud_employer_type,
) -> EmployerType:
    return crud_employer_type.create(EmployerTypeCreate(name=random_string()))


@pytest.fixture
def random_employer_types(
    crud_employer_type,
) -> List[EmployerType]:
    return [
        crud_employer_type.create(
            EmployerTypeCreate(name=random_string())
        ) for _ in range(3)
    ]


@pytest.fixture
def expected_employer_type() -> EmployerType:
    return EmployerType(id=random_integer(), name=random_string())


@pytest.fixture
def expected_employer_types() -> List[EmployerType]:
    return [
        EmployerType(
            id=random_integer(), name=random_string()
        ) for _ in range(3)
    ]


@pytest.fixture
def user_create_data() -> dict[str, Any]:
    return {
        "email": random_email(),
        "password": random_password(),
        "phone": random_phone(),
    }


@pytest.fixture
def user_update_data(
    user_create_data,
    random_role,
    random_status_type,
) -> dict[str, Any]:
    user_create_data.update(
        {
            "role_id": random_role.id,
            "status_type_id": random_status_type.id,
        }
    )
    return user_create_data


@pytest.fixture
def random_user(
    crud_user,
    user_update_data,
) -> User:
    user_update_data.update(
        {
            "creation_date": datetime.utcnow(),
            "activation_date": datetime.utcnow(),
        }
    )
    return crud_user.create(user_update_data)


@pytest.fixture
def random_users(
    crud_user,
    random_role,
    random_status_type,
) -> List[User]:
    return [
        crud_user.create(
            {
                "email": random_email(),
                "password": random_password(),
                "phone": random_phone(),
                "creation_date": datetime.utcnow(),
                "activation_date": datetime.utcnow(),
                "role_id": random_role.id,
                "status_type_id": random_status_type.id,
            }
        ) for _ in range(3)
    ]


@pytest.fixture
def employer_data(
    random_user,
    random_employer_type,
) -> dict[str, Any]:
    return {
        "name": random_string(),
        "address": random_string(),
        "edrpou": random_string(),
        "expire_contract_date": random_date(in_future=True),
        "salary_date": random_date(),
        "prepayment_date": random_date(),
        "user_id": random_user.id,
        "employer_type_id": random_employer_type.id,
    }


@pytest.fixture
def random_employer(
    crud_employer,
    employer_data,
) -> Employer:
    return crud_employer.create(employer_data)


@pytest.fixture
def random_employers(
    crud_employer,
    random_user,
    random_employer_type,
) -> List[Employer]:
    return [
        crud_employer.create(
            {
                "name": random_string(),
                "address": random_string(),
                "edrpou": random_string(),
                "expire_contract_date": random_date(in_future=True),
                "salary_date": random_date(),
                "prepayment_date": random_date(),
                "user_id": random_user.id,
                "employer_type_id": random_employer_type.id,
            }
        ) for _ in range(3)
    ]


@pytest.fixture
def expected_employer() -> Employer:
    return Employer(
        id=random_integer(),
        user_id=random_integer(),
        name=random_string(),
        address=random_string(),
        edrpou=random_string(),
        expire_contract_date=random_date(in_future=True),
        salary_date=random_date(),
        prepayment_date=random_date(),
        employer_type_id=random_integer(),
    )


@pytest.fixture
def expected_employers() -> List[Employer]:
    return [
        Employer(
            id=random_integer(),
            user_id=random_integer(),
            name=random_string(),
            address=random_string(),
            edrpou=random_string(),
            expire_contract_date=random_date(in_future=True),
            salary_date=random_date(),
            prepayment_date=random_date(),
            employer_type_id=random_integer(),
        ) for _ in range(3)
    ]


@pytest.fixture
def expected_response_no_content() -> Response:
    return Response(status_code=status.HTTP_204_NO_CONTENT)
