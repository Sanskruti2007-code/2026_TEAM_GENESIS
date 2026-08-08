# backend/app/utils/marathi_response.py


def success_response(
    message: str,
    data=None
) -> dict:

    return {
        "success": True,
        "language": "mr",
        "message": message,
        "data": data
    }


def error_response(
    message: str
) -> dict:

    return {
        "success": False,
        "language": "mr",
        "message": message
    }


def product_added_response(
    product: str,
    quantity: int
) -> str:

    return (
        f"{product} चे {quantity} युनिट्स "
        f"स्टॉकमध्ये यशस्वीरित्या जोडले आहेत."
    )


def stock_updated_response(
    product: str,
    quantity: int
) -> str:

    if quantity > 0:
        return (
            f"{product} चा स्टॉक "
            f"{quantity} युनिट्सने वाढवला आहे."
        )

    return (
        f"{product} चा स्टॉक "
        f"{abs(quantity)} युनिट्सने कमी केला आहे."
    )


def sale_recorded_response(
    product: str,
    quantity: int,
    total: float
) -> str:

    return (
        f"{product} चे {quantity} युनिट्स विकले गेले. "
        f"एकूण विक्री ₹{total} आहे."
    )


def low_stock_response(
    products: list
) -> str:

    if not products:
        return "सध्या कोणताही उत्पादन कमी स्टॉकमध्ये नाही."

    names = [
        product.get("name", "Unknown")
        for product in products
    ]

    return (
        "कमी स्टॉक असलेली उत्पादने: "
        + ", ".join(names)
    )


def sales_summary_response(
    total_sales: float,
    transactions: int,
    items_sold: int
) -> str:

    return (
        f"आजची एकूण विक्री ₹{total_sales} आहे. "
        f"{transactions} व्यवहार झाले आहेत आणि "
        f"{items_sold} वस्तू विकल्या गेल्या आहेत."
    )


def inventory_summary_response(
    total_products: int,
    total_items: int,
    low_stock_count: int
) -> str:

    return (
        f"एकूण {total_products} उत्पादने आहेत. "
        f"स्टॉकमध्ये {total_items} वस्तू आहेत. "
        f"{low_stock_count} उत्पादने कमी स्टॉकमध्ये आहेत."
    )


def unknown_command_response() -> str:

    return (
        "माफ करा, तुमची विनंती मला समजली नाही. "
        "कृपया पुन्हा सांगा."
    )