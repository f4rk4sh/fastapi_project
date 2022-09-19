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
    session = crud.session.get_by_attribute(order_by="creation_date", desc=True, user_id=data.get("user_id"))
    if not session or session.token != token or session.status == ConstantSessionStatus.logged_out:
        raise HTTPUnauthorizedException()
    return session
