from typing import List

from pydantic import BaseModel

from app.schemas.base import InstanceBase, InstanceCreate, InstanceResponse, InstanceUpdate


class RoleBase(InstanceBase):
    pass


class RoleCreate(RoleBase, InstanceCreate):
    pass


class RoleUpdate(RoleBase, InstanceUpdate):
    pass


class RoleResponse(RoleBase, InstanceResponse):
    pass


class RolesResponse(BaseModel):
    roles: List[RoleResponse]


class RoleSearchResults(BaseModel):
    results: List[RoleResponse]
