from fastapi import APIRouter, HTTPException, status

from app.models.transaction import OrderCreate
from app.services.finance_service import finance_service

router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.get("")
def get_transactions():
    return {
        "success": True,
        "transactions": finance_service.get_transactions(),
    }


@router.post("", status_code=status.HTTP_201_CREATED)
def add_transaction(order: OrderCreate):
    result = finance_service.create_order(
        customer_name=order.customerName,
        items=[item.model_dump() for item in order.items],
        status=order.status,
    )
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])
    return {
        "success": True,
        "message": "Sale recorded successfully",
        "transaction": result["transaction"],
    }


@router.get("/{transaction_id}")
def get_transaction(transaction_id: str):
    transaction = finance_service.get_transaction(transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return {"success": True, "transaction": transaction}


@router.delete("/{transaction_id}")
def delete_transaction(transaction_id: str):
    if not finance_service.delete_transaction(transaction_id):
        raise HTTPException(status_code=404, detail="Transaction not found")
    return {"success": True, "message": "Transaction deleted successfully"}
