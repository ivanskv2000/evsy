from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.routes import events, fields, tags, generic

from . import models
from app.database.database import engine
from app.settings import Settings

models.Base.metadata.create_all(bind=engine)

settings = Settings()

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

app.state.settings = settings

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3012", "http://localhost:5173", "http://localhost:5174"],  # 👈 тут укажи адрес фронта
    allow_credentials=True,
    allow_methods=["*"],  # Разрешить все методы (GET, POST, PUT, DELETE)
    allow_headers=["*"],  # Разрешить все заголовки
)

app.include_router(events.router, prefix="/api/v1", tags=["events"])
app.include_router(tags.router, prefix="/api/v1", tags=["tags"])
app.include_router(fields.router, prefix="/api/v1", tags=["fields"])
app.include_router(generic.router, prefix="/api/v1", tags=["generic"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Evsy API!"}
