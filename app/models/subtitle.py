from pydantic import BaseModel
from typing import List

class SubtitleLine(BaseModel):
    start: float
    end: float
    text: str

class Subtitle(BaseModel):
    job_id: str
    lines: List[SubtitleLine]