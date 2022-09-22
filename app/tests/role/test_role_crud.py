import pytest
from pytest_mock import MockFixture
from sqlalchemy.orm import Session

from app.schemas.role import RoleCreate, RoleUpdate
from app.tests.utils.base import random_string


class TestCreateRole:
    def test_success_create_role_from_schema(
            self,
            override_crud_role,
            mocker: MockFixture
    ) -> None:
        spy = mocker.spy(override_crud_role, "create")

        name = random_string()
        role = override_crud_role.create(RoleCreate(name=name))

        spy.assert_called_once()
        assert role
        assert role.name == name

    def test_successful_create_role_from_dict(
            self,
            override_crud_role,
            mocker: MockFixture
    ) -> None:
        spy = mocker.spy(override_crud_role, "create")

        name = random_string()
        role = override_crud_role.create({"name": name})

        spy.assert_called_once()
        assert role
        assert role.name == name

    def test_successful_create_role_is_flush(
            self,
            override_crud_role,
            db: Session,
            mocker: MockFixture
    ) -> None:
        spy = mocker.spy(override_crud_role, "create")

        role = override_crud_role.create(RoleCreate(name=random_string()), is_flush=True)

        db.rollback()

        roles_in_db = override_crud_role.get_multi()

        spy.assert_called_once()
        assert role not in roles_in_db

    @pytest.mark.xfail(strict=True)
    def test_failed_create_role(
            self,
            override_crud_role,
            mocker: MockFixture
    ) -> None:
        spy = mocker.spy(override_crud_role, "create")

        role = override_crud_role.create({"name": random_string(51)})
        role_in_db = override_crud_role.get(role.id)

        spy.assert_called_once()
        assert not role_in_db


class TestGetRole:
    def test_successful_get_role(
            self,
            override_crud_role,
            mocker: MockFixture
    ) -> None:
        spy = mocker.spy(override_crud_role, "get")

        role = override_crud_role.create(RoleCreate(name=random_string()))
        role_in_db = override_crud_role.get(role.id)

        spy.assert_called_once()
        assert role_in_db
        assert role_in_db.id == role.id
        assert role_in_db.name == role.name

    @pytest.mark.xfail(strict=True)
    def test_failed_get_role(
            self,
            override_crud_role,
            mocker: MockFixture
    ) -> None:
        spy = mocker.spy(override_crud_role, "get")

        role = override_crud_role.create(RoleCreate(name=random_string()))
        role_in_db = override_crud_role.get(role.name)

        spy.assert_called_once()
        assert not role_in_db


class TestGetMultipleRoles:
    def test_successful_get_multiple_roles(
            self,
            override_crud_role,
            mocker: MockFixture
    ) -> None:
        spy = mocker.spy(override_crud_role, "get_multi")

        roles = [override_crud_role.create(RoleCreate(name=random_string())) for _ in range(3)]
        roles_in_db = override_crud_role.get_multi()

        spy.assert_called_once()
        assert roles_in_db
        for role in roles:
            assert role in roles_in_db

    @pytest.mark.xfail(strict=True)
    def test_failed_get_multiple_roles(
            self,
            override_crud_role,
            mocker: MockFixture
    ) -> None:
        spy = mocker.spy(override_crud_role, "get_multi")

        roles = [override_crud_role.create(RoleCreate(name=random_string())) for _ in range(3)]
        roles_in_db = override_crud_role.get_multi(limit=-1)

        spy.assert_called_once()
        assert not roles_in_db
        for role in roles:
            assert role not in roles_in_db


