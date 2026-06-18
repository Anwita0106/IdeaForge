# IdeaForge

IdeaForge has been converted from a static, hard-coded prototype into a real
startup idea validation platform: a FastAPI + PostgreSQL backend now powers
every idea, analysis, and recommendation you see in the (unchanged) UI.

```
IdeaForge/
├── frontend/   the original UI (index.html), now talking to a real API
└── backend/    FastAPI app, validation engine, and external API integrations
```

The visual design, layout, colors, fonts, icons, animations, and every user
flow are untouched - the first 1,194 lines of `frontend/index.html` (the
entire `<head>`, all CSS, and the full `<body>` markup) are byte-for-byte
identical to the original file. Only the `<script>` logic was changed, and
only to replace data with real API calls.

---


---

## Overview

###  Home Screen

The landing page showcasing trending startup ideas, validation metrics, and the live idea feed.

![Home Screen](./screenshots/home_screen.png.jpeg)

---


###  Launch & Validate Ideas

Submit an idea and receive a validation score, market insights, competitor analysis, similar startups, and differentiation opportunities.

![Launch Idea](./screenshots/launch_idea.png.jpeg)

---


###  Featured Startup Ideas

Explore curated and AI-validated startup ideas from the community feed.

![Featured Ideas](./screenshots/after_idea_launch.png.jpeg)

---


###  Export Ideas as PDF

Download and share startup ideas as professionally formatted PDF reports for collaboration, presentations, and feedback.

![Export Idea](./screenshots/export_idea.png.jpeg)

---


###  AI Idea Generation

Generate unique startup concepts instantly using the built-in AI idea generator.

![AI Idea Generation](./screenshots/ai_idea.png.jpeg)

---


###  Light Theme Support

Switch seamlessly between dark and light modes for a personalized experience.

![Light Theme](./screenshots/light_theme.png.jpeg)

---

## 1. What changed, and why

Per the brief, **every frontend change below was necessary to connect the UI
to a real backend** - none of them are visual/design changes. Nothing in the
`<head>`, `<style>`, or `<body>` markup was touched.

| Change | Why it was necessary |
|---|---|
| Removed `defaultIdeas`, `AI_IDEAS`, `ideaLinks`, `similarProjects`, `aiSuggestions`, `categoryLinks` hard-coded objects | These were the static "fake data" the brief asked to remove. There's no way to make the app dynamic while keeping them. |
| Added `API_BASE_URL` + `fetchIdeasFromServer()` | The feed now loads from `GET /ideas` instead of a hard-coded array. |
| `submitIdea()` now calls `POST /ideas/save` (was: pushed a local object into the array) | This is literally what "process the idea dynamically" + "remove hard-coded data" requires - the idea has to be sent somewhere real. |
| `generateAiIdea()` now calls `POST /ideas/generate` (was: picked from a 4-item hard-coded array) | Same reasoning - it now generates and analyzes a genuinely new idea server-side instead of cycling through 4 fixed templates. |
| Card rendering now reads `idea.similarStartups`, `idea.competitors`, `idea.marketCategory`, `idea.suggestedImprovements`, `idea.differentiationOpportunities`, `idea.marketGaps` from the API response | This is the actual "replace static recommendations with dynamic ones" requirement. The HTML/CSS structure of these blocks is identical to the original `category-links` / `ai-suggestions` components - only the data source changed, and components are simply reused for the additional fields. |
| `" Success Score"` now displays the backend's computed `validationScore` | Same visual element, now showing a real, explainable score instead of `votes*2 + comments`. |
| `handleHashChange()` now falls back to `GET /ideas/{id}` if a shared idea isn't already loaded | Makes shared links (`#idea-123`) work for ideas outside the currently loaded list - this is what `GET /ideas/{id}` is for. |
| `saveIdeas()` / `localStorage` idea persistence removed | The database is now the source of truth, so writing the whole list to `localStorage` on every click would just be a stale duplicate. Theme preference still uses `localStorage`, unchanged. |
| One line added near the top of `<body>`'s script: `const API_BASE_URL = "%VITE_API_BASE_URL%";` | This is the single point where the deployed backend URL gets wired in at build time (see "Environment variables" below). Everything else in the script is unchanged in structure. |

