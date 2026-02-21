"""Seed database with initial data."""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.database import SessionLocal
from app.models import Country, Pillar, Dimension, Indicator, IndicatorValue


def seed_countries():
    """Seed countries data."""
    countries_data = [
        {"code": "USA", "name": "United States", "region": "North America", "latitude": 37.0902, "longitude": -95.7129, "population": 331000000, "gdp_usd": 21427700},
        {"code": "GBR", "name": "United Kingdom", "region": "Europe", "latitude": 55.3781, "longitude": -3.4360, "population": 67000000, "gdp_usd": 2827000},
        {"code": "DEU", "name": "Germany", "region": "Europe", "latitude": 51.1657, "longitude": 10.4515, "population": 83000000, "gdp_usd": 3845000},
        {"code": "FRA", "name": "France", "region": "Europe", "latitude": 46.2276, "longitude": 2.2137, "population": 65000000, "gdp_usd": 2716000},
        {"code": "JPN", "name": "Japan", "region": "Asia", "latitude": 36.2048, "longitude": 138.2529, "population": 126000000, "gdp_usd": 5082000},
        {"code": "CHN", "name": "China", "region": "Asia", "latitude": 35.8617, "longitude": 104.1954, "population": 1400000000, "gdp_usd": 14342000},
        {"code": "IND", "name": "India", "region": "Asia", "latitude": 20.5937, "longitude": 78.9629, "population": 1380000000, "gdp_usd": 2875000},
        {"code": "BRA", "name": "Brazil", "region": "South America", "latitude": -14.2350, "longitude": -51.9253, "population": 212000000, "gdp_usd": 1839000},
        {"code": "AUS", "name": "Australia", "region": "Oceania", "latitude": -25.2744, "longitude": 133.7751, "population": 25000000, "gdp_usd": 1393000},
        {"code": "CAN", "name": "Canada", "region": "North America", "latitude": 56.1304, "longitude": -106.3468, "population": 38000000, "gdp_usd": 1736000},
    ]

    db = SessionLocal()
    try:
        for country_data in countries_data:
            existing = db.query(Country).filter(Country.code == country_data["code"]).first()
            if not existing:
                country = Country(**country_data)
                db.add(country)
        db.commit()
        print(f"✓ Seeded {len(countries_data)} countries")
    except Exception as e:
        print(f"✗ Error seeding countries: {e}")
        db.rollback()
    finally:
        db.close()


def seed_pillars():
    """Seed pillars data."""
    pillars_data = [
        {"name": "Brain Capital Drivers", "description": "Factors that enable brain capital development", "display_order": 1},
        {"name": "Brain Health", "description": "Mental and neurological wellbeing indicators", "display_order": 2},
        {"name": "Brain Skills", "description": "Cognitive and educational capabilities", "display_order": 3},
    ]

    db = SessionLocal()
    try:
        for pillar_data in pillars_data:
            existing = db.query(Pillar).filter(Pillar.name == pillar_data["name"]).first()
            if not existing:
                pillar = Pillar(**pillar_data)
                db.add(pillar)
        db.commit()
        print(f"✓ Seeded {len(pillars_data)} pillars")
    except Exception as e:
        print(f"✗ Error seeding pillars: {e}")
        db.rollback()
    finally:
        db.close()


def seed_dimensions():
    """Seed dimensions data."""
    db = SessionLocal()
    try:
        # Get pillar IDs
        pillars = {p.name: p.id for p in db.query(Pillar).all()}

        dimensions_data = [
            {"pillar_id": pillars["Brain Capital Drivers"], "name": "Digitalization", "description": "Digital infrastructure and access", "display_order": 1},
            {"pillar_id": pillars["Brain Capital Drivers"], "name": "Education", "description": "Educational systems and access", "display_order": 2},
            {"pillar_id": pillars["Brain Health"], "name": "Mental Wellbeing", "description": "Psychological health indicators", "display_order": 1},
            {"pillar_id": pillars["Brain Health"], "name": "Neurological Health", "description": "Brain health and disease prevention", "display_order": 2},
            {"pillar_id": pillars["Brain Skills"], "name": "Cognitive Abilities", "description": "Cognitive performance metrics", "display_order": 1},
            {"pillar_id": pillars["Brain Skills"], "name": "Workforce Skills", "description": "Professional and technical skills", "display_order": 2},
        ]

        for dim_data in dimensions_data:
            existing = db.query(Dimension).filter(
                Dimension.pillar_id == dim_data["pillar_id"],
                Dimension.name == dim_data["name"]
            ).first()
            if not existing:
                dimension = Dimension(**dim_data)
                db.add(dimension)
        db.commit()
        print(f"✓ Seeded {len(dimensions_data)} dimensions")
    except Exception as e:
        print(f"✗ Error seeding dimensions: {e}")
        db.rollback()
    finally:
        db.close()


