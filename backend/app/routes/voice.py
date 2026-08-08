from fastapi import APIRouter, UploadFile, File

router = APIRouter()


@router.post("/voice")
async def process_voice(audio: UploadFile = File(...)):
    return {
        "status": "received",
        "filename": audio.filename,
        "message": "Voice input received successfully"
    }