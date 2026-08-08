# backend/app/services/gemini_service.py

import os
import json

try:
    from google import genai
except ImportError:
    genai = None


class GeminiService:

    def __init__(self):

        self.api_key = os.getenv("GEMINI_API_KEY")
        self.client = None

        if genai and self.api_key:
            self.client = genai.Client(
                api_key=self.api_key
            )

    def parse_command(self, text: str) -> dict:

        prompt = f"""
You are an AI agent for an Indian MSME business.

Convert the user's command into JSON.

Possible actions:

ADD_PRODUCT
UPDATE_STOCK
SELL_PRODUCT
GET_INVENTORY
GET_LOW_STOCK
GET_SALES
GET_REPORT

User command:
{text}

Return ONLY valid JSON.

Example:
{{
    "action": "SELL_PRODUCT",
    "product": "Rice",
    "quantity": 5,
    "price": 50
}}
"""

        if not self.client:
            return {
                "action": "UNKNOWN",
                "message": "Gemini API configured nahi hai."
            }

        try:

            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

            result = response.text.strip()

            return json.loads(result)

        except Exception as e:

            return {
                "action": "UNKNOWN",
                "error": str(e)
            }


gemini_service = GeminiService()