from fastapi import APIRouter, Depends, Response, status


from app.api.dependencies import AuthSession
from app.security.permissions import permission

router = APIRouter(tags=["health"])


class HealthEndpoints:
    @staticmethod
    @router.get("/health/ping")
    @permission(["employee", "employer", "superuser"])
    def ping(session: AuthSession = Depends()):
        print(session.data)  # -> {}
        session.add({"test1": "test", "test2": "test"})
        print(session.data)  # -> {"test1": "test", "test2": "test"}
        return Response(status_code=status.HTTP_200_OK, content="Pong")
