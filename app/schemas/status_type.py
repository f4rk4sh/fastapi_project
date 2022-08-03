from app.schemas.base import InstanceBase, InstanceCreate, Instance, InstanceUpdate


class StatusTypeBase(InstanceBase):
    pass


class StatusTypeCreate(StatusTypeBase, InstanceCreate):
    pass


class StatusType(StatusTypeCreate, Instance):
    pass


class StatusTypeUpdate(StatusTypeBase, InstanceUpdate):
    pass
