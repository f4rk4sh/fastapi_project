from datetime import datetime

from app.crud.crud_employer_payment_method import CRUDEmployerPaymentMethod,\
    employer_payment_method as crud_employer_payment_method
from app.db.models import EmployerPaymentMethod, Session
from app.manager.manager_base import ManagerBase
from app.schemas.schema_employer_payment_method import EmployerPaymentMethodCreate,\
    EmployerPaymentMethodUpdate


class EmployerPaymentMethodManager(
    ManagerBase[
        EmployerPaymentMethod,
        CRUDEmployerPaymentMethod,
        EmployerPaymentMethodCreate,
        EmployerPaymentMethodUpdate,
    ]
):
    def create(self, obj_in: EmployerPaymentMethodCreate, session: Session):
        obj_in_data = obj_in.dict()
        obj_in_data.update(
            {
                "creation_date": datetime.utcnow(),
                "is_active": True,
            }
        )
        return self.crud.create(obj_in_data)


employer_payment_method: EmployerPaymentMethodManager = EmployerPaymentMethodManager(
    crud_employer_payment_method
)
