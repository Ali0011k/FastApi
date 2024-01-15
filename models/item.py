from pydantic import BaseModel


class Item(BaseModel):
    id: int
    name: str | None = None
    price: int | None = None

    class Config:
        from_attributes = True
