

from fastapi import APIRouter, Depends, HTTPException
from app.schemas.credits import CreditResponse, AddCreditsRequest
from app.services.credits import check_and_consume_credits, add_credits_to_user
from app.auth.dependencies import require_verified_email
from sqlalchemy.orm import Session
from app.database import get_db

router = APIRouter(prefix="/credits", tags=["Credits"])

@router.get("/check", response_model=CreditResponse)
def check_credits(
    user=Depends(require_verified_email),
    db: Session = Depends(get_db)
):
    return {"credits": user.credits}

@router.post("/add", response_model=CreditResponse)
def add_credits(
    payload: AddCreditsRequest,
    user=Depends(require_verified_email),
    db: Session = Depends(get_db)
):
    updated_credits = add_credits_to_user(db, user.id, payload.amount)
    return {"credits": updated_credits}