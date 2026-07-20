from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from ..database import get_db
from ..models import City, Event
from ..scrapers import koeln, facebook, meetup
from ..services.llm_extractor import extract_events

router = APIRouter()


@router.post("/refresh/{city_slug}")
def refresh_city(city_slug: str):
    """TODO: Trigger a crawl + extract cycle for a specific city."""
    raise HTTPException(status_code=501, detail="Not implemented yet")
