

from pydantic import BaseModel
from typing import Optional

class CreditBase(BaseModel):
    amount: int

class CreditCreate(CreditBase):
    pass

class CreditOut(CreditBase):
    id: int
    user_id: int

    model_config = {
        "from_attributes": True
    }

class CreditUsageRequest(BaseModel):
    operation: str
    estimated_credits: Optional[int] = None