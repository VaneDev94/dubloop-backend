from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from app.services.stripe_service import create_checkout_session
from app.auth.auth_handler import get_current_user
from app.models.user import User

router = APIRouter(prefix="/stripe", tags=["Stripe"])

@router.post("/create-checkout-session")
async def create_checkout_session_endpoint(
    amount: int,
    current_user: User = Depends(get_current_user)
):
    if not current_user.is_verified:
        raise HTTPException(status_code=403, detail="Email not verified.")
    try:
        session_url = create_checkout_session(amount, current_user)
        return JSONResponse(content={"url": session_url})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
