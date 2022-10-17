import pytest
from pytest_mock import MockFixture
from sqlalchemy.exc import DataError, ProgrammingError
from sqlalchemy.orm import Session

from app.crud.crud_employer import employer
from app.tests.utils.base import random_string
from app.utils.exceptions.common_exceptions import HTTPNotFoundException


class TestCRUDCreateEmployer:
    def test_success_create_employer(
        self,
        crud_employer,
        employer_data,
        monkeypatch,
        mocker: MockFixture,
    ) -> None:
        monkeypatch.setattr(
            "app.crud.crud_employer.employer.create", crud_employer.create
        )
        spy_employer_create = mocker.spy(employer, "create")

        created_employer = employer.create(employer_data)

        spy_employer_create.assert_called_once_with(employer_data)
        assert created_employer.name == employer_data["name"]

    def test_success_create_employer_is_flush(
        self,
        crud_employer,
        employer_data,
        db: Session,
        monkeypatch,
        mocker: MockFixture,
    ) -> None:
        monkeypatch.setattr(
            "app.crud.crud_employer.employer.create", crud_employer.create
        )
        monkeypatch.setattr(
            "app.crud.crud_employer.employer.get_multi",
            crud_employer.get_multi,
        )
        spy_employer_create = mocker.spy(employer, "create")

        created_employer = employer.create(employer_data, is_flush=True)

        db.rollback()

        employers_in_db = employer.get_multi()

        spy_employer_create.assert_called_once_with(employer_data, is_flush=True)
        assert created_employer not in employers_in_db

    def test_failed_create_employer(
        self,
        crud_employer,
        employer_data,
        monkeypatch,
    ) -> None:
        monkeypatch.setattr(
            "app.crud.crud_employer.employer.create", crud_employer.create
        )

        employer_data["fullname"] = employer_data.pop("name")
        with pytest.raises(TypeError):
            employer.create(employer_data)


class TestCRUDGetEmployer:
    def test_successful_get_employer(
        self,
        crud_employer,
        random_employer,
        monkeypatch,
        mocker: MockFixture,
    ) -> None:
        monkeypatch.setattr(
            "app.crud.crud_employer.employer.get", crud_employer.get
        )
        spy_employer_get = mocker.spy(employer, "get")

        employer_in_db = employer.get(random_employer.id)

        spy_employer_get.assert_called_once_with(random_employer.id)
        assert random_employer == employer_in_db

    def test_failed_get_employer(
        self,
        crud_employer,
        random_employer,
        monkeypatch,
    ) -> None:
        monkeypatch.setattr(
            "app.crud.crud_employer.employer.get", crud_employer.get
        )

        with pytest.raises(DataError):
            employer.get(random_employer.name)


class TestCRUDGetMultipleEmployers:
    def test_successful_get_multiple_employers(
        self,
        crud_employer,
        random_employers,
        monkeypatch,
        mocker: MockFixture,
    ) -> None:
        monkeypatch.setattr(
            "app.crud.crud_employer.employer.create", crud_employer.create
        )
        monkeypatch.setattr(
            "app.crud.crud_employer.employer.get_multi",
            crud_employer.get_multi,
        )
        spy_employer_get_multi = mocker.spy(employer, "get_multi")

        employers_in_db = employer.get_multi()

        spy_employer_get_multi.assert_called_once()
        for created_employer in random_employers:
            assert created_employer in employers_in_db

    def test_failed_get_multiple_employers(
        self,
        crud_employer,
        monkeypatch,
    ) -> None:
        monkeypatch.setattr(
            "app.crud.crud_employer.employer.get_multi",
            crud_employer.get_multi,
        )

        with pytest.raises(ProgrammingError):
            employer.get_multi(limit=-1)


class TestCRUDGetEmployerByAttribute:
    def test_successful_get_employer_by_employer_attribute(
        self,
        crud_employer,
        random_employer,
        monkeypatch,
        mocker: MockFixture,
    ) -> None:
        monkeypatch.setattr(
            "app.crud.crud_employer.employer.get_by_attribute",
            crud_employer.get_by_attribute,
        )
        spy_employer_get_by_attribute = mocker.spy(employer, "get_by_attribute")

        employer_in_db = employer.get_by_attribute(name=random_employer.name)

        spy_employer_get_by_attribute.assert_called_once_with(
            name=random_employer.name
        )
        assert random_employer == employer_in_db

    def test_successful_get_employer_by_user_attribute(
        self,
        crud_employer,
        random_employer,
        monkeypatch,
        mocker: MockFixture,
    ) -> None:
        monkeypatch.setattr(
            "app.crud.crud_employer.employer.get_by_attribute",
            crud_employer.get_by_attribute,
        )
        spy_employer_get_by_attribute = mocker.spy(employer, "get_by_attribute")

        employer_in_db = employer.get_by_attribute(email=random_employer.user.email)

        spy_employer_get_by_attribute.assert_called_once_with(
            email=random_employer.user.email
        )
        assert random_employer == employer_in_db

    def test_successful_get_employer_by_employer_and_user_attributes(
        self,
        crud_employer,
        random_employer,
        monkeypatch,
        mocker: MockFixture,
    ) -> None:
        monkeypatch.setattr(
            "app.crud.crud_employer.employer.get_by_attribute",
            crud_employer.get_by_attribute,
        )
        spy_employer_get_by_attribute = mocker.spy(employer, "get_by_attribute")

        employer_in_db = employer.get_by_attribute(
            email=random_employer.user.email, name=random_employer.name
        )

        spy_employer_get_by_attribute.assert_called_once_with(
            email=random_employer.user.email, name=random_employer.name
        )
        assert random_employer == employer_in_db

    def test_failed_get_employer_by_employer_attribute(
        self,
        crud_employer,
        random_employer,
        monkeypatch,
    ) -> None:
        monkeypatch.setattr(
            "app.crud.crud_employer.employer.get_by_attribute",
            crud_employer.get_by_attribute,
        )
        with pytest.raises(DataError):
            employer.get_by_attribute(name=random_employer.id)


