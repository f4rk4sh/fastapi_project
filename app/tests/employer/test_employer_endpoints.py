from importlib import reload

from fastapi import Response, status
from pytest_mock import MockerFixture

from app.api.routes.employer import endpoints
from app.db.models import Session, Employer
from app.schemas.employer import EmployerCreate, EmployerUpdate
from app.security import permissions
from app.tests.utils.base import random_string, random_integer, random_date, random_email, random_phone, random_password
from app.tests.utils.mocks import mock_permission_decorator


class TestEndpointCreateEmployer:
    def test_successful_create_employer(
        self,
        get_test_session: Session,
        monkeypatch,
        mocker: MockerFixture,
    ) -> None:
        monkeypatch.setattr(permissions, "permission", mock_permission_decorator)
        reload(endpoints)

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
            user_id=random_integer(),
            **employer_data,
        )
        mocked_employer_create = mocker.patch(
            "app.manager.manager_employer.employer.create",
            return_value=expected_result,
        )

        employer_data["user"] = {
            "email": random_email(),
            "phone": random_phone(),
            "password": random_password(),
        }
        actual_result = endpoints.create_employer(
            EmployerCreate(**employer_data), get_test_session
        )

        mocked_employer_create.assert_called_once_with(
            EmployerCreate(**employer_data), get_test_session
        )
        assert actual_result == expected_result


class TestEndpointGetEmployer:
    def test_successful_get_employer(
        self,
        get_test_session: Session,
        monkeypatch,
        mocker: MockerFixture,
    ) -> None:
        monkeypatch.setattr(permissions, "permission", mock_permission_decorator)
        reload(endpoints)

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
        mocked_employer_fetch_one = mocker.patch(
            "app.manager.manager_employer.employer.fetch_one",
            return_value=expected_result,
        )

        actual_result = endpoints.fetch_employer(employer_id, get_test_session)

        mocked_employer_fetch_one.assert_called_once_with(employer_id, get_test_session)
        assert actual_result.id == expected_result.id


class TestEndpointGetMultipleEmployers:
    def test_successful_get_multiple_employers(
        self,
        get_test_session: Session,
        monkeypatch,
        mocker: MockerFixture,
    ) -> None:
        monkeypatch.setattr(permissions, "permission", mock_permission_decorator)
        reload(endpoints)

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
            ) for _ in range(3)
        ]

        mocked_employer_fetch_all = mocker.patch(
            "app.manager.manager_employer.employer.fetch_all",
            return_value=expected_result,
        )

        actual_result = endpoints.fetch_employers(get_test_session)

        mocked_employer_fetch_all.assert_called_once_with(get_test_session)
        assert actual_result == expected_result


class TestEndpointSearchEmployerByParameter:
    def test_successful_search_employers_by_parameter(
        self,
        get_test_session: Session,
        monkeypatch,
        mocker: MockerFixture,
    ) -> None:
        monkeypatch.setattr(permissions, "permission", mock_permission_decorator)
        reload(endpoints)

        edrpou = random_string()
        parameter = "edrpou"
        expected_employer = Employer(
            id=random_integer(),
            user_id=random_integer(),
            name=random_string(),
            address=random_string(),
            edrpou=edrpou,
            expire_contract_date=random_date(in_future=True),
            salary_date=random_date(),
            prepayment_date=random_date(),
            employer_type_id=random_integer(),
        )

        mocked_employer_search = mocker.patch(
            "app.manager.manager_employer.employer.search",
            return_value=[
                expected_employer,
            ],
        )

        actual_result = endpoints.search_employers(parameter, edrpou, 1, get_test_session)

        mocked_employer_search.assert_called_once_with(
            parameter, edrpou, get_test_session, 1
        )
        assert expected_employer in actual_result


class TestEndpointUpdateEmployer:
    def test_successful_update_employer(
        self,
        get_test_session: Session,
        monkeypatch,
        mocker: MockerFixture,
    ) -> None:
        monkeypatch.setattr(permissions, "permission", mock_permission_decorator)
        reload(endpoints)

        new_address = random_string()
        employer_data = {
            "id": random_integer(),
            "name": random_string(),
            "address": new_address,
            "edrpou": random_string(),
            "expire_contract_date": random_date(in_future=True),
            "salary_date": random_date(),
            "prepayment_date": random_date(),
            "employer_type_id": random_integer(),
        }

        expected_result = Employer(
            user_id=random_integer(),
            **employer_data
        )

        mocked_employer_update = mocker.patch(
            "app.manager.manager_employer.employer.update",
            return_value=expected_result,
        )

        employer_data["user"] = {
            "email": random_email(),
            "phone": random_phone(),
            "password": random_password(),
            "role_id": random_integer(),
            "status_type_id": random_integer(),
        }

        actual_result = endpoints.update_employer(
            EmployerUpdate(**employer_data), get_test_session
        )

        mocked_employer_update.assert_called_once_with(
            EmployerUpdate(**employer_data), get_test_session
        )
        assert actual_result.address == expected_result.address


class TestEndpointDeleteEmployer:
    def test_successful_delete_employer(
        self,
        get_test_session: Session,
        monkeypatch,
        mocker: MockerFixture,
    ) -> None:
        monkeypatch.setattr(permissions, "permission", mock_permission_decorator)
        reload(endpoints)

        employer_id = random_integer()
        expected_result = Response(status_code=status.HTTP_204_NO_CONTENT)
        mocker_employer_delete = mocker.patch(
            "app.manager.manager_employer.employer.delete",
            return_value=expected_result,
        )

        actual_result = endpoints.delete_employer(employer_id, get_test_session)

        mocker_employer_delete.assert_called_once_with(employer_id, get_test_session)
        assert actual_result == expected_result
