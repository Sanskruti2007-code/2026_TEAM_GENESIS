# backend/app/services/finance_service.py

from datetime import datetime
from typing import Dict, List

from app.services.firebase_service import firebase_service
from app.services.inventory_service import inventory_service


class FinanceService:

    def record_sale(
        self,
        product_name: str,
        quantity: int,
        price: float
    ) -> Dict:

        total_amount = quantity * price

        product = inventory_service.find_product(product_name)

        if not product:
            return {
                "success": False,
                "message": f"Product '{product_name}' nahi mila."
            }

        if product.get("quantity", 0) < quantity:
            return {
                "success": False,
                "message": "Itna stock available nahi hai."
            }

        # Reduce inventory
        inventory_service.update_stock(
            product_name,
            -quantity
        )

        transaction = {
            "type": "sale",
            "product": product_name,
            "quantity": quantity,
            "price": price,
            "total": total_amount,
            "created_at": datetime.utcnow().isoformat()
        }

        transaction_id = firebase_service.add_document(
            "transactions",
            transaction
        )

        transaction["id"] = transaction_id

        return {
            "success": True,
            "transaction": transaction
        }

    def get_transactions(self) -> List[Dict]:

        return firebase_service.get_collection(
            "transactions"
        )

    def calculate_total_sales(self) -> float:

        transactions = self.get_transactions()

        total = 0

        for transaction in transactions:

            if transaction.get("type") == "sale":
                total += transaction.get("total", 0)

        return total

    def get_summary(self) -> Dict:

        transactions = self.get_transactions()

        sales = [
            t for t in transactions
            if t.get("type") == "sale"
        ]

        total_sales = sum(
            t.get("total", 0)
            for t in sales
        )

        total_items = sum(
            t.get("quantity", 0)
            for t in sales
        )

        return {
            "total_sales": total_sales,
            "total_transactions": len(sales),
            "items_sold": total_items
        }


finance_service = FinanceService()