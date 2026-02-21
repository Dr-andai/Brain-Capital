"""Pillar model."""

from sqlalchemy import Column, Integer, String, Text, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class Pillar(Base):
    """Pillar model - Top-level categorization."""

    __tablename__ = "pillars"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False)
    description = Column(Text)
    display_order = Column(Integer, default=0, index=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    # Relationships
    dimensions = relationship("Dimension", back_populates="pillar", cascade="all, delete-orphan")
    ai_insights = relationship("AIInsight", back_populates="pillar")

    def __repr__(self) -> str:
        return f"<Pillar(name={self.name})>"
