from typing import List

from fastapi import Response, status

from app.db.models import Session
from app.manager.manager_abstract import (CreateSchemaType, CRUDType,
                                          ManagerAbstract, ModelType,
                                          UpdateSchemaType)


class ManagerBase(
    ManagerAbstract[ModelType, CRUDType, CreateSchemaType, UpdateSchemaType]
):
    def fetch_one(self, obj_id: int, session: Session) -> ModelType:
        return self.crud.get(obj_id)

    def fetch_all(self, session: Session) -> List[ModelType]:
        return self.crud.get_multi()

    def search(
        self, parameter: str, keyword: str, max_results: int, session: Session
    ) -> List[ModelType]:
        return self.crud.search_by_parameter(parameter, keyword, max_results)

    def create(self, obj_in: CreateSchemaType, session: Session) -> ModelType:
        return self.crud.create(obj_in)

    def update(self, obj_in: UpdateSchemaType, session: Session) -> ModelType:
        db_obj = self.crud.get(obj_in.id)
        return self.crud.update(db_obj, obj_in)

    def delete(self, obj_id: int, session: Session) -> Response:
        self.crud.delete(obj_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
