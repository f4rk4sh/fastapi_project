from fastapi import APIRouter

from app.api.routes.account_type.endpoints import router as account_type
from app.api.routes.auth.endpoints import router as auth
from app.api.routes.bank.endpoints import router as bank
from app.api.routes.employee.endpoints import router as employee
from app.api.routes.employee_account.endpoints import \
    router as employee_account
from app.api.routes.employer.endpoints import router as employer
from app.api.routes.employer_payment_method.endpoints import \
    router as employer_payment_method
from app.api.routes.employer_type.endpoints import router as employer_type
from app.api.routes.health.endpoints import router as health
from app.api.routes.payment_history.endpoints import router as payment_history
from app.api.routes.payment_status_type.endpoints import \
    router as payment_status_type
from app.api.routes.role.endpoints import router as role
from app.api.routes.status_type.endpoints import router as status_type

router = APIRouter()
router.include_router(account_type)
router.include_router(auth)
router.include_router(bank)
router.include_router(employee)
router.include_router(employee_account)
router.include_router(employer)
router.include_router(employer_payment_method)
router.include_router(employer_type)
router.include_router(health)
router.include_router(payment_history)
router.include_router(payment_status_type)
router.include_router(role)
router.include_router(status_type)
