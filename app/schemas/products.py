from app.lib.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Float


class Family(Base):
    __tablename__ = "family"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    product = relationship("Product", back_populates="family")


class Product(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Float)
    product_id = Column(Integer, index=True)
    family_id = Column(Integer, ForeignKey("family.id"))

    family = relationship("Family", back_populates="product")
    sales = relationship("Sales", back_populates="product")