**Things intentionally left exactly as-is:** `TAG_TIPS`, `CAT_COLORS`,
`AVATARS` (pure styling constants, not "idea data"), the live tag-suggestion
helper while typing a description, drag-to-reorder, the typing animation,
cursor glow, ripple effects, the theme toggle, and all CSS/markup.

**Known simplification:** voting, commenting, bookmarking ("Save"), and
"Collaborate" counts are currently session-only (in-memory) interactions, not
written back to the database, since the brief's four required endpoints
don't include vote/comment endpoints. Wiring these up for real would need a
lightweight user/session model plus a couple of small additional endpoints -
a natural next step, not included here so as to not invent endpoints beyond
what was specified.

---

## 2. How idea analysis works

`POST /ideas/analyze` and `POST /ideas/save` both run every submitted idea
through `backend/app/services/orchestrator.py`, which:

1. Calls Crunchbase, Product Hunt, and Google Custom Search (each is a no-op
   if its API key isn't configured, or if the call fails for any reason -
   external outages never break the response).
2. Fills in / supplements those results with a small built-in knowledge base
   (`app/services/knowledge_base.py`) keyed by **category and keyword**, not
   by literal idea titles - so it works for any idea you type, not just a
   few demo names.
3. Computes a transparent 0-100 `validationScore` from description clarity,
   how crowded the market looks, differentiation language, and completeness
   (`app/services/heuristics.py`).
