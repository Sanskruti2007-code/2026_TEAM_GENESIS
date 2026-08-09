from fastapi import APIRouter, File, HTTPException, UploadFile

from app.config import settings
from app.models.command import CommandRequest, CommandResponse
from app.services.command_service import command_service
from app.services.gemini_service import gemini_service
from app.services.whisper_service import whisper_service

router = APIRouter(tags=["voice"])


@router.post("/commands", response_model=CommandResponse)
def process_text_command(command: CommandRequest):
    return command_service.execute(command.text, command.language)


@router.post("/voice/process", response_model=CommandResponse)
async def process_voice(audio: UploadFile = File(...), language: str = "mr-IN"):
    content_type = audio.content_type or "audio/webm"
    if not content_type.startswith("audio/"):
        raise HTTPException(status_code=415, detail="Please upload an audio file.")

    audio_bytes = await audio.read(settings.MAX_AUDIO_BYTES + 1)
    if not audio_bytes:
        raise HTTPException(status_code=400, detail="Recorded audio is empty.")
    if len(audio_bytes) > settings.MAX_AUDIO_BYTES:
        raise HTTPException(status_code=413, detail="Audio must be smaller than 10 MB.")

    transcript = whisper_service.transcribe_bytes(
        audio_bytes, audio.filename or "voice-command.webm"
    )
    if not transcript:
        transcript = gemini_service.transcribe_audio(audio_bytes, content_type)

    if not transcript:
        raise HTTPException(
            status_code=503,
            detail=(
                "Voice transcription is not configured. Add GEMINI_API_KEY or "
                "OPENAI_API_KEY in backend/.env. Typed commands still work."
            ),
        )

    return command_service.execute(transcript, language)
