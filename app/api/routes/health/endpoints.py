from fastapi import APIRouter, Response, status, Depends

from app.api.dependencies import get_session
from app.constansts.constants_role import ConstantRole
from app.security.permissions import permission

router = APIRouter(tags=["health"])


class HealthEndpoints:
    @staticmethod
    @router.get("/health/ping")
    @permission([ConstantRole.employee])
    def ping(session=Depends(get_session)):
        return Response(status_code=status.HTTP_200_OK, content="Pong")
