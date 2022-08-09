import logging
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.exceptions import HTTPNotFoundException
from app.db.base import Base
from app.db.get_database import get_db

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

    def get_multi(self, *, skip: int = 0, limit: int = 100) -> List[ModelType]:
        obj_list = self.db.query(self.model).order_by(self.model.id).offset(skip).limit(limit).all()
        if not obj_list:
            raise HTTPNotFoundException(self.model.__name__)
        return obj_list

    def create(self, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        self.db.add(db_obj)
        try:
            self.db.commit()
        except SQLAlchemyError as err:
            logging.exception(err)
            self.db.rollback()
        return db_obj

    def update(self, *, db_obj: ModelType, obj_in: Union[UpdateSchemaType, Dict[str, Any]]) -> ModelType:
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
            self.db.commit()
        except SQLAlchemyError as err:
            logging.exception(err)
            self.db.rollback()
        return db_obj

    def delete(self, *, id: int) -> ModelType:
        obj = self.db.query(self.model).get(id)
        if not obj:
            raise HTTPNotFoundException(self.model.__name__, id)
        self.db.delete(obj)
        try:
            self.db.commit()
        except SQLAlchemyError as err:
            logging.exception(err)
            self.db.rollback()
        return obj
