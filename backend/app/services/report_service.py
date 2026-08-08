# backend/app/services/report_service.py

from typing import Dict

from app.services.inventory_service import inventory_service
from app.services.finance_service import finance_service


class ReportService:

    def generate_dashboard_report(self) -> Dict:

        products = inventory_service.get_products()

        low_stock = inventory_service.get_low_stock_products()

        finance = finance_service.get_summary()

        total_inventory_items = sum(
            product.get("quantity", 0)
            for product in products
        )

        inventory_value = sum(
            product.get("quantity", 0)
            * product.get("price", 0)
            for product in products
        )

        return {
            "inventory": {
                "total_products": len(products),
                "total_items": total_inventory_items,
                "inventory_value": inventory_value,
                "low_stock_count": len(low_stock),
                "low_stock_products": low_stock
            },
            "finance": finance
        }

    def generate_voice_summary(self) -> str:

        report = self.generate_dashboard_report()

        finance = report["finance"]
        inventory = report["inventory"]

        return (
            f"Aaj ki sales summary: "
            f"total sales ₹{finance['total_sales']}. "
            f"{finance['total_transactions']} transactions hui hain. "
            f"{finance['items_sold']} items sell hue hain. "
            f"Inventory mein {inventory['total_items']} items available hain. "
            f"{inventory['low_stock_count']} products low stock mein hain."
        )


report_service = ReportService()