class TestGetRoleByAttribute:
    def test_successful_get_role_by_attribute(
            self,
            override_crud_role,
            mocker: MockFixture
    ) -> None:
        spy = mocker.spy(override_crud_role, "get_by_attribute")

        role = override_crud_role.create(RoleCreate(name=random_string()))
        role_in_db = override_crud_role.get_by_attribute(name=role.name)

        spy.assert_called_once()
        assert role_in_db
        assert role_in_db.id == role.id
        assert role_in_db.name == role.name

    @pytest.mark.xfail(strict=True)
    def test_failed_get_role_by_attribute(
            self,
            override_crud_role,
            mocker: MockFixture
    ) -> None:
        spy = mocker.spy(override_crud_role, "get_by_attribute")

        role = override_crud_role.create(RoleCreate(name=random_string()))
        role_in_db = override_crud_role.get_by_attribute(name=role.id)

        spy.assert_called_once()
        assert not role_in_db


class TestSearchRoleByParameter:
    def test_successful_search_roles_by_parameter(
            self,
            override_crud_role,
            mocker: MockFixture
    ) -> None:
        spy = mocker.spy(override_crud_role, "search_by_parameter")

        role = override_crud_role.create(RoleCreate(name=random_string()))
        roles_in_db = override_crud_role.search_by_parameter(parameter="name", keyword=role.name)

        spy.assert_called_once()
        assert roles_in_db
        assert role in roles_in_db

    @pytest.mark.xfail(strict=True)
    def test_failed_search_roles_by_parameter(
            self,
            override_crud_role,
            mocker: MockFixture
    ) -> None:
        spy = mocker.spy(override_crud_role, "search_by_parameter")

        role = override_crud_role.create(RoleCreate(name=random_string()))
        roles_in_db = override_crud_role.search_by_parameter(parameter=None, keyword=role.name)

        spy.assert_called_once()
        assert not roles_in_db


class TestUpdateRole:
    def test_successful_update_role_from_schema(
            self,
            override_crud_role,
            mocker: MockFixture
    ) -> None:
        spy = mocker.spy(override_crud_role, "update")

        role = override_crud_role.create(RoleCreate(name=random_string()))
        role_in_db = override_crud_role.get(role.id)

        new_name = random_string()
        updated_role = override_crud_role.update(role_in_db, RoleUpdate(id=role.id, name=new_name))

        spy.assert_called_once()
        assert updated_role
        assert updated_role.name == new_name

    def test_successful_update_role_from_dict(
            self,
            override_crud_role,
            mocker: MockFixture
    ) -> None:
        spy = mocker.spy(override_crud_role, "update")

        role = override_crud_role.create(RoleCreate(name=random_string()))
        role_in_db = override_crud_role.get(role.id)

        new_name = random_string()
        updated_role = override_crud_role.update(role_in_db, {"id": role.id, "name": new_name})

        spy.assert_called_once()
        assert updated_role
        assert updated_role.name == new_name

    @pytest.mark.xfail(strict=True)
    def test_failed_update_role(
            self,
            override_crud_role,
            mocker: MockFixture
    ) -> None:
        spy = mocker.spy(override_crud_role, "update")

        role = override_crud_role.create(RoleCreate(name=random_string()))
        role_in_db = override_crud_role.get(role.id)

        new_name = random_string()
        override_crud_role.update(role_in_db, RoleUpdate(id=role.id, new_name=new_name))

        role_in_db = override_crud_role.get(role.id)

        spy.assert_called_once()
        assert role_in_db.name != new_name


class TestDeleteRole:
    def test_successful_delete_role(
            self,
            override_crud_role,
            mocker: MockFixture
    ) -> None:
        spy = mocker.spy(override_crud_role, "delete")

        role = override_crud_role.create(RoleCreate(name=random_string()))
        override_crud_role.delete(role.id)
        role_in_db = override_crud_role.get_by_attribute(id=role.id)

        spy.assert_called_once()
        assert not role_in_db

    @pytest.mark.xfail(strict=True)
    def test_failed_delete_role(
            self,
            override_crud_role,
            mocker: MockFixture
    ) -> None:
        spy = mocker.spy(override_crud_role, "delete")

        role = override_crud_role.create(RoleCreate(name=random_string()))
        override_crud_role.delete(role.id)
        role_in_db = override_crud_role.get_by_attribute(id=role.name)

        spy.assert_called_once()
        assert role_in_db
