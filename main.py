from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine
from app import models
from app.routers import companies, people, deals

# Create all tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="GTM Data Manager API",
    description="FastAPI backend for GTM Hub — Companies, People, and Deals",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict to your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(companies.router)
app.include_router(people.router)
app.include_router(deals.router)


@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "message": "GTM Data Manager API is running"}


@app.get("/health", tags=["Health"])
def health():
    return {"status": "healthy"}
