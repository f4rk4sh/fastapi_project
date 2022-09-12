from datetime import date

from pydantic import BaseModel, PositiveInt, Field

from app.schemas.token import Token


class SessionBase(BaseModel):
    token: Token
    creation_date: date


class SessionCreate(SessionBase):
    pass


class SessionUpdate(SessionBase):
    id: PositiveInt = Field(
        title="The ID of the session",
        description="Note: must be a positive integer",
        example=1,
    )
