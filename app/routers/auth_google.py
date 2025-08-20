from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from app.auth.google_oauth import oauth
from app.services.user_services import get_or_create_google_user

router = APIRouter(prefix="/auth/google", tags=["Google Auth"])

@router.get("/login")
async def login(request: Request):
    redirect_uri = request.url_for('auth_google_callback')
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get("/callback")
async def auth_google_callback(request: Request):
    token = await oauth.google.authorize_access_token(request)
    user_info = await oauth.google.parse_id_token(request, token)
    user = await get_or_create_google_user(user_info)
    response = RedirectResponse(url="https://f465e9e21402.ngrok-free.app")
    # Aquí puedes usar cookies, JWT, etc.
    return response