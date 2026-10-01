from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_env: str = "development"
    cors_origins: str = "http://localhost:5173"
    groq_api_key: str = ""
    groq_model: str = "llama-3.3-70b-versatile"
    read_only_mode: bool = True
    app_db_url: str = "sqlite:///./app.db"
    target_db_url: str = ""
    query_timeout_seconds: int = 10
    max_rows: int = 500


settings = Settings()
