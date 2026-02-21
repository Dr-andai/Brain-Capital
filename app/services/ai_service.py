"""AI service for generating insights."""

from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models import AIInsight
from app.schemas.insight import InsightGenerateRequest
from app.config import settings


class AIService:
    """Service for AI-powered insights."""

    def __init__(self, db: Session):
        self.db = db

    def generate_insight(self, request: InsightGenerateRequest) -> AIInsight:
        """
        Generate an AI insight based on the request.

        This is a placeholder implementation. In production, this would:
        1. Fetch relevant data from the database
        2. Build a context prompt
        3. Call OpenAI/HuggingFace API
        4. Parse and validate the response
        5. Cache the result
        """
        # Placeholder rule-based insight
        insight_text = self._generate_placeholder_insight(request)

        # Create AI insight record
        ai_insight = AIInsight(
            insight_type=request.insight_type,
            country_id=self._get_country_id(request.country_code) if request.country_code else None,
            pillar_id=request.pillar_id,
            dimension_id=request.dimension_id,
            year_start=request.year_start,
            year_end=request.year_end,
            filter_params={
                "insight_type": request.insight_type,
                "country_code": request.country_code,
                "indicator_ids": request.indicator_ids,
            },
            insight_text=insight_text,
            confidence_score=0.75,  # Placeholder confidence
            model_version="rule-based-v1",
            expires_at=datetime.utcnow() + timedelta(hours=24),
        )

        self.db.add(ai_insight)
        self.db.commit()
        self.db.refresh(ai_insight)

        return ai_insight

    def get_cached_insight(
        self,
        insight_type: str,
        country_code: str | None = None,
        indicator_ids: list[int] | None = None,
    ) -> AIInsight | None:
        """Check if a similar insight exists in cache."""
        query = self.db.query(AIInsight).filter(
            AIInsight.insight_type == insight_type,
            AIInsight.expires_at > datetime.utcnow(),
        )

        if country_code:
            country_id = self._get_country_id(country_code)
            if country_id:
                query = query.filter(AIInsight.country_id == country_id)

        return query.first()

    def submit_feedback(self, insight_id: int, rating: int) -> AIInsight | None:
        """Submit user feedback for an insight."""
        insight = self.db.query(AIInsight).filter(AIInsight.id == insight_id).first()
        if not insight:
            return None

        insight.user_feedback = rating
        self.db.commit()
        self.db.refresh(insight)

        return insight

    def _generate_placeholder_insight(self, request: InsightGenerateRequest) -> str:
        """Generate a placeholder insight (to be replaced with real AI)."""
        if request.insight_type == "country":
            return (
                f"Based on the available data for {request.country_code}, "
                f"brain capital indicators show a moderate level of development. "
                f"Key areas for improvement include education access and digital infrastructure."
            )
        elif request.insight_type == "trend":
            return (
                f"Trend analysis from {request.year_start} to {request.year_end} "
                f"indicates steady progress across most brain capital dimensions. "
                f"Notable improvements are observed in digitalization and brain health."
            )
        elif request.insight_type == "comparative":
            return (
                f"Comparative analysis reveals significant variation across regions. "
                f"High-income countries generally outperform in brain skills metrics, "
                f"while emerging economies show rapid improvement in brain capital drivers."
            )
        else:
            return (
                f"Analysis of brain capital indicators provides insights into "
                f"the overall capacity and potential of the population."
            )

    def _get_country_id(self, country_code: str) -> int | None:
        """Get country ID from country code."""
        from app.models import Country

        country = self.db.query(Country).filter(Country.code == country_code.upper()).first()
        return country.id if country else None
