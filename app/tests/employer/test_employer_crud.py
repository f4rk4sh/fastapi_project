import pytest
from pytest_mock import MockFixture
from sqlalchemy.orm import Session

from app.crud.crud_employer import employer
from app.tests.utils.base import random_string, random_date


class TestCRUDCreateEmployer:
    def test_success_create_employer(
        self,
        override_crud_user,
        override_crud_employer,
        create_random_user,
        create_random_employer_type,
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
            "user_id": create_random_user.id,
            "employer_type_id": create_random_employer_type.id,
        }

        created_employer = employer.create(employer_data)

        spy_employer_create.assert_called_once_with(employer_data)
        assert created_employer
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
        override_crud_user,
        override_crud_employer,
        create_random_user,
        create_random_employer_type,
        db: Session,
        monkeypatch,
        mocker: MockFixture,
    ) -> None:
        monkeypatch.setattr(
            "app.crud.crud_employer.employer.create", override_crud_employer.create
        )
        monkeypatch.setattr(
            "app.crud.crud_employer.employer.get_multi", override_crud_employer.get_multi
        )
        spy_employer_create = mocker.spy(employer, "create")

        employer_data = {
            "name": random_string(),
            "address": random_string(),
            "edrpou": random_string(),
            "expire_contract_date": random_date(in_future=True),
            "salary_date": random_date(),
            "prepayment_date": random_date(),
            "user_id": create_random_user.id,
            "employer_type_id": create_random_employer_type.id,
        }

        created_employer = employer.create(employer_data, is_flush=True)

        db.rollback()

        employers_in_db = employer.get_multi()

        spy_employer_create.assert_called_once_with(employer_data, is_flush=True)
        assert created_employer not in employers_in_db

    @pytest.mark.xfail(strict=True)
    def test_failed_create_employer(
        self,
        override_crud_user,
        override_crud_employer,
        create_random_user,
        create_random_employer_type,
        monkeypatch,
        mocker: MockFixture,
    ) -> None:
        monkeypatch.setattr(
            "app.crud.crud_employer.employer.create", override_crud_employer.create
        )
        monkeypatch.setattr(
            "app.crud.crud_employer.employer.get", override_crud_employer.get
        )
        spy_employer_create = mocker.spy(employer, "create")

        employer_data = {
            "name": random_string(101),
            "address": random_string(),
            "edrpou": random_string(),
            "expire_contract_date": random_date(in_future=True),
            "salary_date": random_date(),
            "prepayment_date": random_date(),
            "user_id": create_random_user.id,
            "employer_type_id": create_random_employer_type.id,
        }

        created_employer = employer.create(employer_data)

        employer_id_db = employer.get(created_employer.id)

        spy_employer_create.assert_called_once_with(employer_data)
        assert not employer_id_db


class TestCRUDGetEmployer:
    def test_successful_get_employer(
        self,
        override_crud_user,
        override_crud_employer,
        create_random_user,
        create_random_employer_type,
        monkeypatch,
        mocker: MockFixture,
    ) -> None:
        monkeypatch.setattr(
            "app.crud.crud_employer.employer.create", override_crud_employer.create
        )
        monkeypatch.setattr(
            "app.crud.crud_employer.employer.get", override_crud_employer.get
        )
        spy_employer_get = mocker.spy(employer, "get")

        created_employer = employer.create(
            {
                "name": random_string(),
                "address": random_string(),
                "edrpou": random_string(),
                "expire_contract_date": random_date(in_future=True),
                "salary_date": random_date(),
                "prepayment_date": random_date(),
                "user_id": create_random_user.id,
                "employer_type_id": create_random_employer_type.id,
            }
        )
        employer_in_db = employer.get(created_employer.id)

        spy_employer_get.assert_called_once_with(created_employer.id)
        assert employer_in_db
        assert employer_in_db.id == created_employer.id
        assert employer_in_db.name == created_employer.name

    @pytest.mark.xfail(strict=True)
    def test_failed_get_employer(
        self,
        override_crud_user,
        override_crud_employer,
        create_random_user,
        create_random_employer_type,
        monkeypatch,
        mocker: MockFixture,
    ) -> None:
        monkeypatch.setattr(
            "app.crud.crud_employer.employer.create", override_crud_employer.create
        )
        monkeypatch.setattr(
            "app.crud.crud_employer.employer.get", override_crud_employer.get
        )
        spy_employer_get = mocker.spy(employer, "get")

        created_employer = employer.create(
            {
                "name": random_string(),
                "address": random_string(),
                "edrpou": random_string(),
                "expire_contract_date": random_date(in_future=True),
                "salary_date": random_date(),
                "prepayment_date": random_date(),
                "user_id": create_random_user.id,
                "employer_type_id": create_random_employer_type.id,
            }
        )
        employer_in_db = employer.get(created_employer.name)

        spy_employer_get.assert_called_once_with(created_employer.id)
        assert not employer_in_db


