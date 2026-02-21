"""Indicator service."""

from sqlalchemy.orm import Session, joinedload
from app.models import Pillar, Dimension, Indicator, IndicatorValue


class IndicatorService:
    """Service for indicator operations."""

    def __init__(self, db: Session):
        self.db = db

    # Pillar operations
    def get_all_pillars(self) -> list[Pillar]:
        """Get all pillars."""
        return self.db.query(Pillar).order_by(Pillar.display_order, Pillar.name).all()

    def get_pillar_by_id(self, pillar_id: int) -> Pillar | None:
        """Get pillar by ID."""
        return self.db.query(Pillar).filter(Pillar.id == pillar_id).first()

    # Dimension operations
    def get_dimensions_by_pillar(self, pillar_id: int) -> list[Dimension]:
        """Get dimensions for a specific pillar."""
        return (
            self.db.query(Dimension)
            .filter(Dimension.pillar_id == pillar_id)
            .order_by(Dimension.display_order, Dimension.name)
            .all()
        )

    def get_dimension_by_id(self, dimension_id: int) -> Dimension | None:
        """Get dimension by ID."""
        return (
            self.db.query(Dimension)
            .options(joinedload(Dimension.pillar))
            .filter(Dimension.id == dimension_id)
            .first()
        )

    # Indicator operations
    def get_indicators_by_dimension(self, dimension_id: int) -> list[Indicator]:
        """Get indicators for a specific dimension."""
        return (
            self.db.query(Indicator)
            .filter(Indicator.dimension_id == dimension_id)
            .filter(Indicator.is_active == True)
            .order_by(Indicator.display_order, Indicator.name)
            .all()
        )

    def get_indicator_by_id(self, indicator_id: int) -> Indicator | None:
        """Get indicator by ID with full relationships."""
        return (
            self.db.query(Indicator)
            .options(
                joinedload(Indicator.dimension).joinedload(Dimension.pillar)
            )
            .filter(Indicator.id == indicator_id)
            .first()
        )

    def get_all_active_indicators(self) -> list[Indicator]:
        """Get all active indicators."""
        return (
            self.db.query(Indicator)
            .filter(Indicator.is_active == True)
            .order_by(Indicator.display_order, Indicator.name)
            .all()
        )

    # Indicator value operations
    def get_indicator_values(
        self,
        indicator_id: int | None = None,
        country_id: int | None = None,
        year: int | None = None,
        year_start: int | None = None,
        year_end: int | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[IndicatorValue]:
        """Get indicator values with filters."""
        query = self.db.query(IndicatorValue)

        if indicator_id:
            query = query.filter(IndicatorValue.indicator_id == indicator_id)
        if country_id:
            query = query.filter(IndicatorValue.country_id == country_id)
        if year:
            query = query.filter(IndicatorValue.year == year)
        if year_start:
            query = query.filter(IndicatorValue.year >= year_start)
        if year_end:
            query = query.filter(IndicatorValue.year <= year_end)

        return query.offset(offset).limit(limit).all()
