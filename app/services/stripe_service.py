import os
import stripe
from fastapi import HTTPException
from dotenv import load_dotenv

load_dotenv()

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

PLAN_PRICE_MAPPING = {
    "free": 0,
    "creator": 2900,  # 29€ in cents
    "premium": 3900   # 39€ in cents
}

DOMAIN = os.getenv("FRONTEND_DOMAIN", "http://localhost:3000")

def create_checkout_session(user_id: int, plan: str):
    if plan not in PLAN_PRICE_MAPPING:
        raise HTTPException(status_code=400, detail="Invalid plan selected")

    if plan == "free":
        return "Free plan activated"

    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "eur",
                        "unit_amount": PLAN_PRICE_MAPPING[plan],
                        "product_data": {
                            "name": f"Dubloop {plan.capitalize()} Plan"
                        },
                    },
                    "quantity": 1,
                }
            ],
            mode="subscription",
            metadata={"user_id": str(user_id)},
            success_url=f"{DOMAIN}/success?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=f"{DOMAIN}/cancel",
        )
        return session.url
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
