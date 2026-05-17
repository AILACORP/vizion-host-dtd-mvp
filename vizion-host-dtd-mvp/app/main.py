from fastapi import FastAPI

from app.api.health import router as health_router
from app.api.telegram import router as telegram_router
from app.api.whatsapp import router as whatsapp_router
from app.api.entries import router as entries_router
from app.db.base import Base
from app.db.session import engine
from app.db import models  # noqa: F401

app = FastAPI(title="VIZION HOST + Descarga Tu Dia API", version="0.1.0")


@app.on_event("startup")
def startup_create_tables() -> None:
    # MVP convenience. Replace with Alembic migrations before production scale.
    Base.metadata.create_all(bind=engine)


app.include_router(health_router, prefix="/health", tags=["health"])
app.include_router(telegram_router, prefix="/webhooks/telegram", tags=["telegram"])
app.include_router(whatsapp_router, prefix="/webhooks/whatsapp", tags=["whatsapp"])
app.include_router(entries_router, prefix="/entries", tags=["entries"])
