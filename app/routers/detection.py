from fastapi import APIRouter, UploadFile, File
from app.services.language_detection import detect_language_from_audio

router = APIRouter()

@router.post("/detect-language")
async def detect_language(file: UploadFile = File(...)):
    language = await detect_language_from_audio(file)
    return {"detected_language": language}
