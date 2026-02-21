"""Indicator value model."""

from sqlalchemy import Column, Integer, ForeignKey, DECIMAL, Text, TIMESTAMP, UniqueConstraint, Index
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class IndicatorValue(Base):
    """Indicator value model - Actual data values for each country/indicator/year."""

    __tablename__ = "indicator_values"
    __table_args__ = (
        UniqueConstraint('country_id', 'indicator_id', 'year', name='uq_indicator_value'),
        Index('idx_indicator_values_composite', 'country_id', 'indicator_id', 'year'),
    )

    id = Column(Integer, primary_key=True, index=True)
    country_id = Column(Integer, ForeignKey("countries.id", ondelete="CASCADE"), nullable=False, index=True)
    indicator_id = Column(Integer, ForeignKey("indicators.id", ondelete="CASCADE"), nullable=False, index=True)
    year = Column(Integer, nullable=False, index=True)
    value = Column(DECIMAL(15, 4))
    confidence_score = Column(DECIMAL(3, 2))
    notes = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    # Relationships
    country = relationship("Country", back_populates="indicator_values")
    indicator = relationship("Indicator", back_populates="values")

    def __repr__(self) -> str:
        return f"<IndicatorValue(country_id={self.country_id}, indicator_id={self.indicator_id}, year={self.year}, value={self.value})>"
