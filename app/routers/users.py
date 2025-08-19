from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import user as models
from app.schemas import user as schemas
from app.auth.auth_handler import get_current_user

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me", response_model=schemas.UserBase)
def read_users_me(current_user: models.User = Depends(get_current_user)):
    return current_user

@router.put("/update-email")
def update_email(new_email: str, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    current_user.email = new_email
    db.commit()
    return {"message": "Email actualizado correctamente"}

@router.get("/metrics")
def get_metrics(current_user: models.User = Depends(get_current_user)):
    return {
        "total_tokens_used": current_user.total_tokens,
        "total_minutes_processed": current_user.total_minutes,
        "total_jobs": current_user.total_jobs
    }

@router.delete("/delete")
def delete_account(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db.delete(current_user)
    db.commit()
    return {"message": "Cuenta eliminada correctamente"}