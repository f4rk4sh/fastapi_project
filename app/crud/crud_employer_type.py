from typing import Optional

from app.core.exceptions.common_exceptions import HTTPNotFoundException
from app.crud.crud_base import CRUDBase, ModelType
from app.db.models import EmployerType
from app.schemas.employer_type import EmployerTypeCreate, EmployerTypeUpdate


class CRUDEmployerType(CRUDBase[EmployerType, EmployerTypeCreate, EmployerTypeUpdate]):
    def search_by_name(self, *, employer_type_name: str, skip: int = 0, limit: int = 100) -> Optional[ModelType]:
        results = self.db.query(self.model).filter(self.model.name.contains(employer_type_name)).order_by(self.model.id).offset(skip).limit(limit).all()
        if not results:
            raise HTTPNotFoundException(self.model.__name__)
        return results

    def get_by_name(self, employer_type_name: str) -> Optional[ModelType]:
        return self.db.query(self.model).filter(self.model.name == employer_type_name).first()


employer_type = CRUDEmployerType(EmployerType)
