from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class CityModel(BaseModel):
    id: int
    name: str
    slug: str
    country: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]

    class Config:
        from_attributes = True


class EventModel(BaseModel):
    id: int
    city_id: int
    source: str
    title: str
    description: Optional[str]
    start_at: datetime
    end_at: Optional[datetime]
    location_name: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    url: Optional[str]
    category: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
