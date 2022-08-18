from typing import List, Optional

from app.core.exceptions.common_exceptions import HTTPNotFoundException
from app.crud.crud_base import CRUDBase, ModelType
from app.db.models import StatusType
from app.schemas.status_type import StatusTypeCreate, StatusTypeUpdate


class CRUDStatusType(CRUDBase[StatusType, StatusTypeCreate, StatusTypeUpdate]):
    def search_by_name(self, *, status_type_name: str, skip: int = 0, limit: int = 100) -> List[ModelType]:
        results = self.db.query(self.model).filter(self.model.name.contains(status_type_name)).order_by(self.model.id).offset(skip).limit(limit).all()
        if not results:
            raise HTTPNotFoundException(self.model.__name__)
        return results

    def get_by_name(self, status_type_name: str) -> Optional[ModelType]:
        return self.db.query(self.model).filter(self.model.name == status_type_name).first()


status_type = CRUDStatusType(StatusType)