4. Generates `suggestedImprovements`, `differentiationOpportunities`, and
   `marketGaps` from a template-based heuristic engine (none of the four
   listed providers actually generate advice - they only return raw
   company/listing data, so this part is always IdeaForge's own logic).

**Without any API keys configured, the app is fully functional** - you'll
get real, varied analysis driven by the heuristic engine. Add API keys to
get live company data layered in on top.

---

## 3. Local setup

### Prerequisites
- Node.js 18+ and npm
- Python 3.11+
- A PostgreSQL database (local install, or a free Supabase/Neon project - see §5)

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env
# edit .env: set DATABASE_URL to your Postgres instance (local/Supabase/Neon)

uvicorn main:app --reload
# API now running at http://localhost:8000
# interactive docs at http://localhost:8000/docs
```

The app creates its `ideas` table automatically on first startup. If you
want a few demo ideas to start with, set `SEED_DEMO_DATA=true` in `.env`, or
run it manually:

```bash
python -m app.seed
```

### Frontend

```bash
cd frontend
npm install

cp .env.example .env
# edit .env: VITE_API_BASE_URL=http://localhost:8000

npm run dev
# open the URL Vite prints (usually http://localhost:5173)
```

That's it - same UI, now backed by a real API. Submitting an idea or
clicking "Generate AI Idea" hits the backend and persists to Postgres.

---

## 4. Environment variables

### Backend (`backend/.env`, see `backend/.env.example`)

| Variable | Required | Notes |
|---|---|---|
| `DATABASE_URL` | yes | Postgres connection string (local, Supabase, or Neon) |
| `ALLOWED_ORIGINS` | recommended | Comma-separated list of frontend origins allowed to call the API |
| `SEED_DEMO_DATA` | no | `true` to auto-insert a few demo ideas into an empty database |
| `CRUNCHBASE_API_KEY` | no | Enables live Crunchbase organization search |
| `PRODUCTHUNT_API_TOKEN` | no | Enables live Product Hunt lookups |
| `GOOGLE_API_KEY` + `GOOGLE_CSE_ID` | no | Enables live Google Custom Search |
| `CLEARBIT_API_KEY` | no | Enables Clearbit company enrichment |

### Frontend (`frontend/.env`, see `frontend/.env.example`)

| Variable | Required | Notes |
|---|---|---|
| `VITE_API_BASE_URL` | yes | URL of the running backend, e.g. `http://localhost:8000` locally or your Render/Railway URL in production |

---

## 5. Deployment

### Database → Supabase or Neon

1. Create a free project at [supabase.com](https://supabase.com) or
   [neon.tech](https://neon.tech).
2. Copy the Postgres connection string they give you (Supabase: *Project
   Settings → Database → Connection string → URI*; Neon: *Dashboard →
   Connection Details*).
3. Put it in `DATABASE_URL` for the backend (locally in `.env`, and in your
   host's environment variables once deployed).

### Backend → Render or Railway

Both platforms can deploy directly from this `backend/` folder.

**Render:**
1. New → Web Service → connect your repo, set root directory to `backend`.
2. Build command: `pip install -r requirements.txt`
3. Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT` (already in
   the included `Procfile`, so Render should pick it up automatically).
4. Add the environment variables from §4 in the Render dashboard
   (`DATABASE_URL`, `ALLOWED_ORIGINS` set to your Vercel frontend URL, and any
   external API keys you have).

**Railway:**
1. New Project → Deploy from repo → set root directory to `backend`.
2. Railway auto-detects Python; it will use the `Procfile`/`requirements.txt`
   as-is.
3. Add the same environment variables in the Railway dashboard.

Either way, once deployed you'll have a URL like
`https://ideaforge-api.onrender.com` - that's your `VITE_API_BASE_URL`.

### Frontend → Vercel

1. New Project → import your repo → set root directory to `frontend`.
2. Vercel auto-detects Vite (build command `npm run build`, output `dist`).
3. Add an environment variable `VITE_API_BASE_URL` set to your deployed
   backend URL.
4. Deploy. Once it's live, go back to your backend's `ALLOWED_ORIGINS`
   environment variable and set it to your new Vercel URL (then redeploy the
   backend) so CORS allows the request.

---

## 6. API reference

Interactive docs are auto-generated by FastAPI at `/docs` (Swagger) and
`/redoc` once the backend is running.

| Endpoint | Description |
|---|---|
| `POST /ideas/analyze` | Analyze any idea (title, description, category, tags) without saving it. Returns the full validation analysis. |
| `POST /ideas/save` | Analyze **and persist** a new idea. This is what the "Share Your Idea" form calls. |
| `GET /ideas` | List all saved ideas, newest first (filtering/sorting/search stay client-side, unchanged from the original UI). |
| `GET /ideas/{id}` | Fetch a single idea by id. |
| `POST /ideas/generate` *(bonus)* | Synthesizes, analyzes, and saves a new AI-generated idea in one call - powers the "Generate AI Idea" button. |

Example request:

```bash
curl -X POST http://localhost:8000/ideas/save \
  -H "Content-Type: application/json" \
  -d '{
    "title": "DormPilot AI",
    "description": "An AI concierge for dorm life that handles maintenance requests, roommate coordination, and student FAQs.",
    "category": "Tech",
    "tags": ["AI", "Campus", "Productivity"],
    "author": "Jordan K."
  }'
```

---

## 7. Project structure

```
backend/
├── main.py                          FastAPI app entry point
├── requirements.txt
├── .env.example
├── Procfile                         for Render/Railway
├── app/
│   ├── config.py                    settings loaded from environment variables
│   ├── database.py                  SQLAlchemy engine/session (PostgreSQL)
│   ├── models.py                    Idea ORM model
│   ├── schemas.py                   Pydantic request/response models
│   ├── seed.py                      optional demo-data seeding script
│   ├── routers/ideas.py             the 4 required endpoints + /ideas/generate
│   └── services/
│       ├── orchestrator.py          combines external APIs + heuristics
│       ├── heuristics.py            validation scoring & text generation
│       ├── knowledge_base.py        generalized fallback company/category data
│       ├── idea_generator.py        powers "Generate AI Idea"
│       └── external/                Crunchbase, Product Hunt, Google, Clearbit
└── ...

frontend/
├── index.html                       the original UI - unchanged markup/CSS
├── package.json                     npm install / npm run dev / npm run build
├── vite.config.js
└── .env.example
```
