from pydantic import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Dubloop Backend"
    DEFAULT_TARGET_LANG: str = "en"

    # 🔐 Seguridad
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 día

    # 📨 Email verification
    EMAIL_HOST: str
    EMAIL_PORT: int
    EMAIL_USER: str
    EMAIL_PASS: str

    # 🔁 Google OAuth
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_REDIRECT_URI: str

    # 💳 Stripe
    STRIPE_PUBLIC_KEY: str
    STRIPE_SECRET_KEY: str
    STRIPE_WEBHOOK_SECRET: str

    # 🐘 PostgreSQL
    DATABASE_URL: str

    class Config:
        env_file = ".env"

settings = Settings()