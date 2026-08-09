from typing import Optional

from pydantic import BaseModel, Field


class ProductCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    category: str = Field(default="General", max_length=80)
    purchasePrice: float = Field(ge=0)
    sellingPrice: float = Field(ge=0)
    quantity: int = Field(default=0, ge=0)
    supplier: str = Field(default="Local Supplier", max_length=120)
    reorderLevel: int = Field(default=5, ge=0)


class ProductUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=120)
    category: Optional[str] = Field(default=None, max_length=80)
    purchasePrice: Optional[float] = Field(default=None, ge=0)
    sellingPrice: Optional[float] = Field(default=None, ge=0)
    quantity: Optional[int] = Field(default=None, ge=0)
    supplier: Optional[str] = Field(default=None, max_length=120)
    reorderLevel: Optional[int] = Field(default=None, ge=0)


# Backward-compatible name for old imports.
Product = ProductCreate
