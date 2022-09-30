import pytest
from pytest_mock import MockFixture
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
        assert created_role
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
        assert created_role
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

    @pytest.mark.xfail(strict=True)
    def test_failed_create_role(
        self,
        override_crud_role,
        monkeypatch,
        mocker: MockFixture,
    ) -> None:
        monkeypatch.setattr("app.crud.crud_role.role.create", override_crud_role.create)
        monkeypatch.setattr("app.crud.crud_role.role.get", override_crud_role.get)
        spy_role_create = mocker.spy(role, "create")

        name = random_string(51)
        created_role = role.create({"name": name})
        role_in_db = role.get(created_role.id)

        spy_role_create.assert_called_once_with({"name": name})
        assert not role_in_db


class TestCRUDGetRole:
    def test_successful_get_role(
        self, override_crud_role, monkeypatch, mocker: MockFixture
    ) -> None:
        monkeypatch.setattr("app.crud.crud_role.role.create", override_crud_role.create)
        monkeypatch.setattr("app.crud.crud_role.role.get", override_crud_role.get)
        spy_role_get = mocker.spy(role, "get")

        created_role = role.create(RoleCreate(name=random_string()))
        role_in_db = role.get(created_role.id)

        spy_role_get.assert_called_once_with(created_role.id)
        assert role_in_db
        assert role_in_db.id == created_role.id
        assert role_in_db.name == created_role.name

    @pytest.mark.xfail(strict=True)
    def test_failed_get_role(
        self, override_crud_role, monkeypatch, mocker: MockFixture
    ) -> None:
        monkeypatch.setattr("app.crud.crud_role.role.create", override_crud_role.create)
        monkeypatch.setattr("app.crud.crud_role.role.get", override_crud_role.get)
        spy_role_get = mocker.spy(role, "get")

        created_role = role.create(RoleCreate(name=random_string()))
        role_in_db = role.get(created_role.name)

        spy_role_get.assert_called_once_with(created_role.name)
        assert not role_in_db


class TestCRUDGetMultipleRoles:
    def test_successful_get_multiple_roles(
        self,
        override_crud_role,
        monkeypatch,
        mocker: MockFixture,
    ) -> None:
        monkeypatch.setattr("app.crud.crud_role.role.create", override_crud_role.create)
        monkeypatch.setattr(
            "app.crud.crud_role.role.get_multi", override_crud_role.get_multi
        )
        spy_role_get_multiple = mocker.spy(role, "get_multi")

        created_roles = [
            role.create(RoleCreate(name=random_string())) for _ in range(3)
        ]
        roles_in_db = role.get_multi()

        spy_role_get_multiple.assert_called_once()
        assert roles_in_db
        for created_role in created_roles:
            assert created_role in roles_in_db

    @pytest.mark.xfail(strict=True)
    def test_failed_get_multiple_roles(
        self,
        override_crud_role,
        monkeypatch,
        mocker: MockFixture,
    ) -> None:
        monkeypatch.setattr("app.crud.crud_role.role.create", override_crud_role.create)
        monkeypatch.setattr(
            "app.crud.crud_role.role.get_multi", override_crud_role.get_multi
        )
        spy_role_get_multiple = mocker.spy(role, "get_multi")

        created_roles = [
            role.create(RoleCreate(name=random_string())) for _ in range(3)
        ]
        roles_in_db = role.get_multi(limit=-1)

        spy_role_get_multiple.assert_called_once_with(limit=-1)
        assert not roles_in_db
        for created_role in created_roles:
            assert created_role not in roles_in_db


class TestCRUDGetRoleByAttribute:
    def test_successful_get_role_by_attribute(
        self,
        override_crud_role,
        monkeypatch,
        mocker: MockFixture,
    ) -> None:
        monkeypatch.setattr("app.crud.crud_role.role.create", override_crud_role.create)
        monkeypatch.setattr(
            "app.crud.crud_role.role.get_by_attribute",
            override_crud_role.get_by_attribute,
        )
        spy_role_get_by_attribute = mocker.spy(role, "get_by_attribute")

        created_role = role.create(RoleCreate(name=random_string()))
        role_in_db = role.get_by_attribute(name=created_role.name)

        spy_role_get_by_attribute.assert_called_once_with(name=created_role.name)
        assert role_in_db
        assert role_in_db.id == created_role.id
        assert role_in_db.name == created_role.name

    @pytest.mark.xfail(strict=True)
    def test_failed_get_role_by_attribute(
        self,
        override_crud_role,
        monkeypatch,
        mocker: MockFixture,
    ) -> None:
        monkeypatch.setattr("app.crud.crud_role.role.create", override_crud_role.create)
        monkeypatch.setattr(
            "app.crud.crud_role.role.get_by_attribute",
            override_crud_role.get_by_attribute,
        )
        spy_role_get_by_attribute = mocker.spy(role, "get_by_attribute")

        created_role = role.create(RoleCreate(name=random_string()))
        role_in_db = role.get_by_attribute(name=created_role.id)

        spy_role_get_by_attribute.assert_called_once_with(name=created_role.id)
        assert not role_in_db


