from fastapi import status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_utils.inferring_router import InferringRouter

from app.api.dependencies import Session
from app.manager.manager_auth import auth
from app.schemas.token import Token
from app.utils.exceptions.exception_route_handler import ExceptionRouteHandler

router = InferringRouter(route_class=ExceptionRouteHandler, tags=["Authentication"])


@router.post("/auth/login", status_code=status.HTTP_201_CREATED)
def login(
        data: OAuth2PasswordRequestForm = Depends(),
        session: Session = Depends(),
) -> Token:
    return auth.login(data, session)


@router.get("/auth/logout", status_code=status.HTTP_200_OK)
def logout():
    return auth.logout()
