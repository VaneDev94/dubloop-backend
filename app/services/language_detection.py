import whisper
import tempfile
from fastapi import HTTPException

model = whisper.load_model("base")

async def detect_language(file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
        contents = await file.read()
        temp_file.write(contents)
        temp_path = temp_file.name

    try:
        result = model.transcribe(temp_path, task="transcribe", language=None)
        return result.get("language")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al detectar idioma: {str(e)}")