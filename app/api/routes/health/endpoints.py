from fastapi import APIRouter
from starlette import status
from starlette.responses import Response

router = APIRouter()


class HealthEndpoints:
    @staticmethod
    @router.get("/ping")
    def ping():
        return Response(status_code=status.HTTP_200_OK, content="Pong")
