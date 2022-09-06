import logging
from typing import Callable

from fastapi import HTTPException, Request, Response
from fastapi.exceptions import RequestValidationError
from fastapi.routing import APIRoute

from app.utils.exceptions.common_exceptions import (
    HTTPInternalServerException,
    HTTPUnprocessableEntityException,
)


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
                    raise HTTPUnprocessableEntityException(
                        exception=exc, body=await request.body()
                    )
                logging.exception(exc)
                raise HTTPInternalServerException()

        return exception_route_handler
