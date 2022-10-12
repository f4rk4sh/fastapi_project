import pytest
from pytest_mock import MockFixture
from sqlalchemy.exc import DataError, ProgrammingError
from sqlalchemy.orm import Session

from app.crud.crud_employer import employer
from app.tests.utils.base import random_date, random_string
from app.utils.exceptions.common_exceptions import HTTPNotFoundException


class TestCRUDCreateEmployer:
    def test_success_create_employer(
        self,
        override_crud_employer,
        random_user,
        random_employer_type,
        monkeypatch,
        mocker: MockFixture,
    ) -> None:
        monkeypatch.setattr(
            "app.crud.crud_employer.employer.create", override_crud_employer.create
        )
        spy_employer_create = mocker.spy(employer, "create")

        employer_data = {
            "name": random_string(),
            "address": random_string(),
            "edrpou": random_string(),
            "expire_contract_date": random_date(in_future=True),
            "salary_date": random_date(),
            "prepayment_date": random_date(),
            "user_id": random_user.id,
            "employer_type_id": random_employer_type.id,
        }

        created_employer = employer.create(employer_data)

        spy_employer_create.assert_called_once_with(employer_data)
        assert created_employer.name == employer_data["name"]
        assert created_employer.address == employer_data["address"]
        assert created_employer.edrpou == employer_data["edrpou"]
        assert created_employer.expire_contract_date == employer_data["expire_contract_date"]
        assert created_employer.salary_date == employer_data["salary_date"]
        assert created_employer.prepayment_date == employer_data["prepayment_date"]
        assert created_employer.user_id == employer_data["user_id"]
        assert created_employer.employer_type_id == employer_data["employer_type_id"]

    def test_success_create_employer_is_flush(
        self,
        override_crud_employer,
        random_user,
        random_employer_type,
        db: Session,
        monkeypatch,
        mocker: MockFixture,
    ) -> None:
        monkeypatch.setattr(
            "app.crud.crud_employer.employer.create", override_crud_employer.create
        )
        monkeypatch.setattr(
            "app.crud.crud_employer.employer.get_multi",
            override_crud_employer.get_multi,
        )
        spy_employer_create = mocker.spy(employer, "create")

        employer_data = {
            "name": random_string(),
            "address": random_string(),
            "edrpou": random_string(),
            "expire_contract_date": random_date(in_future=True),
            "salary_date": random_date(),
            "prepayment_date": random_date(),
            "user_id": random_user.id,
            "employer_type_id": random_employer_type.id,
        }

        created_employer = employer.create(employer_data, is_flush=True)

        db.rollback()

        employers_in_db = employer.get_multi()

        spy_employer_create.assert_called_once_with(employer_data, is_flush=True)
        assert created_employer not in employers_in_db

    def test_failed_create_employer(
        self,
        override_crud_employer,
        random_user,
        random_employer_type,
        monkeypatch,
    ) -> None:
        monkeypatch.setattr(
            "app.crud.crud_employer.employer.create", override_crud_employer.create
        )

        with pytest.raises(TypeError):
            employer.create(
                {
                    "fullname": random_string(),
                    "address": random_string(),
                    "edrpou": random_string(),
                    "expire_contract_date": random_date(in_future=True),
                    "salary_date": random_date(),
                    "prepayment_date": random_date(),
                    "user_id": random_user.id,
                    "employer_type_id": random_employer_type.id,
                }
            )


class TestCRUDGetEmployer:
    def test_successful_get_employer(
        self,
        override_crud_employer,
        random_employer,
        monkeypatch,
        mocker: MockFixture,
    ) -> None:
        monkeypatch.setattr(
            "app.crud.crud_employer.employer.get", override_crud_employer.get
        )
        spy_employer_get = mocker.spy(employer, "get")

        employer_in_db = employer.get(random_employer.id)

        spy_employer_get.assert_called_once_with(random_employer.id)
        assert employer_in_db.id == random_employer.id
        assert employer_in_db.name == random_employer.name

    def test_failed_get_employer(
        self,
        override_crud_employer,
        random_employer,
        monkeypatch,
    ) -> None:
        monkeypatch.setattr(
            "app.crud.crud_employer.employer.get", override_crud_employer.get
        )

        with pytest.raises(DataError):
            employer.get(random_employer.name)


class TestCRUDGetMultipleEmployers:
    def test_successful_get_multiple_employers(
        self,
        override_crud_employer,
        random_user,
        random_employer_type,
        monkeypatch,
        mocker: MockFixture,
    ) -> None:
        monkeypatch.setattr(
            "app.crud.crud_employer.employer.create", override_crud_employer.create
        )
        monkeypatch.setattr(
            "app.crud.crud_employer.employer.get_multi",
            override_crud_employer.get_multi,
        )
        spy_employer_get_multi = mocker.spy(employer, "get_multi")

        created_employers = [
            employer.create(
                {
                    "name": random_string(),
                    "address": random_string(),
                    "edrpou": random_string(),
                    "expire_contract_date": random_date(in_future=True),
                    "salary_date": random_date(),
                    "prepayment_date": random_date(),
                    "user_id": random_user.id,
                    "employer_type_id": random_employer_type.id,
                }
            )
            for _ in range(3)
        ]

        employers_in_db = employer.get_multi()

        spy_employer_get_multi.assert_called_once()
        for created_employer in created_employers:
            assert created_employer in employers_in_db

    def test_failed_get_multiple_employers(
        self,
        override_crud_employer,
        monkeypatch,
    ) -> None:
        monkeypatch.setattr(
            "app.crud.crud_employer.employer.get_multi",
            override_crud_employer.get_multi,
        )

        with pytest.raises(ProgrammingError):
            employer.get_multi(limit=-1)


