from app.services.command_service import RuleCommandParser


def test_parse_english_add_product():
    result = RuleCommandParser().parse(
        "Add 20 Dettol Soap, buying price 18, selling price 22"
    )

    assert result["action"] == "ADD_PRODUCT"
    assert result["product"] == "Dettol Soap"
    assert result["quantity"] == 20
    assert result["purchase_price"] == 18
    assert result["selling_price"] == 22


def test_parse_marathi_sale():
    result = RuleCommandParser().parse("डेटॉल साबणाचे तीन नग विकले")

    assert result == {
        "action": "SELL_PRODUCT",
        "product": "Dettol Soap",
        "quantity": 3,
    }


def test_parse_marathi_stock_add():
    result = RuleCommandParser().parse(
        "डेटॉल साबणाचे वीस नग स्टॉकमध्ये जोडा"
    )

    assert result["action"] == "ADD_PRODUCT"
    assert result["product"] == "Dettol Soap"
    assert result["quantity"] == 20


def test_parse_daily_report():
    result = RuleCommandParser().parse("आजची विक्री आणि नफा सांगा")
    assert result["action"] == "GET_REPORT"
