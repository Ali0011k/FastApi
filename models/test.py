from pydantic import BaseModel, Field


class TestModel(BaseModel):
    """a test model"""

    name: str = Field(default="")
    age: int = Field(default=1)
    is_active: bool = Field(default=False)
