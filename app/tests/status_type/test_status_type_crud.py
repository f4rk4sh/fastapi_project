import pytest
from pytest_mock import MockFixture
from sqlalchemy.exc import ProgrammingError, DataError
from sqlalchemy.orm import Session

from app.crud.crud_status_type import status_type
from app.schemas.schema_status_type import StatusTypeCreate, StatusTypeUpdate
from app.tests.utils.base import random_string


class TestCRUDCreateStatusType:
    def test_success_create_status_type_from_schema(
        self,
        crud_status_type,
        monkeypatch,
        mocker: MockFixture,
    ) -> None:
        monkeypatch.setattr(
            "app.crud.crud_status_type.status_type.create",
            crud_status_type.create,
        )
        spy_status_type_create = mocker.spy(status_type, "create")

        name = random_string()
        created_status_type = status_type.create(StatusTypeCreate(name=name))

        spy_status_type_create.assert_called_once_with(StatusTypeCreate(name=name))
        assert created_status_type.name == name

    def test_success_create_status_type_from_dict(
        self,
        crud_status_type,
        monkeypatch,
        mocker: MockFixture,
    ) -> None:
        monkeypatch.setattr(
            "app.crud.crud_status_type.status_type.create",
            crud_status_type.create,
        )
        spy_status_type_create = mocker.spy(status_type, "create")

        name = random_string()
        created_status_type = status_type.create({"name": name})

        spy_status_type_create.assert_called_once_with({"name": name})
        assert created_status_type.name == name

    def test_success_create_status_type_is_flush(
        self,
        crud_status_type,
        db: Session,
        monkeypatch,
        mocker: MockFixture,
    ) -> None:
        monkeypatch.setattr(
            "app.crud.crud_status_type.status_type.create",
            crud_status_type.create,
        )
        monkeypatch.setattr(
            "app.crud.crud_status_type.status_type.get_multi",
            crud_status_type.get_multi,
        )
        spy_status_type_create = mocker.spy(status_type, "create")

        name = random_string()
        created_status_type = status_type.create(
            StatusTypeCreate(name=name), is_flush=True
        )

        db.rollback()

        status_types_in_db = status_type.get_multi()

        spy_status_type_create.assert_called_once_with(
            StatusTypeCreate(name=name), is_flush=True
        )
        assert created_status_type not in status_types_in_db

    def test_failed_create_status_type(
        self,
        crud_status_type,
        monkeypatch,
    ) -> None:
        monkeypatch.setattr(
            "app.crud.crud_status_type.status_type.create",
            crud_status_type.create,
        )

        with pytest.raises(TypeError):
            status_type.create({"address": random_string()})


class TestCRUDGetStatusType:
    def test_successful_get_status_type(
        self,
        crud_status_type,
        random_status_type,
        monkeypatch,
        mocker: MockFixture,
    ) -> None:
        monkeypatch.setattr(
            "app.crud.crud_status_type.status_type.get",
            crud_status_type.get,
        )
        spy_status_type_get = mocker.spy(status_type, "get")

        status_type_in_db = status_type.get(random_status_type.id)

        spy_status_type_get.assert_called_once_with(random_status_type.id)
        assert status_type_in_db == random_status_type

    def test_failed_get_status_type(
        self,
        crud_status_type,
        random_status_type,
        monkeypatch,
    ) -> None:
        monkeypatch.setattr(
            "app.crud.crud_status_type.status_type.get",
            crud_status_type.get,
        )

        with pytest.raises(DataError):
            status_type.get(random_status_type.name)


class TestCRUDGetMultipleStatusTypes:
    def test_successful_get_multiple_status_types(
        self,
        crud_status_type,
        random_status_types,
        monkeypatch,
        mocker: MockFixture,
    ) -> None:
        monkeypatch.setattr(
            "app.crud.crud_status_type.status_type.get_multi",
            crud_status_type.get_multi,
        )
        spy_status_type_get_multi = mocker.spy(status_type, "get_multi")

        status_types_in_db = status_type.get_multi()

        spy_status_type_get_multi.assert_called_once()
        for random_status_type in random_status_types:
            assert random_status_type in status_types_in_db

    def test_failed_get_multiple_status_types(
        self,
        crud_status_type,
        random_status_types,
        monkeypatch,
    ) -> None:
        monkeypatch.setattr(
            "app.crud.crud_status_type.status_type.get_multi",
            crud_status_type.get_multi,
        )

        with pytest.raises(ProgrammingError):
            status_type.get_multi(skip=-1)


class TestCRUDGetStatusTypeByAttribute:
    def test_successful_get_status_type_by_attribute(
        self,
        crud_status_type,
        random_status_type,
        monkeypatch,
        mocker: MockFixture,
    ) -> None:
        monkeypatch.setattr(
            "app.crud.crud_status_type.status_type.get_by_attribute",
            crud_status_type.get_by_attribute,
        )
        spy_status_type_get_by_attribute = mocker.spy(status_type, "get_by_attribute")

        status_type_in_db = status_type.get_by_attribute(name=random_status_type.name)

        spy_status_type_get_by_attribute.assert_called_once_with(
            name=random_status_type.name
        )
        assert status_type_in_db == random_status_type

    def test_failed_get_status_type_by_attribute(
        self,
        crud_status_type,
        random_status_type,
        monkeypatch,
    ) -> None:
        monkeypatch.setattr(
            "app.crud.crud_status_type.status_type.get_by_attribute",
            crud_status_type.get_by_attribute,
        )

        with pytest.raises(DataError):
            status_type.get_by_attribute(name=random_status_type.id)


