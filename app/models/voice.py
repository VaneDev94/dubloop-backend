from pydantic import BaseModel
from typing import Optional

class VoiceProfile(BaseModel):
    user_id: str
    voice_id: str
    name: Optional[str] = None