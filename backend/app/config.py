from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_env: str = "development"
    database_url: str = "postgresql+asyncpg://companion:companion@localhost:5432/companion"
    redis_url: str = "redis://localhost:6379/0"
    memory_embedding_dimensions: int = 1536
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
