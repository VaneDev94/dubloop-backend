from pydantic import BaseModel

class PlanBase(BaseModel):
    name: str
    description: str | None = None
    price: float
    duration_days: int | None = None

class PlanCreate(PlanBase):
    pass

class PlanResponse(PlanBase):
    id: int

    class Config:
        from_attributes = True