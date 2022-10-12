from copy import copy

import pytest
from pytest_mock import MockerFixture

from app.db.models import Employer, Role, Session, User
from app.manager.manager_employer import employer
from app.schemas.employer import EmployerCreate, EmployerUpdate
from app.tests.utils.base import (random_date, random_email, random_integer,
                                  random_password, random_phone, random_string)
from app.utils.exceptions.common_exceptions import HTTPBadRequestException


class TestManagerCreateEmployer:
    def test_successful_create_employer(
        self,
        get_test_session: Session,
        mocker: MockerFixture,
    ) -> None:
        mocker.patch("app.crud.crud_user.user.get_by_attribute", return_value=False)
        mocker.patch(
            "app.crud.crud_role.role.get_by_attribute",
            return_value=Role(id=random_integer()),
        )
        mocker.patch(
            "app.crud.crud_status_type.status_type.get_by_attribute",
            return_value=Role(id=random_integer()),
        )
        user_id = random_integer()
        mocker.patch(
            "app.crud.crud_user.user.create",
            return_value=User(
                id=user_id,
            ),
        )

        employer_data = {
            "name": random_string(),
            "address": random_string(),
            "edrpou": random_string(),
            "expire_contract_date": random_date(in_future=True),
            "salary_date": random_date(),
            "prepayment_date": random_date(),
            "employer_type_id": random_integer(),
        }
        expected_result = Employer(
            id=random_integer(),
            user_id=user_id,
            **employer_data,
        )
        mocked_employer_create = mocker.patch(
            "app.manager.manager_employer.employer.crud.create",
            return_value=expected_result,
        )

        employer_in_data = copy(employer_data)
        employer_in_data["user"] = {
            "email": random_email(),
            "phone": random_phone(),
            "password": random_password(),
        }
        actual_result = employer.create(
            EmployerCreate(**employer_in_data), get_test_session
        )

        employer_data["user_id"] = user_id
        mocked_employer_create.assert_called_once_with(employer_data)
        assert actual_result == expected_result

    def test_failed_create_employer(
        self,
        override_crud_user,
        random_user,
        get_test_session: Session,
        monkeypatch,
    ) -> None:
        monkeypatch.setattr(
            "app.crud.crud_user.user.get_by_attribute",
            override_crud_user.get_by_attribute,
        )

        with pytest.raises(HTTPBadRequestException):
            employer.create(
                EmployerCreate(
                    **{
                        "user": {
                            "email": random_user.email,
                            "phone": random_phone(),
                            "password": random_password(),
                        },
                        "name": random_string(),
                        "address": random_string(),
                        "edrpou": random_string(),
                        "expire_contract_date": random_date(in_future=True),
                        "salary_date": random_date(),
                        "prepayment_date": random_date(),
                        "employer_type_id": random_integer(),
                    }
                ),
                get_test_session,
            )


class TestManagerGetEmployer:
    def test_successful_get_employer(
        self,
        get_test_session: Session,
        mocker: MockerFixture,
    ) -> None:
        employer_id = random_integer()
        expected_result = Employer(
            id=employer_id,
            user_id=random_integer(),
            name=random_string(),
            address=random_string(),
            edrpou=random_string(),
            expire_contract_date=random_date(in_future=True),
            salary_date=random_date(),
            prepayment_date=random_date(),
            employer_type_id=random_integer(),
        )
        mocked_employer_get = mocker.patch(
            "app.manager.manager_employer.employer.crud.get",
            return_value=expected_result,
        )

        actual_result = employer.fetch_one(employer_id, get_test_session)

        mocked_employer_get.assert_called_once_with(employer_id)
        assert actual_result == expected_result


class TestManagerGetMultipleEmployers:
    def test_successful_get_multiple_employers(
        self,
        get_test_session: Session,
        mocker: MockerFixture,
    ) -> None:
        expected_result = [
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
            )
            for _ in range(3)
        ]
        mocked_employer_get_multi = mocker.patch(
            "app.manager.manager_employer.employer.crud.get_multi",
            return_value=expected_result,
        )

        actual_result = employer.fetch_all(get_test_session)

        mocked_employer_get_multi.assert_called_once()
        assert actual_result == expected_result


class TestManagerSearchEmployerByParameter:
    def test_successful_search_employers_by_parameter(
        self,
        get_test_session: Session,
        mocker: MockerFixture,
    ) -> None:
        name = random_string()
        parameter = "name"
        expected_employer = Employer(
            id=random_integer(),
            user_id=random_integer(),
            name=name,
            address=random_string(),
            edrpou=random_string(),
            expire_contract_date=random_date(in_future=True),
            salary_date=random_date(),
            prepayment_date=random_date(),
            employer_type_id=random_integer(),
        )
        mocked_employer_search = mocker.patch(
            "app.manager.manager_employer.employer.crud.search_by_parameter",
            return_value=[
                expected_employer,
            ],
        )

        actual_result = employer.search(parameter, name, get_test_session, 1)

        mocked_employer_search.assert_called_once_with(parameter, name, 1)
        assert expected_employer in actual_result


