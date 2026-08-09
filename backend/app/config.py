import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BACKEND_DIR = Path(__file__).resolve().parents[1]


class Settings:
    APP_NAME: str = "VaaniOS - MSME Voice OS"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")

    # API Keys
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")

    # Firebase
    FIREBASE_PROJECT_ID: str = os.getenv("FIREBASE_PROJECT_ID", "")

    # SQLite is the zero-configuration development database. The file is
    # ignored by Git and can later be replaced with a Firestore adapter.
    DATABASE_PATH: str = os.getenv("DATABASE_PATH") or str(
        BACKEND_DIR / "data" / "vyaparsaathi.db"
    )

    # Voice
    DEFAULT_LANGUAGE: str = os.getenv("DEFAULT_LANGUAGE", "mr-IN")
    MAX_AUDIO_BYTES: int = int(os.getenv("MAX_AUDIO_BYTES", "10485760"))

    # Backend
    HOST: str = os.getenv("HOST", "127.0.0.1")
    PORT: int = int(os.getenv("PORT", "8000"))
    CORS_ORIGINS: list[str] = [
        origin.strip()
        for origin in os.getenv(
            "CORS_ORIGINS",
            "http://localhost:5173,http://127.0.0.1:5173",
        ).split(",")
        if origin.strip()
    ]


settings = Settings()
