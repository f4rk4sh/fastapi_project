from app.crud.crud_base import CRUDBase
from app.db.models import StatusType
from app.schemas.schema_status_type import StatusTypeCreate, StatusTypeUpdate


class CRUDStatusType(CRUDBase[StatusType, StatusTypeCreate, StatusTypeUpdate]):
    pass


status_type = CRUDStatusType(StatusType)