def seed_indicators():
    """Seed indicators data."""
    db = SessionLocal()
    try:
        # Get dimension IDs
        dimensions = {d.name: d.id for d in db.query(Dimension).all()}

        indicators_data = [
            {
                "dimension_id": dimensions["Digitalization"],
                "name": "Digital Infrastructure Index",
                "description": "Composite index of digital connectivity and infrastructure",
                "unit": "score 0-100",
                "data_source": "World Bank",
                "display_order": 1,
            },
            {
                "dimension_id": dimensions["Education"],
                "name": "Education Access Rate",
                "description": "Percentage of population with access to quality education",
                "unit": "%",
                "data_source": "UNESCO",
                "display_order": 1,
            },
            {
                "dimension_id": dimensions["Mental Wellbeing"],
                "name": "Depression Rate",
                "description": "Prevalence of depression per 100,000 population",
                "unit": "per 100k",
                "data_source": "WHO",
                "display_order": 1,
            },
            {
                "dimension_id": dimensions["Neurological Health"],
                "name": "Dementia Prevalence",
                "description": "Prevalence of dementia per 100,000 population",
                "unit": "per 100k",
                "data_source": "WHO",
                "display_order": 1,
            },
            {
                "dimension_id": dimensions["Cognitive Abilities"],
                "name": "Cognitive Performance Index",
                "description": "Composite index of cognitive test performance",
                "unit": "score 0-100",
                "data_source": "OECD",
                "display_order": 1,
            },
            {
                "dimension_id": dimensions["Workforce Skills"],
                "name": "Skills Match Index",
                "description": "Alignment between workforce skills and job market needs",
                "unit": "score 0-100",
                "data_source": "World Economic Forum",
                "display_order": 1,
            },
        ]

        for ind_data in indicators_data:
            existing = db.query(Indicator).filter(
                Indicator.dimension_id == ind_data["dimension_id"],
                Indicator.name == ind_data["name"]
            ).first()
            if not existing:
                indicator = Indicator(**ind_data)
                db.add(indicator)
        db.commit()
        print(f"✓ Seeded {len(indicators_data)} indicators")
    except Exception as e:
        print(f"✗ Error seeding indicators: {e}")
        db.rollback()
    finally:
        db.close()


def seed_indicator_values():
    """Seed sample indicator values."""
    import random

    db = SessionLocal()
    try:
        countries = db.query(Country).all()
        indicators = db.query(Indicator).all()
        years = [2020, 2021, 2022, 2023]

        count = 0
        for country in countries:
            for indicator in indicators:
                for year in years:
                    existing = db.query(IndicatorValue).filter(
                        IndicatorValue.country_id == country.id,
                        IndicatorValue.indicator_id == indicator.id,
                        IndicatorValue.year == year
                    ).first()

                    if not existing:
                        # Generate semi-realistic random values
                        if "rate" in indicator.name.lower() or "index" in indicator.name.lower():
                            value = random.uniform(40, 95)
                        elif "prevalence" in indicator.name.lower():
                            value = random.uniform(500, 5000)
                        else:
                            value = random.uniform(50, 90)

                        indicator_value = IndicatorValue(
                            country_id=country.id,
                            indicator_id=indicator.id,
                            year=year,
                            value=round(value, 2),
                            confidence_score=round(random.uniform(0.7, 0.95), 2),
                        )
                        db.add(indicator_value)
                        count += 1

        db.commit()
        print(f"✓ Seeded {count} indicator values")
    except Exception as e:
        print(f"✗ Error seeding indicator values: {e}")
        db.rollback()
    finally:
        db.close()


def main():
    """Run all seed functions."""
    print("Starting database seeding...")
    print()

    seed_countries()
    seed_pillars()
    seed_dimensions()
    seed_indicators()
    seed_indicator_values()

    print()
    print("✓ Database seeding completed!")
    print()
    print("You can now start the application:")
    print("  uv run uvicorn app.main:app --reload")


if __name__ == "__main__":
    main()
