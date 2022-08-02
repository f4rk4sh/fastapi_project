from fastapi import APIRouter
from app.api.routes.employee.endpoints import router as employee_router
from app.api.routes.employer.endpoints import router as employer_router


api_router = APIRouter()
api_router.include_router(employee_router)
api_router.include_router(employer_router)
