from importlib import reload

from pytest_mock import MockerFixture

from app.api.routes.employer import endpoints
from app.schemas.schema_employer import EmployerCreate, EmployerUpdate
from app.security import permissions
from app.tests.utils.base import random_integer
from app.tests.utils.mocks import mock_permission_decorator


class TestEndpointCreateEmployer:
    def test_successful_create_employer(
        self,
        session,
        expected_employer,
        user_create_data,
        monkeypatch,
        mocker: MockerFixture,
    ) -> None:
        monkeypatch.setattr(permissions, "permission", mock_permission_decorator)
        reload(endpoints)

        mocked_employer_create = mocker.patch(
            "app.manager.manager_employer.employer.create",
            return_value=expected_employer,
        )

        employer_in = EmployerCreate(
            **{
                "user": user_create_data,
                "name": expected_employer.name,
                "address": expected_employer.address,
                "edrpou": expected_employer.edrpou,
                "expire_contract_date": expected_employer.expire_contract_date,
                "salary_date": expected_employer.salary_date,
                "prepayment_date": expected_employer.prepayment_date,
                "employer_type_id": expected_employer.employer_type_id,
            }
        )
        actual_result = endpoints.create_employer(employer_in, session)

        mocked_employer_create.assert_called_once_with(employer_in, session)
        assert actual_result == expected_employer


class TestEndpointGetEmployer:
    def test_successful_get_employer(
        self,
        session,
        expected_employer,
        monkeypatch,
        mocker: MockerFixture,
    ) -> None:
        monkeypatch.setattr(permissions, "permission", mock_permission_decorator)
        reload(endpoints)

        mocked_employer_fetch_one = mocker.patch(
            "app.manager.manager_employer.employer.fetch_one",
            return_value=expected_employer,
        )

        actual_result = endpoints.fetch_employer(
            expected_employer.id, session
        )

        mocked_employer_fetch_one.assert_called_once_with(
            expected_employer.id, session
        )
        assert actual_result == expected_employer


class TestEndpointGetMultipleEmployers:
    def test_successful_get_multiple_employers(
        self,
        session,
        expected_employers,
        monkeypatch,
        mocker: MockerFixture,
    ) -> None:
        monkeypatch.setattr(permissions, "permission", mock_permission_decorator)
        reload(endpoints)

        mocked_employer_fetch_all = mocker.patch(
            "app.manager.manager_employer.employer.fetch_all",
            return_value=expected_employers,
        )

        actual_result = endpoints.fetch_employers(session)

        mocked_employer_fetch_all.assert_called_once_with(session)
        assert actual_result == expected_employers


class TestEndpointSearchEmployerByParameter:
    def test_successful_search_employers_by_parameter(
        self,
        session,
        expected_employer,
        monkeypatch,
        mocker: MockerFixture,
    ) -> None:
        monkeypatch.setattr(permissions, "permission", mock_permission_decorator)
        reload(endpoints)

        mocked_employer_search = mocker.patch(
            "app.manager.manager_employer.employer.search",
            return_value=[expected_employer],
        )

        parameter = "edrpou"
        actual_result = endpoints.search_employers(
            parameter, expected_employer.edrpou, 1, session
        )

        mocked_employer_search.assert_called_once_with(
            parameter, expected_employer.edrpou, session, 1
        )
        assert expected_employer in actual_result


class TestEndpointUpdateEmployer:
    def test_successful_update_employer(
        self,
        session,
        expected_employer,
        user_update_data,
        monkeypatch,
        mocker: MockerFixture,
    ) -> None:
        monkeypatch.setattr(permissions, "permission", mock_permission_decorator)
        reload(endpoints)

        mocked_employer_update = mocker.patch(
            "app.manager.manager_employer.employer.update",
            return_value=expected_employer,
        )

        employer_in = EmployerUpdate(
            **{
                "user": user_update_data,
                "id": expected_employer.id,
                "name": expected_employer.name,
                "address": expected_employer.address,
                "edrpou": expected_employer.edrpou,
                "expire_contract_date": expected_employer.expire_contract_date,
                "salary_date": expected_employer.salary_date,
                "prepayment_date": expected_employer.prepayment_date,
                "employer_type_id": expected_employer.employer_type_id,
            }
        )
        actual_result = endpoints.update_employer(employer_in, session)

        mocked_employer_update.assert_called_once_with(employer_in, session)
        assert actual_result.address == expected_employer.address


class TestEndpointDeleteEmployer:
    def test_successful_delete_employer(
        self,
        session,
        expected_response_no_content,
        monkeypatch,
        mocker: MockerFixture,
    ) -> None:
        monkeypatch.setattr(permissions, "permission", mock_permission_decorator)
        reload(endpoints)

        mocker_employer_delete = mocker.patch(
            "app.manager.manager_employer.employer.delete",
            return_value=expected_response_no_content,
        )

        employer_id = random_integer()
        actual_result = endpoints.delete_employer(employer_id, session)

        mocker_employer_delete.assert_called_once_with(employer_id, session)
        assert actual_result == expected_response_no_content
