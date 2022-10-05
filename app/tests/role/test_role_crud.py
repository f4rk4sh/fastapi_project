import pytest
from pytest_mock import MockFixture
from sqlalchemy.exc import DataError, ProgrammingError
from sqlalchemy.orm import Session

from app.crud.crud_role import role
from app.schemas.role import RoleCreate, RoleUpdate
from app.tests.utils.base import random_string


class TestCRUDCreateRole:
    def test_success_create_role_from_schema(
        self,
        override_crud_role,
        monkeypatch,
        mocker: MockFixture,
    ) -> None:
        monkeypatch.setattr("app.crud.crud_role.role.create", override_crud_role.create)
        spy_role_create = mocker.spy(role, "create")

        name = random_string()
        created_role = role.create(RoleCreate(name=name))

        spy_role_create.assert_called_once_with(RoleCreate(name=name))
        assert created_role.name == name

    def test_successful_create_role_from_dict(
        self,
        override_crud_role,
        monkeypatch,
        mocker: MockFixture,
    ) -> None:
        monkeypatch.setattr("app.crud.crud_role.role.create", override_crud_role.create)
        spy_role_create = mocker.spy(role, "create")

        name = random_string()
        created_role = role.create({"name": name})

        spy_role_create.assert_called_once_with({"name": name})
        assert created_role.name == name

    def test_successful_create_role_is_flush(
        self,
        override_crud_role,
        db: Session,
        monkeypatch,
        mocker: MockFixture,
    ) -> None:
        monkeypatch.setattr("app.crud.crud_role.role.create", override_crud_role.create)
        monkeypatch.setattr(
            "app.crud.crud_role.role.get_multi", override_crud_role.get_multi
        )
        spy_role_create = mocker.spy(role, "create")

        name = random_string()
        created_role = role.create(RoleCreate(name=name), is_flush=True)

        db.rollback()

        roles_in_db = role.get_multi()

        spy_role_create.assert_called_once_with(RoleCreate(name=name), is_flush=True)
        assert created_role not in roles_in_db

    def test_failed_create_role(
        self,
        override_crud_role,
        monkeypatch,
    ) -> None:

        monkeypatch.setattr("app.crud.crud_role.role.create", override_crud_role.create)

        with pytest.raises(TypeError):
            role.create({"fullname": random_string()})


class TestCRUDGetRole:
    def test_successful_get_role(
        self, override_crud_role, random_role, monkeypatch, mocker: MockFixture
    ) -> None:
        monkeypatch.setattr("app.crud.crud_role.role.get", override_crud_role.get)
        spy_role_get = mocker.spy(role, "get")

        role_in_db = role.get(random_role.id)

        spy_role_get.assert_called_once_with(random_role.id)
        assert role_in_db.id == random_role.id
        assert role_in_db.name == random_role.name

    def test_failed_get_role(
        self,
        override_crud_role,
        random_role,
        monkeypatch,
    ) -> None:
        monkeypatch.setattr("app.crud.crud_role.role.get", override_crud_role.get)

        with pytest.raises(DataError):
            role.get(random_role.name)


class TestCRUDGetMultipleRoles:
    def test_successful_get_multiple_roles(
        self,
        override_crud_role,
        get_random_roles,
        monkeypatch,
        mocker: MockFixture,
    ) -> None:
        monkeypatch.setattr(
            "app.crud.crud_role.role.get_multi", override_crud_role.get_multi
        )
        spy_role_get_multiple = mocker.spy(role, "get_multi")

        roles_in_db = role.get_multi()

        spy_role_get_multiple.assert_called_once()
        for random_role in get_random_roles:
            assert random_role in roles_in_db

    def test_failed_get_multiple_roles(
        self,
        override_crud_role,
        get_random_roles,
        monkeypatch,
    ) -> None:
        monkeypatch.setattr(
            "app.crud.crud_role.role.get_multi", override_crud_role.get_multi
        )

        with pytest.raises(ProgrammingError):
            role.get_multi(limit=-1)


class TestCRUDGetRoleByAttribute:
    def test_successful_get_role_by_attribute(
        self,
        override_crud_role,
        random_role,
        monkeypatch,
        mocker: MockFixture,
    ) -> None:
        monkeypatch.setattr(
            "app.crud.crud_role.role.get_by_attribute",
            override_crud_role.get_by_attribute,
        )
        spy_role_get_by_attribute = mocker.spy(role, "get_by_attribute")

        role_in_db = role.get_by_attribute(name=random_role.name)

        spy_role_get_by_attribute.assert_called_once_with(name=random_role.name)
        assert role_in_db.id == random_role.id
        assert role_in_db.name == random_role.name

    def test_failed_get_role_by_attribute(
        self,
        override_crud_role,
        random_role,
        monkeypatch,
    ) -> None:
        monkeypatch.setattr(
            "app.crud.crud_role.role.get_by_attribute",
            override_crud_role.get_by_attribute,
        )

        with pytest.raises(DataError):
            role.get_by_attribute(name=random_role.id)


