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

    if city:
        query = query.filter(City.slug == city)

    if category:
        query = query.filter(Event.category == category)

    if q:
        query = query.filter(
            (Event.title.ilike(f"%{q}%")) | (Event.description.ilike(f"%{q}%"))
        )

    if from_:
        query = query.filter(Event.start_at >= from_)

    if to:
        query = query.filter(Event.start_at <= to)

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
