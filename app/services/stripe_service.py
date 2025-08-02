import os
import stripe
from fastapi import HTTPException
from dotenv import load_dotenv

load_dotenv()

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

# Define some basic pricing (amount in euros -> credits)
PRICE_CREDIT_MAPPING = {
    500: 50,    # 5€ = 50 credits
    1000: 120,  # 10€ = 120 credits
    2000: 260   # 20€ = 260 credits
}

DOMAIN = os.getenv("FRONTEND_DOMAIN", "http://localhost:3000")

def create_checkout_session(user_id: int, amount: int):
    if amount not in PRICE_CREDIT_MAPPING:
        raise HTTPException(status_code=400, detail="Invalid amount selected")

    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "eur",
                        "unit_amount": amount,
                        "product_data": {
                            "name": f"{PRICE_CREDIT_MAPPING[amount]} Dubloop Credits"
                        },
                    },
                    "quantity": 1,
                }
            ],
            mode="payment",
            metadata={"user_id": str(user_id)},
            success_url=f"{DOMAIN}/success?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=f"{DOMAIN}/cancel",
        )
        return session.url
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
