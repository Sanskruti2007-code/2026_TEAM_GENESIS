from datetime import datetime
from typing import Dict, List, Optional
from zoneinfo import ZoneInfo

from app.services.firebase_service import firebase_service
from app.services.inventory_service import inventory_service

INDIA_TZ = ZoneInfo("Asia/Kolkata")


def local_now() -> datetime:
    return datetime.now(INDIA_TZ)


class FinanceService:
    def create_order(
        self,
        customer_name: str,
        items: list[dict],
        status: str = "Completed",
    ) -> Dict:
        if not items:
            return {"success": False, "message": "Kam se kam ek product chahiye."}

        with firebase_service.lock:
            resolved_items = []
            for item in items:
                product = None
                if item.get("productId"):
                    product = inventory_service.get_product(str(item["productId"]))
                if not product and item.get("product"):
                    product = inventory_service.find_product(str(item["product"]))

                quantity = int(item.get("quantity", 0))
                if not product:
                    return {
                        "success": False,
                        "message": f"Product '{item.get('product', '')}' nahi mila.",
                    }
                if quantity <= 0:
                    return {
                        "success": False,
                        "message": f"{product['name']} ki quantity valid nahi hai.",
                    }
                if int(product.get("quantity", 0)) < quantity:
                    return {
                        "success": False,
                        "message": (
                            f"Insufficient stock: {product['name']} ke sirf "
                            f"{product.get('quantity', 0)} units available hain."
                        ),
                    }

                selling_price = float(
                    item.get("price")
                    if item.get("price") is not None
                    else product.get("sellingPrice", product.get("price", 0))
                )
                purchase_price = float(product.get("purchasePrice", 0))
                resolved_items.append(
                    {
                        "productId": product["id"],
                        "name": product["name"],
                        "quantity": quantity,
                        "sellingPrice": selling_price,
                        "purchasePrice": purchase_price,
                        "amount": selling_price * quantity,
                        "profit": (selling_price - purchase_price) * quantity,
                    }
                )

            updated_products = []
            try:
                for item in resolved_items:
                    result = inventory_service.update_stock(
                        item["name"], -item["quantity"]
                    )
                    if not result["success"]:
                        raise ValueError(result["message"])
                    updated_products.append(item)

                now = local_now()
                order = {
                    "id": f"ORD-{now.strftime('%y%m%d%H%M%S%f')[-12:]}",
                    "type": "sale",
                    "customerName": (customer_name or "Walk-in Customer").strip(),
                    "date": now.date().isoformat(),
                    "itemCount": sum(item["quantity"] for item in resolved_items),
                    "totalAmount": sum(item["amount"] for item in resolved_items),
                    "profit": sum(item["profit"] for item in resolved_items),
                    "status": status,
                    "items": resolved_items,
                    "createdAt": now.isoformat(),
                }
                # These fields keep the earlier one-product transaction API
                # compatible while the frontend uses the richer items list.
                if len(resolved_items) == 1:
                    item = resolved_items[0]
                    order.update(
                        {
                            "product": item["name"],
                            "quantity": item["quantity"],
                            "price": item["sellingPrice"],
                            "total": item["amount"],
                        }
                    )
                order_id = firebase_service.add_document("transactions", order)
                order["id"] = order_id
                return {"success": True, "transaction": order}
            except Exception as error:
                # Restore already changed stock if a later write fails.
                for item in updated_products:
                    inventory_service.update_stock(item["name"], item["quantity"])
                return {"success": False, "message": str(error)}

    def record_sale(
        self,
        product_name: str,
        quantity: int,
        price: Optional[float] = None,
    ) -> Dict:
        return self.create_order(
            customer_name="Walk-in Customer",
            items=[
                {
                    "product": product_name,
                    "quantity": quantity,
                    "price": price,
                }
            ],
        )

    def get_transactions(self) -> List[Dict]:
        return firebase_service.get_collection("transactions")

    def get_transaction(self, transaction_id: str) -> Optional[Dict]:
        return firebase_service.get_document("transactions", transaction_id)

    def delete_transaction(self, transaction_id: str) -> bool:
        return firebase_service.delete_document("transactions", transaction_id)

    def calculate_total_sales(self) -> float:
        return sum(
            transaction.get("totalAmount", transaction.get("total", 0))
            for transaction in self.get_transactions()
            if transaction.get("type") == "sale"
        )

    def get_summary(self, today_only: bool = False) -> Dict:
        today = local_now().date().isoformat()
        sales = [
            transaction
            for transaction in self.get_transactions()
            if transaction.get("type") == "sale"
            and (not today_only or transaction.get("date") == today)
        ]
        return {
            "total_sales": sum(
                sale.get("totalAmount", sale.get("total", 0)) for sale in sales
            ),
            "total_profit": sum(sale.get("profit", 0) for sale in sales),
            "total_transactions": len(sales),
            "items_sold": sum(
                sale.get("itemCount", sale.get("quantity", 0)) for sale in sales
            ),
        }


finance_service = FinanceService()
