"""Dimension model."""

from sqlalchemy import Column, Integer, String, Text, ForeignKey, TIMESTAMP, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class Dimension(Base):
    """Dimension model - Sub-categories within pillars."""

    __tablename__ = "dimensions"
    __table_args__ = (
        UniqueConstraint('pillar_id', 'name', name='uq_dimension_pillar_name'),
    )

    id = Column(Integer, primary_key=True, index=True)
    pillar_id = Column(Integer, ForeignKey("pillars.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    display_order = Column(Integer, default=0, index=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    # Relationships
    pillar = relationship("Pillar", back_populates="dimensions")
    indicators = relationship("Indicator", back_populates="dimension", cascade="all, delete-orphan")
    ai_insights = relationship("AIInsight", back_populates="dimension")

    def __repr__(self) -> str:
        return f"<Dimension(name={self.name}, pillar_id={self.pillar_id})>"
