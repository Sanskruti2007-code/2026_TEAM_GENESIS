from typing import Literal, Optional

from pydantic import BaseModel, Field


class OrderItem(BaseModel):
    productId: str
    quantity: int = Field(gt=0)
    price: Optional[float] = Field(default=None, ge=0)


class OrderCreate(BaseModel):
    customerName: str = Field(default="Walk-in Customer", max_length=120)
    items: list[OrderItem] = Field(min_length=1)
    status: Literal["Completed", "Pending"] = "Completed"


class Transaction(BaseModel):
    product_name: str
    quantity: int = Field(gt=0)
    amount: float = Field(ge=0)
    transaction_type: str
    customer_name: Optional[str] = None
