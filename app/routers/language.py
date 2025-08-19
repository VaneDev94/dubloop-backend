from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.language_detection import detect_language_from_audio as detect_language

router = APIRouter(prefix="/language", tags=["Language Detection"])

@router.post("/detect")
async def detect_language_endpoint(file: UploadFile = File(...)):
    """
    Detecta automáticamente el idioma de un archivo de audio o vídeo usando Whisper.
    """
    try:
        language = await detect_language(file)
        return {"language": language}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al detectar el idioma")