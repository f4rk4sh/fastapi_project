from datetime import datetime, timedelta

from jose import jwt

from app.config.jwt_config import JWTConfig


def create_jwt(data: dict = None, set_expire: bool = False):
    if not data:
        data = {}
    if set_expire:
        data.update(
            {
                "exp": datetime.utcnow() + timedelta(minutes=int(JWTConfig.JWT_TOKEN_EXPIRE_TIME))
            }
        )
    return jwt.encode(data, JWTConfig.JWT_SECRET_KEY, algorithm=JWTConfig.JWT_ALGORITHM)


def decode_jwt(token: str):
    try:
        return jwt.decode(token, JWTConfig.JWT_SECRET_KEY, algorithms=JWTConfig.JWT_ALGORITHM)
    except jwt.JWTError:
        return None
