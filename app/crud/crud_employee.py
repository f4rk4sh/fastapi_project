import logging
from datetime import datetime
from typing import Union, Dict, Any

from fastapi.encoders import jsonable_encoder
from sqlalchemy.exc import SQLAlchemyError

from app import crud
from app.core.exceptions.common_exceptions import HTTPNotFoundException
from app.crud.crud_base import CRUDBase, CreateSchemaType, ModelType, UpdateSchemaType
from app.db.models import Employee, User
from app.schemas.employee import EmployeeCreate, EmployeeUpdate


class CRUDEmployee(CRUDBase[Employee, EmployeeCreate, EmployeeUpdate]):
    def create(self, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        user_data = obj_in_data.pop("user")
        user_password = user_data.pop("password")
        role_employee = crud.role.get_by_attribute(attributes=["name"], value="employee")
        status_not_activated = crud.status_type.get_by_attribute(attributes=["name"], value="not active")
        user = User(
            creation_date=datetime.utcnow(),
            role_id=role_employee.id,
            status_type_id=status_not_activated.id,
            **user_data
        )
        # ToDo password hash
        user.password = user_password
        self.db.add(user)
        try:
            self.db.flush()
            db_obj = self.model(user=user, **obj_in_data)
            self.db.add(db_obj)
            self.db.commit()
            return db_obj
        except SQLAlchemyError as err:
            logging.exception(err)
            self.db.rollback()

    def update(self, db_obj: ModelType, obj_in: Union[UpdateSchemaType, Dict[str, Any]]) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        # ToDo user = db_obj.user
        user = self.db.query(User).get(db_obj.user.id)
        user_data = jsonable_encoder(user)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        update_user_data = update_data.pop("user")
        for field in update_user_data:
            if field in user_data:
                setattr(user, field, update_user_data[field])
        for field in update_data:
            if field in obj_data:
                setattr(db_obj, field, update_data[field])
        self.db.add(user, db_obj)
        try:
            self.db.commit()
        except SQLAlchemyError as err:
            logging.exception(err)
            self.db.rollback()
        return db_obj

    def delete(self, id: int):
        obj = self.db.query(self.model).get(id)
        if not obj:
            raise HTTPNotFoundException(self.model.__name__, id)
        self.db.delete(obj.user)
        try:
            self.db.commit()
        except SQLAlchemyError as err:
            logging.exception(err)
            self.db.rollback()


employee: CRUDEmployee = CRUDEmployee(Employee)
