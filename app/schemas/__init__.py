"""Pydantic schemas."""

from app.schemas.country import (
    Country,
    CountryCreate,
    CountryUpdate,
    CountryList,
)
from app.schemas.indicator import (
    Pillar,
    Dimension,
    DimensionWithPillar,
    Indicator,
    IndicatorWithRelations,
    IndicatorValue,
    IndicatorValueWithDetails,
)
from app.schemas.filter import FilterParams, MapDataParams
from app.schemas.insight import (
    InsightGenerateRequest,
    Insight,
    InsightFeedback,
)

__all__ = [
    # Country
    "Country",
    "CountryCreate",
    "CountryUpdate",
    "CountryList",
    # Indicator
    "Pillar",
    "Dimension",
    "DimensionWithPillar",
    "Indicator",
    "IndicatorWithRelations",
    "IndicatorValue",
    "IndicatorValueWithDetails",
    # Filter
    "FilterParams",
    "MapDataParams",
    # Insight
    "InsightGenerateRequest",
    "Insight",
    "InsightFeedback",
]
