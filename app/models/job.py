from pydantic import BaseModel
from typing import Optional, Dict

class Job(BaseModel):
    id: str
    status: str  # queued, processing, done, error
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    input_filename: Optional[str] = None
    language: Optional[str] = None
    flags: Optional[Dict[str, bool]] = {}  # subtítulos, mejora audio, etc.
    tokens_used: Optional[int] = 0
    progress: Optional[float] = 0.0  # Porcentaje del vídeo procesado
    total_time: Optional[float] = None  # Tiempo total del proceso en segundos
    error_message: Optional[str] = None