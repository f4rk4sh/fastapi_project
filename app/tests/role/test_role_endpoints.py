from importlib import reload

import pytest
from fastapi import Response, status
from fastapi.testclient import TestClient

from pytest_mock import MockerFixture

from app.api.routes.role import endpoints
from app.db.models import Session, Role
from app.schemas.role import RoleCreate, RoleUpdate
from app.security import permissions
from app.tests.utils.base import random_string, random_integer
from app.tests.utils.mocks import mock_permission_decorator


class TestEndpointCreateRole:
    def test_successful_create_role(
            self,
            client: TestClient,
            get_test_session: Session,
            monkeypatch,
            mocker: MockerFixture,
    ) -> None:
        monkeypatch.setattr(permissions, "permission", mock_permission_decorator)
        reload(endpoints)

        name = random_string()
        expected_result = Role(id=random_integer(), name=name)
        mocked_role_create = mocker.patch(
            "app.manager.manager_role.role.create",
            return_value=expected_result,
        )

        actual_result = endpoints.create_role(RoleCreate(name=name), get_test_session)

        mocked_role_create.assert_called_once_with(RoleCreate(name=name), get_test_session)
        assert actual_result.name == expected_result.name

    @pytest.mark.xfail(strict=True)
    def test_failed_create_role(
            self,
            client: TestClient,
            get_test_session: Session,
            monkeypatch,
            mocker: MockerFixture,
    ) -> None:
        monkeypatch.setattr(permissions, "permission", mock_permission_decorator)
        reload(endpoints)

        name = random_string()
        mocked_role_create = mocker.patch(
            "app.manager.manager_role.role.create",
            return_value=Role(id=random_integer(), name=name),
        )

        actual_result = endpoints.create_role({"name": name}, get_test_session)  # noqa

        mocked_role_create.assert_called_once_with({"name": name}, get_test_session)
        assert not actual_result


class TestEndpointGetRole:
    def test_successful_get_role(
            self,
            client: TestClient,
            get_test_session: Session,
            monkeypatch,
            mocker: MockerFixture,
    ) -> None:
        monkeypatch.setattr(permissions, "permission", mock_permission_decorator)
        reload(endpoints)

        id = random_integer()
        expected_result = Role(id=id, name=random_string())
        mocked_role_fetch_one = mocker.patch(
            "app.manager.manager_role.role.fetch_one",
            return_value=expected_result,
        )

        actual_result = endpoints.fetch_role(id, get_test_session)

        mocked_role_fetch_one.assert_called_once_with(id, get_test_session)
        assert actual_result.id == expected_result.id

    @pytest.mark.xfail(strict=True)
    def test_failed_get_role(
            self,
            client: TestClient,
            monkeypatch,
            mocker: MockerFixture,
    ) -> None:
        monkeypatch.setattr(permissions, "permission", mock_permission_decorator)
        reload(endpoints)

        id = random_integer()
        mocked_role_fetch_one = mocker.patch(
            "app.manager.manager_role.role.fetch_one",
            return_value=Role(id=id, name=random_string()),
        )

        actual_result = endpoints.fetch_role(id)

        mocked_role_fetch_one.assert_called_once_with(id)
        assert not actual_result


class TestEndpointGetMultipleRoles:
    def test_successful_get_multiple_roles(
            self,
            client: TestClient,
            get_test_session: Session,
            monkeypatch,
            mocker: MockerFixture,
    ) -> None:
        monkeypatch.setattr(permissions, "permission", mock_permission_decorator)
        reload(endpoints)

        expected_result = [Role(id=random_integer(), name=random_string()) for _ in range(3)]
        mocked_role_fetch_all = mocker.patch(
            "app.manager.manager_role.role.fetch_all",
            return_value=expected_result,
        )

        actual_result = endpoints.fetch_roles(get_test_session)

        mocked_role_fetch_all.assert_called_once_with(get_test_session)
        assert actual_result == expected_result

    @pytest.mark.xfail(strict=True)
    def test_failed_get_multiple_roles(
            self,
            client: TestClient,
            monkeypatch,
            mocker: MockerFixture,
    ) -> None:
        monkeypatch.setattr(permissions, "permission", mock_permission_decorator)
        reload(endpoints)

        mocked_role_fetch_all = mocker.patch(
            "app.manager.manager_role.role.fetch_all",
            return_value=[Role(id=random_integer(), name=random_string()) for _ in range(3)],
        )

        actual_result = endpoints.fetch_roles()

        mocked_role_fetch_all.assert_called_once()
        assert not actual_result


