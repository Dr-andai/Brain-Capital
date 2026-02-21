"""Country model."""

from sqlalchemy import Column, Integer, String, BigInteger, DECIMAL, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class Country(Base):
    """Country model."""

    __tablename__ = "countries"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(3), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    region = Column(String(100), index=True)
    latitude = Column(DECIMAL(9, 6))
    longitude = Column(DECIMAL(9, 6))
    population = Column(BigInteger)
    gdp_usd = Column(DECIMAL(15, 2))
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    # Relationships
    indicator_values = relationship("IndicatorValue", back_populates="country", cascade="all, delete-orphan")
    ai_insights = relationship("AIInsight", back_populates="country", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Country(code={self.code}, name={self.name})>"
