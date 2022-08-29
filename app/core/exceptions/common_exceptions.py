from fastapi import HTTPException, status, Request
from fastapi.exceptions import RequestValidationError


class HTTPNotFoundException(HTTPException):
    def __init__(self, model_name: str, obj_id: int = None):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{model_name} with ID {obj_id} not found" if obj_id else f"{model_name}s not found"
        )


class HTTPUnprocessableEntityException(HTTPException):
    def __init__(self, exception: RequestValidationError, body: Request.body = None):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"errors": exception.errors(), "body": body} if body else {"errors": exception.errors()}
        )


class HTTPInternalServerException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


class HTTPBadRequestException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail
        )
