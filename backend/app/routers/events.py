from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional

from ..database import get_db
from ..models import Event, City
from ..schemas import EventModel

router = APIRouter()


@router.get("/", response_model=list[EventModel])
def list_events(
    city: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    q: Optional[str] = Query(None),
    from_: Optional[datetime] = Query(None, alias="from"),
    to: Optional[datetime] = Query(None),
    db: Session = Depends(get_db),
):
    query = db.query(Event).join(City)

    day_filters = [Event.source.in_(['aachen_de','koeln_de','berlin_de','demo'])]

    if city:
        day_filters.append(City.slug == city)

    if category:
        day_filters.append(Event.category == category)

    if q:
        day_filters.append((Event.title.ilike(f"%{q}%")) | (Event.description.ilike(f"%{q}%")))

    if from_:
        day_filters.append(Event.start_at >= from_)

    if to:
        day_filters.append(Event.start_at <= to)

    query = query.filter(*day_filters)
    query = query.order_by(Event.start_at.asc())
    results = query.all()

    # Simple deduplication by title+start_at for v0
    seen = set()
    deduped = []
    for ev in results:
        key = (ev.title, ev.start_at.isoformat())
        if key not in seen:
            seen.add(key)
            deduped.append(ev)
    return deduped


@router.get("/{event_id}", response_model=EventModel)
def get_event(event_id: int, db: Session = Depends(get_db)):
    ev = db.query(Event).filter(Event.id == event_id).first()
    if not ev:
        raise HTTPException(status_code=404, detail="Event not found")
    return ev
