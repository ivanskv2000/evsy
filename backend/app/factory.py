from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import sessionmaker

from app.api.v1.routes import admin, auth, events, fields, generic, tags
from app.modules.auth.schemas import UserCreate
from app.modules.auth.service import create_user_if_not_exists
from app.settings import Settings


def create_app(settings: Settings, SessionLocal: sessionmaker) -> FastAPI:

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        if settings.is_demo:
            with SessionLocal() as db:
                create_user_if_not_exists(
                    db, UserCreate(email="demo@evsy.dev", password="bestructured")
                )
        yield

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
        debug=settings.is_dev,
        root_path="/api",
        lifespan=lifespan,
    )

    app.state.settings = settings

    if settings.is_dev:
        print("Running in development mode")
    elif settings.is_demo:
        print("Running in demo mode")

    allowed_origins = ["http://localhost:5173", "http://localhost:3000"]
    allowed_origins = (
        allowed_origins + [settings.frontend_url]
        if settings.is_dev
        else [settings.frontend_url]
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(events.router, prefix="/v1", tags=["events"])
    app.include_router(tags.router, prefix="/v1", tags=["tags"])
    app.include_router(fields.router, prefix="/v1", tags=["fields"])
    app.include_router(generic.router, prefix="/v1", tags=["generic"])
    app.include_router(admin.router, prefix="/v1", tags=["admin"])
    app.include_router(auth.router, prefix="/v1", tags=["auth"])

    @app.get("/")
    def read_root():
        return {"message": "Welcome to the Evsy API!"}

    return app
