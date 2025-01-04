from pydantic import BaseModel, ConfigDict
from datetime import datetime


class ItemBase(BaseModel):
    title: str
    contents: str


class ItemCreate(ItemBase):
    pass


class ItemUpdate(ItemBase):
    pass


class Item(ItemBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    comment_count: int
    view_count: int
    user_id: int
    is_modified: bool
    created_at: datetime
    updated_at: datetime


# Pydantic models for Comment


class CommentBase(BaseModel):
    contents: str


class CommentCreate(CommentBase):
    pass


class CommentUpdate(CommentBase):
    pass


class Comment(CommentBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    item_id: int
    user_id: int
    is_modified: bool
    created_at: datetime
    updated_at: datetime

