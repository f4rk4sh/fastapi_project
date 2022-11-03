from pytest_mock import MockerFixture

from app.db.models import EmployerType
from app.manager.manager_employer_type import employer_type
from app.schemas.schema_employer_type import EmployerTypeCreate, EmployerTypeUpdate
from app.tests.utils.base import random_string


class TestManagerCreateEmployerType:
    def test_successful_create_employer_type(
        self,
        session,
        expected_employer_type,
        mocker: MockerFixture,
    ) -> None:
        mocked_employer_type_create = mocker.patch(
            "app.manager.manager_employer_type.employer_type.crud.create",
            return_value=expected_employer_type,
        )

        employer_type_in = EmployerTypeCreate(name=expected_employer_type.name)
        actual_result = employer_type.create(employer_type_in, session)

        mocked_employer_type_create.assert_called_once_with(employer_type_in)
        assert actual_result == expected_employer_type


class TestManagerGetEmployerType:
    def test_successful_get_employer_type(
        self,
        session,
        expected_employer_type,
        mocker: MockerFixture,
    ) -> None:
        mocked_employer_type_get = mocker.patch(
            "app.manager.manager_employer_type.employer_type.crud.get",
            return_value=expected_employer_type,
        )

        actual_result = employer_type.fetch_one(expected_employer_type.id, session)

        mocked_employer_type_get.assert_called_once_with(expected_employer_type.id)
        assert actual_result == expected_employer_type


class TestManagerGetMultipleEmployerTypes:
    def test_successful_get_multiple_employer_types(
        self,
        session,
        expected_employer_types,
        mocker: MockerFixture,
    ) -> None:
        mocked_employer_type_get_multi = mocker.patch(
            "app.manager.manager_employer_type.employer_type.crud.get_multi",
            return_value=expected_employer_types,
        )

        actual_result = employer_type.fetch_all(session)

        mocked_employer_type_get_multi.assert_called_once()
        assert actual_result == expected_employer_types


class TestManagerSearchEmployerTypeByParameter:
    def test_successful_search_employer_types_by_parameter(
        self,
        session,
        expected_employer_type,
        mocker: MockerFixture,
    ) -> None:
        mocked_employer_type_search = mocker.patch(
            "app.manager.manager_employer_type.employer_type.crud.search_by_parameter",
            return_value=[expected_employer_type],
        )

        parameter = "name"
        actual_result = employer_type.search(
            parameter, expected_employer_type.name, 1, session
        )

        mocked_employer_type_search.assert_called_once_with(
            parameter, expected_employer_type.name, 1
        )
        assert expected_employer_type in actual_result


class TestManagerUpdateEmployerType:
    def test_successful_update_employer_type(
        self,
        session,
        expected_employer_type,
        mocker: MockerFixture,
    ) -> None:
        employer_type_in_db = EmployerType(id=expected_employer_type.id, name=random_string())
        mocked_employer_type_get = mocker.patch(
            "app.manager.manager_employer_type.employer_type.crud.get",
            return_value=employer_type_in_db,
        )
        mocked_employer_type_update = mocker.patch(
            "app.manager.manager_employer_type.employer_type.crud.update",
            return_value=expected_employer_type,
        )

        employer_type_in = EmployerTypeUpdate(
            id=expected_employer_type.id, name=expected_employer_type.name
        )
        actual_result = employer_type.update(employer_type_in, session)

        mocked_employer_type_get.assert_called_once_with(employer_type_in.id)
        mocked_employer_type_update.assert_called_once_with(
            employer_type_in_db, employer_type_in
        )
        assert actual_result == expected_employer_type


class TestManagerDeleteEmployerType:
    def test_successful_delete_employer_type(
        self,
        session,
        expected_employer_type,
        mocker: MockerFixture,
    ) -> None:
        mocked_employer_type_delete = mocker.patch(
            "app.manager.manager_employer_type.employer_type.crud.delete",
            return_value=expected_employer_type,
        )

        employer_type.delete(expected_employer_type.id, session)

        mocked_employer_type_delete.assert_called_once_with(expected_employer_type.id)
