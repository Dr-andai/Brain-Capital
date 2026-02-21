"""AI Insights API endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.insight import (
    InsightGenerateRequest,
    Insight,
    InsightFeedback,
)
from app.services.ai_service import AIService
from app.api.dependencies import get_ai_service

router = APIRouter()


@router.post("/insights/generate", response_model=Insight, status_code=status.HTTP_201_CREATED)
async def generate_insight(
    request: InsightGenerateRequest,
    service: AIService = Depends(get_ai_service),
):
    """
    Generate an AI insight based on filters.

    This endpoint generates context-aware insights using AI models.
    Results are cached for 24 hours to improve performance.
    """
    # Check for cached insight first
    cached = service.get_cached_insight(
        insight_type=request.insight_type,
        country_code=request.country_code,
        indicator_ids=request.indicator_ids,
    )

    if cached:
        return cached

    # Generate new insight
    insight = service.generate_insight(request)
    return insight


@router.get("/insights/{insight_id}", response_model=Insight)
async def get_insight(
    insight_id: int,
    service: AIService = Depends(get_ai_service),
):
    """Get a specific insight by ID."""
    from app.models import AIInsight

    insight = service.db.query(AIInsight).filter(AIInsight.id == insight_id).first()
    if not insight:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Insight with ID {insight_id} not found",
        )
    return insight


@router.post("/insights/{insight_id}/feedback", response_model=Insight)
async def submit_insight_feedback(
    insight_id: int,
    feedback: InsightFeedback,
    service: AIService = Depends(get_ai_service),
):
    """Submit user feedback for an insight (1-5 stars)."""
    insight = service.submit_feedback(insight_id, feedback.rating)
    if not insight:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Insight with ID {insight_id} not found",
        )
    return insight
