# backend/tests/test_inventory.py

import sys
import os

import pytest

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

from app.services.inventory_service import InventoryService


@pytest.fixture
def inventory_service():
    return InventoryService()


def test_add_product(inventory_service, monkeypatch):

    def mock_add_document(collection, data):
        return "test-product-id"

    monkeypatch.setattr(
        "app.services.inventory_service.firebase_service.add_document",
        mock_add_document
    )

    product = inventory_service.add_product(
        name="Rice",
        quantity=20,
        price=60,
        category="Grocery"
    )

    assert product["id"] == "test-product-id"
    assert product["name"] == "Rice"
    assert product["quantity"] == 20
    assert product["price"] == 60


def test_find_product(inventory_service, monkeypatch):

    mock_products = [
        {
            "id": "1",
            "name": "Rice",
            "quantity": 20,
            "price": 60
        },
        {
            "id": "2",
            "name": "Sugar",
            "quantity": 10,
            "price": 50
        }
    ]

    monkeypatch.setattr(
        inventory_service,
        "get_products",
        lambda: mock_products
    )

    product = inventory_service.find_product("Rice")

    assert product is not None
    assert product["name"] == "Rice"


def test_find_product_case_insensitive(
    inventory_service,
    monkeypatch
):

    mock_products = [
        {
            "id": "1",
            "name": "Rice",
            "quantity": 20,
            "price": 60
        }
    ]

    monkeypatch.setattr(
        inventory_service,
        "get_products",
        lambda: mock_products
    )

    product = inventory_service.find_product("rice")

    assert product is not None
    assert product["name"] == "Rice"


def test_find_missing_product(
    inventory_service,
    monkeypatch
):

    monkeypatch.setattr(
        inventory_service,
        "get_products",
        lambda: []
    )

    product = inventory_service.find_product("Rice")

    assert product is None


def test_update_stock(
    inventory_service,
    monkeypatch
):

    mock_product = {
        "id": "1",
        "name": "Rice",
        "quantity": 20,
        "price": 60
    }

    monkeypatch.setattr(
        inventory_service,
        "find_product",
        lambda name: mock_product
    )

    monkeypatch.setattr(
        "app.services.inventory_service.firebase_service.update_document",
        lambda collection, document_id, data: True
    )

    result = inventory_service.update_stock(
        "Rice",
        10
    )

    assert result["success"] is True
    assert result["old_quantity"] == 20
    assert result["new_quantity"] == 30


def test_stock_decrease(
    inventory_service,
    monkeypatch
):

    mock_product = {
        "id": "1",
        "name": "Rice",
        "quantity": 20,
        "price": 60
    }

    monkeypatch.setattr(
        inventory_service,
        "find_product",
        lambda name: mock_product
    )

    monkeypatch.setattr(
        "app.services.inventory_service.firebase_service.update_document",
        lambda collection, document_id, data: True
    )

    result = inventory_service.update_stock(
        "Rice",
        -5
    )

    assert result["success"] is True
    assert result["new_quantity"] == 15


def test_insufficient_stock(
    inventory_service,
    monkeypatch
):

    mock_product = {
        "id": "1",
        "name": "Rice",
        "quantity": 5,
        "price": 60
    }

    monkeypatch.setattr(
        inventory_service,
        "find_product",
        lambda name: mock_product
    )

    result = inventory_service.update_stock(
        "Rice",
        -10
    )

    assert result["success"] is False
    assert "insufficient" in result["message"].lower()


def test_low_stock_products(
    inventory_service,
    monkeypatch
):

    mock_products = [
        {
            "id": "1",
            "name": "Rice",
            "quantity": 20
        },
        {
            "id": "2",
            "name": "Sugar",
            "quantity": 5
        },
        {
            "id": "3",
            "name": "Tea",
            "quantity": 8
        }
    ]

    monkeypatch.setattr(
        inventory_service,
        "get_products",
        lambda: mock_products
    )

    low_stock = inventory_service.get_low_stock_products(
        threshold=10
    )

    assert len(low_stock) == 2
    assert low_stock[0]["name"] == "Sugar"
    assert low_stock[1]["name"] == "Tea"