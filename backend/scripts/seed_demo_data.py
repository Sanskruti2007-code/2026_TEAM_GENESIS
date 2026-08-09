"""Reset the local database and load predictable hackathon demo data."""

import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.services.finance_service import finance_service
from app.services.firebase_service import firebase_service
from app.services.inventory_service import inventory_service


PRODUCTS = [
    ("Parle-G Biscuits", 45, 8, 10, "Grocery", "ABC Distributors", 15),
    ("Aashirvaad Atta 5kg", 58, 210, 245, "Grocery", "Shree Wholesale", 20),
    ("Dettol Soap", 17, 18, 22, "Personal Care", "Nagpur FMCG Hub", 8),
    ("Tata Salt 1kg", 11, 23, 28, "Grocery", "Shree Wholesale", 12),
    ("Fortune Oil 1L", 7, 128, 145, "Cooking Essentials", "Vidarbha Oils", 10),
    ("Maggi Noodles", 0, 12, 15, "Packaged Food", "ABC Distributors", 10),
]


def main():
    firebase_service.clear_collection("transactions")
    firebase_service.clear_collection("products")

    saved = {}
    for name, quantity, buying, selling, category, supplier, reorder in PRODUCTS:
        product = inventory_service.add_product(
            name=name,
            quantity=quantity,
            purchase_price=buying,
            selling_price=selling,
            category=category,
            supplier=supplier,
            reorder_level=reorder,
        )
        saved[name] = product
        print(f"Added {name}: {quantity} units")

    finance_service.create_order(
        "Walk-in Customer",
        [{"productId": saved["Parle-G Biscuits"]["id"], "quantity": 3}],
    )
    finance_service.create_order(
        "Rahul Traders",
        [{"productId": saved["Dettol Soap"]["id"], "quantity": 2}],
    )
    print("Demo products and today's sales are ready.")


if __name__ == "__main__":
    main()
