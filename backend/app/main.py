from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routes import (
    health,
    products,
    reports,
    transactions,
    voice,
)
from app.routes import settings as settings_routes


app = FastAPI(
    title="VyaparSaathi - MSME Voice OS",
    description="Vernacular Agentic Voice OS for MSME Operators",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(health.router, prefix="/api")
app.include_router(voice.router, prefix="/api")
app.include_router(products.router, prefix="/api")
app.include_router(transactions.router, prefix="/api")
app.include_router(reports.router, prefix="/api")

# settings.py already contains prefix="/api/settings/ai"
app.include_router(settings_routes.router)


@app.get("/")
def root():
    return {
        "message": "VyaparSaathi Backend is running",
        "status": "online",
    }