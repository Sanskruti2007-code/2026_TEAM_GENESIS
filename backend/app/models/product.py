from pydantic import BaseModel, Field
from typing import Optional


class Product(BaseModel):
    name: str
    quantity: int = Field(default=0, ge=0)
    price: float = Field(default=0, ge=0)
    category: Optional[str] = None
    unit: Optional[str] = "piece"


class ProductResponse(BaseModel):
    success: bool
    message: str
    product: Optional[Product] = None