from app.crud.crud_base import CRUDBase
from app.db.models import PaymentHistory
from app.schemas.schema_payment_history import PaymentHistoryCreate, PaymentHistoryUpdate


class CRUDPaymentHistory(
    CRUDBase[
        PaymentHistory,
        PaymentHistoryCreate,
        PaymentHistoryUpdate
    ]
):
    pass


payment_history = CRUDPaymentHistory(PaymentHistory)
