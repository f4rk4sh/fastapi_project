from pytest_mock import MockerFixture
from sqlalchemy.orm import Session

from app.db.models import Role
from app.manager.manager_role import role
from app.schemas.role import RoleCreate, RoleUpdate
from app.tests.utils.base import random_integer, random_string


class TestManagerCreateRole:
    def test_successful_create_role(
        self,
        get_test_session: Session,
        mocker: MockerFixture,
    ) -> None:
        name = random_string()
        expected_result = Role(id=random_integer(), name=name)
        mocked_role_create = mocker.patch(
            "app.manager.manager_role.role.crud.create",
            return_value=expected_result,
        )

        actual_result = role.create(RoleCreate(name=name), get_test_session)

        mocked_role_create.assert_called_once_with(RoleCreate(name=name))
        assert actual_result.name == expected_result.name


class TestManagerGetRole:
    def test_successful_get_role(
        self,
        get_test_session: Session,
        mocker: MockerFixture,
    ) -> None:
        role_id = random_integer()
        expected_result = Role(id=role_id, name=random_string())
        mocked_role_get = mocker.patch(
            "app.manager.manager_role.role.crud.get",
            return_value=expected_result,
        )

        actual_result = role.fetch_one(role_id, get_test_session)

        mocked_role_get.assert_called_once_with(role_id)
        assert actual_result.name == expected_result.name


class TestManagerGetMultipleRoles:
    def test_successful_get_multiple_roles(
        self,
        get_test_session: Session,
        mocker: MockerFixture,
    ) -> None:
        expected_result = [
            Role(id=random_integer(), name=random_string()) for _ in range(3)
        ]
        mocked_role_get_multi = mocker.patch(
            "app.manager.manager_role.role.crud.get_multi",
            return_value=expected_result,
        )

        actual_result = role.fetch_all(get_test_session)

        mocked_role_get_multi.assert_called_once()
        assert actual_result == expected_result


class TestManagerSearchRoleByParameter:
    def test_successful_search_roles_by_parameter(
        self,
        get_test_session: Session,
        mocker: MockerFixture,
    ) -> None:
        name = random_string()
        parameter = "name"
        expected_role = Role(id=random_integer(), name=name)
        mocked_role_search_by_parameter = mocker.patch(
            "app.manager.manager_role.role.crud.search_by_parameter",
            return_value=[
                expected_role,
            ],
        )

        actual_result = role.search(parameter, name, get_test_session, 1)

        mocked_role_search_by_parameter.assert_called_once_with(parameter, name, 1)
        assert expected_role in actual_result


class TestManagerUpdateRole:
    def test_successful_update_role(
        self,
        get_test_session: Session,
        mocker: MockerFixture,
    ) -> None:
        role_id = random_integer()
        name = random_string()
        role_in_db = Role(id=role_id, name=name)
        mocked_role_get = mocker.patch(
            "app.manager.manager_role.role.crud.get",
            return_value=role_in_db,
        )

        new_name = random_string()
        expected_result = Role(id=role_id, name=new_name)
        mocked_role_update = mocker.patch(
            "app.manager.manager_role.role.crud.update",
            return_value=expected_result,
        )

        actual_result = role.update(RoleUpdate(id=role_id, name=new_name), get_test_session)

        mocked_role_get.assert_called_once_with(role_id)
        mocked_role_update.assert_called_once_with(
            role_in_db, RoleUpdate(id=role_id, name=new_name)
        )
        assert actual_result.name == expected_result.name


class TestManagerDeleteRole:
    def test_successful_delete_role(
        self,
        get_test_session: Session,
        mocker: MockerFixture,
    ) -> None:
        role_id = random_integer()
        mocker_role_delete = mocker.patch(
            "app.manager.manager_role.role.crud.delete",
            return_value=Role(id=role_id, name=random_string()),
        )

        role.delete(role_id, get_test_session)

        mocker_role_delete.assert_called_once_with(role_id)
