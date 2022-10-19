from copy import copy

import pytest
from pytest_mock import MockerFixture

from app.db.models import Employer, User
from app.manager.manager_employer import employer
from app.schemas.employer import EmployerCreate, EmployerUpdate
from app.tests.utils.base import (random_email, random_integer,
                                  random_password, random_phone)
from app.utils.exceptions.common_exceptions import HTTPBadRequestException


class TestManagerCreateEmployer:
    def test_successful_create_employer(
        self,
        session,
        expected_role,
        expected_status_type,
        expected_employer,
        mocker: MockerFixture,
    ) -> None:
        mocker.patch("app.crud.crud_user.user.get_by_attribute", return_value=False)
        mocker.patch(
            "app.crud.crud_role.role.get_by_attribute",
            return_value=expected_role,
        )
        mocker.patch(
            "app.crud.crud_status_type.status_type.get_by_attribute",
            return_value=expected_status_type,
        )
        mocker.patch(
            "app.crud.crud_user.user.create",
            return_value=User(id=expected_employer.user_id),
        )
        mocked_employer_create = mocker.patch(
            "app.manager.manager_employer.employer.crud.create",
            return_value=expected_employer,
        )

        employer_data = {
            "name": expected_employer.name,
            "address": expected_employer.address,
            "edrpou": expected_employer.edrpou,
            "expire_contract_date": expected_employer.expire_contract_date,
            "salary_date": expected_employer.salary_date,
            "prepayment_date": expected_employer.prepayment_date,
            "employer_type_id": expected_employer.employer_type_id,
        }

        employer_in_data = copy(employer_data)
        employer_in_data["user"] = {
            "email": random_email(),
            "phone": random_phone(),
            "password": random_password(),
        }
        actual_result = employer.create(
            EmployerCreate(**employer_in_data), session
        )

        employer_data["user_id"] = expected_employer.user_id
        mocked_employer_create.assert_called_once_with(employer_data)
        assert actual_result == expected_employer

    def test_failed_create_employer(
        self,
        crud_user,
        employer_data,
        random_user,
        session,
        monkeypatch,
    ) -> None:
        monkeypatch.setattr(
            "app.crud.crud_user.user.get_by_attribute",
            crud_user.get_by_attribute,
        )

        employer_data.pop("user_id")
        employer_data["user"] = {
            "email": random_user.email,
            "phone": random_phone(),
            "password": random_password(),
        }
        with pytest.raises(HTTPBadRequestException):
            employer.create(EmployerCreate(**employer_data), session)


class TestManagerGetEmployer:
    def test_successful_get_employer(
        self,
        session,
        expected_employer,
        mocker: MockerFixture,
    ) -> None:
        mocked_employer_get = mocker.patch(
            "app.manager.manager_employer.employer.crud.get",
            return_value=expected_employer,
        )

        actual_result = employer.fetch_one(expected_employer.id, session)

        mocked_employer_get.assert_called_once_with(expected_employer.id)
        assert actual_result == expected_employer


class TestManagerGetMultipleEmployers:
    def test_successful_get_multiple_employers(
        self,
        session,
        expected_employers,
        mocker: MockerFixture,
    ) -> None:
        mocked_employer_get_multi = mocker.patch(
            "app.manager.manager_employer.employer.crud.get_multi",
            return_value=expected_employers,
        )

        actual_result = employer.fetch_all(session)

        mocked_employer_get_multi.assert_called_once()
        assert actual_result == expected_employers


class TestManagerSearchEmployerByParameter:
    def test_successful_search_employers_by_parameter(
        self,
        session,
        expected_employer,
        mocker: MockerFixture,
    ) -> None:
        mocked_employer_search = mocker.patch(
            "app.manager.manager_employer.employer.crud.search_by_parameter",
            return_value=[expected_employer],
        )

        parameter = "name"
        actual_result = employer.search(
            parameter, expected_employer.name, session, 1
        )

        mocked_employer_search.assert_called_once_with(
            parameter, expected_employer.name, 1
        )
        assert expected_employer in actual_result


class TestManagerUpdateEmployer:
    def test_successful_update_employer(
        self,
        session,
        expected_employer,
        employer_data,
        mocker: MockerFixture,
    ) -> None:
        employer_in_db = Employer(id=expected_employer.id)
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
        mocker.patch(
            "app.crud.crud_user.user.update",
            return_value=User(id=expected_employer.user_id),
        )

        employer_data.pop("user_id")
        employer_data["id"] = expected_employer.id
        mocked_employer_update = mocker.patch(
            "app.manager.manager_employer.employer.crud.update",
            return_value=expected_employer,
        )

        employer_in_data = copy(employer_data)
        employer_in_data["user"] = {
            "email": random_email(),
            "phone": random_phone(),
            "password": random_password(),
            "role_id": random_integer(),
            "status_type_id": random_integer(),
        }
        employer_in = EmployerUpdate(**employer_in_data)
        actual_result = employer.update(employer_in, session)

        mocked_employer_update.assert_called_once_with(employer_in_db, employer_in)
        assert actual_result == expected_employer

    def test_failed_update_employer(
        self,
        session,
        expected_employer,
        employer_data,
        crud_user,
        random_user,
        mocker,
        monkeypatch,
    ) -> None:
        mocker.patch(
            "app.manager.manager_employer.employer.crud.get",
            return_value=expected_employer,
        )
        monkeypatch.setattr(
            "app.crud.crud_user.user.get_by_attribute",
            crud_user.get_by_attribute,
        )

        employer_data.pop("user_id")
        employer_data["id"] = random_integer()
        employer_data["user"] = {
            "email": random_user.email,
            "phone": random_phone(),
            "password": random_password(),
            "role_id": random_integer(),
            "status_type_id": random_integer(),
        }
        with pytest.raises(HTTPBadRequestException):
            employer.update(EmployerUpdate(**employer_data), session)


class TestManagerDeleteEmployer:
    def test_successful_delete_employer(
        self,
        session,
        expected_employer,
        mocker: MockerFixture,
    ) -> None:
        mocker.patch(
            "app.manager.manager_employer.employer.crud.get",
            return_value=expected_employer,
        )

        mocked_user_delete = mocker.patch(
            "app.crud.crud_user.user.delete",
            return_value=None,
        )

        employer.delete(expected_employer.id, session)

        mocked_user_delete.assert_called_once_with(expected_employer.user_id)
