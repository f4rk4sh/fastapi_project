from datetime import datetime
from typing import Optional

from pydantic import BaseModel, PositiveInt, Field


class SessionBase(BaseModel):
    token: str
    creation_date: datetime
    expiration_date: datetime


class SessionCreate(SessionBase):
    user_id: Optional[PositiveInt] = None


class SessionUpdate(SessionBase):
    id: PositiveInt = Field(
        title="The ID of the session",
        description="Note: must be a positive integer",
        example=1,
    )
    token: Optional[str] = None
    creation_date: Optional[datetime] = None
    expiration_date: Optional[datetime] = None
    user_id: Optional[PositiveInt] = None