class TestCRUDSearchEmployerByParameter:
    def test_successful_search_employers_by_employer_parameter(
        self,
        crud_employer,
        random_employer,
        monkeypatch,
        mocker: MockFixture,
    ) -> None:
        monkeypatch.setattr(
            "app.crud.crud_employer.employer.search_by_parameter",
            crud_employer.search_by_parameter,
        )
        spy_employer_search_by_parameter = mocker.spy(employer, "search_by_parameter")

        employers_in_db = employer.search_by_parameter(
            parameter="address", keyword=random_employer.address
        )

        spy_employer_search_by_parameter.assert_called_once_with(
            parameter="address", keyword=random_employer.address
        )
        assert random_employer in employers_in_db

    def test_successful_search_employers_by_user_parameter(
        self,
        crud_employer,
        random_employer,
        monkeypatch,
        mocker: MockFixture,
    ) -> None:
        monkeypatch.setattr(
            "app.crud.crud_employer.employer.search_by_parameter",
            crud_employer.search_by_parameter,
        )
        spy_employer_search_by_parameter = mocker.spy(employer, "search_by_parameter")

        employers_in_db = employer.search_by_parameter(
            parameter="phone", keyword=random_employer.user.phone
        )

        spy_employer_search_by_parameter.assert_called_once_with(
            parameter="phone", keyword=random_employer.user.phone
        )
        assert random_employer in employers_in_db

    def test_failed_search_employers_by_employer_parameter(
        self,
        crud_employer,
        random_employer,
        monkeypatch,
    ) -> None:
        monkeypatch.setattr(
            "app.crud.crud_employer.employer.search_by_parameter",
            crud_employer.search_by_parameter,
        )

        with pytest.raises(HTTPNotFoundException):
            employer.search_by_parameter(
                parameter="name", keyword=random_employer.address
            )


class TestCRUDUpdateEmployer:
    def test_successful_update_employer(
        self,
        crud_employer,
        random_employer,
        monkeypatch,
        mocker: MockFixture,
    ) -> None:
        monkeypatch.setattr(
            "app.crud.crud_employer.employer.get", crud_employer.get
        )
        monkeypatch.setattr(
            "app.crud.crud_employer.employer.update", crud_employer.update
        )
        spy_employer_update = mocker.spy(employer, "update")

        employer_in_db = employer.get(random_employer.id)

        new_name = random_string()
        employer_update_data = {"id": random_employer.id, "name": new_name}
        updated_employer = employer.update(employer_in_db, employer_update_data)

        spy_employer_update.assert_called_once_with(employer_in_db, employer_update_data)
        assert updated_employer.name == new_name

    def test_failed_update_employer(
        self,
        crud_employer,
        random_employer,
        monkeypatch,
    ) -> None:
        monkeypatch.setattr(
            "app.crud.crud_employer.employer.update", crud_employer.update
        )

        with pytest.raises(TypeError):
            employer.update(
                {"id": random_employer.id, "new_address": random_string()}
            )  # noqa


class TestCRUDDeleteEmployer:
    def test_successful_delete_employer(
        self,
        crud_employer,
        random_employer,
        monkeypatch,
        mocker: MockFixture,
    ) -> None:
        monkeypatch.setattr(
            "app.crud.crud_employer.employer.delete",
            crud_employer.delete,
        )
        monkeypatch.setattr(
            "app.crud.crud_employer.employer.get_by_attribute",
            crud_employer.get_by_attribute,
        )
        spy_employer_delete = mocker.spy(employer, "delete")

        employer.delete(random_employer.id)
        employer_in_db = employer.get_by_attribute(id=random_employer.id)

        spy_employer_delete.assert_called_once_with(id=random_employer.id)
        assert not employer_in_db

    def test_failed_delete_employer(
        self,
        crud_employer,
        random_employer,
        monkeypatch,
    ) -> None:
        monkeypatch.setattr(
            "app.crud.crud_employer.employer.delete",
            crud_employer.delete,
        )

        with pytest.raises(DataError):
            employer.delete(random_employer.name)
