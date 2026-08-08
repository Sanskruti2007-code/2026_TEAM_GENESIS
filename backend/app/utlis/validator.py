# backend/app/utils/validators.py


def validate_product_name(product_name: str) -> bool:

    if not product_name:
        return False

    if not isinstance(product_name, str):
        return False

    if len(product_name.strip()) == 0:
        return False

    return True


def validate_quantity(quantity) -> bool:

    if quantity is None:
        return False

    try:
        quantity = int(quantity)
    except (ValueError, TypeError):
        return False

    return quantity > 0


def validate_price(price) -> bool:

    if price is None:
        return False

    try:
        price = float(price)
    except (ValueError, TypeError):
        return False

    return price >= 0


def validate_category(category: str) -> bool:

    if category is None:
        return True

    if not isinstance(category, str):
        return False

    return len(category.strip()) > 0


def validate_add_product(data: dict) -> dict:

    errors = []

    if not validate_product_name(
        data.get("product")
    ):
        errors.append(
            "Product name required hai."
        )

    if not validate_quantity(
        data.get("quantity")
    ):
        errors.append(
            "Valid quantity required hai."
        )

    if not validate_price(
        data.get("price")
    ):
        errors.append(
            "Valid price required hai."
        )

    return {
        "valid": len(errors) == 0,
        "errors": errors
    }


def validate_sale(data: dict) -> dict:

    errors = []

    if not validate_product_name(
        data.get("product")
    ):
        errors.append(
            "Product name required hai."
        )

    if not validate_quantity(
        data.get("quantity")
    ):
        errors.append(
            "Valid quantity required hai."
        )

    if data.get("price") is not None:

        if not validate_price(
            data.get("price")
        ):
            errors.append(
                "Invalid price hai."
            )

    return {
        "valid": len(errors) == 0,
        "errors": errors
    }


def validate_stock_update(data: dict) -> dict:

    errors = []

    if not validate_product_name(
        data.get("product")
    ):
        errors.append(
            "Product name required hai."
        )

    quantity = data.get("quantity")

    if quantity is None:
        errors.append(
            "Quantity required hai."
        )
    else:
        try:
            int(quantity)
        except (ValueError, TypeError):
            errors.append(
                "Quantity valid number honi chahiye."
            )

    return {
        "valid": len(errors) == 0,
        "errors": errors
    }