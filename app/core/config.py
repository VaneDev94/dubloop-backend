from pydantic import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Dubloop Backend"
    DEFAULT_TARGET_LANG: str = "en"  # Idioma destino por defecto

    class Config:
        env_file = ".env"

settings = Settings()