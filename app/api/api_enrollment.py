from fastapi import APIRouter
from app.api.routes.employee.endpoints import router as employee_router
from app.api.routes.employer.endpoints import router as employer_router
from app.api.routes.health.endpoints import router as health_router


router = APIRouter()
router.include_router(employee_router)
router.include_router(employer_router)
router.include_router(health_router)
