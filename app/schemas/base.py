from typing import Sequence

from pydantic import BaseModel, Field, PositiveInt


class InstanceBase(BaseModel):
    name: str = Field(..., max_length=50)


class InstanceCreate(InstanceBase):
    pass


class InstanceUpdate(InstanceBase):
    id: PositiveInt


class InstanceResponse(InstanceBase):
    id: PositiveInt

    class Config:
        orm_mode = True


class InstanceSearchResults(BaseModel):
    results: Sequence[InstanceResponse]
