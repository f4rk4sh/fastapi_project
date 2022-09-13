from fastapi import Response
from fastapi.security import OAuth2PasswordRequestForm

from app import crud
from app.api.dependencies import Session
from app.security.tokens import create_jwt


class AuthManager:
    @classmethod
    def login(cls, data: OAuth2PasswordRequestForm, session: Session):
        user = crud.user.authenticate(data.username, data.password)
        access_token = create_jwt(data={"sub": user.email}, expire=True)
        response: Response = Response()
        response.set_cookie(key="s_id", value=session.s_id)
        response.set_cookie(key="access_token", value=access_token)
        return response

    @classmethod
    def logout(cls):
        response: Response = Response()
        response.delete_cookie("access_token")
        return response


auth: AuthManager = AuthManager()
