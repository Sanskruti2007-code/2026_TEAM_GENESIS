from typing import Dict

from app.services.finance_service import finance_service
from app.services.inventory_service import inventory_service


class ReportService:
    def generate_dashboard_report(self) -> Dict:
        products = inventory_service.get_products()
        low_stock = inventory_service.get_low_stock_products()
        finance = finance_service.get_summary()
        today = finance_service.get_summary(today_only=True)

        total_inventory_items = sum(
            int(product.get("quantity", 0)) for product in products
        )
        inventory_value = sum(
            int(product.get("quantity", 0))
            * float(product.get("purchasePrice", product.get("price", 0)))
            for product in products
        )

        return {
            "inventory": {
                "total_products": len(products),
                "total_items": total_inventory_items,
                "inventory_value": inventory_value,
                "low_stock_count": len(low_stock),
                "low_stock_products": low_stock,
            },
            "finance": finance,
            "today": today,
        }

    def generate_voice_summary(self) -> str:
        report = self.generate_dashboard_report()
        finance = report["today"]
        inventory = report["inventory"]
        return (
            f"आजची एकूण विक्री ₹{finance['total_sales']:.2f} आणि नफा "
            f"₹{finance['total_profit']:.2f} आहे. "
            f"{finance['total_transactions']} व्यवहारांत "
            f"{finance['items_sold']} वस्तू विकल्या. "
            f"स्टॉकमध्ये {inventory['total_items']} वस्तू आहेत आणि "
            f"{inventory['low_stock_count']} उत्पादने कमी स्टॉकमध्ये आहेत."
        )


report_service = ReportService()
