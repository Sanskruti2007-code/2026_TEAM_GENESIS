from datetime import datetime, timezone
from typing import Dict, List, Optional

from app.services.firebase_service import firebase_service
from app.utlis.product_normalizer import normalize_product_name


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


class InventoryService:
    def add_product(
        self,
        name: str,
        quantity: int,
        price: Optional[float] = None,
        category: str = "General",
        purchase_price: Optional[float] = None,
        selling_price: Optional[float] = None,
        supplier: str = "",
        reorder_level: int = 5,
    ) -> Dict:
        normalized_name = normalize_product_name(name)
        fallback_price = float(price or 0)
        purchase_price = float(
            fallback_price if purchase_price is None else purchase_price
        )
        selling_price = float(
            purchase_price if selling_price is None else selling_price
        )
        quantity = int(quantity)

        product = {
            "name": normalized_name,
            "quantity": quantity,
            "price": selling_price,
            "purchasePrice": purchase_price,
            "sellingPrice": selling_price,
            "category": category or "General",
            "supplier": supplier or "Local Supplier",
            "reorderLevel": int(reorder_level),
            "openingStock": quantity,
            "stockIn": 0,
            "stockOut": 0,
            "createdAt": utc_now(),
            "updatedAt": utc_now(),
        }

        product_id = firebase_service.add_document("products", product)
        product["id"] = product_id
        return product

    def get_products(self) -> List[Dict]:
        return firebase_service.get_collection("products")

    def get_product(self, product_id: str) -> Optional[Dict]:
        return firebase_service.get_document("products", product_id)

    def find_product(self, product_name: str) -> Optional[Dict]:
        normalized = normalize_product_name(product_name).casefold().strip()
        products = self.get_products()

        for product in products:
            if product.get("name", "").casefold().strip() == normalized:
                return product

        # Voice transcription sometimes drops brand suffixes. Only accept a
        # partial match when exactly one product matches, avoiding guesses.
        candidates = [
            product
            for product in products
            if normalized in product.get("name", "").casefold()
            or product.get("name", "").casefold() in normalized
        ]
        return candidates[0] if len(candidates) == 1 else None

    def update_product(self, product_id: str, data: dict) -> Optional[Dict]:
        current = self.get_product(product_id)
        if not current:
            return None

        allowed = {
            "name",
            "category",
            "supplier",
            "purchasePrice",
            "sellingPrice",
            "quantity",
            "reorderLevel",
        }
        updates = {key: value for key, value in data.items() if key in allowed}

        for field in ("purchasePrice", "sellingPrice"):
            if field in updates:
                updates[field] = float(updates[field])

        for field in ("quantity", "reorderLevel"):
            if field in updates:
                updates[field] = int(updates[field])

        if "name" in updates:
            updates["name"] = normalize_product_name(updates["name"])
        if "sellingPrice" in updates:
            updates["price"] = updates["sellingPrice"]

        if "quantity" in updates:
            difference = updates["quantity"] - int(current.get("quantity", 0))
            if difference > 0:
                updates["stockIn"] = int(current.get("stockIn", 0)) + difference
            elif difference < 0:
                updates["stockOut"] = int(current.get("stockOut", 0)) + abs(difference)

        updates["updatedAt"] = utc_now()
        return firebase_service.update_document("products", product_id, updates)

    def delete_product(self, product_id: str) -> bool:
        return firebase_service.delete_document("products", product_id)

    def update_stock(self, product_name: str, quantity_change: int) -> Dict:
        product = self.find_product(product_name)
        if not product:
            return {
                "success": False,
                "message": f"Product '{product_name}' nahi mila.",
            }

        current_quantity = int(product.get("quantity", 0))
        quantity_change = int(quantity_change)
        new_quantity = current_quantity + quantity_change

        if new_quantity < 0:
            return {
                "success": False,
                "message": "Stock insufficient hai.",
            }

        updates = {
            "quantity": new_quantity,
            "updatedAt": utc_now(),
        }
        if quantity_change > 0:
            updates["stockIn"] = int(product.get("stockIn", 0)) + quantity_change
        elif quantity_change < 0:
            updates["stockOut"] = int(product.get("stockOut", 0)) + abs(
                quantity_change
            )

        updated = firebase_service.update_document(
            "products", product["id"], updates
        )
        return {
            "success": True,
            "product": updated,
            "old_quantity": current_quantity,
            "new_quantity": new_quantity,
        }

    def get_low_stock_products(self, threshold: Optional[int] = None) -> List[Dict]:
        products = self.get_products()
        return [
            product
            for product in products
            if int(product.get("quantity", 0))
            <= int(
                threshold
                if threshold is not None
                else product.get("reorderLevel", 10)
            )
        ]


inventory_service = InventoryService()
