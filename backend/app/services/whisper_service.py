import io
import os

from app.services.api_key_store import api_key_store

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None


class WhisperService:
    def _get_api_key(self) -> str:
        """
        App mein entered session key ko priority milegi.
        Agar session key nahi hai, toh .env key use hogi.
        """
        session_key = api_key_store.get_key("openai")

        if session_key:
            return session_key

        return os.getenv("OPENAI_API_KEY", "").strip()

    def _get_client(self):
        api_key = self._get_api_key()

        if OpenAI is None or not api_key:
            return None

        return OpenAI(api_key=api_key)

    @property
    def enabled(self) -> bool:
        return self._get_client() is not None

    @staticmethod
    def _prepare_filename(filename: str) -> str:
        safe_filename = os.path.basename(
            filename or "voice-command.webm"
        )

        if "." not in safe_filename:
            safe_filename += ".webm"

        return safe_filename

    def transcribe_bytes(
        self,
        audio_bytes: bytes,
        filename: str = "voice-command.webm",
    ) -> str:
        """
        Browser se received audio bytes ko OpenAI se transcribe karta hai.
        Temporary audio file create nahi hoti.
        """
        client = self._get_client()

        if not client or not audio_bytes:
            return ""

        model = os.getenv(
            "OPENAI_TRANSCRIPTION_MODEL",
            "gpt-transcribe",
        )

        audio_file = io.BytesIO(audio_bytes)
        audio_file.name = self._prepare_filename(filename)

        try:
            transcript = client.audio.transcriptions.create(
                model=model,
                file=audio_file,
                prompt=(
                    "This is a VyaparSaathi shop-management command. "
                    "Speech may contain Marathi, Hindi, Hinglish, or English. "
                    "Preserve product names, quantities, and prices accurately."
                ),
            )

            return (transcript.text or "").strip()

        except Exception as error:
            print(
                "OpenAI transcription error:",
                type(error).__name__,
            )
            return ""


whisper_service = WhisperService()