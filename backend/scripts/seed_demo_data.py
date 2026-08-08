# backend/scripts/seed_demo_data.py

import sys
import os
from datetime import datetime, timedelta

# Add backend directory to Python path
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

from app.services.firebase_service import firebase_service


def seed_products():
    products = [
        {
            "name": "Rice",
            "quantity": 45,
            "price": 60,
            "category": "Grocery"
        },
        {
            "name": "Wheat",
            "quantity": 30,
            "price": 45,
            "category": "Grocery"
        },
        {
            "name": "Sugar",
            "quantity": 8,
            "price": 50,
            "category": "Grocery"
        },
        {
            "name": "Tea",
            "quantity": 15,
            "price": 120,
            "category": "Beverages"
        },
        {
            "name": "Biscuits",
            "quantity": 5,
            "price": 30,
            "category": "Snacks"
        }
    ]

    print("\nAdding demo products...\n")

    for product in products:

        product["created_at"] = datetime.utcnow().isoformat()

        product_id = firebase_service.add_document(
            "products",
            product
        )

        print(
            f"Added: {product['name']} "
            f"(ID: {product_id})"
        )


def seed_transactions():
    transactions = [
        {
            "type": "sale",
            "product": "Rice",
            "quantity": 5,
            "price": 60,
            "total": 300,
            "created_at": (
                datetime.utcnow() - timedelta(hours=3)
            ).isoformat()
        },
        {
            "type": "sale",
            "product": "Wheat",
            "quantity": 3,
            "price": 45,
            "total": 135,
            "created_at": (
                datetime.utcnow() - timedelta(hours=2)
            ).isoformat()
        },
        {
            "type": "sale",
            "product": "Tea",
            "quantity": 2,
            "price": 120,
            "total": 240,
            "created_at": (
                datetime.utcnow() - timedelta(hours=1)
            ).isoformat()
        }
    ]

    print("\nAdding demo transactions...\n")

    for transaction in transactions:

        transaction_id = firebase_service.add_document(
            "transactions",
            transaction
        )

        print(
            f"Added sale: "
            f"{transaction['product']} × "
            f"{transaction['quantity']} "
            f"(ID: {transaction_id})"
        )


def main():

    print("=" * 50)
    print("       VaaniOS Demo Data Seeder")
    print("=" * 50)

    if not firebase_service.enabled:

        print(
            "\nFirebase is not configured."
        )

        print(
            "Please configure FIREBASE_CREDENTIALS "
            "in your .env file."
        )

        return

    seed_products()
    seed_transactions()

    print("\n" + "=" * 50)
    print("Demo data successfully added!")
    print("=" * 50)


if __name__ == "__main__":
    main()