class TestCRUDGetEmployerByAttribute:
    def test_successful_get_employer_by_employer_attribute(
        self,
        override_crud_employer,
        random_employer,
        monkeypatch,
        mocker: MockFixture,
    ) -> None:
        monkeypatch.setattr(
            "app.crud.crud_employer.employer.get_by_attribute",
            override_crud_employer.get_by_attribute,
        )
        spy_employer_get_by_attribute = mocker.spy(employer, "get_by_attribute")

        employer_in_db = employer.get_by_attribute(name=random_employer.name)

        spy_employer_get_by_attribute.assert_called_once_with(name=random_employer.name)
        assert random_employer == employer_in_db

    def test_successful_get_employer_by_user_attribute(
        self,
        override_crud_employer,
        random_employer,
        monkeypatch,
        mocker: MockFixture,
    ) -> None:
        monkeypatch.setattr(
            "app.crud.crud_employer.employer.get_by_attribute",
            override_crud_employer.get_by_attribute,
        )
        spy_employer_get_by_attribute = mocker.spy(employer, "get_by_attribute")

        employer_in_db = employer.get_by_attribute(email=random_employer.user.email)

        spy_employer_get_by_attribute.assert_called_once_with(
            email=random_employer.user.email
        )
        assert random_employer == employer_in_db

    def test_successful_get_employer_by_employer_and_user_attributes(
        self,
        override_crud_employer,
        random_employer,
        monkeypatch,
        mocker: MockFixture,
    ) -> None:
        monkeypatch.setattr(
            "app.crud.crud_employer.employer.get_by_attribute",
            override_crud_employer.get_by_attribute,
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
        override_crud_employer,
        random_employer,
        monkeypatch,
    ) -> None:
        monkeypatch.setattr(
            "app.crud.crud_employer.employer.get_by_attribute",
            override_crud_employer.get_by_attribute,
        )
        with pytest.raises(DataError):
            employer.get_by_attribute(name=random_employer.id)


class TestCRUDSearchEmployerByParameter:
    def test_successful_search_employers_by_employer_parameter(
        self,
        override_crud_employer,
        random_employer,
        monkeypatch,
        mocker: MockFixture,
    ) -> None:
        monkeypatch.setattr(
            "app.crud.crud_employer.employer.search_by_parameter",
            override_crud_employer.search_by_parameter,
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
        override_crud_employer,
        random_employer,
        monkeypatch,
        mocker: MockFixture,
    ) -> None:
        monkeypatch.setattr(
            "app.crud.crud_employer.employer.search_by_parameter",
            override_crud_employer.search_by_parameter,
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
        override_crud_employer,
        random_employer,
        monkeypatch,
    ) -> None:
        monkeypatch.setattr(
            "app.crud.crud_employer.employer.search_by_parameter",
            override_crud_employer.search_by_parameter,
        )

        with pytest.raises(HTTPNotFoundException):
            employer.search_by_parameter(
                parameter="name", keyword=random_employer.address
            )


class TestCRUDUpdateEmployer:
    def test_successful_update_employer(
        self,
        override_crud_employer,
        random_employer,
        monkeypatch,
        mocker: MockFixture,
    ) -> None:
        monkeypatch.setattr(
            "app.crud.crud_employer.employer.get", override_crud_employer.get
        )
        monkeypatch.setattr(
            "app.crud.crud_employer.employer.update", override_crud_employer.update
        )
        spy_employer_update = mocker.spy(employer, "update")

        employer_in_db = employer.get(random_employer.id)

        new_name = random_string()
        updated_employer = employer.update(
            employer_in_db, {"id": random_employer.id, "name": new_name}
        )

        spy_employer_update.assert_called_once_with(
            employer_in_db, {"id": random_employer.id, "name": new_name}
        )
        assert updated_employer.name == new_name

    def test_failed_update_employer(
        self,
        override_crud_employer,
        random_employer,
        monkeypatch,
    ) -> None:
        monkeypatch.setattr(
            "app.crud.crud_employer.employer.update", override_crud_employer.update
        )

        with pytest.raises(TypeError):
            employer.update(
                {"id": random_employer.id, "new_address": random_string()}
            )  # noqa


class TestCRUDDeleteEmployer:
    def test_successful_delete_employer(
        self,
        override_crud_employer,
        random_employer,
        monkeypatch,
        mocker: MockFixture,
    ) -> None:
        monkeypatch.setattr(
            "app.crud.crud_employer.employer.delete",
            override_crud_employer.delete,
        )
        monkeypatch.setattr(
            "app.crud.crud_employer.employer.get_by_attribute",
            override_crud_employer.get_by_attribute,
        )
        spy_employer_delete = mocker.spy(employer, "delete")

        employer.delete(random_employer.id)
        employer_in_db = employer.get_by_attribute(id=random_employer.id)

        spy_employer_delete.assert_called_once_with(id=random_employer.id)
        assert not employer_in_db

    def test_failed_delete_employer(
        self,
        override_crud_employer,
        random_employer,
        monkeypatch,
    ) -> None:
        monkeypatch.setattr(
            "app.crud.crud_employer.employer.delete",
            override_crud_employer.delete,
        )

        with pytest.raises(DataError):
            employer.delete(random_employer.name)
