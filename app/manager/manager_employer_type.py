from app.crud.crud_employer_type import CRUDEmployerType
from app.crud.crud_employer_type import employer_type as employer_type_crud
from app.db.models import EmployerType
from app.manager.manager_base import ManagerBase
from app.schemas.schema_employer_type import (EmployerTypeCreate,
                                              EmployerTypeUpdate)


class EmployerTypeManager(
    ManagerBase[EmployerType, CRUDEmployerType, EmployerTypeCreate, EmployerTypeUpdate]
):
    pass


employer_type: EmployerTypeManager = EmployerTypeManager(employer_type_crud)