class TestCRUDGetMultipleEmployers:
    def test_successful_get_multiple_employers(
        self,
        override_crud_user,
        override_crud_employer,
        create_random_user,
        create_random_employer_type,
        monkeypatch,
        mocker: MockFixture,
    ) -> None:
        monkeypatch.setattr(
            "app.crud.crud_employer.employer.create", override_crud_employer.create
        )
        monkeypatch.setattr(
            "app.crud.crud_employer.employer.get_multi", override_crud_employer.get_multi
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
                    "user_id": create_random_user.id,
                    "employer_type_id": create_random_employer_type.id,
                }
            ) for _ in range(3)
        ]

        employers_in_db = employer.get_multi()

        spy_employer_get_multi.assert_called_once()
        assert employers_in_db
        for created_employer in created_employers:
            assert created_employer in employers_in_db

    @pytest.mark.xfail(strict=True)
    def test_failed_get_multiple_employers(
        self,
        override_crud_user,
        override_crud_employer,
        create_random_user,
        create_random_employer_type,
        monkeypatch,
        mocker: MockFixture,
    ) -> None:
        monkeypatch.setattr(
            "app.crud.crud_employer.employer.create", override_crud_employer.create
        )
        monkeypatch.setattr(
            "app.crud.crud_employer.employer.get_multi", override_crud_employer.get_multi
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
                    "user_id": create_random_user.id,
                    "employer_type_id": create_random_employer_type.id,
                }
            ) for _ in range(3)
        ]

        employers_in_db = employer.get_multi(limit=-1)

        spy_employer_get_multi.assert_called_once_with(limit=-1)
        assert not employers_in_db
        for created_employer in created_employers:
            assert created_employer not in employers_in_db


