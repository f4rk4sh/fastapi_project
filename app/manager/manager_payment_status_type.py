from app.crud.crud_payment_status_type import CRUDPaymentStatusType
from app.crud.crud_payment_status_type import \
    payment_status_type as crud_payment_status_type
from app.db.models import PaymentStatusType
from app.manager.manager_base import ManagerBase
from app.schemas.schema_payment_status_type import (PaymentStatusTypeCreate,
                                                    PaymentStatusTypeUpdate)


class PaymentStatusTypeManager(
    ManagerBase[
        PaymentStatusType,
        CRUDPaymentStatusType,
        PaymentStatusTypeCreate,
        PaymentStatusTypeUpdate,
    ]
):
    pass


payment_status_type: PaymentStatusTypeManager = PaymentStatusTypeManager(
    crud_payment_status_type
)
