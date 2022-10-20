import pytest
from pytest_mock import MockFixture
from sqlalchemy.exc import DataError, ProgrammingError
from sqlalchemy.orm import Session

from app.crud.crud_user import user
from app.schemas.schema_user import UserCreate, UserUpdate
from app.tests.utils.base import random_string


class TestCRUDCreateUser:
    def test_success_create_user_from_schema(
        self,
        crud_user,
        user_create_data,
        monkeypatch,
        mocker: MockFixture,
    ) -> None:
        monkeypatch.setattr("app.crud.crud_user.user.create", crud_user.create)
        spy_user_create = mocker.spy(user, "create")

        created_user = user.create(UserCreate(**user_create_data))

        spy_user_create.assert_called_once_with(UserCreate(**user_create_data))
        assert created_user.email == user_create_data["email"]

    def test_successful_create_user_from_dict(
        self,
        crud_user,
        user_create_data,
        monkeypatch,
        mocker: MockFixture,
    ) -> None:
        monkeypatch.setattr("app.crud.crud_user.user.create", crud_user.create)
        spy_user_create = mocker.spy(user, "create")

        created_user = user.create(user_create_data)

        spy_user_create.assert_called_once_with(user_create_data)
        assert created_user.email == user_create_data["email"]

    def test_successful_create_user_is_flush(
        self,
        crud_user,
        user_create_data,
        db: Session,
        monkeypatch,
        mocker: MockFixture,
    ) -> None:
        monkeypatch.setattr("app.crud.crud_user.user.create", crud_user.create)
        monkeypatch.setattr(
            "app.crud.crud_user.user.get_multi", crud_user.get_multi
        )
        spy_user_create = mocker.spy(user, "create")

        created_user = user.create(UserCreate(**user_create_data), is_flush=True)

        db.rollback()

        users_in_db = user.get_multi()

        spy_user_create.assert_called_once_with(
            UserCreate(**user_create_data), is_flush=True
        )
        assert created_user not in users_in_db

    def test_failed_create_user(
        self,
        crud_user,
        user_create_data,
        monkeypatch,
    ) -> None:

        monkeypatch.setattr("app.crud.crud_user.user.create", crud_user.create)

        user_create_data["username"] = random_string()
        with pytest.raises(TypeError):
            user.create(**user_create_data)


class TestCRUDGetUser:
    def test_successful_get_user(
        self,
        crud_user,
        random_user,
        monkeypatch,
        mocker: MockFixture,
    ) -> None:
        monkeypatch.setattr("app.crud.crud_user.user.get", crud_user.get)
        spy_user_get = mocker.spy(user, "get")

        user_in_db = user.get(random_user.id)

        spy_user_get.assert_called_once_with(random_user.id)
        assert user_in_db == random_user

    def test_failed_get_user(
        self,
        crud_user,
        random_user,
        monkeypatch,
    ) -> None:
        monkeypatch.setattr("app.crud.crud_user.user.get", crud_user.get)

        with pytest.raises(DataError):
            user.get(random_user.email)


class TestCRUDGetMultipleUsers:
    def test_successful_get_multiple_users(
        self,
        crud_user,
        random_users,
        monkeypatch,
        mocker: MockFixture,
    ) -> None:
        monkeypatch.setattr(
            "app.crud.crud_user.user.get_multi", crud_user.get_multi
        )
        spy_user_get_multiple = mocker.spy(user, "get_multi")

        users_in_db = user.get_multi()

        spy_user_get_multiple.assert_called_once()
        for random_user in random_users:
            assert random_user in users_in_db

    def test_failed_get_multiple_users(
        self,
        crud_user,
        monkeypatch,
    ) -> None:
        monkeypatch.setattr(
            "app.crud.crud_user.user.get_multi", crud_user.get_multi
        )

        with pytest.raises(ProgrammingError):
            user.get_multi(limit=-1)


class TestCRUDGetUserByAttribute:
    def test_successful_get_user_by_attribute(
        self,
        crud_user,
        random_user,
        monkeypatch,
        mocker: MockFixture,
    ) -> None:
        monkeypatch.setattr(
            "app.crud.crud_user.user.get_by_attribute",
            crud_user.get_by_attribute,
        )
        spy_user_get_by_attribute = mocker.spy(user, "get_by_attribute")

        user_in_db = user.get_by_attribute(email=random_user.email)

        spy_user_get_by_attribute.assert_called_once_with(email=random_user.email)
        assert user_in_db == random_user

    def test_failed_get_user_by_attribute(
        self,
        crud_user,
        random_user,
        monkeypatch,
    ) -> None:
        monkeypatch.setattr(
            "app.crud.crud_user.user.get_by_attribute",
            crud_user.get_by_attribute,
        )

        with pytest.raises(DataError):
            user.get_by_attribute(email=random_user.id)


