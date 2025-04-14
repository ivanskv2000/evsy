from fastapi import FastAPI
from app.api.v1.routers import events, tags, fields
from . import models
from .database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Evsy API",
    description="Evsy is a service for managing and tracking product events.",
    version="1.0.0",
    contact={
        "name": "Ivan Skvortsov",
        "email": "ivanskv2000@gmail.com",
    },
)

# Подключаем эндпоинты
app.include_router(events.router, prefix="/api/v1", tags=["events"])
app.include_router(tags.router, prefix="/api/v1", tags=["tags"])
app.include_router(fields.router, prefix="/api/v1", tags=["fields"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Evsy API!"}
