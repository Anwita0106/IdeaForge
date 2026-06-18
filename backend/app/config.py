"""
Centralized application configuration.

Every value here can be overridden with an environment variable (or a `.env`
file sitting next to this app when running locally). Nothing secret is
hard-coded - see `.env.example` for the full list of variables you can set.
"""
from typing import List, Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # --- General -----------------------------------------------------
    ENVIRONMENT: str = "development"
    APP_NAME: str = "IdeaForge API"

    # --- Database ------------------------------------------------------
    # Example values:
    #   Supabase:  postgresql://postgres:[PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres
    #   Neon:      postgresql://[user]:[password]@[host]/[dbname]?sslmode=require
    #   Local:     postgresql://postgres:postgres@localhost:5432/ideaforge
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/ideaforge"

    # --- CORS ------------------------------------------------------------
    # Comma separated list of origins allowed to call this API, e.g.
    # "http://localhost:5173,https://your-frontend.vercel.app"
    ALLOWED_ORIGINS: str = "*"

    # --- Feature flags ---------------------------------------------------
    # If true, the app inserts a handful of demo ideas the first time it
    # connects to an empty database. Off by default so the platform is
    # genuinely dynamic out of the box.
    SEED_DEMO_DATA: bool = False

    # --- External startup / business data providers ----------------------
    # All of these are OPTIONAL. If a key is missing, that provider is simply
    # skipped and IdeaForge's built-in heuristic engine fills the gap so the
    # /ideas/analyze and /ideas/save endpoints always return a complete,
    # useful response.
    CRUNCHBASE_API_KEY: Optional[str] = None

    PRODUCTHUNT_API_TOKEN: Optional[str] = None

    GOOGLE_API_KEY: Optional[str] = None
    GOOGLE_CSE_ID: Optional[str] = None

    CLEARBIT_API_KEY: Optional[str] = None

    EXTERNAL_API_TIMEOUT_SECONDS: float = 6.0

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @property
    def cors_origins(self) -> List[str]:
        if self.ALLOWED_ORIGINS.strip() == "*":
            return ["*"]
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",") if origin.strip()]


settings = Settings()
