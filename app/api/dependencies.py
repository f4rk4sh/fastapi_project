from datetime import datetime, timedelta
from typing import Union

from fastapi import Cookie

from app import crud
from app.schemas.session import SessionCreate, SessionUpdate
from app.security.tokens import create_jwt, decode_jwt
from app.utils.exceptions.common_exceptions import HTTPUnauthorizedException


class Session:
    def __init__(self, s_id: Union[int, None] = Cookie(default=None)):
        if s_id:
            session = crud.session.get(s_id)
            if session:
                if session.expiration_date > datetime.utcnow():
                    self.s_id = s_id
                    self.data = decode_jwt(session.token)
                    self._session = session
        else:
            self._session = self._create_new()
            self.s_id = self._session.id
            self.data = {}

    @classmethod
    def _create_new(cls):
        return crud.session.create(
            SessionCreate(
                token=create_jwt(data={}),
                creation_date=datetime.utcnow(),
                expiration_date=datetime.utcnow() + timedelta(minutes=120),
            )
        )

    def _update(self, data: dict = None, user_id: int = None):
        session = crud.session.get(self.s_id)
        session_data = decode_jwt(session.token)
        update_session = SessionUpdate(
            id=session.id,
            expiration_date=datetime.utcnow() + timedelta(minutes=120)
        )
        if data:
            session_data.update(data)
            update_session.token = create_jwt(data=session_data)
        if user_id:
            update_session.user_id = user_id
        crud.session.update(session, update_session)
        self.data = session_data

    def add(self, data: dict):
        self._update(data)


class AuthSession(Session):
    def __init__(
            self,
            s_id: Union[int, None] = Cookie(default=None),
            access_token: Union[str, None] = Cookie(default=None),
    ):
        self.s_id = s_id
        super().__init__(self.s_id)
        if not access_token:
            raise HTTPUnauthorizedException()
        decoded_token = decode_jwt(access_token)
        if not decoded_token:
            raise HTTPUnauthorizedException()
        user_email = decoded_token["sub"]
        user = crud.user.get_by_attribute(email=user_email)
        if not user:
            raise HTTPUnauthorizedException()
        self._update(user_id=user.id)
        self._user_role = user.role.name
