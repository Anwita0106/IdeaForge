from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import Base, engine
from app.routers import ideas
from app.seed import run as run_seed

app = FastAPI(
    title=settings.APP_NAME,
    description="Backend API for IdeaForge - a real startup idea validation platform.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ideas.router)


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
    if settings.SEED_DEMO_DATA:
        run_seed()


@app.get("/")
def root():
    return {"name": settings.APP_NAME, "status": "ok", "environment": settings.ENVIRONMENT}


@app.get("/health")
def health():
    return {"status": "ok"}
