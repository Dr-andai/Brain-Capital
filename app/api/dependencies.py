"""API dependencies."""

from fastapi import Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.country_service import CountryService
from app.services.indicator_service import IndicatorService
from app.services.filter_service import FilterService
from app.services.ai_service import AIService


def get_country_service(db: Session = Depends(get_db)) -> CountryService:
    """Get country service dependency."""
    return CountryService(db)


def get_indicator_service(db: Session = Depends(get_db)) -> IndicatorService:
    """Get indicator service dependency."""
    return IndicatorService(db)


def get_filter_service(db: Session = Depends(get_db)) -> FilterService:
    """Get filter service dependency."""
    return FilterService(db)


def get_ai_service(db: Session = Depends(get_db)) -> AIService:
    """Get AI service dependency."""
    return AIService(db)
