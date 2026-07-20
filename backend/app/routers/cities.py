from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime

from ..database import get_db
from ..models import City, Event
from ..schemas import CityModel, EventModel

router = APIRouter()


@router.get("/", response_model=list[CityModel])
def list_cities(db: Session = Depends(get_db)):
    return db.query(City).order_by(City.name).all()


@router.get("/{city_slug}", response_model=CityModel)
def get_city(city_slug: str, db: Session = Depends(get_db)):
    city = db.query(City).filter(City.slug == city_slug).first()
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    return city


@router.post("/", response_model=CityModel)
def create_city(payload: CityModel, db: Session = Depends(get_db)):
    exists = db.query(City).filter(City.slug == payload.slug).first()
    if exists:
        raise HTTPException(status_code=400, detail="City already exists")
    city = City(**payload.dict(exclude={"id"}))
    db.add(city)
    db.commit()
    db.refresh(city)
    return city
