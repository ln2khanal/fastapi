from datetime import datetime
from pydantic import BaseModel, ConfigDict

from .products import Product


class Sales(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="ignore")

    date: datetime
    sales: int
    item: Product
