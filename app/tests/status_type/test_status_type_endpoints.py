from importlib import reload

from pytest_mock import MockerFixture

from app.api.routes.status_type import endpoints
from app.schemas.schema_status_type import StatusTypeCreate, StatusTypeUpdate
from app.security import permissions
from app.tests.utils.base import random_integer
from app.tests.utils.mocks import mock_permission_decorator


class TestEndpointCreateStatusType:
    def test_successful_create_status_type(
        self,
        session,
        expected_status_type,
        monkeypatch,
        mocker: MockerFixture,
    ) -> None:
        monkeypatch.setattr(permissions, "permission", mock_permission_decorator)
        reload(endpoints)

        mocked_status_type_create = mocker.patch(
            "app.manager.manager_status_type.status_type.create",
            return_value=expected_status_type,
        )

        status_type_in = StatusTypeCreate(name=expected_status_type.name)
        actual_result = endpoints.create_status_type(status_type_in, session)

        mocked_status_type_create.assert_called_once_with(status_type_in, session)
        assert actual_result == expected_status_type


class TestEndpointGetStatusType:
    def test_successful_get_status_type(
        self,
        session,
        expected_status_type,
        monkeypatch,
        mocker: MockerFixture,
    ) -> None:
        monkeypatch.setattr(permissions, "permission", mock_permission_decorator)
        reload(endpoints)

        mocked_status_type_fetch_one = mocker.patch(
            "app.manager.manager_status_type.status_type.fetch_one",
            return_value=expected_status_type,
        )

        actual_result = endpoints.fetch_status_type(expected_status_type.id, session)

        mocked_status_type_fetch_one.assert_called_once_with(
            expected_status_type.id, session
        )
        assert actual_result == expected_status_type


class TestEndpointGetMultipleStatusTypes:
    def test_successful_get_multiple_status_type(
        self,
        session,
        expected_status_types,
        monkeypatch,
        mocker: MockerFixture,
    ) -> None:
        monkeypatch.setattr(permissions, "permission", mock_permission_decorator)
        reload(endpoints)

        mocked_status_type_fetch_all = mocker.patch(
            "app.manager.manager_status_type.status_type.fetch_all",
            return_value=expected_status_types,
        )

        actual_result = endpoints.fetch_status_types(session)

        mocked_status_type_fetch_all.assert_called_once_with(session)
        assert actual_result == expected_status_types


class TestEndpointSearchStatusTypeByParameter:
    def test_successful_search_status_types_by_parameter(
        self,
        session,
        expected_status_type,
        monkeypatch,
        mocker: MockerFixture,
    ) -> None:
        monkeypatch.setattr(permissions, "permission", mock_permission_decorator)
        reload(endpoints)

        mocked_status_type_search = mocker.patch(
            "app.manager.manager_status_type.status_type.search",
            return_value=[expected_status_type],
        )

        parameter = "name"
        actual_result = endpoints.search_status_types(
            parameter, expected_status_type.name, 1, session
        )

        mocked_status_type_search.assert_called_once_with(
            parameter, expected_status_type.name, session, 1
        )
        assert expected_status_type in actual_result


class TestEndpointUpdateStatusType:
    def test_successful_update_status_type(
        self,
        session,
        expected_status_type,
        monkeypatch,
        mocker: MockerFixture,
    ) -> None:
        monkeypatch.setattr(permissions, "permission", mock_permission_decorator)
        reload(endpoints)

        mocked_status_type_update = mocker.patch(
            "app.manager.manager_status_type.status_type.update",
            return_value=expected_status_type,
        )

        status_type_in = StatusTypeUpdate(
            id=expected_status_type.id, name=expected_status_type.name
        )
        actual_result = endpoints.update_status_type(status_type_in, session)

        mocked_status_type_update.assert_called_once_with(status_type_in, session)
        assert actual_result == expected_status_type


class TestEndpointDeleteStatusType:
    def test_successful_update_status_type(
        self,
        session,
        expected_response_no_content,
        monkeypatch,
        mocker: MockerFixture,
    ) -> None:
        monkeypatch.setattr(permissions, "permission", mock_permission_decorator)
        reload(endpoints)

        mocked_status_type_update = mocker.patch(
            "app.manager.manager_status_type.status_type.delete",
            return_value=expected_response_no_content,
        )

        status_type_id = random_integer()
        actual_result = endpoints.delete_status_type(status_type_id, session)

        mocked_status_type_update.assert_called_once_with(status_type_id, session)
        assert actual_result == expected_response_no_content
