from app.crud.crud_status_type import CRUDStatusType
from app.db.models import StatusType
from app.manager.manager_base import ManagerBase
from app.schemas.status_type import StatusTypeCreate, StatusTypeUpdate


class StatusTypeManager(ManagerBase[StatusType, CRUDStatusType, StatusTypeCreate, StatusTypeUpdate]):
    pass


status_type: StatusTypeManager = StatusTypeManager(StatusType, CRUDStatusType)