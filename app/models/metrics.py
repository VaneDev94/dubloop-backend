from pydantic import BaseModel
from typing import Optional

class JobMetrics(BaseModel):
    job_id: str
    total_tokens: Optional[int] = None
    total_time: Optional[float] = None
    progress_percent: Optional[float] = None