const API = 'http://localhost:8000';

const cityNames = {
    aachen: 'Aachen',
    koeln: 'Cologne',
    berlin: 'Berlin'
};

let currentCity = 'koeln';
let calendar, map;
let mapInitialized = false;

function $(id) { return document.getElementById(id); }

function initTabs() {
    document.querySelectorAll('.tab').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.view-section').forEach(s => s.classList.remove('active'));
            btn.classList.add('active');
            $('calendar-view').classList.toggle('active', btn.dataset.view === 'calendar');
            $('map-view').classList.toggle('active', btn.dataset.view === 'map');
            if (btn.dataset.view === 'map' && !mapInitialized) {
                initMap();
            } else if (btn.dataset.view === 'map' && mapInitialized) {
                setTimeout(() => map.invalidateSize(), 50);
            }
        });
    });
}

function getFilters() {
    return {
        city: currentCity,
        q: $('search-input').value,
        category: $('category-filter').value || undefined
    };
}

function buildUrl() {
    const p = new URLSearchParams();
    Object.entries(getFilters()).forEach(([k, v]) => {
        if (v !== undefined && v !== '') p.set(k, v);
    });
    return `${API}/events?${p.toString()}`;
}

function fmtDate(d) {
    const date = new Date(d);
    return date.toLocaleString('en-DE', {
        weekday: 'short',
        day: '2-digit',
        month: 'short',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    })
}

async function loadEvents() {
    const res = await fetch(buildUrl());
    if (!res.ok) {
        console.error('API error', res.status, await res.text());
        return [];
    }
    return await res.json();
}

function initCalendar(events) {
    if (calendar) {
        calendar.destroy();
        calendar = null;
    }
    const el = $('calendar');
    calendar = new FullCalendar.Calendar(el, {
        initialView: 'dayGridMonth',
        headerToolbar: { start: 'prev,next today', center: 'title', end: 'listWeek,dayGridMonth' },
        locale: 'en',
        height: 'auto',
        events: events.map(ev => ({
            id: ev.id,
            title: ev.title,
            start: ev.start_at,
            end: ev.end_at,
            allDay: false,
            extendedProps: { ...ev }
        })),
        eventClick(info) {
            alert(`${info.event.title}\n\n${fmtDate(info.event.start)}\n\n${info.event.extendedProps.location_name || ''}\n\n${info.event.extendedProps.url || ''}`)
        }
    });
    calendar.render();
}

function initMap(events) {
    if (mapInitialized) {
        if (events.length) {
            const group = new L.featureGroup(
                events
                    .filter(e => e.latitude && e.longitude)
                    .map(e => L.marker([e.latitude, e.longitude])
                        .bindPopup(`<b>${e.title}</b><br>${fmtDate(e.start_at)}<br>${e.location_name || ''}`)
                    )
            );
            map.eachLayer(l => { if (l instanceof L.Marker || l instanceof L.FeatureGroup) map.removeLayer(l); });
            group.addTo(map);
            map.fitBounds(group.getBounds().pad(0.2));
        }
        setTimeout(() => map.invalidateSize(), 50);
        return;
    }
    const defaultCenter = { koeln: [50.9375, 6.9603], aachen: [50.7753, 6.0839], berlin: [52.5200, 13.4050] }[currentCity];
    map = L.map('map').setView(defaultCenter, 12);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(map);
    mapInitialized = true;
    if (events.length) initMap(events);
}

function renderEventsList(events) {
    const container = $('events-container');
    $('event-count').textContent = `Showing ${events.length} events for ${cityNames[currentCity] || currentCity}`;
    if (!events.length) {
        container.innerHTML = '<p>No events found.</p>';
        return;
    }
    container.innerHTML = events.map(ev => `
        <div class="event-card">
            <h3>${escapeHtml(ev.title)}</h3>
            <div class="meta">🕒 ${fmtDate(ev.start_at)}${ev.end_at ? ' – ' + fmtDate(ev.end_at) : ''} · ${ev.location_name || 'TBA'}</div>
            ${ev.description ? `<p class="meta" style="margin-top:6px;color:#c9d1d9">${escapeHtml(ev.description.slice(0, 240))}</p>` : ''}
            ${ev.url ? `<p class="meta" style="margin-top:6px"><a href="${escapeHtml(ev.url)}" target="_blank" rel="noopener">Open source ↗</a></p>` : ''}
            ${ev.category ? `<span class="meta" style="display:inline-block;margin-top:6px;padding:4px 8px;background:#ffffff0d;border-radius:999px">${escapeHtml(ev.category)}</span>` : ''}
        </div>
    `).join('');
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

async function refresh() {
    const events = await loadEvents();
    if ($('calendar-view').classList.contains('active')) initCalendar(events);
    if ($('map-view').classList.contains('active')) initMap(events);
    renderEventsList(events);
}

function init() {
    initTabs();
    $('city-select').value = currentCity;
    $('city-select').addEventListener('change', e => {
        currentCity = e.target.value;
        refresh();
    });
    $('search-input').addEventListener('input', refresh);
    $('category-filter').addEventListener('change', refresh);
    refresh();
}

window.addEventListener('DOMContentLoaded', init);
