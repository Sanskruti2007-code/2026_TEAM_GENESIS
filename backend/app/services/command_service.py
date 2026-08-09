import re
from typing import Optional

from app.services.finance_service import finance_service
from app.services.gemini_service import gemini_service
from app.services.inventory_service import inventory_service
from app.services.report_service import report_service
from app.utlis.product_normalizer import normalize_product_name


NUMBER_WORDS = {
    "one": "1", "two": "2", "three": "3", "four": "4", "five": "5",
    "six": "6", "seven": "7", "eight": "8", "nine": "9", "ten": "10",
    "eleven": "11", "twelve": "12", "thirteen": "13", "fourteen": "14",
    "fifteen": "15", "sixteen": "16", "seventeen": "17", "eighteen": "18",
    "nineteen": "19", "twenty": "20",
    "एक": "1", "दोन": "2", "तीन": "3", "चार": "4", "पाच": "5",
    "सहा": "6", "सात": "7", "आठ": "8", "नऊ": "9", "दहा": "10",
    "अकरा": "11", "बारा": "12", "तेरा": "13", "चौदा": "14",
    "पंधरा": "15", "सोळा": "16", "सतरा": "17", "अठरा": "18",
    "एकोणीस": "19", "वीस": "20",
    "दो": "2", "चार": "4", "पांच": "5", "छह": "6", "सात": "7",
    "आठ": "8", "नौ": "9", "दस": "10", "बीस": "20",
}

ADD_WORDS = r"add|restock|जोडा|जोड़ो|वाढवा|डालो"
SELL_WORDS = r"sell|sold|sale|विका|विकले|बेचा|बेचो|बिके"
PRICE_START = (
    r"buying\s+price|purchase\s+price|cost\s+price|खरेदी\s+किंमत|खरीद\s+कीमत|"
    r"selling\s+price|sale\s+price|विक्री\s+किंमत|बेचने\s+कीमत|reorder|supplier|category"
)


def replace_number_words(text: str) -> str:
    result = text
    for word, number in sorted(NUMBER_WORDS.items(), key=lambda item: -len(item[0])):
        result = re.sub(rf"(?<!\w){re.escape(word)}(?!\w)", number, result, flags=re.I)
    return result


def number_after(text: str, labels: str) -> Optional[float]:
    match = re.search(
        rf"(?:{labels})\s*(?:is|है|आहे|=|:)?\s*(?:₹|rs\.?|रुपये?)?\s*(\d+(?:\.\d+)?)",
        text,
        flags=re.I,
    )
    return float(match.group(1)) if match else None


def clean_product(value: str) -> str:
    value = re.sub(r"[,.;:]", " ", value)
    value = re.sub(r"\b(?:units?|pieces?|pcs?|नग|युनिट्स?|पीस)\b", " ", value, flags=re.I)
    value = re.sub(r"साबणाचे$", "साबण", value.strip())
    value = re.sub(r"\s+(?:के|का|की)$", "", value.strip())
    value = re.sub(r"(?:चे|चा|ची|च्या)$", "", value.strip())
    value = re.sub(r"\s+", " ", value).strip(" -")
    return normalize_product_name(value)


class RuleCommandParser:
    def parse(self, raw_text: str) -> dict:
        text = replace_number_words(raw_text.strip())
        lower = text.casefold()

        if re.search(r"low\s*stock|कमी\s*स्टॉक|कम\s*स्टॉक|stock.*(?:empty|खाली)", lower):
            return {"action": "GET_LOW_STOCK"}
        if re.search(r"today|आज|profit|नफा|sales?\s*(?:summary|report)|विक्री.*(?:सांगा|बताओ)", lower):
            return {"action": "GET_REPORT"}
        if re.search(r"inventory|सगळा\s*स्टॉक|पूरा\s*स्टॉक|stock\s*(?:list|दिखाओ|दाखवा)", lower):
            return {"action": "GET_INVENTORY"}

        if re.search(
            rf"(?:^|\s)(?:{SELL_WORDS})(?=[\s,.;:]|$)", lower
        ):
            parsed = self._parse_product_quantity(text, SELL_WORDS, is_add=False)
            return {"action": "SELL_PRODUCT", **parsed}

        if re.search(
            rf"(?:^|\s)(?:{ADD_WORDS})(?=[\s,.;:]|$)", lower
        ) or re.search(
            r"stock\s*(?:mein|me|मध्ये).*\d|\d.*stock\s*(?:mein|me|मध्ये)", lower
        ):
            parsed = self._parse_product_quantity(text, ADD_WORDS, is_add=True)
            parsed["purchase_price"] = number_after(
                text, r"buying\s+price|purchase\s+price|cost\s+price|खरेदी\s+किंमत|खरीद\s+कीमत"
            )
            parsed["selling_price"] = number_after(
                text, r"selling\s+price|sale\s+price|विक्री\s+किंमत|बेचने\s+कीमत"
            )
            reorder = number_after(text, r"reorder(?:\s+level)?")
            if reorder is not None:
                parsed["reorder_level"] = int(reorder)
            return {"action": "ADD_PRODUCT", **parsed}

        return {"action": "UNKNOWN"}

    def _parse_product_quantity(self, text: str, verbs: str, is_add: bool) -> dict:
        patterns = [
            (
                "quantity-first",
                rf"(?:{verbs})\s+(\d+)\s+(.+?)(?=\s+(?:{PRICE_START})|$)",
            ),
            (
                "product-first",
                rf"(.+?)\s+(\d+)\s*(?:units?|pieces?|pcs?|नग|युनिट्स?|पीस)?"
                rf"(?:\s+(?:stock\s*(?:mein|me)|स्टॉकमध्ये))?\s+(?:{verbs})(?:\s|$)",
            ),
            (
                "quantity-first",
                rf"(\d+)\s+(.+?)\s+(?:{verbs})(?:\s|$)",
            ),
        ]

        for mode, pattern in patterns:
            match = re.search(pattern, text, flags=re.I)
            if not match:
                continue
            if mode == "quantity-first":
                quantity, product = match.group(1), match.group(2)
            else:
                product, quantity = match.group(1), match.group(2)

            if is_add:
                product = re.sub(
                    r"\s+(?:stock\s*(?:mein|me|मध्ये)|स्टॉकमध्ये).*$",
                    "",
                    product,
                    flags=re.I,
                )
            return {"product": clean_product(product), "quantity": int(quantity)}

        numbers = re.findall(r"\d+", text)
        return {"quantity": int(numbers[0]) if numbers else None, "product": ""}


