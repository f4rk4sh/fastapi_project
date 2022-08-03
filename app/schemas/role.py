from app.schemas.base import InstanceBase, InstanceCreate, Instance, InstanceUpdate


class RoleBase(InstanceBase):
    pass


class RoleCreate(RoleBase, InstanceCreate):
    pass


class Role(RoleCreate, Instance):
    pass


class RoleUpdate(RoleBase, InstanceUpdate):
    pass

