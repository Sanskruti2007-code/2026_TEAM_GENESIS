# backend/app/utils/product_normalizer.py

import re


PRODUCT_ALIASES = {
    # Rice
    "तांदूळ": "Rice",
    "तांदुळ": "Rice",
    "चावल": "Rice",
    "चांवल": "Rice",
    "rice": "Rice",

    # Wheat
    "गहू": "Wheat",
    "गेहूं": "Wheat",
    "wheat": "Wheat",

    # Sugar
    "साखर": "Sugar",
    "चीनी": "Sugar",
    "sugar": "Sugar",

    # Tea
    "चहा": "Tea",
    "चाय": "Tea",
    "tea": "Tea",

    # Milk
    "दूध": "Milk",
    "दुध": "Milk",
    "milk": "Milk",

    # Oil
    "तेल": "Oil",
    "खाने का तेल": "Cooking Oil",
    "cooking oil": "Cooking Oil",
    "oil": "Oil",

    # Biscuits
    "बिस्कीट": "Biscuits",
    "बिस्किट": "Biscuits",
    "बिस्कुट": "Biscuits",
    "बिस्किट्स": "Biscuits",
    "biscuits": "Biscuits",
    "biscuit": "Biscuits",

    # Salt
    "मीठ": "Salt",
    "नमक": "Salt",
    "salt": "Salt",

    # Soap
    "साबण": "Soap",
    "साबुन": "Soap",
    "soap": "Soap",

    # Water
    "पाणी": "Water",
    "पानी": "Water",
    "water": "Water"
}


def normalize_product_name(product_name: str) -> str:
    """
    Convert Marathi/Hindi/English product name
    into a standard product name.
    """

    if not product_name:
        return ""

    product_name = product_name.strip()

    # Direct alias match
    if product_name.lower() in PRODUCT_ALIASES:
        return PRODUCT_ALIASES[product_name.lower()]

    if product_name in PRODUCT_ALIASES:
        return PRODUCT_ALIASES[product_name]

    # Case-insensitive search
    for alias, standard_name in PRODUCT_ALIASES.items():

        if alias.lower() == product_name.lower():
            return standard_name

    # Remove unnecessary spaces
    product_name = re.sub(r"\s+", " ", product_name)

    # If unknown, preserve original name
    return product_name.title()