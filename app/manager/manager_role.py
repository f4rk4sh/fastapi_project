from app.crud.crud_role import CRUDRole
from app.db.models import Role
from app.manager.manager_base import ManagerBase
from app.schemas.role import RoleCreate, RoleUpdate


class RoleManager(ManagerBase[Role, CRUDRole, RoleCreate, RoleUpdate]):
    pass


role: RoleManager = RoleManager(Role, CRUDRole)