class TestCRUDGetEmployerByAttribute:
    def test_successful_get_employer_by_employer_attribute(
        self,
        override_crud_user,
        override_crud_employer,
        create_random_user,
        create_random_employer_type,
        monkeypatch,
        mocker: MockFixture,
    ) -> None:
        monkeypatch.setattr(
            "app.crud.crud_employer.employer.create", override_crud_employer.create
        )
        monkeypatch.setattr(
            "app.crud.crud_employer.employer.get_by_attribute",
            override_crud_employer.get_by_attribute,
        )
        spy_employer_get_by_attribute = mocker.spy(employer, "get_by_attribute")

        name = random_string()
        created_employer = employer.create(
            {
                "name": name,
                "address": random_string(),
                "edrpou": random_string(),
                "expire_contract_date": random_date(in_future=True),
                "salary_date": random_date(),
                "prepayment_date": random_date(),
                "user_id": create_random_user.id,
                "employer_type_id": create_random_employer_type.id,
            }
        )
        employer_in_db = employer.get_by_attribute(name=name)

        spy_employer_get_by_attribute.assert_called_once_with(name=name)
        assert employer_in_db
        assert created_employer.name == employer_in_db.name
        assert created_employer.address == employer_in_db.address
        assert created_employer.edrpou == employer_in_db.edrpou
        assert created_employer.expire_contract_date == employer_in_db.expire_contract_date
        assert created_employer.salary_date == employer_in_db.salary_date
        assert created_employer.prepayment_date == employer_in_db.prepayment_date
        assert created_employer.user_id == employer_in_db.user_id
        assert created_employer.employer_type_id == employer_in_db.employer_type_id

    def test_successful_get_employer_by_user_attribute(
        self,
        override_crud_user,
        override_crud_employer,
        create_random_user,
        create_random_employer_type,
        monkeypatch,
        mocker: MockFixture,
    ) -> None:
        monkeypatch.setattr(
            "app.crud.crud_employer.employer.create", override_crud_employer.create
        )
        monkeypatch.setattr(
            "app.crud.crud_employer.employer.get_by_attribute",
            override_crud_employer.get_by_attribute,
        )
        spy_employer_get_by_attribute = mocker.spy(employer, "get_by_attribute")

        created_employer = employer.create(
            {
                "name": random_string(),
                "address": random_string(),
                "edrpou": random_string(),
                "expire_contract_date": random_date(in_future=True),
                "salary_date": random_date(),
                "prepayment_date": random_date(),
                "user_id": create_random_user.id,
                "employer_type_id": create_random_employer_type.id,
            }
        )
        employer_in_db = employer.get_by_attribute(email=create_random_user.email)

        spy_employer_get_by_attribute.assert_called_once_with(email=create_random_user.email)
        assert employer_in_db
        assert created_employer.name == employer_in_db.name
        assert created_employer.address == employer_in_db.address
        assert created_employer.edrpou == employer_in_db.edrpou
        assert created_employer.expire_contract_date == employer_in_db.expire_contract_date
        assert created_employer.salary_date == employer_in_db.salary_date
        assert created_employer.prepayment_date == employer_in_db.prepayment_date
        assert created_employer.user_id == employer_in_db.user_id
        assert created_employer.employer_type_id == employer_in_db.employer_type_id

    def test_successful_get_employer_by_employer_and_user_attributes(
        self,
        override_crud_user,
        override_crud_employer,
        create_random_user,
        create_random_employer_type,
        monkeypatch,
        mocker: MockFixture,
    ) -> None:
        monkeypatch.setattr(
            "app.crud.crud_employer.employer.create", override_crud_employer.create
        )
        monkeypatch.setattr(
            "app.crud.crud_employer.employer.get_by_attribute",
            override_crud_employer.get_by_attribute,
        )
        spy_employer_get_by_attribute = mocker.spy(employer, "get_by_attribute")

        name = random_string()
        created_employer = employer.create(
            {
                "name": name,
                "address": random_string(),
                "edrpou": random_string(),
                "expire_contract_date": random_date(in_future=True),
                "salary_date": random_date(),
                "prepayment_date": random_date(),
                "user_id": create_random_user.id,
                "employer_type_id": create_random_employer_type.id,
            }
        )
        employer_in_db = employer.get_by_attribute(
            email=create_random_user.email, name=name
        )

        spy_employer_get_by_attribute.assert_called_once_with(
            email=create_random_user.email, name=name
        )
        assert employer_in_db
        assert created_employer.name == employer_in_db.name
        assert created_employer.address == employer_in_db.address
        assert created_employer.edrpou == employer_in_db.edrpou
        assert created_employer.expire_contract_date == employer_in_db.expire_contract_date
        assert created_employer.salary_date == employer_in_db.salary_date
        assert created_employer.prepayment_date == employer_in_db.prepayment_date
        assert created_employer.user_id == employer_in_db.user_id
        assert created_employer.employer_type_id == employer_in_db.employer_type_id

    @pytest.mark.xfail(strict=True)
    def test_failed_get_employer_by_employer_attribute(
        self,
        override_crud_user,
        override_crud_employer,
        create_random_user,
        create_random_employer_type,
        monkeypatch,
        mocker: MockFixture,
    ) -> None:
        monkeypatch.setattr(
            "app.crud.crud_employer.employer.create", override_crud_employer.create
        )
        monkeypatch.setattr(
            "app.crud.crud_employer.employer.get_by_attribute",
            override_crud_employer.get_by_attribute,
        )
        spy_employer_get_by_attribute = mocker.spy(employer, "get_by_attribute")

        name = random_string()
        created_employer = employer.create(
            {
                "name": name,
                "address": random_string(),
                "edrpou": random_string(),
                "expire_contract_date": random_date(in_future=True),
                "salary_date": random_date(),
                "prepayment_date": random_date(),
                "user_id": create_random_user.id,
                "employer_type_id": create_random_employer_type.id,
            }
        )
        employer_in_db = employer.get_by_attribute(name=created_employer.id)

        spy_employer_get_by_attribute.assert_called_once_with(name=created_employer.id)
        assert not employer_in_db


