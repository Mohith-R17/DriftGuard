from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import List, Optional
from pydantic import model_validator


class Settings(BaseSettings):
    app_name:    str = "DriftGuard"
    app_version: str = "1.0.0"
    debug:       bool = False
    secret_key:  Optional[str] = None

    # Database
    database_url: str

    @model_validator(mode='after')
    def fix_database_url(self) -> 'Settings':
        if self.database_url:
            if self.database_url.startswith("postgres://"):
                self.database_url = self.database_url.replace("postgres://", "postgresql+asyncpg://", 1)
            elif self.database_url.startswith("postgresql://"):
                self.database_url = self.database_url.replace("postgresql://", "postgresql+asyncpg://", 1)
        return self

    # Gemini (fallback)
    gemini_api_key: str = ""
    gemini_model:   str = "gemini-2.5-flash"

    # OpenRouter (primary, when no Groq key)
    openrouter_api_key: str = ""
    openrouter_model:   str = "anthropic/claude-3.5-sonnet"

    # Groq (fallback)
    grok_api_key: str = ""
    groq_model:   str = "llama-3.3-70b-versatile"

    # GitHub PAT (for doc generation / PR creation)
    github_token: str = ""

    # GitHub OAuth App
    github_client_id:      str = ""
    github_client_secret:  str = ""
    github_oauth_redirect: str = "http://localhost:8000/api/auth/github/callback"
    frontend_url:          str = "http://localhost:5500"

    # CORS
    cors_origins: str = "http://localhost:5500,http://127.0.0.1:5500,http://localhost:3000"

    def get_cors_origins(self) -> List[str]:
        origins = [o.strip() for o in self.cors_origins.split(",") if o.strip()]
        dev = [
            "http://localhost:5500", "http://127.0.0.1:5500",
            "http://localhost:3000", "http://localhost:8000",
        ]
        return list(set(origins + dev))

    class Config:
        env_file = ".env"
        case_sensitive = False

    @model_validator(mode='after')
    def validate_secret_key(self) -> 'Settings':
        if not self.secret_key:
            if self.debug:
                self.secret_key = "development-secret-key-do-not-use-in-production"
            else:
                raise ValueError("CRITICAL: SECRET_KEY environment variable is missing. It MUST be set in production.")
        return self


@lru_cache()
def get_settings() -> Settings:
    return Settings()
    
