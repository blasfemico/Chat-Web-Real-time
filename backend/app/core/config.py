from pydantic_settings import BaseSettings
class Settings(BaseSettings):
    app_name: str = "Real-Time Chat App"
    secret_key: str = "your_secret_key"  # Cambiar en producción
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    database_url: str = "postgresql+psycopg2://postgres:dante20121@localhost:5432/evasoft"

    class Config:
        env_file = ".env"

settings = Settings()







