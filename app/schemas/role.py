from typing import Sequence

from pydantic import BaseModel

from app.schemas.base import InstanceBase, InstanceCreate, InstanceResponse, InstanceUpdate, InstanceSearchResults


class RoleBase(InstanceBase):
    pass


class RoleCreate(RoleBase, InstanceCreate):
    pass


class RoleUpdate(RoleBase, InstanceUpdate):
    pass


class RoleResponse(RoleBase, InstanceResponse):
    pass


class RolesResponse(BaseModel):
    roles: Sequence[RoleResponse]


class RoleSearchResults(BaseModel):
    results: Sequence[RoleResponse]
