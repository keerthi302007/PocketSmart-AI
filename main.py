from contextlib import asynccontextmanager

from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from fastapi.staticfiles import StaticFiles

from starlette.middleware.sessions import (
    SessionMiddleware,
)

from app.config import get_settings

from app.database import (
    Base,
    engine,
)

from app import auth
from app.routes import pages, planners

settings = get_settings()


@asynccontextmanager
async def lifespan(
    app: FastAPI,
):

    Base.metadata.create_all(
        bind=engine
    )

    yield


app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description=(
        "Budget-aware GenAI "
        "recommendation assistant"
    ),
    lifespan=lifespan,
)


app.add_middleware(
    SessionMiddleware,
    secret_key=settings.secret_key,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.mount(
    "/static",
    StaticFiles(
        directory="app/static"
    ),
    name="static",
)


app.include_router(
    pages.router
)

app.include_router(
    auth.router
)

app.include_router(
    planners.router
)


@app.get("/health")
def health():

    return {
        "status": "ok",
        "service": settings.app_name,
        "ai_configured": bool(
            settings.gemini_api_key
        ),
    }


@app.get("/api/session-info")
def session_info():

    return {
        "authenticated": True,
        "service": settings.app_name,
    }


@app.get("/api/session-data")
def session_data():

    return {
        "message": (
            "Use /api/auth/me and "
            "/api/history for authenticated "
            "session data."
        )
    }