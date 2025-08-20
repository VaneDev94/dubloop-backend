from dotenv import load_dotenv
load_dotenv()
import os
from app.database import engine
from app.models import user
from app.models.plans import Subscription

user.Base.metadata.create_all(bind=engine)
# subscription.Base.metadata.create_all(bind=engine)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi import Request
from app.routers.dubbing import router as dubbing_router
from app.routers.stripe import router as stripe_router
from app.routers import payments, subscription
from app.routers import webhook
from app.routers import health
from starlette.middleware.sessions import SessionMiddleware
# Routers faltantes
from app.routers import auth, billing, detection, users

app = FastAPI(title="Dubloop Backend")

SESSION_SECRET = os.getenv("SESSION_SECRET", "fallback-secret")

app.add_middleware(
    SessionMiddleware,
    secret_key=SESSION_SECRET,
)

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
app.include_router(stripe_router, prefix="/stripe", tags=["Stripe"])
app.include_router(payments.router)
app.include_router(webhook.router)
from app.routers import auth_google
app.include_router(auth_google.router)
app.include_router(health.router)
from app.routers.language import router as language_router
app.include_router(language_router, prefix="/language", tags=["Language Detection"])

# Routers añadidos
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(billing.router, prefix="/billing", tags=["Billing"])
app.include_router(subscription.router, prefix="/subscriptions", tags=["Subscriptions"])
app.include_router(detection.router, prefix="/detection", tags=["Detection"])
app.include_router(users.router, prefix="/users", tags=["Users"])


@app.get("/ping")
def ping():
    return {"message": "pong"}


from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, RedirectResponse
import os

frontend_path = os.path.join(os.path.dirname(__file__), "frontend")


@app.get("/iniciar-sesion")
async def iniciar_sesion():
    return RedirectResponse(url="/auth/google/login")

app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")
