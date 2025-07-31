from pydantic import BaseModel
from typing import List, Dict

class SubtitleLine(BaseModel):
    start: float
    end: float
    text: str

class Subtitle(BaseModel):
    job_id: str
    lines: List[SubtitleLine]

def generate_subtitles(transcript: str, timestamps: List[dict]) -> Subtitle:
    lines = [
        SubtitleLine(
            start=segment["start"],
            end=segment["end"],
            text=segment["text"].strip()
        )
        for segment in timestamps
    ]
    return Subtitle(job_id="", lines=lines)