from app.crud.crud_base import CRUDBase
from app.db.models import EmployeeAccount
from app.schemas.schema_employee_account import EmployeeAccountCreate, EmployeeAccountUpdate


class CRUDEmployeeAccount(
    CRUDBase[
        EmployeeAccount,
        EmployeeAccountCreate,
        EmployeeAccountUpdate
    ]
):
    pass


employee_account = CRUDEmployeeAccount(EmployeeAccount)
