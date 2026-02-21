"""Country service."""

from sqlalchemy.orm import Session
from app.models import Country
from app.schemas.country import CountryCreate, CountryUpdate


class CountryService:
    """Service for country operations."""

    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100) -> list[Country]:
        """Get all countries."""
        return self.db.query(Country).offset(skip).limit(limit).all()

    def get_by_id(self, country_id: int) -> Country | None:
        """Get country by ID."""
        return self.db.query(Country).filter(Country.id == country_id).first()

    def get_by_code(self, country_code: str) -> Country | None:
        """Get country by code."""
        return self.db.query(Country).filter(Country.code == country_code.upper()).first()

    def get_by_region(self, region: str) -> list[Country]:
        """Get countries by region."""
        return self.db.query(Country).filter(Country.region == region).all()

    def create(self, country: CountryCreate) -> Country:
        """Create a new country."""
        db_country = Country(**country.model_dump())
        self.db.add(db_country)
        self.db.commit()
        self.db.refresh(db_country)
        return db_country

    def update(self, country_id: int, country: CountryUpdate) -> Country | None:
        """Update a country."""
        db_country = self.get_by_id(country_id)
        if not db_country:
            return None

        update_data = country.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_country, field, value)

        self.db.commit()
        self.db.refresh(db_country)
        return db_country

    def delete(self, country_id: int) -> bool:
        """Delete a country."""
        db_country = self.get_by_id(country_id)
        if not db_country:
            return False

        self.db.delete(db_country)
        self.db.commit()
        return True

    def count(self) -> int:
        """Count total countries."""
        return self.db.query(Country).count()
