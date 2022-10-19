from app.crud.crud_role import CRUDRole, role as role_crud
from app.db.models import Role
from app.manager.manager_base import ManagerBase
from app.schemas.schema_role import RoleCreate, RoleUpdate


class RoleManager(ManagerBase[Role, CRUDRole, RoleCreate, RoleUpdate]):
    pass


role: RoleManager = RoleManager(role_crud)
