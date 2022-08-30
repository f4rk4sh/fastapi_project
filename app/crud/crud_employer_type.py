from app.crud.crud_base import CRUDBase
from app.db.models import EmployerType
from app.schemas.employer_type import EmployerTypeCreate, EmployerTypeUpdate


class CRUDEmployerType(CRUDBase[EmployerType, EmployerTypeCreate, EmployerTypeUpdate]):
    pass


employer_type = CRUDEmployerType(EmployerType)
