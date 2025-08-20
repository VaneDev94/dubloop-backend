from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from app.auth.google_oauth import oauth
from app.services.user_services import get_or_create_google_user
from markupsafe import escape

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
    id_token = escape(token.get("id_token", ""))
    return HTMLResponse(content=f"""
<html>
  <body>
    <script>
      window.opener.postMessage({{
        type: "google-auth-success",
        token: "{id_token}"
      }}, "*");
      window.close();
    </script>
    <p>Autenticación completada. Puedes cerrar esta ventana.</p>
  </body>
</html>
""")