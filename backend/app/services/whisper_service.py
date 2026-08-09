import io

from app.config import settings

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None


class WhisperService:
    def __init__(self):
        self.client = (
            OpenAI(api_key=settings.OPENAI_API_KEY)
            if OpenAI and settings.OPENAI_API_KEY
            else None
        )

    @property
    def enabled(self) -> bool:
        return self.client is not None

    def transcribe_bytes(self, audio_bytes: bytes, filename: str) -> str:
        if not self.client:
            return ""

        try:
            audio_file = io.BytesIO(audio_bytes)
            audio_file.name = filename or "voice-command.webm"
            transcript = self.client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
            )
            return (transcript.text or "").strip()
        except Exception:
            return ""


whisper_service = WhisperService()
