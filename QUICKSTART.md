# Quick Start Guide

## Brain Capital Intelligence Platform MVP

All 15 tasks completed! Here's how to get started.

## Prerequisites

- Docker and Docker Compose installed
- Python 3.13+ (optional, for local development)

## Installation & Setup

### Option 1: Docker (Recommended)

1. **Copy environment file**
   ```bash
   cp .env.example .env
   ```

2. **Start PostgreSQL and Redis**
   ```bash
   docker-compose up -d db redis
   ```

3. **Wait for database to be ready** (about 10 seconds)
   ```bash
   sleep 10
   ```

4. **Run database migrations**
   ```bash
   uv run alembic upgrade head
   ```

5. **Seed the database with sample data**
   ```bash
   uv run python scripts/seed_database.py
   ```

6. **Start the web application**
   ```bash
   uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

### Option 2: Full Docker Compose (if you have Docker Compose working)

```bash
cp .env.example .env
docker-compose up -d
docker-compose exec web alembic upgrade head
docker-compose exec web python scripts/seed_database.py
```

## Access the Application

- **Web UI**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/api/health

## Test the Application

### 1. Test API Endpoints

```bash
# Get all countries
curl http://localhost:8000/api/v1/countries

# Get all pillars
curl http://localhost:8000/api/v1/pillars

# Get filtered indicator values
curl "http://localhost:8000/api/v1/indicators/values?year=2023&limit=10"

# Get map data
curl "http://localhost:8000/api/v1/map/data?indicator_id=1&year=2023"
```

### 2. Test Web Interface

1. Open http://localhost:8000 in your browser
2. Select a **Pillar** from the dropdown (e.g., "Brain Capital Drivers")
3. Select a **Dimension** (e.g., "Digitalization")
4. Select an **Indicator** (e.g., "Digital Infrastructure Index")
5. Select a **Year** (e.g., "2023")
6. The map will update automatically with data points
7. Click **"Generate Insight"** to get AI-powered analysis

## What's Included

### Backend (Fully Functional)
✅ FastAPI application with REST API
✅ PostgreSQL database with 6 tables
✅ SQLAlchemy models with relationships
✅ Alembic migrations
✅ Pydantic schemas for validation
✅ Service layer with business logic
✅ Cascading filter logic (Pillar → Dimension → Indicator)
✅ AI insight generation (placeholder implementation)

### Frontend (Fully Functional)
✅ Jinja2 templates (base, index, components, partials)
✅ Leaflet.js map visualization
✅ htmx-powered dynamic updates
✅ Responsive CSS design
✅ Filter interactions without page reload
✅ AI insight panel

### Sample Data
✅ 10 countries (USA, UK, Germany, France, Japan, China, India, Brazil, Australia, Canada)
✅ 3 pillars (Brain Capital Drivers, Brain Health, Brain Skills)
✅ 6 dimensions
✅ 6 indicators
✅ 240 indicator values (10 countries × 6 indicators × 4 years)

## Project Structure

```
brain-capital/
├── app/
│   ├── api/v1/              # API endpoints ✅
│   ├── core/                # Configuration, database, logging ✅
│   ├── models/              # SQLAlchemy models ✅
│   ├── schemas/             # Pydantic schemas ✅
│   ├── services/            # Business logic ✅
│   ├── templates/           # Jinja2 templates ✅
│   ├── static/              # CSS, JavaScript ✅
│   ├── web/                 # Web routes + htmx ✅
│   ├── config.py            # Settings ✅
│   └── main.py              # FastAPI app ✅
├── alembic/                 # Database migrations ✅
├── scripts/                 # Seed script ✅
├── Dockerfile               # Docker configuration ✅
├── docker-compose.yml       # Multi-container setup ✅
└── pyproject.toml           # Dependencies ✅
```

## API Endpoints

### Core API
- `GET /api/v1/countries` - List all countries
- `GET /api/v1/countries/{code}` - Get country details
- `GET /api/v1/pillars` - List all pillars
- `GET /api/v1/pillars/{id}/dimensions` - Get dimensions for pillar
- `GET /api/v1/dimensions/{id}/indicators` - Get indicators for dimension
- `GET /api/v1/indicators/values` - Get filtered indicator values
- `GET /api/v1/map/data` - Get map visualization data
- `POST /api/v1/insights/generate` - Generate AI insight

### htmx Endpoints
- `GET /htmx/dimensions?pillar_id={id}` - Dynamic dimension select
- `GET /htmx/indicators?dimension_id={id}` - Dynamic indicator select
- `GET /htmx/filter-results` - Update map based on filters
- `POST /htmx/insights/generate` - Generate insight

## Development

### Install dependencies locally
```bash
uv sync
```

### Run tests (when implemented)
```bash
uv run pytest
```

### Code formatting
```bash
uv run black app/
uv run ruff app/
```

## Troubleshooting

### Database connection errors
- Make sure PostgreSQL is running: `docker-compose ps`
- Check logs: `docker-compose logs db`
- Verify DATABASE_URL in .env

### Port already in use
```bash
# Change port in docker-compose.yml or run on different port
uv run uvicorn app.main:app --reload --port 8001
```

### Map not loading
- Check browser console for JavaScript errors
- Verify static files are being served: http://localhost:8000/static/js/map.js
- Ensure Leaflet CDN is accessible

## Next Steps

### Phase 2: AI Integration (Weeks 5-6)
- Replace placeholder AI service with OpenAI/HuggingFace integration
- Add API key configuration
- Implement more sophisticated insight generation
- Add insight caching with Redis

### Phase 3: Production Readiness (Weeks 7-8)
- Add Redis caching for API responses
- Implement rate limiting
- Add comprehensive tests
- Security hardening
- Deployment documentation

## Support

For issues or questions:
- Check the logs: `docker-compose logs web`
- Review the plan: `.claude/plans/fancy-twirling-fern.md`
- Check API docs: http://localhost:8000/docs

## Success! 🎉

You now have a fully functional Brain Capital Intelligence Platform MVP with:
- Interactive map visualization
- Multi-level cascading filters
- htmx-powered dynamic updates
- AI insight generation (placeholder)
- RESTful API
- SEO-friendly server-rendered pages
- Docker containerization
- Sample data for testing

Happy developing!
