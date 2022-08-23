import logging
from datetime import datetime
from typing import List, Optional, Union, Dict, Any

from fastapi.encoders import jsonable_encoder
from sqlalchemy.exc import SQLAlchemyError

from app.core.exceptions.common_exceptions import HTTPNotFoundException
from app.core.security import get_password_hash
from app.crud.crud_base import CRUDBase, ModelType, CreateSchemaType, UpdateSchemaType
from app.db.models import Employer, User
from app.schemas.employer import EmployerCreate, EmployerUpdate


class CRUDEmployer(CRUDBase[Employer, EmployerCreate, EmployerUpdate]):
    def create(self, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        user_password = obj_in_data.pop("password")
        user_data = {}
        for key in User.__table__.columns.keys():
            if key in obj_in_data.keys():
                user_data[key] = obj_in_data[key]
                obj_in_data.pop(key)
        user = User(creation_date=datetime.utcnow(), **user_data)
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

    def update(self, *, db_obj: ModelType, obj_in: Union[UpdateSchemaType, Dict[str, Any]]) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        user = self.db.query(User).get(db_obj.user.id)
        user_data = jsonable_encoder(user)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        update_data.pop("id")
        for field in update_data:
            if field in user_data:
                setattr(user, field, update_data[field])
            elif field in obj_data:
                setattr(db_obj, field, update_data[field])
        self.db.add(user, db_obj)
        try:
            self.db.commit()
        except SQLAlchemyError as err:
            logging.exception(err)
            self.db.rollback()
        return db_obj

    def delete(self, *, id: int):
        obj = self.db.query(self.model).get(id)
        if not obj:
            raise HTTPNotFoundException(self.model.__name__, id)
        self.db.delete(obj.user)
        try:
            self.db.commit()
        except SQLAlchemyError as err:
            logging.exception(err)
            self.db.rollback()

    def search_by_name(self, *, employer_name, skip: int = 0, limit: int = 100) -> List[ModelType]:
        results = self.db.query(self.model).filter(self.model.name.contains(employer_name)).order_by(self.model.id).offset(skip).limit(limit).all()
        if not results:
            raise HTTPNotFoundException(self.model.__name__)
        return results

    def get_by_name(self, employer_name) -> Optional[ModelType]:
        return self.db.query(self.model).filter(self.model.name == employer_name).first()


employer = CRUDEmployer(Employer)
