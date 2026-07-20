from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import engine, Base
from .routers import cities, events, crawl

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="CityCal API",
    description="Unified events API for Aachen, Köln, Berlin",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(cities.router, prefix="/cities", tags=["cities"])
app.include_router(events.router, prefix="/events", tags=["events"])
app.include_router(crawl.router, prefix="/crawl", tags=["crawling"])


@app.get("/health", tags=["health"])
def health():
    return {"status": "ok"}
