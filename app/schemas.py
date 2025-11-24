from pydantic import BaseModel, condecimal
from typing import Optional

class ProductBase(BaseModel):
    sku: str
    name: Optional[str]
    description: Optional[str]
    price: Optional[condecimal(max_digits=10, decimal_places=2)]
    active: Optional[bool] = True

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    pass

class ProductOut(ProductBase):
    id: int
    class Config:
        orm_mode = True
