import logging
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import and_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.db.base import Base
from app.db.session import get_session
from app.utils.exceptions.common_exceptions import HTTPBadRequestException, HTTPNotFoundException

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType], session: Session = next(get_session())):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        **Parameters**
        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        * `session`: A database session
        """
        self.model = model
        self.session = session

    def get(self, id: Any) -> Optional[ModelType]:
        obj = self.session.query(self.model).filter(self.model.id == id).first()
        if not obj:
            raise HTTPNotFoundException(self.model.__name__, id)
        return obj

    def get_multi(self, skip: int = 0, limit: int = 100) -> List[ModelType]:
        obj_list = (
            self.session.query(self.model)
            .order_by(self.model.id)
            .offset(skip)
            .limit(limit)
            .all()
        )
        if not obj_list:
            raise HTTPNotFoundException(self.model.__name__)
        return obj_list

    def get_by_attribute(self, order_by: str = None, desc: bool = False, **kwargs) -> ModelType:
        filter_args = []
        for key, value in kwargs.items():
            filter_args.append(getattr(self.model, key) == value)
        order_by_arg = getattr(self.model, order_by) if order_by else self.model.id
        if desc:
            order_by_arg = order_by_arg.desc()
        return self.session.query(self.model).filter(and_(*filter_args)).order_by(order_by_arg).first()

    def search_by_parameter(
        self, parameter: str, keyword: str, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        if not hasattr(self.model, parameter):
            raise HTTPBadRequestException(detail="Invalid search parameter")
        results = (
            self.session.query(self.model)
            .filter(getattr(self.model, parameter).contains(keyword))
            .order_by(self.model.id)
            .offset(skip)
            .limit(limit)
            .all()
        )
        if not results:
            raise HTTPNotFoundException(self.model.__name__)
        return results

    def create(
        self, obj_in: Union[CreateSchemaType, Dict[str, Any]], is_flush: bool = False
    ) -> ModelType:
        if isinstance(obj_in, dict):
            obj_in_data = obj_in
        else:
            obj_in_data = obj_in.dict(exclude_unset=True)
        db_obj = self.model(**obj_in_data)
        self.session.add(db_obj)
        try:
            if is_flush:
                self.session.flush()
            else:
                self.session.commit()
        except SQLAlchemyError as err:
            logging.exception(err)
            self.session.rollback()
        return db_obj

    def update(
        self,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]],
        is_flush: bool = False,
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        self.session.add(db_obj)
        try:
            if is_flush:
                self.session.flush()
            else:
                self.session.commit()
        except SQLAlchemyError as err:
            logging.exception(err)
            self.session.rollback()
        return db_obj

    def delete(self, id: int, is_flush: bool = False) -> ModelType:
        obj = self.session.query(self.model).get(id)
        if not obj:
            raise HTTPNotFoundException(self.model.__name__, id)
        self.session.delete(obj)
        try:
            if is_flush:
                self.session.flush()
            else:
                self.session.commit()
        except SQLAlchemyError as err:
            logging.exception(err)
            self.session.rollback()
        return obj
