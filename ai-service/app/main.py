from fastapi import FastAPI
from app.routes import health, document, ask

app = FastAPI(title="Intervu AI Service")

app.include_router(health.router)
app.include_router(document.router)
app.include_router(ask.router)