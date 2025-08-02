

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
import os

FROM_EMAIL = os.getenv("EMAIL_FROM")
FROM_NAME = os.getenv("EMAIL_FROM_NAME", "Dubloop")
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

def send_verification_email(user_email: str, token: str):
    verification_link = f"https://yourfrontend.com/verify-email/{token}"

    msg = MIMEMultipart()
    msg["From"] = formataddr((FROM_NAME, FROM_EMAIL))
    msg["To"] = user_email
    msg["Subject"] = "Verifica tu correo en Dubloop"

    body = f"""Hola,

Gracias por registrarte en Dubloop.

Por favor, haz clic en el siguiente enlace para verificar tu dirección de correo electrónico:

{verification_link}

Si no has creado una cuenta, puedes ignorar este mensaje.

Saludos,
El equipo de Dubloop
"""

    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.send_message(msg)
            print(f"Correo de verificación enviado a {user_email}")
    except Exception as e:
        print(f"Error al enviar el correo: {e}")