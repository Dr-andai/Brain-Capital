"""Brain Capital Intelligence Platform - Main Application."""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.core.logging import configure_logging, logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    configure_logging()
    logger.info("Starting Brain Capital Intelligence Platform...")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"Debug mode: {settings.DEBUG}")

    yield

    # Shutdown
    logger.info("Shutting down Brain Capital Intelligence Platform...")


# Create FastAPI application
app = FastAPI(
    title="Brain Capital Intelligence Platform",
    description="Country-level brain capital indicators with AI-driven insights",
    version="0.1.0",
    lifespan=lifespan,
    debug=settings.DEBUG,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Set up Jinja2 templates
templates = Jinja2Templates(directory="app/templates")

# Include API routers
from app.api.v1 import countries, indicators, insights
app.include_router(countries.router, prefix="/api/v1", tags=["countries"])
app.include_router(indicators.router, prefix="/api/v1", tags=["indicators"])
app.include_router(insights.router, prefix="/api/v1", tags=["insights"])

# Include web routes
from app.web import routes, htmx
app.include_router(htmx.router, prefix="/htmx", tags=["htmx"])
app.include_router(routes.router, prefix="", tags=["pages"])  # Must be last for catch-all routes


@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "version": "0.1.0",
        "environment": settings.ENVIRONMENT,
    }