class TestCRUDSearchEmployerByParameter:
    def test_successful_search_employers_by_employer_parameter(
        self,
        override_crud_user,
        override_crud_employer,
        create_random_user,
        create_random_employer_type,
        monkeypatch,
        mocker: MockFixture,
    ) -> None:
        monkeypatch.setattr(
            "app.crud.crud_employer.employer.create", override_crud_employer.create
        )
        monkeypatch.setattr(
            "app.crud.crud_employer.employer.search_by_parameter",
            override_crud_employer.search_by_parameter,
        )
        spy_employer_search_by_parameter = mocker.spy(employer, "search_by_parameter")

        created_employer = employer.create(
            {
                "name": random_string(),
                "address": random_string(),
                "edrpou": random_string(),
                "expire_contract_date": random_date(in_future=True),
                "salary_date": random_date(),
                "prepayment_date": random_date(),
                "user_id": create_random_user.id,
                "employer_type_id": create_random_employer_type.id,
            }
        )
        employers_in_db = employer.search_by_parameter(
            parameter="address", keyword=created_employer.address
        )

        spy_employer_search_by_parameter.assert_called_once_with(
            parameter="address", keyword=created_employer.address
        )
        assert employers_in_db
        assert created_employer in employers_in_db

    def test_successful_search_employers_by_user_parameter(
        self,
        override_crud_user,
        override_crud_employer,
        create_random_user,
        create_random_employer_type,
        monkeypatch,
        mocker: MockFixture,
    ) -> None:
        monkeypatch.setattr(
            "app.crud.crud_employer.employer.create", override_crud_employer.create
        )
        monkeypatch.setattr(
            "app.crud.crud_employer.employer.search_by_parameter",
            override_crud_employer.search_by_parameter,
        )
        spy_employer_search_by_parameter = mocker.spy(employer, "search_by_parameter")

        created_employer = employer.create(
            {
                "name": random_string(),
                "address": random_string(),
                "edrpou": random_string(),
                "expire_contract_date": random_date(in_future=True),
                "salary_date": random_date(),
                "prepayment_date": random_date(),
                "user_id": create_random_user.id,
                "employer_type_id": create_random_employer_type.id,
            }
        )
        employers_in_db = employer.search_by_parameter(
            parameter="phone", keyword=create_random_user.phone
        )

        spy_employer_search_by_parameter.assert_called_once_with(
            parameter="phone", keyword=create_random_user.phone
        )
        assert employers_in_db
        assert created_employer in employers_in_db

    @pytest.mark.xfail(strict=True)
    def test_failed_search_employers_by_employer_parameter(
        self,
        override_crud_user,
        override_crud_employer,
        create_random_user,
        create_random_employer_type,
        monkeypatch,
        mocker: MockFixture,
    ) -> None:
        monkeypatch.setattr(
            "app.crud.crud_employer.employer.create", override_crud_employer.create
        )
        monkeypatch.setattr(
            "app.crud.crud_employer.employer.search_by_parameter",
            override_crud_employer.search_by_parameter,
        )
        spy_employer_search_by_parameter = mocker.spy(employer, "search_by_parameter")

        created_employer = employer.create(
            {
                "name": random_string(),
                "address": random_string(),
                "edrpou": random_string(),
                "expire_contract_date": random_date(in_future=True),
                "salary_date": random_date(),
                "prepayment_date": random_date(),
                "user_id": create_random_user.id,
                "employer_type_id": create_random_employer_type.id,
            }
        )

        employers_in_db_wrong_keyword = employer.search_by_parameter(
            parameter="name", keyword=created_employer.address
        )

        spy_employer_search_by_parameter.assert_called_with(
            parameter="name", keyword=created_employer.address
        )
        assert not employers_in_db_wrong_keyword


