from fastapi import status, Depends, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_utils.inferring_router import InferringRouter

from app.api.dependencies import Session
from app.manager.manager_auth import auth
from app.utils.exceptions.exception_route_handler import ExceptionRouteHandler

router = InferringRouter(route_class=ExceptionRouteHandler, tags=["Authentication"])


@router.post("/auth/token", status_code=status.HTTP_201_CREATED)
def login(response: Response, data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends()):
    return auth.login(response, data, session)
