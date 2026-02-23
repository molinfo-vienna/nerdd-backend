from enum import IntEnum

from pydantic import BaseModel

__all__ = ["AnonymousUser", "User", "UserType"]


class UserType(IntEnum):
    ANONYMOUS = 0


class User(BaseModel):
    id: str
    user_type: UserType = UserType.ANONYMOUS


class AnonymousUser(User):
    ip_address: str