class TestCRUDUpdateEmployer:
    def test_successful_update_employer(
        self,
        override_crud_user,
        override_crud_employer,
        create_random_user,
        create_random_employer_type,
        monkeypatch,
        mocker: MockFixture,
    ) -> None:
        monkeypatch.setattr(
            "app.crud.crud_employer.employer.create", override_crud_employer.create
        )
        monkeypatch.setattr(
            "app.crud.crud_employer.employer.get", override_crud_employer.get
        )
        monkeypatch.setattr(
            "app.crud.crud_employer.employer.update", override_crud_employer.update
        )
        spy_employer_update = mocker.spy(employer, "update")

        created_employer = employer.create(
            {
                "name": random_string(),
                "address": random_string(),
                "edrpou": random_string(),
                "expire_contract_date": random_date(in_future=True),
                "salary_date": random_date(),
                "prepayment_date": random_date(),
                "user_id": create_random_user.id,
                "employer_type_id": create_random_employer_type.id,
            }
        )
        employer_in_db = employer.get(created_employer.id)

        new_name = random_string()
        updated_employer = employer.update(
            employer_in_db, {"id": created_employer.id, "name": new_name}
        )

        spy_employer_update.assert_called_once_with(
            employer_in_db, {"id": created_employer.id, "name": new_name}
        )
        assert updated_employer
        assert updated_employer.name == new_name

    @pytest.mark.xfail(strict=True)
    def test_failed_update_employer(
        self,
        override_crud_user,
        override_crud_employer,
        create_random_user,
        create_random_employer_type,
        monkeypatch,
        mocker: MockFixture,
    ) -> None:
        monkeypatch.setattr(
            "app.crud.crud_employer.employer.create", override_crud_employer.create
        )
        monkeypatch.setattr(
            "app.crud.crud_employer.employer.get", override_crud_employer.get
        )
        monkeypatch.setattr(
            "app.crud.crud_employer.employer.update", override_crud_employer.update
        )
        spy_employer_update = mocker.spy(employer, "update")

        created_employer = employer.create(
            {
                "name": random_string(),
                "address": random_string(),
                "edrpou": random_string(),
                "expire_contract_date": random_date(in_future=True),
                "salary_date": random_date(),
                "prepayment_date": random_date(),
                "user_id": create_random_user.id,
                "employer_type_id": create_random_employer_type.id,
            }
        )
        employer_in_db = employer.get(created_employer.id)

        new_address = random_string()
        employer.update({"id": created_employer.id, "new_address": new_address})  # noqa

        updated_employer_in_db = employer.get(created_employer.id)

        spy_employer_update.assert_called_once_with(
            employer_in_db, {"id": created_employer.id, "new_address": new_address}
        )
        assert updated_employer_in_db.address != new_address


class TestCRUDDeleteEmployer:
    def test_successful_delete_employer(
        self,
        override_crud_user,
        override_crud_employer,
        create_random_user,
        create_random_employer_type,
        monkeypatch,
        mocker: MockFixture,
    ) -> None:
        monkeypatch.setattr(
            "app.crud.crud_employer.employer.create", override_crud_employer.create
        )
        monkeypatch.setattr(
            "app.crud.crud_employer.employer.delete",
            override_crud_employer.delete,
        )
        monkeypatch.setattr(
            "app.crud.crud_employer.employer.get_by_attribute",
            override_crud_employer.get_by_attribute,
        )
        spy_employer_delete = mocker.spy(employer, "delete")

        created_employer = employer.create(
            {
                "name": random_string(),
                "address": random_string(),
                "edrpou": random_string(),
                "expire_contract_date": random_date(in_future=True),
                "salary_date": random_date(),
                "prepayment_date": random_date(),
                "user_id": create_random_user.id,
                "employer_type_id": create_random_employer_type.id,
            }
        )
        employer.delete(created_employer.id)
        employer_in_db = employer.get_by_attribute(id=created_employer.id)

        spy_employer_delete.assert_called_once_with(id=created_employer.id)
        assert not employer_in_db

    @pytest.mark.xfail(strict=True)
    def test_failed_delete_employer(
            self,
            override_crud_user,
            override_crud_employer,
            create_random_user,
            create_random_employer_type,
            monkeypatch,
            mocker: MockFixture,
    ) -> None:
        monkeypatch.setattr(
            "app.crud.crud_employer.employer.create", override_crud_employer.create
        )
        monkeypatch.setattr(
            "app.crud.crud_employer.employer.delete",
            override_crud_employer.delete,
        )
        monkeypatch.setattr(
            "app.crud.crud_employer.employer.get_by_attribute",
            override_crud_employer.get_by_attribute,
        )
        spy_employer_delete = mocker.spy(employer, "delete")

        created_employer = employer.create(
            {
                "name": random_string(),
                "address": random_string(),
                "edrpou": random_string(),
                "expire_contract_date": random_date(in_future=True),
                "salary_date": random_date(),
                "prepayment_date": random_date(),
                "user_id": create_random_user.id,
                "employer_type_id": create_random_employer_type.id,
            }
        )
        employer.delete(created_employer.name)
        employer_in_db = employer.get_by_attribute(id=created_employer.id)

        spy_employer_delete.assert_called_once_with(id=created_employer.id)
        assert employer_in_db
