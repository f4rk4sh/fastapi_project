import functools
from typing import List

from app.api.dependencies import AuthSession
from app.utils.exceptions.common_exceptions import HTTPForbiddenException


def permission(roles: List = None):
    def inner(func):
        @functools.wraps(func)
        def wrapper(session: AuthSession, *args, **kwargs):
            if roles and session._user_role not in roles:
                raise HTTPForbiddenException()
            return func(session, *args, **kwargs)
        return wrapper
    return inner
