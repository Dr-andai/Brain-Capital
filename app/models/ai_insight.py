"""AI Insight model."""

from sqlalchemy import Column, Integer, String, Text, ForeignKey, DECIMAL, TIMESTAMP, Index
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class AIInsight(Base):
    """AI Insight model - AI-generated insights."""

    __tablename__ = "ai_insights"
    __table_args__ = (
        Index('idx_ai_insights_filter_params', 'filter_params', postgresql_using='gin'),
    )

    id = Column(Integer, primary_key=True, index=True)
    insight_type = Column(String(50), nullable=False, index=True)
    country_id = Column(Integer, ForeignKey("countries.id", ondelete="CASCADE"), index=True)
    indicator_id = Column(Integer, ForeignKey("indicators.id", ondelete="CASCADE"), index=True)
    pillar_id = Column(Integer, ForeignKey("pillars.id", ondelete="CASCADE"))
    dimension_id = Column(Integer, ForeignKey("dimensions.id", ondelete="CASCADE"))
    year_start = Column(Integer)
    year_end = Column(Integer)
    filter_params = Column(JSONB)
    insight_text = Column(Text, nullable=False)
    confidence_score = Column(DECIMAL(3, 2))
    model_version = Column(String(100))
    generated_at = Column(TIMESTAMP, server_default=func.now(), index=True)
    expires_at = Column(TIMESTAMP)
    user_feedback = Column(Integer)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    # Relationships
    country = relationship("Country", back_populates="ai_insights")
    indicator = relationship("Indicator", back_populates="ai_insights")
    pillar = relationship("Pillar", back_populates="ai_insights")
    dimension = relationship("Dimension", back_populates="ai_insights")

    def __repr__(self) -> str:
        return f"<AIInsight(type={self.insight_type}, country_id={self.country_id})>"
