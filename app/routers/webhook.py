from fastapi import APIRouter, Request, HTTPException, status
import stripe
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/webhook", tags=["Webhook"])

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
endpoint_secret = os.getenv("STRIPE_WEBHOOK_SECRET")

@router.post("/")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    try:
        event = stripe.Webhook.construct_event(
            payload=payload,
            sig_header=sig_header,
            secret=endpoint_secret
        )
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid signature")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    # Evento específico: se ha completado un pago
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        customer_email = session.get("customer_email")
        amount_total = session.get("amount_total", 0) / 100  # Convertir a euros
        print(f"✅ Pago completado de {customer_email}, total: {amount_total}€")

        # Aquí puedes añadir los créditos al usuario, si quieres hacerlo directamente.

    return {"status": "success"}