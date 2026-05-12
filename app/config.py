from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    anthropic_api_key: str = ""
    model_name: str = "claude-sonnet-4-6"
    max_tokens: int = 8192
    temperature: float = 0.0
    static_dir: str = "static"


settings = Settings()
