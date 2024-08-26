from datetime import datetime
from pydantic import BaseModel, Field

from .products import Product

class Sales(BaseModel):
    date: datetime
    sales: int = Field(gt=0)
    item: Product

    class Config:
        orm_mode = True