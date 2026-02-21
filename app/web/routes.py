"""SEO-friendly web page routes."""

from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.indicator_service import IndicatorService

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
async def index(request: Request, db: Session = Depends(get_db)):
    """Homepage with interactive map and filters."""
    service = IndicatorService(db)
    pillars = service.get_all_pillars()

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "pillars": pillars,
            "map_data": [],
        }
    )


@router.get("/countries", response_class=HTMLResponse)
async def countries_list(request: Request):
    """Countries list page."""
    # TODO: Implement countries list page
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )


@router.get("/countries/{country_code}", response_class=HTMLResponse)
async def country_detail(request: Request, country_code: str):
    """Country detail page."""
    # TODO: Implement country detail page
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )


@router.get("/indicators", response_class=HTMLResponse)
async def indicators_list(request: Request):
    """Indicators list page."""
    # TODO: Implement indicators list page
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )
