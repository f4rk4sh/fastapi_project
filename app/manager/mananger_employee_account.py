from datetime import datetime

from app import crud
from app.crud.crud_employee_account import CRUDEmployeeAccount, employee_account as crud_employee_account
from app.db.models import EmployeeAccount, Session
from app.manager.manager_base import ManagerBase, ModelType
from app.schemas.schema_employee_account import EmployeeAccountCreate, EmployeeAccountUpdate


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
                "employee_id": crud.employer.get_by_attribute(
                    user_id=session.user_id
                ),
            }
        )
        return self.crud.create(obj_in_data)


employee_account: EmployeeAccountManager = EmployeeAccountManager(crud_employee_account)
