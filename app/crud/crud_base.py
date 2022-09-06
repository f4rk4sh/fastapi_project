import logging
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import and_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.db.base import Base
from app.db.get_database import get_db
from app.utils.exceptions.common_exceptions import HTTPBadRequestException, HTTPNotFoundException

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType], db: Session = next(get_db())):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        **Parameters**
        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        * `db`: A database session
        """
        self.model = model
        self.db = db

    def get(self, id: Any) -> Optional[ModelType]:
        obj = self.db.query(self.model).filter(self.model.id == id).first()
        if not obj:
            raise HTTPNotFoundException(self.model.__name__, id)
        return obj

    def get_multi(self, skip: int = 0, limit: int = 100) -> List[ModelType]:
        obj_list = (
            self.db.query(self.model)
            .order_by(self.model.id)
            .offset(skip)
            .limit(limit)
            .all()
        )
        if not obj_list:
            raise HTTPNotFoundException(self.model.__name__)
        return obj_list

    def get_by_attribute(self, **kwargs) -> ModelType:
        filter_args = []
        for key, value in kwargs.items():
            filter_args.append(getattr(self.model, key) == value)
        return self.db.query(self.model).filter(and_(*filter_args)).first()

    def search_by_parameter(
        self, parameter: str, keyword: str, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        if not hasattr(self.model, parameter):
            raise HTTPBadRequestException(detail="Invalid search parameter")
        results = (
            self.db.query(self.model)
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
        self.db.add(db_obj)
        try:
            if is_flush:
                self.db.flush()
            else:
                self.db.commit()
        except SQLAlchemyError as err:
            logging.exception(err)
            self.db.rollback()
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
        self.db.add(db_obj)
        try:
            if is_flush:
                self.db.flush()
            else:
                self.db.commit()
        except SQLAlchemyError as err:
            logging.exception(err)
            self.db.rollback()
        return db_obj

    def delete(self, id: int, is_flush: bool = False) -> ModelType:
        obj = self.db.query(self.model).get(id)
        if not obj:
            raise HTTPNotFoundException(self.model.__name__, id)
        self.db.delete(obj)
        try:
            if is_flush:
                self.db.flush()
            else:
                self.db.commit()
        except SQLAlchemyError as err:
            logging.exception(err)
            self.db.rollback()
        return obj
