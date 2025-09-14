from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    AUTH0_DOMAIN: str
    AUTH0_API_AUDIENCE: str
    MAX_SESSIONS: int = 3

    class Config:
        env_file = ".env"

settings = Settings()


