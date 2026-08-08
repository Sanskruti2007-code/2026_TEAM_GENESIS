from fastapi import APIRouter

router = APIRouter()


@router.get("/transactions")
def get_transactions():
    return {
        "status": "success",
        "transactions": []
    }


@router.post("/transactions")
def add_transaction(transaction: dict):
    return {
        "status": "success",
        "message": "Transaction added successfully",
        "transaction": transaction
    }


@router.get("/transactions/{transaction_id}")
def get_transaction(transaction_id: str):
    return {
        "status": "success",
        "transaction_id": transaction_id
    }


@router.delete("/transactions/{transaction_id}")
def delete_transaction(transaction_id: str):
    return {
        "status": "success",
        "message": "Transaction deleted successfully",
        "transaction_id": transaction_id
    }