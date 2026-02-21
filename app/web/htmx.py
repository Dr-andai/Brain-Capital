"""htmx-specific endpoints for dynamic updates."""

from fastapi import APIRouter, Request, Depends, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.indicator_service import IndicatorService
from app.services.filter_service import FilterService
from app.services.ai_service import AIService
from app.schemas.filter import FilterParams
from app.schemas.insight import InsightGenerateRequest

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/dimensions", response_class=HTMLResponse)
async def get_dimensions(
    request: Request,
    pillar_id: int = Query(...),
    db: Session = Depends(get_db)
):
    """Get dimensions for a pillar (htmx endpoint)."""
    service = IndicatorService(db)
    dimensions = service.get_dimensions_by_pillar(pillar_id)

    # Return just the select element
    html = '<select id="dimension-select" name="dimension_id" hx-get="/htmx/indicators" hx-target="#indicator-select-container" hx-trigger="change">'
    html += '<option value="">All Dimensions</option>'
    for dimension in dimensions:
        html += f'<option value="{dimension.id}">{dimension.name}</option>'
    html += '</select>'

    return HTMLResponse(content=html)


@router.get("/indicators", response_class=HTMLResponse)
async def get_indicators(
    request: Request,
    dimension_id: int = Query(...),
    db: Session = Depends(get_db)
):
    """Get indicators for a dimension (htmx endpoint)."""
    service = IndicatorService(db)
    indicators = service.get_indicators_by_dimension(dimension_id)

    # Return just the select element
    html = '<select id="indicator-select" name="indicator_id">'
    html += '<option value="">All Indicators</option>'
    for indicator in indicators:
        html += f'<option value="{indicator.id}">{indicator.name}</option>'
    html += '</select>'

    return HTMLResponse(content=html)


@router.get("/filter-results", response_class=HTMLResponse)
async def get_filter_results(
    request: Request,
    pillar_id: int | None = Query(None),
    dimension_id: int | None = Query(None),
    indicator_id: int | None = Query(None),
    year: int = Query(2023),
    db: Session = Depends(get_db)
):
    """Get filtered map data (htmx endpoint)."""
    if not indicator_id:
        # If no indicator selected, return empty map
        return templates.TemplateResponse(
            "partials/filter_results.html",
            {
                "request": request,
                "map_data": [],
                "total": 0,
            }
        )

    # Get map data
    filter_service = FilterService(db)
    map_data = filter_service.get_map_data(indicator_id, year)

    # Get indicator name
    indicator_service = IndicatorService(db)
    indicator = indicator_service.get_indicator_by_id(indicator_id)
    indicator_name = indicator.name if indicator else None

    return templates.TemplateResponse(
        "partials/filter_results.html",
        {
            "request": request,
            "map_data": map_data,
            "indicator_name": indicator_name,
            "total": len(map_data),
        }
    )


@router.post("/insights/generate", response_class=HTMLResponse)
async def generate_insight(
    request: Request,
    insight_type: str = Query("country"),
    country_code: str | None = Query(None),
    indicator_id: int | None = Query(None),
    year_start: int | None = Query(None),
    year_end: int | None = Query(None),
    db: Session = Depends(get_db)
):
    """Generate AI insight (htmx endpoint)."""
    service = AIService(db)

    # Create request
    insight_request = InsightGenerateRequest(
        insight_type=insight_type,
        country_code=country_code,
        indicator_ids=[indicator_id] if indicator_id else None,
        year_start=year_start,
        year_end=year_end,
    )

    # Generate insight
    insight = service.generate_insight(insight_request)

    return templates.TemplateResponse(
        "partials/insight_content.html",
        {
            "request": request,
            "insight": insight,
        }
    )


@router.post("/insights/{insight_id}/feedback", response_class=HTMLResponse)
async def submit_feedback(
    request: Request,
    insight_id: int,
    rating: int = Query(..., ge=1, le=5),
    db: Session = Depends(get_db)
):
    """Submit feedback for an insight (htmx endpoint)."""
    service = AIService(db)
    service.submit_feedback(insight_id, rating)

    # Return a simple confirmation message
    return HTMLResponse(content='<p class="feedback-success">✓ Thank you for your feedback!</p>')
