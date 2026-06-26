from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://desenreda:desenreda123@localhost:5432/desenreda"
    SECRET_KEY: str = "desenreda-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    GOOGLE_API_KEY: str = ""
    GOOGLE_MODEL: str = "gemini-3.1-flash-lite"

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "ignore",
    }


settings = Settings()
