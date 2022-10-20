import pytest
from pytest_mock import MockFixture
from sqlalchemy.exc import DataError, ProgrammingError
from sqlalchemy.orm import Session

from app.crud.crud_employer_type import employer_type
from app.schemas.schema_employer_type import EmployerTypeCreate, EmployerTypeUpdate
from app.tests.utils.base import random_string


class TestCRUDCreateEmployerType:
    def test_success_create_employer_type_from_schema(
        self,
        crud_employer_type,
        monkeypatch,
        mocker: MockFixture,
    ) -> None:
        monkeypatch.setattr(
            "app.crud.crud_employer_type.employer_type.create",
            crud_employer_type.create,
        )
        spy_employer_type_create = mocker.spy(employer_type, "create")

        name = random_string()
        created_employer_type = employer_type.create(EmployerTypeCreate(name=name))

        spy_employer_type_create.assert_called_once_with(EmployerTypeCreate(name=name))
        assert created_employer_type.name == name

    def test_success_create_employer_type_from_dict(
        self,
        crud_employer_type,
        monkeypatch,
        mocker: MockFixture,
    ) -> None:
        monkeypatch.setattr(
            "app.crud.crud_employer_type.employer_type.create",
            crud_employer_type.create,
        )
        spy_employer_type_create = mocker.spy(employer_type, "create")

        name = random_string()
        created_employer_type = employer_type.create({"name": name})

        spy_employer_type_create.assert_called_once_with({"name": name})
        assert created_employer_type.name == name

    def test_success_create_employer_type_is_flush(
        self,
        crud_employer_type,
        db: Session,
        monkeypatch,
        mocker: MockFixture,
    ) -> None:
        monkeypatch.setattr(
            "app.crud.crud_employer_type.employer_type.create",
            crud_employer_type.create,
        )
        monkeypatch.setattr(
            "app.crud.crud_employer_type.employer_type.get_multi",
            crud_employer_type.get_multi,
        )
        spy_employer_type_create = mocker.spy(employer_type, "create")

        name = random_string()
        created_employer_type = employer_type.create(
            EmployerTypeCreate(name=name), is_flush=True
        )

        db.rollback()

        employer_types_in_db = employer_type.get_multi()

        spy_employer_type_create.assert_called_once_with(
            EmployerTypeCreate(name=name), is_flush=True
        )
        assert created_employer_type not in employer_types_in_db

    def test_failed_create_employer_type(
        self,
        crud_employer_type,
        monkeypatch,
    ) -> None:
        monkeypatch.setattr(
            "app.crud.crud_employer_type.employer_type.create",
            crud_employer_type.create,
        )

        with pytest.raises(TypeError):
            employer_type.create({"address": random_string()})


class TestCRUDGetEmployerType:
    def test_successful_get_employer_type(
        self,
        crud_employer_type,
        random_employer_type,
        monkeypatch,
        mocker: MockFixture,
    ) -> None:
        monkeypatch.setattr(
            "app.crud.crud_employer_type.employer_type.get",
            crud_employer_type.get,
        )
        spy_employer_type_get = mocker.spy(employer_type, "get")

        employer_type_in_db = employer_type.get(random_employer_type.id)

        spy_employer_type_get.assert_called_once_with(random_employer_type.id)
        assert employer_type_in_db == random_employer_type

    def test_failed_get_employer_type(
        self,
        crud_employer_type,
        random_employer_type,
        monkeypatch,
    ) -> None:
        monkeypatch.setattr(
            "app.crud.crud_employer_type.employer_type.get",
            crud_employer_type.get,
        )

        with pytest.raises(DataError):
            employer_type.get(random_employer_type.name)


class TestCRUDGetMultipleEmployerTypes:
    def test_successful_get_multiple_employer_types(
        self,
        crud_employer_type,
        random_employer_types,
        monkeypatch,
        mocker: MockFixture,
    ) -> None:
        monkeypatch.setattr(
            "app.crud.crud_employer_type.employer_type.get_multi",
            crud_employer_type.get_multi,
        )
        spy_employer_type_get_multi = mocker.spy(employer_type, "get_multi")

        employer_types_in_db = employer_type.get_multi()

        spy_employer_type_get_multi.assert_called_once()
        for random_employer_type in random_employer_types:
            assert random_employer_type in employer_types_in_db

    def test_failed_get_multiple_employer_types(
        self,
        crud_employer_type,
        monkeypatch,
    ) -> None:
        monkeypatch.setattr(
            "app.crud.crud_employer_type.employer_type.get_multi",
            crud_employer_type.get_multi,
        )

        with pytest.raises(ProgrammingError):
            employer_type.get_multi(skip=-1)


class TestCRUDGetEmployerTypeByAttribute:
    def test_successful_get_employer_type_by_attribute(
        self,
        crud_employer_type,
        random_employer_type,
        monkeypatch,
        mocker: MockFixture,
    ) -> None:
        monkeypatch.setattr(
            "app.crud.crud_employer_type.employer_type.get_by_attribute",
            crud_employer_type.get_by_attribute,
        )
        spy_employer_type_get_by_attribute = mocker.spy(
            employer_type, "get_by_attribute"
        )

        employer_type_in_db = employer_type.get_by_attribute(
            name=random_employer_type.name
        )

        spy_employer_type_get_by_attribute.assert_called_once_with(
            name=random_employer_type.name
        )
        assert employer_type_in_db == random_employer_type

    def test_failed_get_employer_type_by_attribute(
        self,
        crud_employer_type,
        random_employer_type,
        monkeypatch,
    ) -> None:
        monkeypatch.setattr(
            "app.crud.crud_employer_type.employer_type.get_by_attribute",
            crud_employer_type.get_by_attribute,
        )

        with pytest.raises(DataError):
            employer_type.get_by_attribute(name=random_employer_type.id)


