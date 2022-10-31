from abc import ABC
from typing import Generic, List, TypeVar

from fastapi import Response
from pydantic import BaseModel

from app.crud.crud_base import CRUDBase
from app.db.base import Base
from app.db.models import Session

ModelType = TypeVar("ModelType", bound=Base)
CRUDType = TypeVar("CRUDType", bound=CRUDBase)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class ManagerAbstract(
    ABC, Generic[ModelType, CRUDType, CreateSchemaType, UpdateSchemaType]
):
    def __init__(self, crud: CRUDType):
        self.crud = crud

    def fetch_one(self, obj_id: int, session: Session) -> ModelType:
        raise NotImplementedError

    def fetch_all(self, session: Session) -> List[ModelType]:
        raise NotImplementedError

    def search(
        self, parameter: str, keyword: str, max_results: int, session: Session
    ) -> List[ModelType]:
        raise NotImplementedError

    def create(self, obj_in: CreateSchemaType, session: Session) -> ModelType:
        raise NotImplementedError

    def update(self, obj_in: UpdateSchemaType, session: Session) -> ModelType:
        raise NotImplementedError

    def delete(self, obj_id: int, session: Session) -> Response:
        raise NotImplementedError
