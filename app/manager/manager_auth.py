from fastapi import Response
from fastapi.security import OAuth2PasswordRequestForm

from app import crud
from app.api.dependencies import Session
from app.security.tokens import create_jwt


class AuthManager:
    @classmethod
    def login(cls, response: Response, data: OAuth2PasswordRequestForm, session: Session):
        user = crud.user.authenticate(data.username, data.password)
        access_token = create_jwt(data={"sub": user.email}, expire=True)
        response.set_cookie(key="s_id", value=session.s_id)
        response.set_cookie(key="access_token", value=access_token)
        return {"access_token": access_token, "token_type": "bearer"}

    @classmethod
    def logout(cls, response: Response):
        response.delete_cookie("access_token")


auth: AuthManager = AuthManager()
