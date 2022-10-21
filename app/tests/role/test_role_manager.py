from pytest_mock import MockerFixture

from app.db.models import Role
from app.manager.manager_role import role
from app.schemas.schema_role import RoleCreate, RoleUpdate
from app.tests.utils.base import random_string


class TestManagerCreateRole:
    def test_successful_create_role(
        self,
        session,
        expected_role,
        mocker: MockerFixture,
    ) -> None:
        mocked_role_create = mocker.patch(
            "app.manager.manager_role.role.crud.create",
            return_value=expected_role,
        )

        role_in = RoleCreate(name=expected_role.name)
        actual_result = role.create(role_in, session)

        mocked_role_create.assert_called_once_with(role_in)
        assert actual_result == expected_role


class TestManagerGetRole:
    def test_successful_get_role(
        self,
        session,
        expected_role,
        mocker: MockerFixture,
    ) -> None:
        mocked_role_get = mocker.patch(
            "app.manager.manager_role.role.crud.get",
            return_value=expected_role,
        )

        actual_result = role.fetch_one(expected_role.id, session)

        mocked_role_get.assert_called_once_with(expected_role.id)
        assert actual_result == expected_role


class TestManagerGetMultipleRoles:
    def test_successful_get_multiple_roles(
        self,
        session,
        expected_roles,
        mocker: MockerFixture,
    ) -> None:
        mocked_role_get_multi = mocker.patch(
            "app.manager.manager_role.role.crud.get_multi",
            return_value=expected_roles,
        )

        actual_result = role.fetch_all(session)

        mocked_role_get_multi.assert_called_once()
        assert actual_result == expected_roles


class TestManagerSearchRoleByParameter:
    def test_successful_search_roles_by_parameter(
        self,
        session,
        expected_role,
        mocker: MockerFixture,
    ) -> None:
        mocked_role_search_by_parameter = mocker.patch(
            "app.manager.manager_role.role.crud.search_by_parameter",
            return_value=[
                expected_role,
            ],
        )

        parameter = "name"
        actual_result = role.search(
            parameter,
            expected_role.name,
            session,
            1,
        )

        mocked_role_search_by_parameter.assert_called_once_with(
            parameter,
            expected_role.name,
            1,
        )
        assert expected_role in actual_result


class TestManagerUpdateRole:
    def test_successful_update_role(
        self,
        session,
        expected_role,
        mocker: MockerFixture,
    ) -> None:
        role_in_db = Role(id=expected_role.id, name=random_string())
        mocked_role_get = mocker.patch(
            "app.manager.manager_role.role.crud.get",
            return_value=role_in_db,
        )

        mocked_role_update = mocker.patch(
            "app.manager.manager_role.role.crud.update",
            return_value=expected_role,
        )

        role_in = RoleUpdate(id=expected_role.id, name=expected_role.name)
        actual_result = role.update(role_in, session)

        mocked_role_get.assert_called_once_with(expected_role.id)
        mocked_role_update.assert_called_once_with(role_in_db, role_in)
        assert actual_result == expected_role


class TestManagerDeleteRole:
    def test_successful_delete_role(
        self,
        session,
        expected_role,
        mocker: MockerFixture,
    ) -> None:
        mocker_role_delete = mocker.patch(
            "app.manager.manager_role.role.crud.delete",
            return_value=expected_role,
        )

        role.delete(expected_role.id, session)

        mocker_role_delete.assert_called_once_with(expected_role.id)
