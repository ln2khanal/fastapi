from app.lib.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, ForeignKey, DateTime

class Sales(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, index=True)
    value = Column(Integer)
    product_id = Column(Integer, ForeignKey("product.id"))

    product = relationship("Product", back_populates="sales")