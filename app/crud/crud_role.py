from app.crud.crud_base import CRUDBase
from app.db.models import Role
from app.schemas.role import RoleCreate, RoleUpdate


class CRUDRole(CRUDBase[Role, RoleCreate, RoleUpdate]):
    pass


role = CRUDRole(Role)
