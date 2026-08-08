from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import health, voice, products, transactions, reports

app = FastAPI(
    title="VaaniOS - MSME Voice OS",
    description="Vernacular Agentic Voice OS for MSME Operators",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api")
app.include_router(voice.router, prefix="/api")
app.include_router(products.router, prefix="/api")
app.include_router(transactions.router, prefix="/api")
app.include_router(reports.router, prefix="/api")


@app.get("/")
def root():
    return {
        "message": "VaaniOS Backend is running",
        "status": "online"
    }