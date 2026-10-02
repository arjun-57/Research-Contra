"""Configuration settings for Contra research trial engine."""

import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=[".env", "contra/.env"], extra="allow")

    GEMINI_API_KEY: Optional[str] = None
    GOOGLE_API_KEY: Optional[str] = None
    TAVILY_API_KEY: Optional[str] = None

    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True

    MAX_RESEARCH_LOOPS: int = 2
    SANDBOX_TIMEOUT_SECONDS: int = 30
    DEFAULT_CONFIDENCE_THRESHOLD: float = 0.70


settings = Settings()
