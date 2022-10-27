from fastapi import APIRouter

from app.api.routes.auth.endpoints import router as auth_router
from app.api.routes.bank.endpoints import router as bank_router
from app.api.routes.employee.endpoints import router as employee_router
from app.api.routes.employer.endpoints import router as employer_router
from app.api.routes.employer_type.endpoints import router as employer_type_router
from app.api.routes.health.endpoints import router as health_router
from app.api.routes.role.endpoints import router as role_router
from app.api.routes.status_type.endpoints import router as status_type_router

router = APIRouter()
router.include_router(auth_router)
router.include_router(bank_router)
router.include_router(employee_router)
router.include_router(employer_router)
router.include_router(health_router)
router.include_router(role_router)
router.include_router(status_type_router)
router.include_router(employer_type_router)
