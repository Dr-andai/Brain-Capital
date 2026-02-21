"""Country schemas."""

from decimal import Decimal
from datetime import datetime
from pydantic import BaseModel, Field


class CountryBase(BaseModel):
    """Base country schema."""
    code: str = Field(..., min_length=2, max_length=3)
    name: str = Field(..., min_length=1, max_length=255)
    region: str | None = None
    latitude: Decimal | None = None
    longitude: Decimal | None = None
    population: int | None = None
    gdp_usd: Decimal | None = None


class CountryCreate(CountryBase):
    """Schema for creating a country."""
    pass


class CountryUpdate(BaseModel):
    """Schema for updating a country."""
    name: str | None = None
    region: str | None = None
    latitude: Decimal | None = None
    longitude: Decimal | None = None
    population: int | None = None
    gdp_usd: Decimal | None = None


class Country(CountryBase):
    """Country response schema."""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CountryList(BaseModel):
    """Schema for country list response."""
    countries: list[Country]
    total: int
