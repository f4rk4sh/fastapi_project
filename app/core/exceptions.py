from typing import Callable

from fastapi import Request, Response, HTTPException, status
from fastapi.exceptions import RequestValidationError
from fastapi.routing import APIRoute
import logging


class ExceptionRouteHandler(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def exception_route_handler(request: Request) -> Response:
            try:
                return await original_route_handler(request)
            except Exception as exc:
                if isinstance(exc, HTTPException):
                    raise HTTPException(status_code=exc.status_code, detail=exc.detail)
                if isinstance(exc, RequestValidationError):
                    detail = {"errors": exc.errors()}
                    body = await request.body()
                    if body:
                        detail.update({"body": body})
                    raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=detail)
                logging.exception(exc)
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return exception_route_handler


class HTTPNotFoundException(HTTPException):
    def __init__(self, model_name: str, obj_id: int = None):
        self.status_code = status.HTTP_404_NOT_FOUND
        self.detail = f"{model_name} with ID {obj_id} not found" if obj_id else f"{model_name}s not found"
        super().__init__(status_code=self.status_code, detail=self.detail)
