from typing import List, Optional

from app.core.exceptions.common_exceptions import HTTPNotFoundException
from app.crud.crud_base import CRUDBase, ModelType
from app.db.models import StatusType
from app.schemas.status_type import StatusTypeCreate, StatusTypeUpdate


class CRUDStatusType(CRUDBase[StatusType, StatusTypeCreate, StatusTypeUpdate]):
    pass


status_type = CRUDStatusType(StatusType)