class TestCRUDSearchEmployerTypeByParameter:
    def test_successful_search_employer_types_by_parameter(
        self,
        crud_employer_type,
        random_employer_type,
        monkeypatch,
        mocker: MockFixture,
    ) -> None:
        monkeypatch.setattr(
            "app.crud.crud_employer_type.employer_type.search_by_parameter",
            crud_employer_type.search_by_parameter,
        )
        spy_employer_type_search_by_parameter = mocker.spy(
            employer_type, "search_by_parameter"
        )
        employer_types_in_db = employer_type.search_by_parameter(
            parameter="name", keyword=random_employer_type.name
        )

        spy_employer_type_search_by_parameter.assert_called_once_with(
            parameter="name", keyword=random_employer_type.name
        )
        assert random_employer_type in employer_types_in_db

    def test_failed_search_employer_types_by_parameter(
        self,
        crud_employer_type,
        random_employer_type,
        monkeypatch,
    ) -> None:
        monkeypatch.setattr(
            "app.crud.crud_employer_type.employer_type.search_by_parameter",
            crud_employer_type.search_by_parameter,
        )

        with pytest.raises(TypeError):
            employer_type.search_by_parameter(
                parameter=None, keyword=random_employer_type.name
            )


class TestCRUDUpdateEmployerType:
    def test_successful_update_employer_type_from_schema(
        self,
        crud_employer_type,
        random_employer_type,
        monkeypatch,
        mocker: MockFixture,
    ) -> None:
        monkeypatch.setattr(
            "app.crud.crud_employer_type.employer_type.get",
            crud_employer_type.get,
        )
        monkeypatch.setattr(
            "app.crud.crud_employer_type.employer_type.update",
            crud_employer_type.update,
        )
        spy_employer_type_update = mocker.spy(employer_type, "update")

        employer_type_in_db = employer_type.get(random_employer_type.id)

        new_name = random_string()
        updated_employer_type = employer_type.update(
            employer_type_in_db,
            EmployerTypeUpdate(id=random_employer_type.id, name=new_name),
        )

        spy_employer_type_update.assert_called_once_with(
            employer_type_in_db,
            EmployerTypeUpdate(id=random_employer_type.id, name=new_name),
        )
        assert updated_employer_type.name == new_name

    def test_successful_update_employer_type_from_dict(
        self,
        crud_employer_type,
        random_employer_type,
        monkeypatch,
        mocker: MockFixture,
    ) -> None:
        monkeypatch.setattr(
            "app.crud.crud_employer_type.employer_type.get",
            crud_employer_type.get,
        )
        monkeypatch.setattr(
            "app.crud.crud_employer_type.employer_type.update",
            crud_employer_type.update,
        )
        spy_employer_type_update = mocker.spy(employer_type, "update")

        employer_type_in_db = employer_type.get(random_employer_type.id)

        new_name = random_string()
        updated_employer_type = employer_type.update(
            employer_type_in_db,
            {"id": random_employer_type.id, "name": new_name},
        )

        spy_employer_type_update.assert_called_once_with(
            employer_type_in_db,
            {"id": random_employer_type.id, "name": new_name},
        )
        assert updated_employer_type.name == new_name

    def test_failed_update_employer_type(
        self,
        crud_employer_type,
        random_employer_type,
        monkeypatch,
    ) -> None:
        monkeypatch.setattr(
            "app.crud.crud_employer_type.employer_type.get",
            crud_employer_type.get,
        )
        monkeypatch.setattr(
            "app.crud.crud_employer_type.employer_type.update",
            crud_employer_type.update,
        )

        with pytest.raises(TypeError):
            employer_type_in_db = employer_type.get(random_employer_type.id)
            employer_type.update(employer_type_in_db)


class TestCRUDDeleteEmployerType:
    def test_successful_delete_employer_type(
        self,
        crud_employer_type,
        random_employer_type,
        monkeypatch,
        mocker: MockFixture,
    ) -> None:
        monkeypatch.setattr(
            "app.crud.crud_employer_type.employer_type.delete",
            crud_employer_type.delete,
        )
        monkeypatch.setattr(
            "app.crud.crud_employer_type.employer_type.get_by_attribute",
            crud_employer_type.get_by_attribute,
        )
        spy_employer_type_delete = mocker.spy(employer_type, "delete")

        employer_type.delete(random_employer_type.id)
        employer_type_in_db = employer_type.get_by_attribute(
            id=random_employer_type.id
        )

        spy_employer_type_delete.assert_called_once_with(random_employer_type.id)
        assert not employer_type_in_db

    def test_failed_delete_employer_type(
        self,
        crud_employer_type,
        random_employer_type,
        monkeypatch,
    ) -> None:
        monkeypatch.setattr(
            "app.crud.crud_employer_type.employer_type.delete",
            crud_employer_type.delete,
        )
        monkeypatch.setattr(
            "app.crud.crud_employer_type.employer_type.get_by_attribute",
            crud_employer_type.get_by_attribute,
        )

        with pytest.raises(DataError):
            employer_type.delete(random_employer_type.name)
