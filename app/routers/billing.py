# app/router/billing.py

from fastapi import APIRouter

router = APIRouter()

# Ejemplo de ruta básica
@router.get("/stripe")
def stripe_placeholder():
    return {"message": "Stripe endpoint (aún sin implementar)"}