from typing import List, Dict, Any, Optional
import math
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.entities import City, State

# Pre-mapped high-value metro cluster fallback
SURROUNDING_CLUSTERS = {
    "fort wayne": [
        {"name": "New Haven", "distance_miles": 7.5, "population": 16000},
        {"name": "Auburn", "distance_miles": 22.0, "population": 13500},
        {"name": "Columbia City", "distance_miles": 21.0, "population": 9800},
        {"name": "Huntington", "distance_miles": 25.0, "population": 17000},
        {"name": "Bluffton", "distance_miles": 26.0, "population": 10200},
    ],
    "dallas": [
        {"name": "Plano", "distance_miles": 19.0, "population": 285000},
        {"name": "Irving", "distance_miles": 12.0, "population": 240000},
        {"name": "Garland", "distance_miles": 15.0, "population": 235000},
        {"name": "Grand Prairie", "distance_miles": 13.0, "population": 195000},
        {"name": "Mesquite", "distance_miles": 14.0, "population": 140000},
    ],
    "mesa": [
        {"name": "Gilbert", "distance_miles": 6.5, "population": 270000},
        {"name": "Chandler", "distance_miles": 8.0, "population": 275000},
        {"name": "Tempe", "distance_miles": 9.0, "population": 185000},
        {"name": "Scottsdale", "distance_miles": 12.0, "population": 240000},
    ],
}


def haversine_distance_miles(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Computes great-circle distance between two GPS coordinates in miles."""
    r = 3958.8  # Earth radius in miles
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(dlon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return round(r * c, 2)


async def discover_surrounding_cities(
    db: AsyncSession,
    base_city_id: str,
    radius_miles: float = 30.0,
) -> List[Dict[str, Any]]:
    """
    Expands a target city to discover surrounding satellite municipalities within service radius.
    """
    res = await db.execute(select(City).where(City.id == base_city_id))
    base_city = res.scalars().first()
    if not base_city:
        return []

    city_key = base_city.name.strip().lower()
    discovered = []

    # Check known cluster definitions
    if city_key in SURROUNDING_CLUSTERS:
        for item in SURROUNDING_CLUSTERS[city_key]:
            if item["distance_miles"] <= radius_miles:
                discovered.append({
                    "name": item["name"],
                    "state_id": base_city.state_id,
                    "distance_miles": item["distance_miles"],
                    "population": item["population"],
                    "coverage_type": "SATELLITE_SERVICE_AREA",
                })

    # If coordinates are available, also query other stored cities in same state
    if base_city.latitude and base_city.longitude:
        other_cities_res = await db.execute(
            select(City).where(City.state_id == base_city.state_id, City.id != base_city.id)
        )
        for other in other_cities_res.scalars().all():
            if other.latitude and other.longitude:
                dist = haversine_distance_miles(
                    float(base_city.latitude),
                    float(base_city.longitude),
                    float(other.latitude),
                    float(other.longitude),
                )
                if dist <= radius_miles:
                    if not any(d["name"].lower() == other.name.lower() for d in discovered):
                        discovered.append({
                            "name": other.name,
                            "state_id": other.state_id,
                            "distance_miles": dist,
                            "population": other.population,
                            "coverage_type": "REGISTERED_NEIGHBOR_CITY",
                        })

    return discovered
