from pydantic import BaseModel, Field
from typing import Optional


class Transaction(BaseModel):
    product_name: str
    quantity: int = Field(..., gt=0)
    amount: float = Field(..., ge=0)
    transaction_type: str
    customer_name: Optional[str] = None


class TransactionResponse(BaseModel):
    success: bool
    message: str
    transaction: Optional[Transaction] = None