from typing import Optional
from pydantic import BaseModel, ConfigDict


class Family(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="ignore")

    name: str


class Product(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="ignore")

    name: Optional[str] = None
    family: Optional["Family"] = None
    product_id: Optional[int] = None
    price: Optional[float] = None
