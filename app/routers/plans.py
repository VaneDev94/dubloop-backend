from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.plans import Plan
from app.schemas.plans import PlanCreate, PlanResponse

router = APIRouter(prefix="/plans", tags=["Plans"])

@router.get("/", response_model=list[PlanResponse])
def list_plans(db: Session = Depends(get_db)):
    return db.query(Plan).all()

@router.post("/", response_model=PlanResponse)
def create_plan(payload: PlanCreate, db: Session = Depends(get_db)):
    plan = Plan(**payload.dict())
    db.add(plan)
    db.commit()
    db.refresh(plan)
    return plan


# GET /plans/{plan_id}
@router.get("/{plan_id}", response_model=PlanResponse)
def get_plan(plan_id: int, db: Session = Depends(get_db)):
    plan = db.query(Plan).filter(Plan.id == plan_id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    return plan

# PUT /plans/{plan_id}
@router.put("/{plan_id}", response_model=PlanResponse)
def update_plan(plan_id: int, payload: PlanCreate, db: Session = Depends(get_db)):
    plan = db.query(Plan).filter(Plan.id == plan_id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    for key, value in payload.dict().items():
        setattr(plan, key, value)
    db.commit()
    db.refresh(plan)
    return plan

# DELETE /plans/{plan_id}
@router.delete("/{plan_id}", response_model=PlanResponse)
def delete_plan(plan_id: int, db: Session = Depends(get_db)):
    plan = db.query(Plan).filter(Plan.id == plan_id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    db.delete(plan)
    db.commit()
    return plan