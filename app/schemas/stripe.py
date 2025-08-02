from pydantic import BaseModel
from typing import Optional

class PaymentIntentRequest(BaseModel):
    amount: int  # in cents
    currency: str = "eur"
    description: Optional[str] = None

class PaymentIntentResponse(BaseModel):
    client_secret: str
