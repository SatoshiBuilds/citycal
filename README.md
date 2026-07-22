# CityCal - Neighborhood Event Radar

Discover everything happening in your city — festivals, workshop groups, small dance classes, meetups, underground happenings — all in one place.

## What It Does
- **City Picker**: Choose from supported cities. Initially: **Aachen · Köln · Berlin**
- **Event Calendar**: Chronological feed with category filters (music, sports, arts, workshops, etc.)
- **Map View**: See events pinned to their real locations in the city
- **Daily Refresh**: An automated crawler/LLM extractor pulls new events from diverse sources each day

## Current State
- Backend API scaffolded with FastAPI + SQLite/SQLAlchemy
- Frontend skeleton with FullCalendar and Leaflet map
- Working endpoints: `/health`, `/cities`, `/events`

## Getting Started

### Backend
From the `backend/` directory:
```bash
python3 -m uvicorn app.main:app --reload
```
Then visit:
- API docs: `http://localhost:8000/docs`
- Healthcheck: `http://localhost:8000/health`

### Frontend
Serve the frontend folder with any static server:
```bash
python3 -m http.server 8080
```
Then visit `http://localhost:8080`.

## API
- `GET /health`
- `GET /cities`
- `GET /events?city=koeln&category=music&q=techno&from=2026-01-01T00:00:00&to=2026-12-31T23:59:59`

## Project Structure
- `backend/app/`: FastAPI app, models, schemas, routers
- `frontend/`: Vanilla HTML/CSS/JS frontend with calendar + map
- `docker-compose.yml`: Optional containerized dev environment

## Sources
In order of difficulty/prioritization for v1:
- Official city event portals:
  - Aachen: `aachen.de`, `REGIOTREND Aachen/Euregio`
  - Köln: `koeln.de`, `stadt-koeln.de`
  - Berlin: `visitberlin.de`, `berlin.de`
- Meetup.com city pages
- Facebook Events public pages (more difficult due to login walls)
- Subreddits: r/aachen, r/koeln, r/berlin
- Event platforms: Eventbrite local sections
- Local forum/public calendar feeds: RSS/Atom

## License
MIT
