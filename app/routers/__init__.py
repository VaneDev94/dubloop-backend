# /app/routers/__init__.py

from app.routers.auth import router as auth_router
from app.routers.plans import router as plan_router
from app.routers.detection import router as detection_router
from app.routers.health import router as health_router
from app.routers.stripe import router as stripe_router

__all__ = [
    "auth_router",
    "plan_router",
    "detection_router",
    "health_router",
    "stripe_router",
]