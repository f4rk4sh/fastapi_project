from fastapi import APIRouter
from app.api.routes.employee.endpoints import router as employee_router
from app.api.routes.employer.endpoints import router as employer_router
from app.api.routes.health.endpoints import router as health_router
from app.api.routes.role.endpoints import router as role_router


router = APIRouter()
router.include_router(employee_router, prefix="/employers", tags=["employers"])
router.include_router(employer_router, prefix="/employees", tags=["employees"])
router.include_router(health_router, prefix="/health", tags=["health"])
router.include_router(role_router, prefix="/roles", tags=["roles"])
