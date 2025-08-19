from fastapi import APIRouter, Depends, HTTPException, status
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Subscription, User
from app.auth.dependencies import get_current_user

subscription_router = APIRouter(prefix="/subscriptions", tags=["subscriptions"])


@subscription_router.post("/subscribe")
def subscribe(plan_name: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    now = datetime.utcnow()
    active_subscription = (
        db.query(Subscription)
        .filter(
            Subscription.user_id == current_user.id,
            Subscription.start_date <= now,
            Subscription.end_date >= now,
        )
        .first()
    )
    if active_subscription:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already has an active subscription.",
        )
    new_subscription = Subscription(
        user_id=current_user.id,
        plan_name=plan_name,
        start_date=now,
        end_date=now + timedelta(days=30),
    )
    db.add(new_subscription)
    db.commit()
    db.refresh(new_subscription)
    return {"message": "Subscription created successfully", "subscription": new_subscription}


@subscription_router.get("/my-subscription")
def get_my_subscription(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    now = datetime.utcnow()
    subscription = (
        db.query(Subscription)
        .filter(
            Subscription.user_id == current_user.id,
            Subscription.start_date <= now,
            Subscription.end_date >= now,
        )
        .first()
    )
    if not subscription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No active subscription found.",
        )
    return subscription


@subscription_router.post("/cancel")
def cancel_subscription(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Note: In Dubloop, plans auto-cancel after one month and cannot be canceled manually.
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Subscription cancellation is not supported. Plans auto-cancel after one month.",
    )
