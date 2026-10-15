"""Application settings loaded from environment variables or a .env file."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "Resume Matcher Agent"
    log_level: str = "INFO"

    # LLM settings (the agent still works without an LLM, using rule-based extraction)
    use_llm: bool = True
    llm_provider: str = "openai"  # openai | azure_openai | anthropic | ollama
    llm_model: str = "gpt-4o-mini"
    llm_temperature: float = 0.0

    # Upload limits
    max_file_size_mb: int = 5

    # Scoring weights (should add up to 1.0)
    weight_required: float = 0.55
    weight_preferred: float = 0.15
    weight_experience: float = 0.20
    weight_education: float = 0.10


@lru_cache
def get_settings() -> Settings:
    return Settings()
