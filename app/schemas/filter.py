"""Filter schemas."""

from pydantic import BaseModel, Field


class FilterParams(BaseModel):
    """Query parameters for filtering indicator data."""
    pillar_id: int | None = None
    dimension_id: int | None = None
    indicator_id: int | None = None
    country_codes: str | None = Field(None, description="Comma-separated country codes")
    year_start: int | None = Field(None, ge=1900, le=2100)
    year_end: int | None = Field(None, ge=1900, le=2100)
    limit: int = Field(100, ge=1, le=1000)
    offset: int = Field(0, ge=0)

    @property
    def country_code_list(self) -> list[str] | None:
        """Parse country_codes into a list."""
        if self.country_codes:
            return [code.strip().upper() for code in self.country_codes.split(",")]
        return None


class MapDataParams(BaseModel):
    """Query parameters for map visualization data."""
    indicator_id: int
    year: int = Field(..., ge=1900, le=2100)
