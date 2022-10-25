from app.crud.crud_base import CRUDBase
from app.db.models import EmployerPaymentMethod
from app.schemas.schema_employer_payment_method import EmployerPaymentMethodCreate, \
    EmployerPaymentMethodUpdate


class CRUDEmployerPaymentMethod(
    CRUDBase[
        EmployerPaymentMethod,
        EmployerPaymentMethodCreate,
        EmployerPaymentMethodUpdate,
    ]
):
    pass


employer_payment_method = CRUDEmployerPaymentMethod(EmployerPaymentMethod)
