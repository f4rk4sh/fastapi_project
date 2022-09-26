from importlib import reload

from fastapi.testclient import TestClient
from unittest import mock

from pytest_mock import MockerFixture

from app.api.routes.role import endpoints
from app.db.models import Session, Role
from app.manager.manager_role import role
from app.schemas.role import RoleCreate
from app.tests.utils.base import random_string
from app.tests.utils.mocks import mock_permission_decorator


class TestCreateRole:
    def test_create_role(
            self,
            client_as_su: TestClient,
            get_test_session: Session,
            mocker: MockerFixture
    ) -> None:
        with mock.patch("app.security.permissions.permission", mock_permission_decorator):
            reload(endpoints)

            name = random_string()
            return_value = Role(name=name)
            role.create = mock.Mock(return_value=return_value)

            spy = mocker.spy(role, "create")

            result = endpoints.create_role(RoleCreate(name=name), get_test_session)

            spy.assert_called_once_with(RoleCreate(name=name), get_test_session)
            assert result.name == name
