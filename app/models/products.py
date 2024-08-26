from typing import Optional
from pydantic import BaseModel, Field


class Family(BaseModel):
    name: str

    class Config:
        orm_mode = True


class Product(BaseModel):
    name: Optional[str] = None
    family: Optional["Family"] = None
    product_id: Optional[int] = None
    price: Optional[float] = None

    class Config:
        orm_mode = True