class TestCRUDSearchRoleByParameter:
    def test_successful_search_roles_by_parameter(
        self,
        override_crud_role,
        monkeypatch,
        mocker: MockFixture,
    ) -> None:
        monkeypatch.setattr("app.crud.crud_role.role.create", override_crud_role.create)
        monkeypatch.setattr(
            "app.crud.crud_role.role.search_by_parameter",
            override_crud_role.search_by_parameter,
        )
        spy_role_search_by_parameter = mocker.spy(role, "search_by_parameter")

        created_role = role.create(RoleCreate(name=random_string()))
        roles_in_db = role.search_by_parameter(
            parameter="name", keyword=created_role.name
        )

        spy_role_search_by_parameter.assert_called_once_with(
            parameter="name", keyword=created_role.name
        )
        assert roles_in_db
        assert created_role in roles_in_db

    @pytest.mark.xfail(strict=True)
    def test_failed_search_roles_by_parameter(
        self,
        override_crud_role,
        monkeypatch,
        mocker: MockFixture,
    ) -> None:
        monkeypatch.setattr("app.crud.crud_role.role.create", override_crud_role.create)
        monkeypatch.setattr(
            "app.crud.crud_role.role.search_by_parameter",
            override_crud_role.search_by_parameter,
        )
        spy = mocker.spy(role, "search_by_parameter")

        created_role = role.create(RoleCreate(name=random_string()))
        roles_in_db = role.search_by_parameter(
            parameter=None, keyword=created_role.name
        )

        spy.assert_called_once_with(parameter=None, keyword=created_role.name)
        assert not roles_in_db


class TestCRUDUpdateRole:
    def test_successful_update_role_from_schema(
        self,
        override_crud_role,
        monkeypatch,
        mocker: MockFixture,
    ) -> None:
        monkeypatch.setattr("app.crud.crud_role.role.create", override_crud_role.create)
        monkeypatch.setattr("app.crud.crud_role.role.get", override_crud_role.get)
        monkeypatch.setattr("app.crud.crud_role.role.update", override_crud_role.update)
        spy_role_update = mocker.spy(role, "update")

        created_role = role.create(RoleCreate(name=random_string()))
        role_in_db = role.get(created_role.id)

        new_name = random_string()
        updated_role = role.update(
            role_in_db, RoleUpdate(id=created_role.id, name=new_name)
        )

        spy_role_update.assert_called_once_with(
            role_in_db, RoleUpdate(id=created_role.id, name=new_name)
        )
        assert updated_role
        assert updated_role.name == new_name

    def test_successful_update_role_from_dict(
        self,
        override_crud_role,
        monkeypatch,
        mocker: MockFixture,
    ) -> None:
        monkeypatch.setattr("app.crud.crud_role.role.create", override_crud_role.create)
        monkeypatch.setattr("app.crud.crud_role.role.get", override_crud_role.get)
        monkeypatch.setattr("app.crud.crud_role.role.update", override_crud_role.update)
        spy_role_update = mocker.spy(role, "update")

        created_role = role.create(RoleCreate(name=random_string()))
        role_in_db = role.get(created_role.id)

        new_name = random_string()
        updated_role = role.update(
            role_in_db, {"id": created_role.id, "name": new_name}
        )

        spy_role_update.assert_called_once_with(
            role_in_db, {"id": created_role.id, "name": new_name}
        )
        assert updated_role
        assert updated_role.name == new_name

    @pytest.mark.xfail(strict=True)
    def test_failed_update_role(
        self,
        override_crud_role,
        monkeypatch,
        mocker: MockFixture,
    ) -> None:
        monkeypatch.setattr("app.crud.crud_role.role.create", override_crud_role.create)
        monkeypatch.setattr("app.crud.crud_role.role.get", override_crud_role.get)
        monkeypatch.setattr("app.crud.crud_role.role.update", override_crud_role.update)
        spy_role_update = mocker.spy(role, "update")

        created_role = role.create(RoleCreate(name=random_string()))
        role_in_db = role.get(created_role.id)

        new_name = random_string()
        role.update(role_in_db, RoleUpdate(id=created_role.id, new_name=new_name))

        updated_role_in_db = role.get(created_role.id)

        spy_role_update.assert_called_once_with(
            role_in_db, RoleUpdate(id=created_role.id, new_name=new_name)
        )
        assert updated_role_in_db.name != new_name


class TestCRUDDeleteRole:
    def test_successful_delete_role(
        self,
        override_crud_role,
        monkeypatch,
        mocker: MockFixture,
    ) -> None:
        monkeypatch.setattr("app.crud.crud_role.role.create", override_crud_role.create)
        monkeypatch.setattr("app.crud.crud_role.role.delete", override_crud_role.delete)
        monkeypatch.setattr(
            "app.crud.crud_role.role.get_by_attribute",
            override_crud_role.get_by_attribute,
        )
        spy_role_delete = mocker.spy(role, "delete")

        created_role = role.create(RoleCreate(name=random_string()))
        role.delete(created_role.id)
        role_in_db = role.get_by_attribute(id=created_role.id)

        spy_role_delete.assert_called_once_with(created_role.id)
        assert not role_in_db

    @pytest.mark.xfail(strict=True)
    def test_failed_delete_role(
        self,
        override_crud_role,
        monkeypatch,
        mocker: MockFixture,
    ) -> None:
        monkeypatch.setattr("app.crud.crud_role.role.create", override_crud_role.create)
        monkeypatch.setattr("app.crud.crud_role.role.delete", override_crud_role.delete)
        monkeypatch.setattr(
            "app.crud.crud_role.role.get_by_attribute",
            override_crud_role.get_by_attribute,
        )
        spy_role_delete = mocker.spy(role, "delete")

        created_role = role.create(RoleCreate(name=random_string()))
        role.delete(created_role.name)
        role_in_db = role.get_by_attribute(id=created_role.id)

        spy_role_delete.assert_called_once_with(id=created_role.id)
        assert role_in_db
