# CityCal - Neighborhood Event Radar

Discover everything happening in your city — festivals, workshop groups, small dance classes, meetups, underground happenings — all in one place.

## What It Does
- **City Picker**: Choose from supported cities. Initially: **Aachen · Köln · Berlin**
- **Event Calendar**: Chronological feed with category filters (music, sports, arts, workshops, etc.)
- **Map View**: See events pinned to their real locations in the city
- **Daily Refresh**: An automated crawler/LLM extractor pulls new events from diverse sources each day

## Screenshot
> Coming soon once scaffold is styled and launched.

## Current Wireframe / Notes
- Frontend-only prototype state while backend API endpoints are implemented.
- **Framework**: Vanilla HTML/CSS/JS with **OpenStreetMap (Leaflet)** — no build step required.
- **Calendar**: FullCalendar v6 in list/timeline view.
- **Colors**: Berlin clay red (#D14955), Cologne lake blue (#0072CE), Aachen cathedral gold (#C9A96E).

## Getting Started
```bash
git clone https://github.com/<your-username>/citycal.git
cd citycal
# Just open index.html or serve the folder with any static server:
python3 -m http.server 8080
```

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

## Development
Run this backend locally:
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Then visit:
- Frontend: `http://localhost:8080`
- API docs: `http://localhost:8000/docs`
- Healthcheck: `http://localhost:8000/health`

## Via Docker
```bash
docker compose up --build
```

## Planned v1 Milestones
1. Scaffold project (done)
2. Backend city + events API
3. First scrapers for Köln city portal + Facebook Events
4. LLM-based unstructured-text extractor (supports small/obscure sources)
5. Calendar + map frontend
6. Add Berlin + Aachen sources

## License
MIT
