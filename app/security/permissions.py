import functools
from typing import List

from app.constansts.constants_role import ConstantRole
from app.utils.exceptions.common_exceptions import HTTPForbiddenException


def permission(allowed_roles: List[str]):
    def inner(func):
        @functools.wraps(func)
        def wrapper(session, *args, **kwargs):
            user_role = session.user.role.name
            if user_role != ConstantRole.su:
                if user_role not in allowed_roles:
                    raise HTTPForbiddenException()
            return func(*args, **kwargs)
        return wrapper
    return inner
