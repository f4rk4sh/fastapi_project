from abc import ABC, abstractmethod
from typing import List, TypeVar, Generic

from fastapi import Response
from pydantic import BaseModel

from app.crud.crud_base import CRUDBase
from app.db.base import Base

ModelType = TypeVar("ModelType", bound=Base)
CRUDType = TypeVar("CRUDType", bound=CRUDBase)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class ManagerAbstract(
    ABC, Generic[ModelType, CRUDType, CreateSchemaType, UpdateSchemaType]
):
    def fetch_one(self, *args, **kwargs) -> ModelType:
        raise NotImplementedError

    def fetch_all(self, *args, **kwargs) -> List[ModelType]:
        raise NotImplementedError

    def search(self, *args, **kwargs) -> List[ModelType]:
        raise NotImplementedError

    def create(self, *args, **kwargs) -> ModelType:
        raise NotImplementedError

    def update(self, *args, **kwargs) -> ModelType:
        raise NotImplementedError

    def delete(self, *args, **kwargs) -> Response:
        raise NotImplementedError
