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
        get_test_session,
        get_expected_role,
        get_expected_status_type,
        get_expected_employer,
        mocker: MockerFixture,
    ) -> None:
        mocker.patch("app.crud.crud_user.user.get_by_attribute", return_value=False)
        mocker.patch(
            "app.crud.crud_role.role.get_by_attribute",
            return_value=get_expected_role,
        )
        mocker.patch(
            "app.crud.crud_status_type.status_type.get_by_attribute",
            return_value=get_expected_status_type,
        )
        mocker.patch(
            "app.crud.crud_user.user.create",
            return_value=User(id=get_expected_employer.user_id),
        )
        mocked_employer_create = mocker.patch(
            "app.manager.manager_employer.employer.crud.create",
            return_value=get_expected_employer,
        )

        employer_data = {
            "name": get_expected_employer.name,
            "address": get_expected_employer.address,
            "edrpou": get_expected_employer.edrpou,
            "expire_contract_date": get_expected_employer.expire_contract_date,
            "salary_date": get_expected_employer.salary_date,
            "prepayment_date": get_expected_employer.prepayment_date,
            "employer_type_id": get_expected_employer.employer_type_id,
        }

        employer_in_data = copy(employer_data)
        employer_in_data["user"] = {
            "email": random_email(),
            "phone": random_phone(),
            "password": random_password(),
        }
        actual_result = employer.create(
            EmployerCreate(**employer_in_data), get_test_session
        )

        employer_data["user_id"] = get_expected_employer.user_id
        mocked_employer_create.assert_called_once_with(employer_data)
        assert actual_result == get_expected_employer

    def test_failed_create_employer(
        self,
        override_crud_user,
        get_employer_data,
        get_random_user,
        get_test_session,
        monkeypatch,
    ) -> None:
        monkeypatch.setattr(
            "app.crud.crud_user.user.get_by_attribute",
            override_crud_user.get_by_attribute,
        )

        get_employer_data.pop("user_id")
        get_employer_data["user"] = {
            "email": get_random_user.email,
            "phone": random_phone(),
            "password": random_password(),
        }
        with pytest.raises(HTTPBadRequestException):
            employer.create(EmployerCreate(**get_employer_data), get_test_session)


class TestManagerGetEmployer:
    def test_successful_get_employer(
        self,
        get_test_session,
        get_expected_employer,
        mocker: MockerFixture,
    ) -> None:
        mocked_employer_get = mocker.patch(
            "app.manager.manager_employer.employer.crud.get",
            return_value=get_expected_employer,
        )

        actual_result = employer.fetch_one(get_expected_employer.id, get_test_session)

        mocked_employer_get.assert_called_once_with(get_expected_employer.id)
        assert actual_result == get_expected_employer


class TestManagerGetMultipleEmployers:
    def test_successful_get_multiple_employers(
        self,
        get_test_session,
        get_expected_employers,
        mocker: MockerFixture,
    ) -> None:
        mocked_employer_get_multi = mocker.patch(
            "app.manager.manager_employer.employer.crud.get_multi",
            return_value=get_expected_employers,
        )

        actual_result = employer.fetch_all(get_test_session)

        mocked_employer_get_multi.assert_called_once()
        assert actual_result == get_expected_employers


class TestManagerSearchEmployerByParameter:
    def test_successful_search_employers_by_parameter(
        self,
        get_test_session,
        get_expected_employer,
        mocker: MockerFixture,
    ) -> None:
        mocked_employer_search = mocker.patch(
            "app.manager.manager_employer.employer.crud.search_by_parameter",
            return_value=[get_expected_employer],
        )

        parameter = "name"
        actual_result = employer.search(
            parameter, get_expected_employer.name, get_test_session, 1
        )

        mocked_employer_search.assert_called_once_with(
            parameter, get_expected_employer.name, 1
        )
        assert get_expected_employer in actual_result


class TestManagerUpdateEmployer:
    def test_successful_update_employer(
        self,
        get_test_session,
        get_expected_employer,
        get_employer_data,
        mocker: MockerFixture,
    ) -> None:
        employer_in_db = Employer(id=get_expected_employer.id)
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
            return_value=User(id=get_expected_employer.user_id),
        )

        get_employer_data.pop("user_id")
        get_employer_data["id"] = get_expected_employer.id
        mocked_employer_update = mocker.patch(
            "app.manager.manager_employer.employer.crud.update",
            return_value=get_expected_employer,
        )

        employer_in_data = copy(get_employer_data)
        employer_in_data["user"] = {
            "email": random_email(),
            "phone": random_phone(),
            "password": random_password(),
            "role_id": random_integer(),
            "status_type_id": random_integer(),
        }
        employer_in = EmployerUpdate(**employer_in_data)
        actual_result = employer.update(employer_in, get_test_session)

        mocked_employer_update.assert_called_once_with(employer_in_db, employer_in)
        assert actual_result == get_expected_employer

    def test_failed_update_employer(
        self,
        get_test_session,
        get_expected_employer,
        get_employer_data,
        override_crud_user,
        get_random_user,
        mocker,
        monkeypatch,
    ) -> None:
        mocker.patch(
            "app.manager.manager_employer.employer.crud.get",
            return_value=get_expected_employer,
        )
        monkeypatch.setattr(
            "app.crud.crud_user.user.get_by_attribute",
            override_crud_user.get_by_attribute,
        )

        get_employer_data.pop("user_id")
        get_employer_data["id"] = random_integer()
        get_employer_data["user"] = {
            "email": get_random_user.email,
            "phone": random_phone(),
            "password": random_password(),
            "role_id": random_integer(),
            "status_type_id": random_integer(),
        }
        with pytest.raises(HTTPBadRequestException):
            employer.update(EmployerUpdate(**get_employer_data), get_test_session)


class TestManagerDeleteEmployer:
    def test_successful_delete_employer(
        self,
        get_test_session,
        get_expected_employer,
        mocker: MockerFixture,
    ) -> None:
        mocker.patch(
            "app.manager.manager_employer.employer.crud.get",
            return_value=get_expected_employer,
        )

        mocked_user_delete = mocker.patch(
            "app.crud.crud_user.user.delete",
            return_value=None,
        )

        employer.delete(get_expected_employer.id, get_test_session)

        mocked_user_delete.assert_called_once_with(get_expected_employer.user_id)
