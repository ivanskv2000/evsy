from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.routers import events, fields, tags

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
    openapi_tags=[
        {
            "name": "events",
            "description": "Manage analytics events. Includes tags and fields associations.",
        },
        {
            "name": "tags",
            "description": "Manage tags. Tags can be used to classify events by product domain or feature.",
        },
        {
            "name": "fields",
            "description": "Define reusable attributes for describing events.",
        },
    ],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3012"],  # 👈 тут укажи адрес фронта
    allow_credentials=True,
    allow_methods=["*"],  # Разрешить все методы (GET, POST, PUT, DELETE)
    allow_headers=["*"],  # Разрешить все заголовки
)

app.include_router(events.router, prefix="/api/v1", tags=["events"])
app.include_router(tags.router, prefix="/api/v1", tags=["tags"])
app.include_router(fields.router, prefix="/api/v1", tags=["fields"])


@app.get("/")
def read_root():
    return {"message": "Welcome to the Evsy API!"}
