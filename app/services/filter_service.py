"""Filter service with cascading logic."""

from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_
from app.models import Country, Pillar, Dimension, Indicator, IndicatorValue
from app.schemas.filter import FilterParams


class FilterService:
    """Service for cascading filter operations."""

    def __init__(self, db: Session):
        self.db = db

    def get_filtered_indicator_values(self, filters: FilterParams) -> list[dict]:
        """
        Get indicator values with comprehensive filtering and full details.

        Returns a list of dictionaries with all relevant information.
        """
        query = (
            self.db.query(
                IndicatorValue.id,
                Country.code.label("country_code"),
                Country.name.label("country_name"),
                Country.latitude,
                Country.longitude,
                Indicator.name.label("indicator_name"),
                Indicator.unit,
                Dimension.name.label("dimension_name"),
                Pillar.name.label("pillar_name"),
                IndicatorValue.year,
                IndicatorValue.value,
                IndicatorValue.confidence_score,
            )
            .join(Country, IndicatorValue.country_id == Country.id)
            .join(Indicator, IndicatorValue.indicator_id == Indicator.id)
            .join(Dimension, Indicator.dimension_id == Dimension.id)
            .join(Pillar, Dimension.pillar_id == Pillar.id)
            .filter(Indicator.is_active == True)
        )

        # Apply filters
        if filters.pillar_id:
            query = query.filter(Pillar.id == filters.pillar_id)

        if filters.dimension_id:
            query = query.filter(Dimension.id == filters.dimension_id)

        if filters.indicator_id:
            query = query.filter(Indicator.id == filters.indicator_id)

        if filters.country_code_list:
            query = query.filter(Country.code.in_(filters.country_code_list))

        if filters.year_start:
            query = query.filter(IndicatorValue.year >= filters.year_start)

        if filters.year_end:
            query = query.filter(IndicatorValue.year <= filters.year_end)

        # Apply pagination
        query = query.offset(filters.offset).limit(filters.limit)

        # Execute and convert to dictionaries
        results = query.all()
        return [
            {
                "id": row.id,
                "country_code": row.country_code,
                "country_name": row.country_name,
                "latitude": float(row.latitude) if row.latitude else None,
                "longitude": float(row.longitude) if row.longitude else None,
                "indicator_name": row.indicator_name,
                "unit": row.unit,
                "dimension_name": row.dimension_name,
                "pillar_name": row.pillar_name,
                "year": row.year,
                "value": float(row.value) if row.value else None,
                "confidence_score": float(row.confidence_score) if row.confidence_score else None,
            }
            for row in results
        ]

    def get_map_data(self, indicator_id: int, year: int) -> list[dict]:
        """
        Get map visualization data for a specific indicator and year.

        Returns country data with coordinates and values.
        """
        results = (
            self.db.query(
                Country.code,
                Country.name,
                Country.latitude,
                Country.longitude,
                IndicatorValue.value,
                Indicator.unit,
            )
            .join(IndicatorValue, Country.id == IndicatorValue.country_id)
            .join(Indicator, IndicatorValue.indicator_id == Indicator.id)
            .filter(
                and_(
                    IndicatorValue.indicator_id == indicator_id,
                    IndicatorValue.year == year,
                    Country.latitude.isnot(None),
                    Country.longitude.isnot(None),
                )
            )
            .all()
        )

        return [
            {
                "country_code": row.code,
                "country_name": row.name,
                "latitude": float(row.latitude),
                "longitude": float(row.longitude),
                "value": float(row.value) if row.value else None,
                "unit": row.unit,
            }
            for row in results
        ]

    def count_filtered_values(self, filters: FilterParams) -> int:
        """Count total indicator values matching filters."""
        query = (
            self.db.query(IndicatorValue)
            .join(Country, IndicatorValue.country_id == Country.id)
            .join(Indicator, IndicatorValue.indicator_id == Indicator.id)
            .join(Dimension, Indicator.dimension_id == Dimension.id)
            .join(Pillar, Dimension.pillar_id == Pillar.id)
            .filter(Indicator.is_active == True)
        )

        if filters.pillar_id:
            query = query.filter(Pillar.id == filters.pillar_id)
        if filters.dimension_id:
            query = query.filter(Dimension.id == filters.dimension_id)
        if filters.indicator_id:
            query = query.filter(Indicator.id == filters.indicator_id)
        if filters.country_code_list:
            query = query.filter(Country.code.in_(filters.country_code_list))
        if filters.year_start:
            query = query.filter(IndicatorValue.year >= filters.year_start)
        if filters.year_end:
            query = query.filter(IndicatorValue.year <= filters.year_end)

        return query.count()
