# backend/tests/test_sales.py

import sys
import os

import pytest

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

from app.services.finance_service import FinanceService


@pytest.fixture
def finance_service():
    return FinanceService()


def test_record_sale(
    finance_service,
    monkeypatch
):

    mock_product = {
        "id": "1",
        "name": "Rice",
        "quantity": 20,
        "price": 60
    }

    monkeypatch.setattr(
        "app.services.finance_service.inventory_service.find_product",
        lambda name: mock_product
    )

    monkeypatch.setattr(
        "app.services.finance_service.inventory_service.update_stock",
        lambda name, quantity: {
            "success": True
        }
    )

    monkeypatch.setattr(
        "app.services.finance_service.firebase_service.add_document",
        lambda collection, data: "transaction-1"
    )

    result = finance_service.record_sale(
        product_name="Rice",
        quantity=5,
        price=60
    )

    assert result["success"] is True

    transaction = result["transaction"]

    assert transaction["id"] == "transaction-1"
    assert transaction["product"] == "Rice"
    assert transaction["quantity"] == 5
    assert transaction["price"] == 60
    assert transaction["total"] == 300


def test_sale_reduces_inventory(
    finance_service,
    monkeypatch
):

    mock_product = {
        "id": "1",
        "name": "Rice",
        "quantity": 20,
        "price": 60
    }

    stock_update_called = {
        "called": False
    }

    monkeypatch.setattr(
        "app.services.finance_service.inventory_service.find_product",
        lambda name: mock_product
    )

    def mock_update_stock(name, quantity):

        stock_update_called["called"] = True

        assert name == "Rice"
        assert quantity == -5

        return {
            "success": True
        }

    monkeypatch.setattr(
        "app.services.finance_service.inventory_service.update_stock",
        mock_update_stock
    )

    monkeypatch.setattr(
        "app.services.finance_service.firebase_service.add_document",
        lambda collection, data: "transaction-1"
    )

    result = finance_service.record_sale(
        product_name="Rice",
        quantity=5,
        price=60
    )

    assert result["success"] is True
    assert stock_update_called["called"] is True


def test_sale_product_not_found(
    finance_service,
    monkeypatch
):

    monkeypatch.setattr(
        "app.services.finance_service.inventory_service.find_product",
        lambda name: None
    )

    result = finance_service.record_sale(
        product_name="Unknown",
        quantity=5,
        price=60
    )

    assert result["success"] is False

    # Finance service Hindi/Hinglish message return karta hai
    assert "nahi mila" in result["message"].lower()


def test_sale_insufficient_stock(
    finance_service,
    monkeypatch
):

    mock_product = {
        "id": "1",
        "name": "Rice",
        "quantity": 2,
        "price": 60
    }

    monkeypatch.setattr(
        "app.services.finance_service.inventory_service.find_product",
        lambda name: mock_product
    )

    result = finance_service.record_sale(
        product_name="Rice",
        quantity=5,
        price=60
    )

    assert result["success"] is False
    assert "stock" in result["message"].lower()


def test_get_transactions(
    finance_service,
    monkeypatch
):

    mock_transactions = [
        {
            "id": "1",
            "type": "sale",
            "product": "Rice",
            "quantity": 5,
            "total": 300
        },
        {
            "id": "2",
            "type": "sale",
            "product": "Tea",
            "quantity": 2,
            "total": 240
        }
    ]

    # Firebase ko directly call karne ke bajay
    # service method ko mock kar rahe hain
    monkeypatch.setattr(
        finance_service,
        "get_transactions",
        lambda: mock_transactions
    )

    transactions = finance_service.get_transactions()

    assert len(transactions) == 2
    assert transactions[0]["product"] == "Rice"
    assert transactions[1]["product"] == "Tea"


def test_calculate_total_sales(
    finance_service,
    monkeypatch
):

    mock_transactions = [
        {
            "type": "sale",
            "total": 300
        },
        {
            "type": "sale",
            "total": 240
        },
        {
            "type": "purchase",
            "total": 100
        }
    ]

    monkeypatch.setattr(
        finance_service,
        "get_transactions",
        lambda: mock_transactions
    )

    total = finance_service.calculate_total_sales()

    assert total == 540


def test_sales_summary(
    finance_service,
    monkeypatch
):

    mock_transactions = [
        {
            "type": "sale",
            "quantity": 5,
            "total": 300
        },
        {
            "type": "sale",
            "quantity": 2,
            "total": 240
        }
    ]

    monkeypatch.setattr(
        finance_service,
        "get_transactions",
        lambda: mock_transactions
    )

    summary = finance_service.get_summary()

    assert summary["total_sales"] == 540
    assert summary["total_transactions"] == 2
    assert summary["items_sold"] == 7