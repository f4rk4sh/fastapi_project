import logging
from datetime import datetime
from typing import Union, Dict, Any, List

from fastapi.encoders import jsonable_encoder
from sqlalchemy import and_
from sqlalchemy.exc import SQLAlchemyError

from app import crud
from app.core.exceptions.common_exceptions import HTTPNotFoundException, HTTPBadRequestException
from app.core.security import get_password_hash
from app.crud.crud_base import CRUDBase, ModelType, CreateSchemaType, UpdateSchemaType
from app.db.models import Employer, User
from app.schemas.employer import EmployerCreate, EmployerUpdate


class CRUDEmployer(CRUDBase[Employer, EmployerCreate, EmployerUpdate]):
    def get_by_attribute(self, **kwargs) -> ModelType:
        filter_user_args = []
        filter_employer_args = []
        for key, value in kwargs.items():
            if hasattr(User, key):
                filter_user_args.append(getattr(User, key) == value)
            else:
                filter_employer_args.append(getattr(self.model, key) == value)
        obj = self.db.query(self.model).join(User).filter(and_(*filter_user_args)).filter(and_(*filter_employer_args)).first()
        if isinstance(obj, User):
            if obj.employer:
                return obj.employer
        return obj

    def search_by_parameter(self, parameter: str, keyword: str, skip: int = 0, limit: int = 100) -> List[ModelType]:
        if hasattr(User, parameter):
            filter_arg = getattr(User, parameter)
            users = self.db.query(User).filter(filter_arg.contains(keyword)).order_by(
                User.id).offset(skip).limit(limit).all()
            results = [user.employer for user in users if user.employer]
        elif hasattr(self.model, parameter):
            filter_arg = getattr(self.model, parameter)
            results = self.db.query(self.model).filter(filter_arg.contains(keyword)).order_by(self.model.id).offset(
                skip).limit(limit).all()
        else:
            raise HTTPBadRequestException(detail="Invalid search parameter")
        if not results:
            raise HTTPNotFoundException(self.model.__name__)
        return results

    def create(self, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        user_data = obj_in_data.pop("user")
        user_password = user_data.pop("password")
        role_employer = crud.role.get_by_attribute(name="employer")
        status_not_activated = crud.status_type.get_by_attribute(name="not active")
        user = User(
            creation_date=datetime.utcnow(),
            role_id=role_employer.id,
            status_type_id=status_not_activated.id,
            **user_data)
        user.password = get_password_hash(user_password)
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


employer = CRUDEmployer(Employer)