class CommandService:
    def __init__(self):
        self.rule_parser = RuleCommandParser()

    def parse(self, text: str) -> tuple[dict, str]:
        ai_result = gemini_service.parse_command(text)
        if ai_result and ai_result.get("action") not in (None, "UNKNOWN"):
            return ai_result, "gemini"
        return self.rule_parser.parse(text), "rules"

    def execute(self, text: str, language: str = "mr-IN") -> dict:
        command, source = self.parse(text)
        action = command.get("action", "UNKNOWN")
        base = {
            "success": True,
            "action": action,
            "transcript": text,
            "source": source,
        }

        if action == "ADD_PRODUCT":
            product_name = clean_product(str(command.get("product") or ""))
            quantity = int(command.get("quantity") or 0)
            if not product_name or quantity <= 0:
                return {
                    **base,
                    "success": False,
                    "message": "Product name aur valid quantity dobara boliye.",
                }

            existing = inventory_service.find_product(product_name)
            if existing:
                result = inventory_service.update_stock(product_name, quantity)
                if command.get("purchase_price") is not None or command.get("selling_price") is not None:
                    inventory_service.update_product(
                        existing["id"],
                        {
                            key: value
                            for key, value in {
                                "purchasePrice": command.get("purchase_price"),
                                "sellingPrice": command.get("selling_price"),
                            }.items()
                            if value is not None
                        },
                    )
                return {
                    **base,
                    "message": f"{product_name} चे {quantity} नग स्टॉकमध्ये जोडले.",
                    "data": result,
                }

            purchase_price = command.get("purchase_price")
            selling_price = command.get("selling_price")
            if purchase_price is None or selling_price is None:
                return {
                    **base,
                    "success": False,
                    "message": (
                        f"{product_name} नवीन product आहे. Buying price आणि "
                        "selling price दोन्ही सांगा."
                    ),
                    "data": {"needs": ["purchase_price", "selling_price"]},
                }

            product = inventory_service.add_product(
                name=product_name,
                quantity=quantity,
                purchase_price=float(purchase_price),
                selling_price=float(selling_price),
                category=str(command.get("category") or "General"),
                supplier=str(command.get("supplier") or "Local Supplier"),
                reorder_level=int(command.get("reorder_level") or 5),
            )
            return {
                **base,
                "message": f"{product_name} चे {quantity} नग नवीन स्टॉकमध्ये जोडले.",
                "data": {"product": product},
            }

        if action == "SELL_PRODUCT":
            product_name = clean_product(str(command.get("product") or ""))
            quantity = int(command.get("quantity") or 0)
            if not product_name or quantity <= 0:
                return {
                    **base,
                    "success": False,
                    "message": "कोणता product आणि किती quantity विकली ते पुन्हा सांगा.",
                }
            result = finance_service.record_sale(
                product_name=product_name,
                quantity=quantity,
                price=command.get("price") or command.get("selling_price"),
            )
            if not result["success"]:
                return {**base, **result}
            order = result["transaction"]
            return {
                **base,
                "message": (
                    f"{product_name} चे {quantity} नग विकले. "
                    f"विक्री ₹{order['totalAmount']:.2f} आणि नफा "
                    f"₹{order['profit']:.2f} नोंदवला."
                ),
                "data": {"transaction": order},
            }

        if action == "GET_INVENTORY":
            products = inventory_service.get_products()
            total_units = sum(int(product.get("quantity", 0)) for product in products)
            return {
                **base,
                "message": f"एकूण {len(products)} products आणि {total_units} units स्टॉकमध्ये आहेत.",
                "data": {"products": products, "total_units": total_units},
            }

        if action == "GET_LOW_STOCK":
            products = inventory_service.get_low_stock_products()
            names = ", ".join(product["name"] for product in products)
            message = (
                f"कमी स्टॉक products: {names}."
                if products
                else "सध्या कोणताही product कमी स्टॉकमध्ये नाही."
            )
            return {**base, "message": message, "data": {"products": products}}

        if action == "GET_REPORT":
            return {
                **base,
                "message": report_service.generate_voice_summary(),
                "data": report_service.generate_dashboard_report(),
            }

        return {
            **base,
            "success": False,
            "message": (
                "Command समजला नाही. उदाहरण: ‘Sell 3 Dettol Soap’ किंवा "
                "‘आजची विक्री आणि नफा सांगा’."
            ),
        }


command_service = CommandService()
