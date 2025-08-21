from pydantic import BaseModel
from typing import Optional, List

class StartDubbingRequest(BaseModel):
    target_language: str
    voice_cloning: bool = True
    enable_lip_sync: bool = False
    enable_subtitles: bool = False
    enable_audio_enhancement: bool = False

class JobResponse(BaseModel):
    job_id: str
    status: str

class JobStatus(BaseModel):
    job_id: str
    status: str
    progress: float
    error: Optional[str] = None
    result_url: Optional[str] = None

class MetricsResponse(BaseModel):
    job_id: str
    processing_time: float
    tokens_used: int
    steps: List[str]

class SubtitlesResponse(BaseModel):
    job_id: str
    format: str
    content: str
