from pydantic import BaseSettings
from app.database.database import SQLALCHEMY_DATABASE_URL
class Settings(BaseSettings):
    app_name: str = "Real-Time Chat App"
    secret_key: str = "your_secret_key"  # Cambiar en producción, idealmente en un archivo .env
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    database_url: str = SQLALCHEMY_DATABASE_URL

    class Config:
        env_file = ".env"  # Archivo de entorno para cargar variables de entorno

settings = Settings()
