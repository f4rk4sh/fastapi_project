import pytest
from pytest_mock import MockerFixture
from sqlalchemy.orm import Session


from app.db.models import Role
from app.manager.manager_role import role
from app.schemas.role import RoleCreate, RoleUpdate
from app.tests.utils.base import random_string, random_integer


class TestManagerCreateRole:
    def test_successful_create_role(
            self,
            get_test_session: Session,
            mocker: MockerFixture,
    ) -> None:
        name = random_string()
        expected_result = Role(id=random_integer(), name=name)
        mocked_create = mocker.patch(
            "app.manager.manager_role.role.crud.create",
            return_value=expected_result,
        )

        actual_result = role.create(RoleCreate(name=name), get_test_session)

        mocked_create.assert_called_once_with(RoleCreate(name=name))
        assert actual_result.name == expected_result.name

    @pytest.mark.xfail(strict=True)
    def test_failed_create_role(
            self,
            get_test_session: Session,
            mocker: MockerFixture,
    ) -> None:
        mocked_create = mocker.patch(
            "app.manager.manager_role.role.crud.create",
            return_value=Role(id=random_integer(), name=random_string()),
        )

        actual_result = role.create(get_test_session)  # noqa

        mocked_create.assert_called_once()
        assert not actual_result


class TestManagerGetRole:
    def test_successful_get_role(
            self,
            get_test_session: Session,
            mocker: MockerFixture,
    ) -> None:
        id = random_integer()
        expected_result = Role(id=id, name=random_string())
        mocked_get = mocker.patch(
            "app.manager.manager_role.role.crud.get",
            return_value=expected_result,
        )

        actual_result = role.fetch_one(id, get_test_session)

        mocked_get.assert_called_once_with(id)
        assert actual_result.name == expected_result.name

    @pytest.mark.xfail(strict=True)
    def test_failed_get_role(
            self,
            get_test_session: Session,
            mocker: MockerFixture,
    ) -> None:
        id = random_integer()
        mocked_get = mocker.patch(
            "app.manager.manager_role.role.crud.get",
            return_value=Role(id=id, name=random_string()),
        )

        actual_result = role.fetch_one(id)  # noqa

        mocked_get.assert_called_once_with(id)
        assert not actual_result


class TestManagerGetMultipleRoles:
    def test_successful_get_multiple_roles(
            self,
            get_test_session: Session,
            mocker: MockerFixture,
    ) -> None:
        expected_result = [Role(id=random_integer(), name=random_string()) for _ in range(3)]
        mocked_get_multi = mocker.patch(
            "app.manager.manager_role.role.crud.get_multi",
            return_value=expected_result,
        )

        actual_result = role.fetch_all(get_test_session)

        mocked_get_multi.assert_called_once()
        assert actual_result == expected_result

    @pytest.mark.xfail(strict=True)
    def test_failed_get_multiple_roles(
            self,
            get_test_session: Session,
            mocker: MockerFixture,
    ) -> None:
        mocked_get_multi = mocker.patch(
            "app.manager.manager_role.role.crud.get_multi",
            return_value=[Role(id=random_integer(), name=random_string()) for _ in range(3)],
        )

        actual_result = role.fetch_all()  # noqa

        mocked_get_multi.assert_called_once()
        assert not actual_result


class TestManagerSearchRoleByParameter:
    def test_successful_search_roles_by_parameter(
            self,
            get_test_session: Session,
            mocker: MockerFixture,
    ) -> None:
        name = random_string()
        parameter = "name"
        expected_role = Role(id=random_integer(), name=name)
        mocked_search_by_parameter = mocker.patch(
            "app.manager.manager_role.role.crud.search_by_parameter",
            return_value=[expected_role, ],
        )

        actual_result = role.search(parameter, name, get_test_session, 1)

        mocked_search_by_parameter.assert_called_once_with(parameter, name, 1)
        assert expected_role in actual_result

    @pytest.mark.xfail(strict=True)
    def test_failed_search_roles_by_parameter(
            self,
            get_test_session: Session,
            mocker: MockerFixture,
    ) -> None:
        parameter = "name"
        mocked_search_by_parameter = mocker.patch(
            "app.manager.manager_role.role.crud.search_by_parameter",
            return_value=[Role(id=random_integer(), name=random_string()), ],
        )

        actual_result = role.search(parameter, get_test_session, 100)  # noqa

        mocked_search_by_parameter.assert_called_once_with(parameter, 100)
        assert not actual_result


class TestManagerUpdateRole:
    def test_successful_update_role(
            self,
            get_test_session: Session,
            mocker: MockerFixture,
    ) -> None:
        id = random_integer()
        name = random_string()
        role_in_db = Role(id=id, name=name)
        mocked_get = mocker.patch(
            "app.manager.manager_role.role.crud.get",
            return_value=role_in_db,
        )

        new_name = random_string()
        expected_result = Role(id=id, name=new_name)
        mocked_update = mocker.patch(
            "app.manager.manager_role.role.crud.update",
            return_value=expected_result,
        )

        actual_result = role.update(RoleUpdate(id=id, name=new_name), get_test_session)

        mocked_get.assert_called_once_with(id)
        mocked_update.assert_called_once_with(role_in_db, RoleUpdate(id=id, name=new_name))
        assert actual_result.name == expected_result.name

    @pytest.mark.xfail(strict=True)
    def test_failed_update_role(
            self,
            get_test_session: Session,
            mocker: MockerFixture,
    ) -> None:
        id = random_integer()
        name = random_string()
        role_in_db = Role(id=id, name=name)
        mocked_get = mocker.patch(
            "app.manager.manager_role.role.crud.get",
            return_value=None,
        )

        new_name = random_string()
        expected_result = Role(id=id, name=new_name)
        mocked_update = mocker.patch(
            "app.manager.manager_role.role.crud.update",
            return_value=expected_result,
        )

        actual_result = role.update(RoleUpdate(id=id, name=new_name), get_test_session)

        mocked_get.assert_called_once_with(id)
        mocked_update.assert_called_once_with(role_in_db, RoleUpdate(id=id, name=new_name))
        assert not actual_result


class TestManagerDeleteRole:
    def test_successful_delete_role(
            self,
            get_test_session: Session,
            mocker: MockerFixture,
    ) -> None:
        id = random_integer()
        mocker_delete = mocker.patch(
            "app.manager.manager_role.role.crud.delete",
            return_value=Role(id=id, name=random_string()),
        )

        role.delete(id, get_test_session)

        mocker_delete.assert_called_once_with(id)

    @pytest.mark.xfail(strict=True)
    def test_failed_delete_role(
            self,
            get_test_session: Session,
            mocker: MockerFixture,
    ) -> None:
        id = random_integer()
        mocker_delete = mocker.patch(
            "app.manager.manager_role.role.crud.delete",
            return_value=Role(id=id, name=random_string()),
        )

        actual_result = role.delete(get_test_session)  # noqa

        mocker_delete.assert_called_once()
        assert not actual_result