class TestCRUDSearchStatusTypeByParameter:
    def test_successful_search_status_types_by_parameter(
        self,
        crud_status_type,
        random_status_type,
        monkeypatch,
        mocker: MockFixture,
    ) -> None:
        monkeypatch.setattr(
            "app.crud.crud_status_type.status_type.search_by_parameter",
            crud_status_type.search_by_parameter,
        )
        spy_status_type_search_by_parameter = mocker.spy(
            status_type, "search_by_parameter"
        )
        status_types_in_db = status_type.search_by_parameter(
            parameter="name", keyword=random_status_type.name
        )

        spy_status_type_search_by_parameter.assert_called_once_with(
            parameter="name", keyword=random_status_type.name
        )
        assert random_status_type in status_types_in_db

    def test_failed_search_status_types_by_parameter(
        self,
        crud_status_type,
        random_status_type,
        monkeypatch,
    ) -> None:
        monkeypatch.setattr(
            "app.crud.crud_status_type.status_type.search_by_parameter",
            crud_status_type.search_by_parameter,
        )

        with pytest.raises(TypeError):
            status_type.search_by_parameter(
                parameter=None, keyword=random_status_type.name
            )


class TestCRUDUpdateStatusType:
    def test_successful_update_status_type_from_schema(
        self,
        crud_status_type,
        random_status_type,
        monkeypatch,
        mocker: MockFixture,
    ) -> None:
        monkeypatch.setattr(
            "app.crud.crud_status_type.status_type.get",
            crud_status_type.get,
        )
        monkeypatch.setattr(
            "app.crud.crud_status_type.status_type.update",
            crud_status_type.update,
        )
        spy_status_type_update = mocker.spy(status_type, "update")

        status_type_in_db = status_type.get(random_status_type.id)

        new_name = random_string()
        updated_status_type = status_type.update(
            status_type_in_db,
            StatusTypeUpdate(id=random_status_type.id, name=new_name),
        )

        spy_status_type_update.assert_called_once_with(
            status_type_in_db,
            StatusTypeUpdate(id=random_status_type.id, name=new_name),
        )
        assert updated_status_type.name == new_name

    def test_successful_update_status_type_from_dict(
        self,
        crud_status_type,
        random_status_type,
        monkeypatch,
        mocker: MockFixture,
    ) -> None:
        monkeypatch.setattr(
            "app.crud.crud_status_type.status_type.get",
            crud_status_type.get,
        )
        monkeypatch.setattr(
            "app.crud.crud_status_type.status_type.update",
            crud_status_type.update,
        )
        spy_status_type_update = mocker.spy(status_type, "update")

        status_type_in_db = status_type.get(random_status_type.id)

        new_name = random_string()
        updated_status_type = status_type.update(
            status_type_in_db,
            {"id": random_status_type.id, "name": new_name},
        )

        spy_status_type_update.assert_called_once_with(
            status_type_in_db,
            {"id": random_status_type.id, "name": new_name},
        )
        assert updated_status_type.name == new_name

    def test_failed_update_status_type(
        self,
        crud_status_type,
        random_status_type,
        monkeypatch,
    ) -> None:
        monkeypatch.setattr(
            "app.crud.crud_status_type.status_type.get",
            crud_status_type.get,
        )
        monkeypatch.setattr(
            "app.crud.crud_status_type.status_type.update",
            crud_status_type.update,
        )

        with pytest.raises(TypeError):
            status_type_in_db = status_type.get(random_status_type.id)
            status_type.update(status_type_in_db)


class TestCRUDDeleteStatusType:
    def test_successful_delete_status_type(
        self,
        crud_status_type,
        random_status_type,
        monkeypatch,
        mocker: MockFixture,
    ) -> None:
        monkeypatch.setattr(
            "app.crud.crud_status_type.status_type.delete",
            crud_status_type.delete,
        )
        monkeypatch.setattr(
            "app.crud.crud_status_type.status_type.get_by_attribute",
            crud_status_type.get_by_attribute,
        )
        spy_status_type_delete = mocker.spy(
            status_type, "delete"
        )

        status_type.delete(random_status_type.id)
        status_type_in_db = status_type.get_by_attribute(id=random_status_type.id)

        spy_status_type_delete.assert_called_once_with(random_status_type.id)
        assert not status_type_in_db

    def test_failed_delete_status_type(
        self,
        crud_status_type,
        random_status_type,
        monkeypatch,
    ) -> None:
        monkeypatch.setattr(
            "app.crud.crud_status_type.status_type.delete",
            crud_status_type.delete,
        )
        monkeypatch.setattr(
            "app.crud.crud_status_type.status_type.get_by_attribute",
            crud_status_type.get_by_attribute,
        )

        with pytest.raises(DataError):
            status_type.delete(random_status_type.name)
