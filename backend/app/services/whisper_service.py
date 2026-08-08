# backend/app/services/whisper_service.py

import os

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None


class WhisperService:

    def __init__(self):

        self.api_key = os.getenv("OPENAI_API_KEY")
        self.client = None

        if OpenAI and self.api_key:
            self.client = OpenAI(
                api_key=self.api_key
            )

    def transcribe(self, audio_file: str) -> str:

        if not self.client:
            return "Voice service configured nahi hai."

        try:

            with open(audio_file, "rb") as file:

                transcript = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=file
                )

            return transcript.text

        except Exception as e:

            print(f"Whisper error: {e}")

            return ""


whisper_service = WhisperService()