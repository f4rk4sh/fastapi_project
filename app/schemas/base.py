from pydantic import BaseModel, Field, PositiveInt


class InstanceBase(BaseModel):
    name: str = Field(..., max_length=50)


class InstanceCreate(InstanceBase):
    pass


class Instance(InstanceCreate):
    id: PositiveInt

    class Config:
        orm_mode = True


class InstanceUpdate(InstanceBase):
    class Config:
        orm_mode = True
