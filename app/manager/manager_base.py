from typing import Generic, TypeVar, Type, List

from pydantic import BaseModel
from fastapi import Response, status

from app.crud.crud_base import CRUDBase
from app.db.base import Base

ModelType = TypeVar("ModelType", bound=Base)
CRUDType = TypeVar("CRUDType", bound=CRUDBase)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class ManagerBase(Generic[ModelType, CRUDType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType], crud: Type[CRUDType]):
        self.manager = crud(model)

    def fetch_one(self, id: int) -> ModelType:
        return self.manager.get(id)

    def fetch_all(self) -> List[ModelType]:
        return self.manager.get_multi()

    def search(self, parameter: str, keyword: str, max_results: int = 100) -> List[ModelType]:
        return self.manager.search_by_parameter(parameter, keyword, max_results)

    def create(self, obj_in: CreateSchemaType) -> ModelType:
        return self.manager.create(obj_in)

    def update(self, obj_in: UpdateSchemaType) -> ModelType:
        db_obj = self.manager.get(obj_in.id)
        return self.manager.update(db_obj, obj_in)

    def delete(self, id: int) -> Response:
        self.manager.delete(id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
