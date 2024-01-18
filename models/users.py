from pydantic import BaseModel
from .item import Item


class User(BaseModel):
    id: int
    first_name: str = None
    last_name: str = None
    username: str = None
    email: str = None
    password: str = None
    is_active: bool = None
    items: list[Item] = []

    class Config:
        from_attributes = True


class SafeUser(BaseModel):
    id: int
    first_name: str = None
    last_name: str = None
    username: str = None
    email: str = None
    is_active: bool = None
    items: list[Item] = []
