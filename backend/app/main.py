from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api import auth, materials, cards, reviews, push_progress, seed

app = FastAPI(
    title="Daily Interview Prep",
    docs_url=None if settings.ENV == "production" else "/docs",
)

origins = settings.CORS_ORIGINS.split(",") if settings.CORS_ORIGINS != "*" else ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(materials.router)
app.include_router(cards.router)
app.include_router(reviews.router)
app.include_router(push_progress.router)
app.include_router(seed.router)


@app.get("/health")
async def health():
    return {"status": "ok"}
