from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite+aiosqlite:///./interview_prep.db"
    JWT_SECRET: str = "change-me-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_DAYS: int = 7
    DEEPSEEK_API_KEY: str = ""
    DEEPSEEK_BASE_URL: str = "https://api.deepseek.com"
    AI_MODEL: str = "deepseek-v4-flash"
    VAPID_PRIVATE_KEY: str = ""
    VAPID_CLAIMS_EMAIL: str = ""
    DAILY_NEW_CARDS: int = 10
    DAILY_REVIEW_CARDS: int = 20
    PUSH_HOUR: int = 9
    CORS_ORIGINS: str = "*"
    ENV: str = "development"

    model_config = {"env_file": ".env"}


settings = Settings()
