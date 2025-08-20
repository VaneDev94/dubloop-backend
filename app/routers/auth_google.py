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
    print("✅ LLEGÓ AL CALLBACK DE GOOGLE ✅")
    token = await oauth.google.authorize_access_token(request)
    user_info = await oauth.google.parse_id_token(request, token)
    user = await get_or_create_google_user(user_info)
    id_token = escape(token.get("id_token", ""))
    return HTMLResponse(content=f"""
  <html>
    <head>
      <title>Autenticación completada</title>
      <style>
        body {{
          font-family: Arial, sans-serif;
          display: flex;
          align-items: center;
          justify-content: center;
          height: 100vh;
          background-color: #d2f4ea;
          color: #333;
        }}
        .container {{
          text-align: center;
          background: white;
          padding: 30px;
          border-radius: 12px;
          box-shadow: 0 0 15px rgba(0,0,0,0.1);
        }}
      </style>
    </head>
    <body>
      <div class="container">
        <h2>✅ Autenticación completada</h2>
        <p>Redirigiendo...</p>
      </div>
      <script>
        const token = "{id_token}";
        window.addEventListener("load", () => {{
          window.opener?.postMessage({{
            type: "google-auth-success",
            token
          }}, "*");
          setTimeout(() => window.close(), 1500);
        }});
      </script>
    </body>
  </html>
""")