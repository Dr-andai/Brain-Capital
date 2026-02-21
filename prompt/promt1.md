You are an experienced senior software architect and full-stack developer.

Your task is to design and scaffold an MVP for a “Brain Capital Intelligence Platform.”

This is not a toy demo. It should be realistic, scalable, and production-oriented — but minimal enough to ship quickly.

-----------------------------------------
PROJECT CONTEXT
-----------------------------------------

We are building a Brain Capital Intelligence Platform that:

- Visualizes country-level indicators
- Allows filtering by:
    - Pillar (e.g., Brain Capital Drivers, Brain Health, Brain Skills)
    - Dimension (e.g., Digitalization, Education, etc.)
    - Indicator
    - Year
- Displays data on an interactive map
- Provides AI-generated insights based on selected filters
- Is SEO-friendly
- Is backend-driven (not a heavy React SPA)

We prefer:

- FastAPI (Python)
- Jinja2 templates
- htmx for dynamic interactivity
- Leaflet (or similar lightweight map library)
- PostgreSQL as the primary database
- Clean API-first architecture
- Easy future AI integration

-----------------------------------------
ARCHITECTURE REQUIREMENTS
-----------------------------------------

1. Must be SEO-friendly:
   - Server-rendered initial HTML
   - URL-state-based filtering
   - Crawlable routes

2. Must support:
   - Country-level indicator data
   - Multiple years
   - Multiple pillars and dimensions
   - Easy addition of new indicators

3. Must be structured to:
   - Add authentication later
   - Add role-based dashboards later
   - Add data export (CSV) later
   - Add AI insights per country or per filter selection

4. Must prioritize PostgreSQL schema design for:
   - Indicators
   - Dimensions
   - Pillars
   - Countries
   - Yearly values
   - AI insight logs (future-ready)

-----------------------------------------
DELIVERABLES
-----------------------------------------

Provide:

1. High-level system architecture diagram (in text form)
2. Database schema (PostgreSQL) with:
   - Table definitions
   - Primary keys
   - Foreign keys
   - Indexing strategy
3. Folder structure for the FastAPI project
4. Example API endpoints:
   - Fetch indicator data
   - Fetch country data
   - AI insight endpoint
5. Example htmx usage for:
   - Filter update
   - Map update
   - AI insight panel update
6. Minimal MVP roadmap:
   - Phase 1: Core map + filtering
   - Phase 2: AI integration
   - Phase 3: Scaling

-----------------------------------------
CONSTRAINTS
-----------------------------------------

- Do NOT recommend React unless absolutely necessary.
- Prefer simplicity over overengineering.
- Avoid microservices for MVP.
- Assume a small technical team (1–2 developers).
- Must be deployable via Docker.
- Must be compatible with future ML/LLM integration (e.g., HuggingFace or local models).

-----------------------------------------
GOAL
-----------------------------------------

Design a Brain Capital Intelligence Platform MVP that can realistically be built in 6–8 weeks and scaled later into a global data + AI system.

Be concrete, specific, and practical.

The long-term goal is to integrate this platform with AI-driven analytics, 
including country-level insight generation, trend analysis, and policy 
recommendation summaries.

Design with this evolution in mind.
