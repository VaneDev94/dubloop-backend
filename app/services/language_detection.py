import whisper
import tempfile
import os
from fastapi import UploadFile, HTTPException

model = whisper.load_model("base")

async def detect_language_from_audio(file: UploadFile) -> str:
    try:
        suffix = os.path.splitext(file.filename)[-1] or ".mp4"
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
            contents = await file.read()
            temp_file.write(contents)
            temp_path = temp_file.name

        result = model.transcribe(temp_path, task="transcribe", language=None)
        return result.get("language")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al detectar idioma: {str(e)}")

    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)