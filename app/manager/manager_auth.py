from datetime import datetime

from fastapi import Response, status
from fastapi.security import OAuth2PasswordRequestForm

from app import crud
from app.constansts.constants_session import ConstantSessionStatus
from app.schemas.schema_session import SessionCreate, SessionUpdate
from app.security.tokens import create_jwt


class AuthManager:
    @classmethod
    def login(cls, data: OAuth2PasswordRequestForm):
        user = crud.user.authenticate(data.username, data.password)
        access_token = create_jwt(data={"user_id": user.id}, set_expire=True)
        crud.session.create(
            SessionCreate(
                token=access_token,
                creation_date=datetime.utcnow(),
                status=ConstantSessionStatus.logged_in,
                user_id=user.id,
            )
        )
        return {"access_token": access_token, "token_type": "bearer"}

    @classmethod
    def logout(cls, session):
        crud.session.update(session, SessionUpdate(id=session.id, status=ConstantSessionStatus.logged_out))
        return Response(status_code=status.HTTP_200_OK)
