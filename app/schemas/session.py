from datetime import datetime

from pydantic import BaseModel, Field, PositiveInt


class SessionBase(BaseModel):
    token: str = Field(..., max_length=100)


class SessionCreate(SessionBase):
    pass


class Session(SessionBase):
    id: PositiveInt
    creation_date: datetime

    class Config:
        orm_mode = True


class SessionUpdate(SessionBase):
    class Config:
        orm_mode = True
