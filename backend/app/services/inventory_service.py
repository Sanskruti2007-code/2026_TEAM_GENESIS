# backend/app/services/inventory_service.py

from datetime import datetime
from typing import Dict, List, Optional

from app.services.firebase_service import firebase_service


class InventoryService:

    def add_product(
        self,
        name: str,
        quantity: int,
        price: float,
        category: str = "General"
    ) -> Dict:

        product = {
            "name": name,
            "quantity": quantity,
            "price": price,
            "category": category,
            "created_at": datetime.utcnow().isoformat()
        }

        product_id = firebase_service.add_document(
            "products",
            product
        )

        product["id"] = product_id

        return product

    def get_products(self) -> List[Dict]:

        return firebase_service.get_collection("products")

    def find_product(
        self,
        product_name: str
    ) -> Optional[Dict]:

        products = self.get_products()

        product_name = product_name.lower().strip()

        for product in products:
            name = product.get("name", "").lower()

            if name == product_name:
                return product

        return None

    def update_stock(
        self,
        product_name: str,
        quantity_change: int
    ) -> Dict:

        product = self.find_product(product_name)

        if not product:
            return {
                "success": False,
                "message": f"Product '{product_name}' nahi mila."
            }

        current_quantity = product.get("quantity", 0)

        new_quantity = current_quantity + quantity_change

        if new_quantity < 0:
            return {
                "success": False,
                "message": "Stock insufficient hai."
            }

        firebase_service.update_document(
            "products",
            product["id"],
            {
                "quantity": new_quantity,
                "updated_at": datetime.utcnow().isoformat()
            }
        )

        return {
            "success": True,
            "product": product_name,
            "old_quantity": current_quantity,
            "new_quantity": new_quantity
        }

    def get_low_stock_products(
        self,
        threshold: int = 10
    ) -> List[Dict]:

        products = self.get_products()

        return [
            product
            for product in products
            if product.get("quantity", 0) <= threshold
        ]


inventory_service = InventoryService()