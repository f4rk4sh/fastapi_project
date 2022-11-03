from importlib import reload

from pytest_mock import MockerFixture

from app.api.routes.employer_type import endpoints
from app.schemas.schema_employer_type import EmployerTypeCreate, EmployerTypeUpdate
from app.security import permissions
from app.tests.utils.base import random_integer
from app.tests.utils.mocks import mock_permission_decorator


class TestEndpointCreateEmployerType:
    def test_successful_create_employer_type(
        self,
        session,
        expected_employer_type,
        monkeypatch,
        mocker: MockerFixture,
    ) -> None:
        monkeypatch.setattr(permissions, "permission", mock_permission_decorator)
        reload(endpoints)

        mocked_employer_type_create = mocker.patch(
            "app.manager.manager_employer_type.employer_type.create",
            return_value=expected_employer_type,
        )

        employer_type_in = EmployerTypeCreate(name=expected_employer_type.name)
        actual_result = endpoints.create_employer_type(employer_type_in, session)

        mocked_employer_type_create.assert_called_once_with(employer_type_in, session)
        assert actual_result == expected_employer_type


class TestEndpointGetEmployerType:
    def test_successful_get_employer_type(
        self,
        session,
        expected_employer_type,
        monkeypatch,
        mocker: MockerFixture,
    ) -> None:
        monkeypatch.setattr(permissions, "permission", mock_permission_decorator)
        reload(endpoints)

        mocked_employer_type_fetch_one = mocker.patch(
            "app.manager.manager_employer_type.employer_type.fetch_one",
            return_value=expected_employer_type,
        )

        actual_result = endpoints.fetch_employer_type(expected_employer_type.id, session)

        mocked_employer_type_fetch_one.assert_called_once_with(
            expected_employer_type.id, session
        )
        assert actual_result == expected_employer_type


class TestEndpointGetMultipleEmployerTypes:
    def test_successful_get_multiple_employer_type(
        self,
        session,
        expected_employer_types,
        monkeypatch,
        mocker: MockerFixture,
    ) -> None:
        monkeypatch.setattr(permissions, "permission", mock_permission_decorator)
        reload(endpoints)

        mocked_employer_type_fetch_all = mocker.patch(
            "app.manager.manager_employer_type.employer_type.fetch_all",
            return_value=expected_employer_types,
        )

        actual_result = endpoints.fetch_employer_types(session)

        mocked_employer_type_fetch_all.assert_called_once_with(session)
        assert actual_result == expected_employer_types


class TestEndpointSearchEmployerTypeByParameter:
    def test_successful_search_employer_types_by_parameter(
        self,
        session,
        expected_employer_type,
        monkeypatch,
        mocker: MockerFixture,
    ) -> None:
        monkeypatch.setattr(permissions, "permission", mock_permission_decorator)
        reload(endpoints)

        mocked_employer_type_search = mocker.patch(
            "app.manager.manager_employer_type.employer_type.search",
            return_value=[expected_employer_type],
        )

        parameter = "name"
        actual_result = endpoints.search_employer_types(
            parameter, expected_employer_type.name, 1, session
        )

        mocked_employer_type_search.assert_called_once_with(
            parameter, expected_employer_type.name, 1, session
        )
        assert expected_employer_type in actual_result


class TestEndpointUpdateEmployerType:
    def test_successful_update_employer_type(
        self,
        session,
        expected_employer_type,
        monkeypatch,
        mocker: MockerFixture,
    ) -> None:
        monkeypatch.setattr(permissions, "permission", mock_permission_decorator)
        reload(endpoints)

        mocked_employer_type_update = mocker.patch(
            "app.manager.manager_employer_type.employer_type.update",
            return_value=expected_employer_type,
        )

        employer_type_in = EmployerTypeUpdate(
            id=expected_employer_type.id, name=expected_employer_type.name
        )
        actual_result = endpoints.update_employer_type(employer_type_in, session)

        mocked_employer_type_update.assert_called_once_with(employer_type_in, session)
        assert actual_result == expected_employer_type


class TestEndpointDeleteEmployerType:
    def test_successful_delete_employer_type(
        self,
        session,
        expected_response_no_content,
        monkeypatch,
        mocker: MockerFixture,
    ) -> None:
        monkeypatch.setattr(permissions, "permission", mock_permission_decorator)
        reload(endpoints)

        mocked_employer_type_update = mocker.patch(
            "app.manager.manager_employer_type.employer_type.delete",
            return_value=expected_response_no_content,
        )

        employer_type_id = random_integer()
        actual_result = endpoints.delete_employer_type(employer_type_id, session)

        mocked_employer_type_update.assert_called_once_with(employer_type_id, session)
        assert actual_result == expected_response_no_content