class TestManagerUpdateEmployer:
    def test_successful_update_employer(
        self,
        get_test_session: Session,
        mocker: MockerFixture,
    ) -> None:
        employer_id = random_integer()
        employer_in_db = Employer(
            id=employer_id,
            user_id=random_integer(),
            name=random_string(),
            address=random_string(),
            edrpou=random_string(),
            expire_contract_date=random_date(in_future=True),
            salary_date=random_date(),
            prepayment_date=random_date(),
            employer_type_id=random_integer(),
        )
        mocker.patch(
            "app.manager.manager_employer.employer.crud.get",
            return_value=employer_in_db,
        )
        mocker.patch(
            "app.crud.crud_user.user.get_by_attribute",
            return_value=None,
        )
        mocker.patch(
            "app.crud.crud_user.user.get",
            return_value=User(id=random_integer()),
        )

        user_id = random_integer()
        user_data = {
            "email": random_email(),
            "phone": random_phone(),
            "password": random_password(),
            "role_id": random_integer(),
            "status_type_id": random_integer(),
        }
        mocker.patch(
            "app.crud.crud_user.user.update",
            return_value=User(id=user_id, **user_data),
        )

        employer_update_data = {
            "id": employer_id,
            "name": random_string(),
            "address": random_string(),
            "edrpou": random_string(),
            "expire_contract_date": random_date(in_future=True),
            "salary_date": random_date(),
            "prepayment_date": random_date(),
            "employer_type_id": random_integer(),
        }
        expected_result = Employer(user_id=user_id, **employer_update_data)
        mocked_employer_update = mocker.patch(
            "app.manager.manager_employer.employer.crud.update",
            return_value=expected_result,
        )

        employer_in_data = copy(employer_update_data)
        employer_in_data["user"] = user_data
        actual_result = employer.update(
            EmployerUpdate(**employer_in_data), get_test_session
        )

        employer_update_data["user_id"] = user_id
        mocked_employer_update.assert_called_once_with(
            employer_in_db, EmployerUpdate(**employer_in_data)
        )
        assert actual_result == expected_result

    def test_failed_update_employer(
        self,
        override_crud_user,
        random_user,
        get_test_session: Session,
        mocker,
        monkeypatch,
    ) -> None:
        mocker.patch(
            "app.manager.manager_employer.employer.crud.get",
            return_value=Employer(
                id=random_integer(),
                user_id=random_integer(),
                name=random_string(),
                address=random_string(),
                edrpou=random_string(),
                expire_contract_date=random_date(in_future=True),
                salary_date=random_date(),
                prepayment_date=random_date(),
                employer_type_id=random_integer(),
            ),
        )
        monkeypatch.setattr(
            "app.crud.crud_user.user.get_by_attribute",
            override_crud_user.get_by_attribute,
        )

        with pytest.raises(HTTPBadRequestException):
            employer.update(
                EmployerUpdate(
                    **{
                        "user": {
                            "email": random_user.email,
                            "phone": random_phone(),
                            "password": random_password(),
                            "role_id": random_integer(),
                            "status_type_id": random_integer(),
                        },
                        "id": random_integer(),
                        "name": random_string(),
                        "address": random_string(),
                        "edrpou": random_string(),
                        "expire_contract_date": random_date(in_future=True),
                        "salary_date": random_date(),
                        "prepayment_date": random_date(),
                        "employer_type_id": random_integer(),
                    }
                ),
                get_test_session,
            )


class TestManagerDeleteEmployer:
    def test_successful_delete_employer(
        self,
        get_test_session: Session,
        mocker: MockerFixture,
    ) -> None:
        employer_id = random_integer()
        employer_in_db = Employer(
            id=employer_id,
            user_id=random_integer(),
            name=random_string(),
            address=random_string(),
            edrpou=random_string(),
            expire_contract_date=random_date(in_future=True),
            salary_date=random_date(),
            prepayment_date=random_date(),
            employer_type_id=random_integer(),
        )

        mocker.patch(
            "app.manager.manager_employer.employer.crud.get",
            return_value=employer_in_db,
        )

        mocked_user_delete = mocker.patch(
            "app.crud.crud_user.user.delete",
            return_value=None,
        )

        employer.delete(employer_id, get_test_session)

        mocked_user_delete.assert_called_once_with(employer_in_db.user_id)
