from typing import Generic, List, Type, TypeVar

from fastapi import Response, status
from pydantic import BaseModel

from app.crud.crud_base import CRUDBase
from app.db.base import Base
from app.db.models import Session

ModelType = TypeVar("ModelType", bound=Base)
CRUDType = TypeVar("CRUDType", bound=CRUDBase)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class ManagerBase(Generic[ModelType, CRUDType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, crud: CRUDType):
        self.crud = crud

    def fetch_one(self, id: int, session: Session) -> ModelType:
        return self.crud.get(id)

    def fetch_all(self, session: Session) -> List[ModelType]:
        return self.crud.get_multi()

    def search(self, parameter: str, keyword: str, session: Session, max_results: int = 100) -> List[ModelType]:
        return self.crud.search_by_parameter(parameter, keyword, max_results)

    def create(self, obj_in: CreateSchemaType, session: Session) -> ModelType:
        return self.crud.create(obj_in)

    def update(self, obj_in: UpdateSchemaType, session: Session) -> ModelType:
        db_obj = self.crud.get(obj_in.id)
        return self.crud.update(db_obj, obj_in)

    def delete(self, id: int, session: Session) -> Response:
        self.crud.delete(id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
