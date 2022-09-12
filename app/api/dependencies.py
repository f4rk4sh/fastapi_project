from datetime import datetime, timedelta
from typing import Union

from fastapi import Cookie

from app import crud
from app.security.tokens import create_jwt, decode_jwt
from app.utils.exceptions.common_exceptions import HTTPUnauthorizedException


class Session:
    def __init__(self, s_id: Union[int, None] = Cookie(default=None)):
        if s_id:
            session = crud.session.get(self.s_id)
            if session:
                if session.expiration_date > datetime.utcnow():
                    self.s_id = s_id
                    self.data = decode_jwt(session.token)["data"]
        else:
            new_session = self._create_new()
            self.s_id = new_session.id
            self.data = {}

    @classmethod
    def _create_new(cls):
        return crud.session.create(
            {
                "token": create_jwt(data={"data": {}}),
                "creation_date": datetime.utcnow(),
                "expiration_date": datetime.utcnow() + timedelta(minutes=120),
            }
        )

    def _update(self, data: dict):
        session = crud.session.get(self.s_id)
        session_data = decode_jwt(session.token)
        session_data["data"].update(data)
        crud.session.update(
            session,
            {
                "token": create_jwt(data=session_data),
                "expiration_date": datetime.utcnow() + timedelta(minutes=120),
            }
        )
        self.data = session_data

    def add(self, data: dict):
        self._update(data)


class AuthSession(Session):
    def __init__(self, s_id: Union[int, None] = Cookie(default=None)):
        self.s_id = s_id
        super().__init__(self.s_id)
        access_token = self.data.get("access_token")
        if access_token:
            decoded_token = decode_jwt(access_token)
            if datetime.fromtimestamp(decoded_token["exp"]) > datetime.utcnow():
                user_email = decoded_token["sub"]
                user = crud.user.get_by_attribute(email=user_email)
                self.add(
                    {
                        "access_token": create_jwt(data={"sub": user_email}, expire=True),
                        "user_id": user.id
                    }
                )
                self._user_role = user.role.name
        else:
            raise HTTPUnauthorizedException()
