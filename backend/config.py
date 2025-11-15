from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    DATABASE_URL: str

    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000

    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"

    MIN_PREDICTION_CONFIDENCE: float = 0.6

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    return Settings()
