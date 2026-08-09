import json
import re

from app.config import settings
from app.services.api_key_store import api_key_store

try:
    from google import genai
    from google.genai import types
except ImportError:
    genai = None
    types = None


class GeminiService:
    def _get_api_key(self) -> str:
        """
        First use the key entered through the app.
        If unavailable, fall back to backend/.env.
        """
        return api_key_store.get_key("gemini") or settings.GEMINI_API_KEY

    def _get_client(self):
        api_key = self._get_api_key()

        if not genai or not api_key:
            return None

        return genai.Client(api_key=api_key)

    @property
    def enabled(self) -> bool:
        return self._get_client() is not None

    @staticmethod
    def _json_from_text(text: str) -> dict:
        cleaned = re.sub(
            r"^```(?:json)?\s*|\s*```$",
            "",
            text.strip(),
        )
        return json.loads(cleaned)

    def parse_command(self, text: str) -> dict:
        client = self._get_client()

        if not client:
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

            response = client.models.generate_content(
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

        except Exception as error:
            print(
                f"[GEMINI PARSE ERROR] {type(error).__name__}: {error}",
                flush=True,
            )
            return {}

    def transcribe_audio(
        self,
        audio_bytes: bytes,
        mime_type: str,
    ) -> str:
        client = self._get_client()

        if not client or not types:
            return ""

        prompt = (
            "Transcribe this shopkeeper voice command exactly. "
            "The language may be Marathi, Hindi, Hinglish, or English. "
            "Return only the transcript, without quotation marks or explanation."
        )

        try:
            audio_part = types.Part.from_bytes(
                data=audio_bytes,
                mime_type=mime_type or "audio/webm",
            )

            response = client.models.generate_content(
                model=settings.GEMINI_MODEL,
                contents=[prompt, audio_part],
                config=types.GenerateContentConfig(temperature=0),
            )

            return (response.text or "").strip()

        except Exception as error:
            print(
                f"[GEMINI AUDIO ERROR] {type(error).__name__}: {error}",
                flush=True,
            )
            return ""


gemini_service = GeminiService()