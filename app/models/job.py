from pydantic import BaseModel
from typing import Optional, Dict

class Job(BaseModel):
    id: str
    status: str
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    input_filename: Optional[str] = None
    language: Optional[str] = None
    flags: Optional[Dict[str, bool]] = {}