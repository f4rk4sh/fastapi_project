from app.crud.crud_base import CRUDBase
from app.db.models import PaymentStatusType
from app.schemas.schema_payment_status_type import PaymentStatusTypeCreate, PaymentStatusTypeUpdate


class CRUDPaymentStatusType(CRUDBase[PaymentStatusType, PaymentStatusTypeCreate, PaymentStatusTypeUpdate]):
    pass


payment_status_type = CRUDPaymentStatusType(PaymentStatusType)
