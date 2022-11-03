from importlib import reload

from pytest_mock import MockerFixture

from app.api.routes.role import endpoints
from app.schemas.schema_role import RoleCreate, RoleUpdate
from app.security import permissions
from app.tests.utils.base import random_integer
from app.tests.utils.mocks import mock_permission_decorator


class TestEndpointCreateRole:
    def test_successful_create_role(
        self,
        session,
        expected_role,
        monkeypatch,
        mocker: MockerFixture,
    ) -> None:
        monkeypatch.setattr(permissions, "permission", mock_permission_decorator)
        reload(endpoints)

        mocked_role_create = mocker.patch(
            "app.manager.manager_role.role.create",
            return_value=expected_role,
        )

        role_in = RoleCreate(name=expected_role.name)
        actual_result = endpoints.create_role(role_in, session)

        mocked_role_create.assert_called_once_with(role_in, session)
        assert actual_result == expected_role


class TestEndpointGetRole:
    def test_successful_get_role(
        self,
        session,
        expected_role,
        monkeypatch,
        mocker: MockerFixture,
    ) -> None:
        monkeypatch.setattr(permissions, "permission", mock_permission_decorator)
        reload(endpoints)

        mocked_role_fetch_one = mocker.patch(
            "app.manager.manager_role.role.fetch_one",
            return_value=expected_role,
        )

        actual_result = endpoints.fetch_role(expected_role.id, session)

        mocked_role_fetch_one.assert_called_once_with(
            expected_role.id, session
        )
        assert actual_result == expected_role


class TestEndpointGetMultipleRoles:
    def test_successful_get_multiple_roles(
        self,
        session,
        expected_roles,
        monkeypatch,
        mocker: MockerFixture,
    ) -> None:
        monkeypatch.setattr(permissions, "permission", mock_permission_decorator)
        reload(endpoints)

        mocked_role_fetch_all = mocker.patch(
            "app.manager.manager_role.role.fetch_all",
            return_value=expected_roles,
        )

        actual_result = endpoints.fetch_roles(session)

        mocked_role_fetch_all.assert_called_once_with(session)
        assert actual_result == expected_roles


class TestEndpointSearchRoleByParameter:
    def test_successful_search_roles_by_parameter(
        self,
        session,
        expected_role,
        monkeypatch,
        mocker: MockerFixture,
    ) -> None:
        monkeypatch.setattr(permissions, "permission", mock_permission_decorator)
        reload(endpoints)

        mocked_role_search = mocker.patch(
            "app.manager.manager_role.role.search",
            return_value=[
                expected_role,
            ],
        )

        parameter = "name"
        actual_result = endpoints.search_roles(
            parameter, expected_role.name, 1, session
        )

        mocked_role_search.assert_called_once_with(
            parameter, expected_role.name, 1, session
        )
        assert expected_role in actual_result


class TestEndpointUpdateRole:
    def test_successful_update_role(
        self,
        session,
        expected_role,
        monkeypatch,
        mocker: MockerFixture,
    ) -> None:
        monkeypatch.setattr(permissions, "permission", mock_permission_decorator)
        reload(endpoints)

        mocked_role_update = mocker.patch(
            "app.manager.manager_role.role.update",
            return_value=expected_role,
        )

        role_in = RoleUpdate(id=expected_role.id, name=expected_role.name)
        actual_result = endpoints.update_role(role_in, session)

        mocked_role_update.assert_called_once_with(role_in, session)
        assert actual_result == expected_role


class TestEndpointDeleteRole:
    def test_successful_delete_role(
        self,
        session,
        expected_response_no_content,
        monkeypatch,
        mocker: MockerFixture,
    ):
        monkeypatch.setattr(permissions, "permission", mock_permission_decorator)
        reload(endpoints)

        mocked_role_delete = mocker.patch(
            "app.manager.manager_role.role.delete",
            return_value=expected_response_no_content,
        )

        role_id = random_integer()
        actual_result = endpoints.delete_role(role_id, session)

        mocked_role_delete.assert_called_once_with(role_id, session)
        assert actual_result == expected_response_no_content
