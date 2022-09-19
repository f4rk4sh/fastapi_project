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
    def __init__(self, model: Type[ModelType], crud: Type[CRUDType]):
        self.executor: CRUDType = crud(model)

    def fetch_one(self, id: int, session: Session) -> ModelType:
        return self.executor.get(id)

    def fetch_all(self, session: Session) -> List[ModelType]:
        return self.executor.get_multi()

    def search(self, parameter: str, keyword: str, session: Session, max_results: int = 100) -> List[ModelType]:
        return self.executor.search_by_parameter(parameter, keyword, max_results)

    def create(self, obj_in: CreateSchemaType, session: Session) -> ModelType:
        return self.executor.create(obj_in)

    def update(self, obj_in: UpdateSchemaType, session: Session) -> ModelType:
        db_obj = self.executor.get(obj_in.id)
        return self.executor.update(db_obj, obj_in)

    def delete(self, id: int, session: Session) -> Response:
        self.executor.delete(id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
