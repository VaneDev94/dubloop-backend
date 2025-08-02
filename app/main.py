from app.database import engine
from app.models import user, credits

user.Base.metadata.create_all(bind=engine)
credits.Base.metadata.create_all(bind=engine)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi import Request
from app.api.endpoints.dubbing import router as dubbing_router
from app.routers.gateway import router as gateway_router
from app.routers.stripe import router as stripe_router
from app.routers import payments
from app.routers import webhook
from app.routers import health

app = FastAPI(title="Dubloop Backend")

# Add rate limiting
limiter = Limiter(key_func=get_remote_address, default_limits=["5/minute"])
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Activar CORS para permitir conexión desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # puedes restringir a ["http://localhost:5173"] si usáis Vite
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rutas
app.include_router(dubbing_router, prefix="/dubbing", tags=["Dubbing"])
app.include_router(gateway_router)
app.include_router(stripe_router, prefix="/stripe", tags=["Stripe"])
app.include_router(payments.router)
app.include_router(webhook.router)
from app.routers import auth_google
app.include_router(auth_google.router)
app.include_router(health.router)
from app.routers.language import router as language_router
app.include_router(language_router, prefix="/language", tags=["Language Detection"])