"""Countries API endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.country import Country, CountryList
from app.services.country_service import CountryService
from app.api.dependencies import get_country_service

router = APIRouter()


@router.get("/countries", response_model=CountryList)
async def list_countries(
    skip: int = 0,
    limit: int = 100,
    service: CountryService = Depends(get_country_service),
):
    """Get list of all countries."""
    countries = service.get_all(skip=skip, limit=limit)
    total = service.count()
    return CountryList(countries=countries, total=total)


@router.get("/countries/{country_code}", response_model=Country)
async def get_country(
    country_code: str,
    service: CountryService = Depends(get_country_service),
):
    """Get country by code."""
    country = service.get_by_code(country_code)
    if not country:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Country with code '{country_code}' not found",
        )
    return country
