from fastapi import APIRouter
from app.api.endpoints import dubbing
from app.routers import auth, billing, users
from app.routers import detection
from app.routers import stripe, health

gateway_router = APIRouter()

# Redirigir las peticiones a los endpoints clave
gateway_router.include_router(dubbing.router, prefix="/dubbing", tags=["Doblaje"])

# Preparado para incluir más routers en el futuro
gateway_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
gateway_router.include_router(users.router, prefix="/users", tags=["Usuarios"])
gateway_router.include_router(billing.router, prefix="/billing", tags=["Billing"])
gateway_router.include_router(detection.router, prefix="/detection", tags=["Detección"])
gateway_router.include_router(stripe.router, prefix="/stripe", tags=["Stripe"])
gateway_router.include_router(health.router, tags=["Health"])

router = gateway_router
