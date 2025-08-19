from fastapi import APIRouter, HTTPException, Depends, Request
from pydantic import BaseModel
import stripe
import os
from app.auth.auth_handler import get_current_user
from app.database import get_db
from sqlalchemy.orm import Session

router = APIRouter()
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")


class CheckoutRequest(BaseModel):
    plan: str  # "creator" o "premium"


@router.post("/payments/create-checkout-session")
def create_checkout_session(
    checkout_data: CheckoutRequest,
    user: dict = Depends(get_current_user),
):
    PLAN_PRICES = {
        "creator": {"name": "Plan Creador Dubloop", "price": 2900},
        "premium": {"name": "Plan Premium Dubloop", "price": 3900},
    }
    plan_info = PLAN_PRICES.get(checkout_data.plan)
    if not plan_info:
        raise HTTPException(status_code=400, detail="Plan inválido")

    try:
        # Stripe activará automáticamente Apple Pay y Google Pay si están disponibles en el navegador
        session = stripe.checkout.Session.create(
            payment_method_types=["card", "klarna"],
            line_items=[{
                "price_data": {
                    "currency": "eur",
                    "product_data": {
                        "name": plan_info["name"],
                    },
                    "unit_amount": plan_info["price"],  # precio en céntimos
                },
                "quantity": 1,
            }],
            mode="payment",
            success_url="https://dubloop-backend.up.railway.app/payments/success",
            cancel_url="https://dubloop-backend.up.railway.app/payments/cancel",
            metadata={"user_id": user["id"], "plan": checkout_data.plan},
        )
        return {"checkout_url": session.url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/payments/webhook")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    webhook_secret = os.getenv("STRIPE_WEBHOOK_SECRET")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, webhook_secret
        )
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid signature")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Procesamos el evento del pago completado
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        metadata = session.get("metadata", {})
        user_id = metadata.get("user_id")
        plan = metadata.get("plan")

        if user_id and plan:
            db = next(get_db())
            from app.routers.subscription import create_or_update_subscription
            create_or_update_subscription(user_id, plan, db)

    return {"status": "success"}