class TestCRUDSearchUserByParameter:
    def test_successful_search_users_by_parameter(
        self,
        crud_user,
        random_user,
        monkeypatch,
        mocker: MockFixture,
    ) -> None:
        monkeypatch.setattr(
            "app.crud.crud_user.user.search_by_parameter",
            crud_user.search_by_parameter,
        )
        spy_user_search_by_parameter = mocker.spy(user, "search_by_parameter")

        users_in_db = user.search_by_parameter(
            parameter="email", keyword=random_user.email
        )

        spy_user_search_by_parameter.assert_called_once_with(
            parameter="email", keyword=random_user.email
        )
        assert random_user in users_in_db

    def test_failed_search_users_by_parameter(
        self,
        crud_user,
        random_user,
        monkeypatch,
    ) -> None:
        monkeypatch.setattr(
            "app.crud.crud_user.user.search_by_parameter",
            crud_user.search_by_parameter,
        )

        with pytest.raises(TypeError):
            user.search_by_parameter(parameter=None, keyword=random_user.email)  # noqa


class TestCRUDUpdateUser:
    def test_successful_update_user_from_schema(
        self,
        crud_user,
        user_update_data,
        random_user,
        monkeypatch,
        mocker: MockFixture,
    ) -> None:
        monkeypatch.setattr("app.crud.crud_user.user.get", crud_user.get)
        monkeypatch.setattr("app.crud.crud_user.user.update", crud_user.update)
        spy_user_update = mocker.spy(user, "update")

        user_in_db = user.get(random_user.id)

        updated_user = user.update(user_in_db, UserUpdate(**user_update_data))

        spy_user_update.assert_called_once_with(
            user_in_db, UserUpdate(**user_update_data)
        )
        assert updated_user.email == user_update_data["email"]

    def test_successful_update_user_from_dict(
        self,
        crud_user,
        user_update_data,
        random_user,
        monkeypatch,
        mocker: MockFixture,
    ) -> None:
        monkeypatch.setattr("app.crud.crud_user.user.get", crud_user.get)
        monkeypatch.setattr("app.crud.crud_user.user.update", crud_user.update)
        spy_user_update = mocker.spy(user, "update")

        user_in_db = user.get(random_user.id)

        updated_user = user.update(user_in_db, user_update_data)

        spy_user_update.assert_called_once_with(user_in_db, user_update_data)
        assert updated_user.email == user_update_data["email"]

    def test_failed_update_user(
        self,
        crud_user,
        random_user,
        monkeypatch,
    ) -> None:
        monkeypatch.setattr("app.crud.crud_user.user.get", crud_user.get)
        monkeypatch.setattr("app.crud.crud_user.user.update", crud_user.update)

        with pytest.raises(TypeError):
            user_in_db = user.get(random_user.id)
            user.update(user_in_db)  # noqa


class TestCRUDDeleteUser:
    def test_successful_delete_user(
        self,
        crud_user,
        random_user,
        monkeypatch,
        mocker: MockFixture,
    ) -> None:
        monkeypatch.setattr("app.crud.crud_user.user.delete", crud_user.delete)
        monkeypatch.setattr(
            "app.crud.crud_user.user.get_by_attribute",
            crud_user.get_by_attribute,
        )
        spy_user_delete = mocker.spy(user, "delete")

        user.delete(random_user.id)
        user_in_db = user.get_by_attribute(id=random_user.id)

        spy_user_delete.assert_called_once_with(random_user.id)
        assert not user_in_db

    def test_failed_delete_user(
        self,
        crud_user,
        random_user,
        monkeypatch,
    ) -> None:
        monkeypatch.setattr("app.crud.crud_user.user.delete", crud_user.delete)
        monkeypatch.setattr(
            "app.crud.crud_user.user.get_by_attribute",
            crud_user.get_by_attribute,
        )

        with pytest.raises(DataError):
            user.delete(random_user.email)