class TestCRUDSearchRoleByParameter:
    def test_successful_search_roles_by_parameter(
        self,
        override_crud_role,
        random_role,
        monkeypatch,
        mocker: MockFixture,
    ) -> None:
        monkeypatch.setattr(
            "app.crud.crud_role.role.search_by_parameter",
            override_crud_role.search_by_parameter,
        )
        spy_role_search_by_parameter = mocker.spy(role, "search_by_parameter")

        roles_in_db = role.search_by_parameter(
            parameter="name", keyword=random_role.name
        )

        spy_role_search_by_parameter.assert_called_once_with(
            parameter="name", keyword=random_role.name
        )
        assert random_role in roles_in_db

    def test_failed_search_roles_by_parameter(
        self,
        override_crud_role,
        random_role,
        monkeypatch,
    ) -> None:
        monkeypatch.setattr(
            "app.crud.crud_role.role.search_by_parameter",
            override_crud_role.search_by_parameter,
        )

        with pytest.raises(TypeError):
            role.search_by_parameter(parameter=None, keyword=random_role.name)


class TestCRUDUpdateRole:
    def test_successful_update_role_from_schema(
        self,
        override_crud_role,
        random_role,
        monkeypatch,
        mocker: MockFixture,
    ) -> None:
        monkeypatch.setattr("app.crud.crud_role.role.get", override_crud_role.get)
        monkeypatch.setattr("app.crud.crud_role.role.update", override_crud_role.update)
        spy_role_update = mocker.spy(role, "update")

        role_in_db = role.get(random_role.id)

        new_name = random_string()
        updated_role = role.update(
            role_in_db, RoleUpdate(id=random_role.id, name=new_name)
        )

        spy_role_update.assert_called_once_with(
            role_in_db, RoleUpdate(id=random_role.id, name=new_name)
        )
        assert updated_role.name == new_name

    def test_successful_update_role_from_dict(
        self,
        override_crud_role,
        random_role,
        monkeypatch,
        mocker: MockFixture,
    ) -> None:
        monkeypatch.setattr("app.crud.crud_role.role.get", override_crud_role.get)
        monkeypatch.setattr("app.crud.crud_role.role.update", override_crud_role.update)
        spy_role_update = mocker.spy(role, "update")

        role_in_db = role.get(random_role.id)

        new_name = random_string()
        updated_role = role.update(role_in_db, {"id": random_role.id, "name": new_name})

        spy_role_update.assert_called_once_with(
            role_in_db, {"id": random_role.id, "name": new_name}
        )
        assert updated_role.name == new_name

    def test_failed_update_role(
        self,
        override_crud_role,
        random_role,
        monkeypatch,
    ) -> None:
        monkeypatch.setattr("app.crud.crud_role.role.get", override_crud_role.get)
        monkeypatch.setattr("app.crud.crud_role.role.update", override_crud_role.update)

        with pytest.raises(TypeError):
            role_in_db = role.get(random_role.id)
            role.update(role_in_db)


class TestCRUDDeleteRole:
    def test_successful_delete_role(
        self,
        override_crud_role,
        random_role,
        monkeypatch,
        mocker: MockFixture,
    ) -> None:
        monkeypatch.setattr("app.crud.crud_role.role.delete", override_crud_role.delete)
        monkeypatch.setattr(
            "app.crud.crud_role.role.get_by_attribute",
            override_crud_role.get_by_attribute,
        )
        spy_role_delete = mocker.spy(role, "delete")

        role.delete(random_role.id)
        role_in_db = role.get_by_attribute(id=random_role.id)

        spy_role_delete.assert_called_once_with(random_role.id)
        assert not role_in_db

    def test_failed_delete_role(
        self,
        override_crud_role,
        random_role,
        monkeypatch,
    ) -> None:
        monkeypatch.setattr("app.crud.crud_role.role.delete", override_crud_role.delete)
        monkeypatch.setattr(
            "app.crud.crud_role.role.get_by_attribute",
            override_crud_role.get_by_attribute,
        )

        with pytest.raises(DataError):
            role.delete(random_role.name)
