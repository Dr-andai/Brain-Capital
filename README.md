# Brain Capital Intelligence Platform MVP

A production-ready platform for visualizing country-level brain capital indicators with AI-driven insights.

## Features

- **Interactive Map Visualization** - Leaflet.js-powered maps showing country-level data
- **Multi-level Filtering** - Filter by Pillar → Dimension → Indicator → Year
- **AI-Generated Insights** - Context-aware insights using LLMs (future-ready)
- **SEO-Friendly** - Server-side rendering with URL-based state
- **htmx-Powered** - Dynamic updates without full page reloads
- **Production-Ready** - Docker containerization, health checks, structured logging

## Tech Stack

- **Backend**: FastAPI (Python 3.13)
- **Database**: PostgreSQL 16
- **ORM**: SQLAlchemy + Alembic
- **Templates**: Jinja2
- **Frontend**: htmx + Leaflet.js
- **Caching**: Redis
- **Package Manager**: uv

## Quick Start

### Prerequisites

- Docker & Docker Compose
- Python 3.13+ (for local development)
- uv package manager

### Installation

1. **Create environment file**
   \`\`\`bash
   cp .env.example .env
   # Edit .env with your configuration
   \`\`\`

2. **Start services with Docker Compose**
   \`\`\`bash
   docker-compose up -d
   \`\`\`

3. **Run database migrations**
   \`\`\`bash
   uv run alembic upgrade head
   \`\`\`

4. **Access the application**
   - Web UI: http://localhost:8000
   - API Docs: http://localhost:8000/docs
   - Health Check: http://localhost:8000/api/health

## Development

### Local Development (without Docker)

1. **Install dependencies**
   \`\`\`bash
   uv sync
   \`\`\`

2. **Start PostgreSQL and Redis**
   \`\`\`bash
   docker-compose up -d db redis
   \`\`\`

3. **Run migrations**
   \`\`\`bash
   uv run alembic upgrade head
   \`\`\`

4. **Start development server**
   \`\`\`bash
   uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   \`\`\`

## Project Structure

See the plan file for detailed architecture and implementation guide.

## License

[Add your license here]