class TestEndpointSearchRoleByParameter:
    def test_successful_search_roles_by_parameter(
            self,
            client: TestClient,
            get_test_session: Session,
            monkeypatch,
            mocker: MockerFixture,
    ) -> None:
        monkeypatch.setattr(permissions, "permission", mock_permission_decorator)
        reload(endpoints)

        name = random_string()
        parameter = "name"
        expected_role = Role(id=random_integer(), name=name)
        mocked_role_search = mocker.patch(
            "app.manager.manager_role.role.search",
            return_value=[expected_role, ],
        )

        actual_result = endpoints.search_roles(parameter, name, 1, get_test_session)

        mocked_role_search.assert_called_once_with(parameter, name, get_test_session, 1)
        assert expected_role in actual_result

    @pytest.mark.xfail(strict=True)
    def test_failed_search_roles_by_parameter(
            self,
            client: TestClient,
            get_test_session: Session,
            monkeypatch,
            mocker: MockerFixture,
    ) -> None:
        monkeypatch.setattr(permissions, "permission", mock_permission_decorator)
        reload(endpoints)

        parameter = "name"
        mocked_role_search = mocker.patch(
            "app.manager.manager_role.role.search",
            return_value=[Role(id=random_integer(), name=random_string()), ],
        )

        actual_result = endpoints.search_roles(parameter, 1, get_test_session)  # noqa

        mocked_role_search.assert_called_once_with(parameter, get_test_session, 1)
        assert not actual_result


class TestEndpointUpdateRole:
    def test_successful_update_role(
            self,
            client: TestClient,
            get_test_session: Session,
            monkeypatch,
            mocker: MockerFixture,
    ) -> None:
        monkeypatch.setattr(permissions, "permission", mock_permission_decorator)
        reload(endpoints)

        id = random_integer()
        new_name = random_string()
        expected_result = Role(id=id, name=new_name)
        mocked_role_update = mocker.patch(
            "app.manager.manager_role.role.update",
            return_value=expected_result,
        )

        actual_result = endpoints.update_role(RoleUpdate(id=id, name=new_name), get_test_session)

        mocked_role_update.assert_called_once_with(RoleUpdate(id=id, name=new_name), get_test_session)
        assert actual_result.name == expected_result.name

    @pytest.mark.xfail(strict=True)
    def test_failed_update_role(
            self,
            client: TestClient,
            get_test_session: Session,
            monkeypatch,
            mocker: MockerFixture,
    ) -> None:
        monkeypatch.setattr(permissions, "permission", mock_permission_decorator)
        reload(endpoints)

        mocked_role_update = mocker.patch(
            "app.manager.manager_role.role.update",
            return_value=Role(id=random_integer(), name=random_string()),
        )

        actual_result = endpoints.update_role(get_test_session)

        mocked_role_update.assert_called_once_with(get_test_session)
        assert not actual_result


class TestEndpointDeleteRole:
    def test_successful_delete_role(
            self,
            client: TestClient,
            get_test_session: Session,
            monkeypatch,
            mocker: MockerFixture,
    ):
        monkeypatch.setattr(permissions, "permission", mock_permission_decorator)
        reload(endpoints)

        id = random_integer()
        expected_result = Response(status_code=status.HTTP_204_NO_CONTENT)
        mocked_role_delete = mocker.patch(
            "app.manager.manager_role.role.delete",
            return_value=expected_result,
        )

        actual_result = endpoints.delete_role(id, get_test_session)

        mocked_role_delete.assert_called_once_with(id, get_test_session)
        assert actual_result == expected_result

    @pytest.mark.xfail(strict=True)
    def test_failed_delete_role(
            self,
            client: TestClient,
            get_test_session: Session,
            monkeypatch,
            mocker: MockerFixture,
    ):
        monkeypatch.setattr(permissions, "permission", mock_permission_decorator)
        reload(endpoints)

        mocked_role_delete = mocker.patch(
            "app.manager.manager_role.role.delete",
            return_value=Response(status_code=status.HTTP_204_NO_CONTENT),
        )

        actual_result = endpoints.delete_role(get_test_session)

        mocked_role_delete.assert_called_once_with(get_test_session)
        assert not actual_result
