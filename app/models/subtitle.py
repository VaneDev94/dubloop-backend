from pydantic import BaseModel
from typing import List, Dict

class SubtitleLine(BaseModel):
    start: float
    end: float
    text: str

class Subtitle(BaseModel):
    job_id: str
    lines: List[SubtitleLine]

def generate_subtitles(job_id: str, transcript: str, timestamps: List[dict]) -> Subtitle:
    lines = [
        SubtitleLine(
            start=segment["start"],
            end=segment["end"],
            text=segment["text"].strip()
        )
        for segment in timestamps
    ]
    return Subtitle(job_id=job_id, lines=lines)


# Export subtitles to .srt format
def to_srt(subtitles: Subtitle) -> str:
    def format_timestamp(seconds: float) -> str:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int((seconds - int(seconds)) * 1000)
        return f"{hours:02}:{minutes:02}:{secs:02},{millis:03}"

    srt_lines = []
    for i, line in enumerate(subtitles.lines, start=1):
        srt_lines.append(str(i))
        srt_lines.append(f"{format_timestamp(line.start)} --> {format_timestamp(line.end)}")
        srt_lines.append(line.text)
        srt_lines.append("")  # línea vacía entre subtítulos

    return "\n".join(srt_lines)