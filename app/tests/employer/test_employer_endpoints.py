from importlib import reload

from pytest_mock import MockerFixture

from app.api.routes.employer import endpoints
from app.schemas.employer import EmployerCreate, EmployerUpdate
from app.security import permissions
from app.tests.utils.base import (random_email, random_integer,
                                  random_password, random_phone)
from app.tests.utils.mocks import mock_permission_decorator


class TestEndpointCreateEmployer:
    def test_successful_create_employer(
        self,
        get_test_session,
        get_expected_employer,
        monkeypatch,
        mocker: MockerFixture,
    ) -> None:
        monkeypatch.setattr(permissions, "permission", mock_permission_decorator)
        reload(endpoints)

        mocked_employer_create = mocker.patch(
            "app.manager.manager_employer.employer.create",
            return_value=get_expected_employer,
        )

        employer_in = EmployerCreate(
            **{
                "user": {
                    "email": random_email(),
                    "phone": random_phone(),
                    "password": random_password(),
                },
                "name": get_expected_employer.name,
                "address": get_expected_employer.address,
                "edrpou": get_expected_employer.edrpou,
                "expire_contract_date": get_expected_employer.expire_contract_date,
                "salary_date": get_expected_employer.salary_date,
                "prepayment_date": get_expected_employer.prepayment_date,
                "employer_type_id": get_expected_employer.employer_type_id,
            }
        )
        actual_result = endpoints.create_employer(employer_in, get_test_session)

        mocked_employer_create.assert_called_once_with(employer_in, get_test_session)
        assert actual_result == get_expected_employer


class TestEndpointGetEmployer:
    def test_successful_get_employer(
        self,
        get_test_session,
        get_expected_employer,
        monkeypatch,
        mocker: MockerFixture,
    ) -> None:
        monkeypatch.setattr(permissions, "permission", mock_permission_decorator)
        reload(endpoints)

        mocked_employer_fetch_one = mocker.patch(
            "app.manager.manager_employer.employer.fetch_one",
            return_value=get_expected_employer,
        )

        actual_result = endpoints.fetch_employer(
            get_expected_employer.id, get_test_session
        )

        mocked_employer_fetch_one.assert_called_once_with(
            get_expected_employer.id, get_test_session
        )
        assert actual_result == get_expected_employer


class TestEndpointGetMultipleEmployers:
    def test_successful_get_multiple_employers(
        self,
        get_test_session,
        get_expected_employers,
        monkeypatch,
        mocker: MockerFixture,
    ) -> None:
        monkeypatch.setattr(permissions, "permission", mock_permission_decorator)
        reload(endpoints)

        mocked_employer_fetch_all = mocker.patch(
            "app.manager.manager_employer.employer.fetch_all",
            return_value=get_expected_employers,
        )

        actual_result = endpoints.fetch_employers(get_test_session)

        mocked_employer_fetch_all.assert_called_once_with(get_test_session)
        assert actual_result == get_expected_employers


class TestEndpointSearchEmployerByParameter:
    def test_successful_search_employers_by_parameter(
        self,
        get_test_session,
        get_expected_employer,
        monkeypatch,
        mocker: MockerFixture,
    ) -> None:
        monkeypatch.setattr(permissions, "permission", mock_permission_decorator)
        reload(endpoints)

        mocked_employer_search = mocker.patch(
            "app.manager.manager_employer.employer.search",
            return_value=[get_expected_employer],
        )

        parameter = "edrpou"
        actual_result = endpoints.search_employers(
            parameter, get_expected_employer.edrpou, 1, get_test_session
        )

        mocked_employer_search.assert_called_once_with(
            parameter, get_expected_employer.edrpou, get_test_session, 1
        )
        assert get_expected_employer in actual_result


class TestEndpointUpdateEmployer:
    def test_successful_update_employer(
        self,
        get_test_session,
        get_expected_employer,
        monkeypatch,
        mocker: MockerFixture,
    ) -> None:
        monkeypatch.setattr(permissions, "permission", mock_permission_decorator)
        reload(endpoints)

        mocked_employer_update = mocker.patch(
            "app.manager.manager_employer.employer.update",
            return_value=get_expected_employer,
        )

        employer_in = EmployerUpdate(
            **{
                "user": {
                    "email": random_email(),
                    "phone": random_phone(),
                    "password": random_password(),
                    "role_id": random_integer(),
                    "status_type_id": random_integer(),
                },
                "id": get_expected_employer.id,
                "name": get_expected_employer.name,
                "address": get_expected_employer.address,
                "edrpou": get_expected_employer.edrpou,
                "expire_contract_date": get_expected_employer.expire_contract_date,
                "salary_date": get_expected_employer.salary_date,
                "prepayment_date": get_expected_employer.prepayment_date,
                "employer_type_id": get_expected_employer.employer_type_id,
            }
        )
        actual_result = endpoints.update_employer(employer_in, get_test_session)

        mocked_employer_update.assert_called_once_with(employer_in, get_test_session)
        assert actual_result.address == get_expected_employer.address


class TestEndpointDeleteEmployer:
    def test_successful_delete_employer(
        self,
        get_test_session,
        get_expected_response_no_content,
        monkeypatch,
        mocker: MockerFixture,
    ) -> None:
        monkeypatch.setattr(permissions, "permission", mock_permission_decorator)
        reload(endpoints)

        mocker_employer_delete = mocker.patch(
            "app.manager.manager_employer.employer.delete",
            return_value=get_expected_response_no_content,
        )

        employer_id = random_integer()
        actual_result = endpoints.delete_employer(employer_id, get_test_session)

        mocker_employer_delete.assert_called_once_with(employer_id, get_test_session)
        assert actual_result == get_expected_response_no_content
