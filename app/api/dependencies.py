from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer


from app import crud
from app.constansts.constants_session import ConstantSessionStatus
from app.security.tokens import decode_jwt
from app.utils.exceptions.common_exceptions import HTTPUnauthorizedException

oauth2_schema = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_session(token: str = Depends(oauth2_schema)):
    data = decode_jwt(token)
    if not data:
        raise HTTPUnauthorizedException()
    session = crud.session.get_one_ordered_by_creation_date(user_id=data.get("user_id"))
    if not session:
        raise HTTPUnauthorizedException()
    if session.token != token:
        raise HTTPUnauthorizedException()
    if session.status == ConstantSessionStatus.logged_out:
        raise HTTPUnauthorizedException()
    return session
