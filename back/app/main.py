import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.routing import APIRoute
from starlette.middleware.cors import CORSMiddleware

from app.core.logging import configure_logging
from app.settings import settings

# Configure root logger before any further imports/log calls.
configure_logging()
logger = logging.getLogger(__name__)


# ---- FASTAPI APP CREATION ----
def custom_generate_unique_id(route: APIRoute) -> str:
    # Handle routes without tags
    if route.tags and len(route.tags) > 0:
        return f"{route.tags[0]}-{route.name}"
    else:
        return route.name or "unnamed_route"


# ---- Add lifespan manager ----
@asynccontextmanager
async def lifespan() -> AsyncGenerator[None]:
    # Perform startup tasks
    logger.info(f"{settings.ENVIRONMENT} application starting")
    yield
    logger.info(f"{settings.ENVIRONMENT} application ending")


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
    if settings.ENVIRONMENT == "dev"
    else None,
    docs_url="/docs" if settings.ENVIRONMENT == "dev" else None,
    redoc_url="/redoc" if settings.ENVIRONMENT == "dev" else None,
    generate_unique_id_function=custom_generate_unique_id,
    lifespan=lifespan,
    swagger_ui_parameters={
        "persistAuthorization": True,
        "displayRequestDuration": True,
        "tryItOutEnabled": True,
    },
)

# ---- CORS MIDDLEWARE ----
# Set all CORS enabled origins - must be added before subdomain routing
if settings.all_cors_origins:
    logger.info(f"CORS origin(s) are: {settings.all_cors_origins}")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.all_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
