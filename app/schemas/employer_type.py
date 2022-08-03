from app.schemas.base import InstanceBase, InstanceCreate, Instance, InstanceUpdate


class EmployerTypeBase(InstanceBase):
    pass


class EmployerTypeCreate(EmployerTypeBase, InstanceCreate):
    pass


class EmployerType(EmployerTypeCreate, Instance):
    pass


class EmployerUpdate(EmployerTypeBase, InstanceUpdate):
    pass
