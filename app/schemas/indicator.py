"""Indicator schemas."""

from decimal import Decimal
from datetime import datetime
from pydantic import BaseModel, Field


class PillarBase(BaseModel):
    """Base pillar schema."""
    name: str = Field(..., min_length=1, max_length=255)
    description: str | None = None
    display_order: int = 0


class Pillar(PillarBase):
    """Pillar response schema."""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class DimensionBase(BaseModel):
    """Base dimension schema."""
    pillar_id: int
    name: str = Field(..., min_length=1, max_length=255)
    description: str | None = None
    display_order: int = 0


class Dimension(DimensionBase):
    """Dimension response schema."""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class DimensionWithPillar(Dimension):
    """Dimension with pillar information."""
    pillar: Pillar


class IndicatorBase(BaseModel):
    """Base indicator schema."""
    dimension_id: int
    name: str = Field(..., min_length=1, max_length=255)
    description: str | None = None
    unit: str | None = None
    data_source: str | None = None
    methodology_url: str | None = None
    display_order: int = 0
    is_active: bool = True


class Indicator(IndicatorBase):
    """Indicator response schema."""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class IndicatorWithRelations(Indicator):
    """Indicator with dimension and pillar information."""
    dimension: DimensionWithPillar


class IndicatorValueBase(BaseModel):
    """Base indicator value schema."""
    country_id: int
    indicator_id: int
    year: int = Field(..., ge=1900, le=2100)
    value: Decimal | None = None
    confidence_score: Decimal | None = Field(None, ge=0, le=1)
    notes: str | None = None


class IndicatorValue(IndicatorValueBase):
    """Indicator value response schema."""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class IndicatorValueWithDetails(BaseModel):
    """Indicator value with country and indicator details."""
    id: int
    country_code: str
    country_name: str
    indicator_name: str
    dimension_name: str
    pillar_name: str
    year: int
    value: Decimal | None
    unit: str | None
    confidence_score: Decimal | None

    class Config:
        from_attributes = True
