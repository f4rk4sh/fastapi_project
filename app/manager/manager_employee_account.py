from datetime import datetime

from app.crud.crud_employee_account import CRUDEmployeeAccount
from app.crud.crud_employee_account import \
    employee_account as crud_employee_account
from app.db.models import EmployeeAccount, Session
from app.manager.manager_abstract import ModelType
from app.manager.manager_base import ManagerBase
from app.schemas.schema_employee_account import (EmployeeAccountCreate,
                                                 EmployeeAccountUpdate)


class EmployeeAccountManager(
    ManagerBase[
        EmployeeAccount,
        CRUDEmployeeAccount,
        EmployeeAccountCreate,
        EmployeeAccountUpdate,
    ]
):
    def create(self, obj_in: EmployeeAccountCreate, session: Session) -> ModelType:
        obj_in_data = obj_in.dict()
        obj_in_data.update(
            {
                "creation_date": datetime.utcnow(),
                "is_active": True,
            }
        )
        return self.crud.create(obj_in_data)


employee_account: EmployeeAccountManager = EmployeeAccountManager(crud_employee_account)
