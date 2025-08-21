import whisper
import tempfile
import os
from fastapi import UploadFile, HTTPException

model = whisper.load_model("base")

async def detect_language_from_audio(file: UploadFile) -> str:
    temp_path = None
    try:
        suffix = os.path.splitext(file.filename)[-1] or ".mp4"
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
            contents = await file.read()
            temp_file.write(contents)
            temp_path = temp_file.name

        print(f"[LanguageDetection] Procesando archivo temporal: {temp_path}")

        result = model.transcribe(temp_path, task="transcribe", language=None)
        detected_lang = result.get("language") or "unknown"

        print(f"[LanguageDetection] Idioma detectado: {detected_lang}")
        return detected_lang

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al detectar idioma: {str(e)}")

    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)
            print(f"[LanguageDetection] Archivo temporal eliminado: {temp_path}")