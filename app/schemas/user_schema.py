from pydantic import BaseModel, ConfigDict
from datetime import datetime


class UserBase(BaseModel):
    email: str
    user_name: str


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    password: str | None = None
    is_active: bool | None = None


class UserOut(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
