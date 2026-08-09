import json
import re
from typing import Optional

from app.config import settings

try:
    from google import genai
    from google.genai import types
except ImportError:  # The rule parser still works without google-genai.
    genai = None
    types = None


class GeminiService:
    def __init__(self):
        self.client = (
            genai.Client(api_key=settings.GEMINI_API_KEY)
            if genai and settings.GEMINI_API_KEY
            else None
        )

    @property
    def enabled(self) -> bool:
        return self.client is not None

    @staticmethod
    def _json_from_text(text: str) -> dict:
        cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", text.strip())
        return json.loads(cleaned)

    def parse_command(self, text: str) -> dict:
        if not self.client:
            return {}

        prompt = f"""
You are the command parser for VyaparSaathi, an Indian shop management app.
The user may speak Marathi, Hindi, Hinglish, or English. Return ONLY JSON.

Allowed actions:
ADD_PRODUCT, SELL_PRODUCT, GET_INVENTORY, GET_LOW_STOCK, GET_REPORT, UNKNOWN

Return this shape, omitting unknown optional values:
{{
  "action": "ADD_PRODUCT",
  "product": "Dettol Soap",
  "quantity": 20,
  "purchase_price": 18,
  "selling_price": 22,
  "category": "Personal Care",
  "supplier": "Local Supplier",
  "reorder_level": 5
}}

Rules:
- ADD_PRODUCT also covers adding/restocking inventory.
- SELL_PRODUCT means a completed sale and must reduce stock.
- Keep brand/product names readable; translate common nouns to English when useful.
- Never invent quantity or prices.
- For a daily sales/profit/summary question use GET_REPORT.

User command: {text}
"""

        try:
            config = (
                types.GenerateContentConfig(
                    temperature=0,
                    response_mime_type="application/json",
                )
                if types
                else None
            )
            response = self.client.models.generate_content(
                model=settings.GEMINI_MODEL,
                contents=prompt,
                config=config,
            )
            parsed = self._json_from_text(response.text or "{}")
            if parsed.get("action") not in {
                "ADD_PRODUCT",
                "SELL_PRODUCT",
                "GET_INVENTORY",
                "GET_LOW_STOCK",
                "GET_REPORT",
                "UNKNOWN",
            }:
                return {}
            return parsed
        except Exception:
            return {}

    def transcribe_audio(self, audio_bytes: bytes, mime_type: str) -> str:
        if not self.client or not types:
            return ""

        prompt = (
            "Transcribe this shopkeeper voice command exactly. The language may "
            "be Marathi, Hindi, Hinglish, or English. Return only the transcript, "
            "without quotation marks or explanation."
        )
        try:
            audio_part = types.Part.from_bytes(
                data=audio_bytes,
                mime_type=mime_type or "audio/webm",
            )
            response = self.client.models.generate_content(
                model=settings.GEMINI_MODEL,
                contents=[prompt, audio_part],
                config=types.GenerateContentConfig(temperature=0),
            )
            return (response.text or "").strip()
        except Exception:
            return ""


gemini_service = GeminiService()
