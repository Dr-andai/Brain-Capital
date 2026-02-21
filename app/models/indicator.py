"""Indicator model."""

from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean, TIMESTAMP, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class Indicator(Base):
    """Indicator model - Specific measurable metrics."""

    __tablename__ = "indicators"
    __table_args__ = (
        UniqueConstraint('dimension_id', 'name', name='uq_indicator_dimension_name'),
    )

    id = Column(Integer, primary_key=True, index=True)
    dimension_id = Column(Integer, ForeignKey("dimensions.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    unit = Column(String(100))
    data_source = Column(String(255))
    methodology_url = Column(Text)
    display_order = Column(Integer, default=0, index=True)
    is_active = Column(Boolean, default=True, index=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    # Relationships
    dimension = relationship("Dimension", back_populates="indicators")
    values = relationship("IndicatorValue", back_populates="indicator", cascade="all, delete-orphan")
    ai_insights = relationship("AIInsight", back_populates="indicator")

    def __repr__(self) -> str:
        return f"<Indicator(name={self.name}, dimension_id={self.dimension_id})>"
