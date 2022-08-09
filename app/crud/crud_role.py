from typing import List

from app.core.exceptions import HTTPNotFoundException
from app.crud.crud_base import CRUDBase, ModelType
from app.db.models import Role
from app.schemas.role import RoleCreate, RoleUpdate


class CRUDRole(CRUDBase[Role, RoleCreate, RoleUpdate]):
    def search_by_name(self, *, role_name: str, skip: int = 0, limit: int = 100) -> List[ModelType]:
        results = self.db.query(self.model).filter(self.model.name.contains(role_name)).order_by(self.model.id).offset(skip).limit(limit).all()
        if not results:
            raise HTTPNotFoundException(self.model.__name__)
        return results


role = CRUDRole(Role)
