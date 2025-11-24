from sqlalchemy import Column, Integer, String, Text, Numeric, Boolean, Index, func
from .database import Base

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String(128), nullable=False)
    name = Column(String(255))
    description = Column(Text)
    price = Column(Numeric(10,2))
    active = Column(Boolean, default=True)

    __table_args__ = (
        Index('ix_products_sku_ci', func.lower(sku), unique=True),
    )
