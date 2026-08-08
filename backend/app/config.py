import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    APP_NAME: str = "VaaniOS - MSME Voice OS"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")

    # API Keys
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")

    # Firebase
    FIREBASE_PROJECT_ID: str = os.getenv("FIREBASE_PROJECT_ID", "")

    # Voice
    DEFAULT_LANGUAGE: str = os.getenv("DEFAULT_LANGUAGE", "mr-IN")

    # Backend
    HOST: str = os.getenv("HOST", "127.0.0.1")
    PORT: int = int(os.getenv("PORT", "8000"))


settings = Settings()