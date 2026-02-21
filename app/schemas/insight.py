"""AI Insight schemas."""

from decimal import Decimal
from datetime import datetime
from pydantic import BaseModel, Field


class InsightGenerateRequest(BaseModel):
    """Request schema for generating AI insights."""
    insight_type: str = Field(..., description="Type: country, indicator, comparative, trend")
    country_code: str | None = Field(None, max_length=3)
    indicator_ids: list[int] | None = None
    pillar_id: int | None = None
    dimension_id: int | None = None
    year_start: int | None = Field(None, ge=1900, le=2100)
    year_end: int | None = Field(None, ge=1900, le=2100)


class InsightBase(BaseModel):
    """Base insight schema."""
    insight_type: str
    insight_text: str
    confidence_score: Decimal | None = None
    model_version: str | None = None


class Insight(InsightBase):
    """Insight response schema."""
    id: int
    country_id: int | None
    indicator_id: int | None
    pillar_id: int | None
    dimension_id: int | None
    year_start: int | None
    year_end: int | None
    generated_at: datetime
    expires_at: datetime | None
    user_feedback: int | None

    class Config:
        from_attributes = True


class InsightFeedback(BaseModel):
    """Schema for submitting insight feedback."""
    rating: int = Field(..., ge=1, le=5, description="Rating from 1 to 5 stars")
