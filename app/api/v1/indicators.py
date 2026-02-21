"""Indicators API endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from app.schemas.indicator import (
    Pillar,
    Dimension,
    Indicator,
    IndicatorValueWithDetails,
)
from app.schemas.filter import FilterParams, MapDataParams
from app.services.indicator_service import IndicatorService
from app.services.filter_service import FilterService
from app.api.dependencies import get_indicator_service, get_filter_service

router = APIRouter()


# Pillar endpoints
@router.get("/pillars", response_model=list[Pillar])
async def list_pillars(
    service: IndicatorService = Depends(get_indicator_service),
):
    """Get list of all pillars."""
    return service.get_all_pillars()


@router.get("/pillars/{pillar_id}/dimensions", response_model=list[Dimension])
async def get_pillar_dimensions(
    pillar_id: int,
    service: IndicatorService = Depends(get_indicator_service),
):
    """Get dimensions for a specific pillar."""
    pillar = service.get_pillar_by_id(pillar_id)
    if not pillar:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pillar with ID {pillar_id} not found",
        )
    return service.get_dimensions_by_pillar(pillar_id)


# Dimension endpoints
@router.get("/dimensions/{dimension_id}/indicators", response_model=list[Indicator])
async def get_dimension_indicators(
    dimension_id: int,
    service: IndicatorService = Depends(get_indicator_service),
):
    """Get indicators for a specific dimension."""
    dimension = service.get_dimension_by_id(dimension_id)
    if not dimension:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Dimension with ID {dimension_id} not found",
        )
    return service.get_indicators_by_dimension(dimension_id)


# Indicator endpoints
@router.get("/indicators", response_model=list[Indicator])
async def list_indicators(
    service: IndicatorService = Depends(get_indicator_service),
):
    """Get list of all active indicators."""
    return service.get_all_active_indicators()


@router.get("/indicators/{indicator_id}", response_model=Indicator)
async def get_indicator(
    indicator_id: int,
    service: IndicatorService = Depends(get_indicator_service),
):
    """Get indicator by ID."""
    indicator = service.get_indicator_by_id(indicator_id)
    if not indicator:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Indicator with ID {indicator_id} not found",
        )
    return indicator


# Indicator values with filtering
@router.get("/indicators/values")
async def get_indicator_values(
    pillar_id: int | None = Query(None),
    dimension_id: int | None = Query(None),
    indicator_id: int | None = Query(None),
    country_codes: str | None = Query(None, description="Comma-separated country codes"),
    year_start: int | None = Query(None, ge=1900, le=2100),
    year_end: int | None = Query(None, ge=1900, le=2100),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    service: FilterService = Depends(get_filter_service),
):
    """Get indicator values with comprehensive filtering."""
    filters = FilterParams(
        pillar_id=pillar_id,
        dimension_id=dimension_id,
        indicator_id=indicator_id,
        country_codes=country_codes,
        year_start=year_start,
        year_end=year_end,
        limit=limit,
        offset=offset,
    )

    data = service.get_filtered_indicator_values(filters)
    total = service.count_filtered_values(filters)

    return {
        "data": data,
        "total": total,
        "filters": filters.model_dump(),
    }


# Map data endpoint
@router.get("/map/data")
async def get_map_data(
    indicator_id: int = Query(..., description="Indicator ID"),
    year: int = Query(..., ge=1900, le=2100, description="Year"),
    service: FilterService = Depends(get_filter_service),
):
    """Get map visualization data for a specific indicator and year."""
    data = service.get_map_data(indicator_id, year)

    return {
        "indicator_id": indicator_id,
        "year": year,
        "data": data,
        "total": len(data),
    }
