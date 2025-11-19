from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.db import create_db_and_tables
from app.routes import health, jobs, resumes, apply, followups, settings, ai, dashboard
from app.utils.logger import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting CloudHire Nexus Backend...")
    create_db_and_tables()
    logger.info("Database tables created/verified")
    yield
    logger.info("Shutting down CloudHire Nexus Backend...")


app = FastAPI(
    title="CloudHire Nexus Backend",
    description="Production-grade job application automation backend with dual AI/manual modes",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(jobs.router)
app.include_router(resumes.router)
app.include_router(apply.router)
app.include_router(followups.router)
app.include_router(settings.router)
app.include_router(ai.router)
app.include_router(dashboard.router)


@app.get("/")
async def root():
    return {
        "message": "CloudHire Nexus Backend API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/api/health"
    }
