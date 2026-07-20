import sys
sys.path.insert(0, '/home/michaelb/citycal/backend')

from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models import City, Event
from app.database import Base

Base.metadata.create_all(bind=engine)

db = SessionLocal()

aachen = City(name='Aachen', slug='aachen', country='DE', latitude=50.7753, longitude=6.0839)
koeln = City(name='Cologne', slug='koeln', country='DE', latitude=50.9375, longitude=6.9603)
berlin = City(name='Berlin', slug='berlin', country='DE', latitude=52.5200, longitude=13.4050)
db.add_all([aachen, koeln, berlin])
db.commit()

events = [
    Event(city_id=koeln.id, source='demo', title='Cologne Street Food Festival', start_at='2026-12-05T12:00:00', end_at='2026-12-06T22:00:00',
          location_name='Rheinauhafen, Cologne', latitude=50.9203, longitude=6.9619, category='community'),
    Event(city_id=koeln.id, source='demo', title='HipHop Open Class', start_at='2026-12-07T18:00:00', end_at='2026-12-07T19:30:00',
          location_name='Dance Studio Köln', latitude=50.9386, longitude=6.9561, category='workshops'),
    Event(city_id=berlin.id, source='demo', title='Berlin Techno Night', start_at='2026-12-12T23:00:00', end_at='2026-12-13T06:00:00',
          location_name='Berghain', latitude=52.5118, longitude=13.4434, category='nightlife'),
    Event(city_id=aachen.id, source='demo', title='Christmas Market Aachen', start_at='2026-12-10T11:00:00', end_at='2026-12-23T21:00:00',
          location_name='Markt, Aachen', latitude=50.7753, longitude=6.0839, category='community'),
]
db.add_all(events)
db.commit()
print('Seeded', len(events), 'events')
