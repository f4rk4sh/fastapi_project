from datetime import datetime, timedelta

from jose import jwt

from app.config.jwt_config import jwt_cfg


def create_jwt(data: dict = None, set_expire: bool = False):
    if not data:
        data = {}
    if set_expire:
        data.update(
            {
                "exp": datetime.utcnow() + timedelta(minutes=int(jwt_cfg.JWT_TOKEN_EXPIRE_TIME))
            }
        )
    return jwt.encode(data, jwt_cfg.JWT_SECRET_KEY, algorithm=jwt_cfg.JWT_ALGORITHM)


def decode_jwt(token: str):
    try:
        return jwt.decode(token, jwt_cfg.JWT_SECRET_KEY, algorithms=jwt_cfg.JWT_ALGORITHM)
    except jwt.JWTError:
        return None
