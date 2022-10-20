from pytest_mock import MockerFixture

from app.db.models import StatusType
from app.manager.manager_status_type import status_type
from app.schemas.schema_status_type import StatusTypeCreate, StatusTypeUpdate
from app.tests.utils.base import random_string


class TestManagerCreateStatusType:
    def test_successful_create_status_type(
        self,
        session,
        expected_status_type,
        mocker: MockerFixture,
    ) -> None:
        mocked_status_type_create = mocker.patch(
            "app.manager.manager_status_type.status_type.crud.create",
            return_value=expected_status_type,
        )

        status_type_in = StatusTypeCreate(name=expected_status_type.name)
        actual_result = status_type.create(status_type_in, session)

        mocked_status_type_create.assert_called_once_with(status_type_in)
        assert actual_result == expected_status_type


class TestManagerGetStatusType:
    def test_successful_get_status_type(
        self,
        session,
        expected_status_type,
        mocker: MockerFixture,
    ) -> None:
        mocked_status_type_get = mocker.patch(
            "app.manager.manager_status_type.status_type.crud.get",
            return_value=expected_status_type,
        )

        actual_result = status_type.fetch_one(expected_status_type.id, session)

        mocked_status_type_get.assert_called_once_with(expected_status_type.id)
        assert actual_result == expected_status_type


class TestManagerGetMultipleStatusTypes:
    def test_successful_get_multiple_status_types(
        self,
        session,
        expected_status_types,
        mocker: MockerFixture,
    ) -> None:
        mocked_status_type_get_multi = mocker.patch(
            "app.manager.manager_status_type.status_type.crud.get_multi",
            return_value=expected_status_types,
        )

        actual_result = status_type.fetch_all(session)

        mocked_status_type_get_multi.assert_called_once()
        assert actual_result == expected_status_types


class TestManagerSearchStatusTypeByParameter:
    def test_successful_search_status_types_by_parameter(
        self,
        session,
        expected_status_type,
        mocker: MockerFixture,
    ) -> None:
        mocked_status_type_search = mocker.patch(
            "app.manager.manager_status_type.status_type.crud.search_by_parameter",
            return_value=[expected_status_type],
        )

        parameter = "name"
        actual_result = status_type.search(
            parameter, expected_status_type.name, session, 1
        )

        mocked_status_type_search.assert_called_once_with(
            parameter, expected_status_type.name, 1
        )
        assert expected_status_type in actual_result


class TestManagerUpdateStatusType:
    def test_successful_update_status_type(
        self,
        session,
        expected_status_type,
        mocker: MockerFixture,
    ) -> None:
        status_type_in_db = StatusType(
            id=expected_status_type.id, name=random_string()
        )
        mocked_status_type_get = mocker.patch(
            "app.manager.manager_status_type.status_type.crud.get",
            return_value=status_type_in_db,
        )
        mocked_status_type_update = mocker.patch(
            "app.manager.manager_status_type.status_type.crud.update",
            return_value=expected_status_type,
        )

        status_type_in = StatusTypeUpdate(
            id=expected_status_type.id, name=expected_status_type.name
        )
        actual_result = status_type.update(status_type_in, session)

        mocked_status_type_get.assert_called_once_with(status_type_in.id)
        mocked_status_type_update.assert_called_once_with(
            status_type_in_db, status_type_in
        )
        assert actual_result == expected_status_type


class TestManagerDeleteStatusType:
    def test_successful_delete_status_type(
        self,
        session,
        expected_status_type,
        mocker: MockerFixture,
    ) -> None:
        mocked_status_type_delete = mocker.patch(
            "app.manager.manager_status_type.status_type.crud.delete",
            return_value=expected_status_type,
        )

        status_type.delete(expected_status_type.id, session)

        mocked_status_type_delete.assert_called_once_with(expected_status_type.id)
