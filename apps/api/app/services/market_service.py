from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.models.entities import Country, State, City, Niche, Opportunity, Contractor

INITIAL_NICHES = [
    {"name": "Water Damage Restoration", "slug": "water-damage-restoration", "avg_lead_value": 150.0, "emergency_level": "critical", "description": "Emergency flood, burst pipe, and water mitigation services."},
    {"name": "Emergency Plumbing", "slug": "emergency-plumbing", "avg_lead_value": 85.0, "emergency_level": "high", "description": "24/7 burst pipe, drain backup, and emergency plumbing repairs."},
    {"name": "Roof Repair", "slug": "roof-repair", "avg_lead_value": 95.0, "emergency_level": "high", "description": "Storm damage, leak detection, and asphalt/metal roof repairs."},
    {"name": "Roof Replacement", "slug": "roof-replacement", "avg_lead_value": 220.0, "emergency_level": "medium", "description": "Complete residential and commercial roof replacement."},
    {"name": "HVAC Repair", "slug": "hvac-repair", "avg_lead_value": 75.0, "emergency_level": "high", "description": "Heating, ventilation, and air conditioning maintenance & repair."},
    {"name": "Emergency AC Repair", "slug": "emergency-ac-repair", "avg_lead_value": 90.0, "emergency_level": "critical", "description": "Rapid response air conditioning system breakdowns."},
    {"name": "Mold Remediation", "slug": "mold-remediation", "avg_lead_value": 140.0, "emergency_level": "high", "description": "Toxic black mold removal, containment, and air quality restoration."},
    {"name": "Emergency Tree Removal", "slug": "emergency-tree-removal", "avg_lead_value": 110.0, "emergency_level": "critical", "description": "Hazardous fallen trees and storm cleanup."},
    {"name": "Electrical Repair", "slug": "electrical-repair", "avg_lead_value": 70.0, "emergency_level": "high", "description": "Licensed residential electrical panel and emergency wiring services."},
    {"name": "Garage Door Repair", "slug": "garage-door-repair", "avg_lead_value": 65.0, "emergency_level": "high", "description": "Broken spring replacement and overhead door tracking repairs."},
    {"name": "Pest Control", "slug": "pest-control", "avg_lead_value": 55.0, "emergency_level": "medium", "description": "Termite, bed bug, rodent, and insect extermination."},
    {"name": "Foundation Repair", "slug": "foundation-repair", "avg_lead_value": 180.0, "emergency_level": "medium", "description": "Slabjacking, piering, and structural crack reinforcement."},
    {"name": "Carpet Cleaning", "slug": "carpet-cleaning", "avg_lead_value": 45.0, "emergency_level": "low", "description": "Deep steam and commercial carpet sanitization."},
    {"name": "Fire Damage Restoration", "slug": "fire-damage-restoration", "avg_lead_value": 250.0, "emergency_level": "critical", "description": "Soot, smoke, and structural fire recovery."},
    {"name": "Drain Cleaning", "slug": "drain-cleaning", "avg_lead_value": 60.0, "emergency_level": "high", "description": "Hydro-jetting and mainline sewer blockage clearing."},
    {"name": "Window Replacement", "slug": "window-replacement", "avg_lead_value": 125.0, "emergency_level": "low", "description": "Energy-efficient vinyl and architectural window installations."},
    {"name": "Gutter Repair", "slug": "gutter-repair", "avg_lead_value": 50.0, "emergency_level": "medium", "description": "Seamless gutter installation, leaf guards, and downspout repairs."},
    {"name": "Landscaping", "slug": "landscaping", "avg_lead_value": 55.0, "emergency_level": "low", "description": "Hardscaping, lawn renovation, and seasonal maintenance."},
    {"name": "Moving Services", "slug": "moving-services", "avg_lead_value": 90.0, "emergency_level": "medium", "description": "Long-distance and local residential relocation."},
    {"name": "Home Remodeling", "slug": "home-remodeling", "avg_lead_value": 200.0, "emergency_level": "low", "description": "Kitchen, bathroom, and complete residential home renovations."},
    {"name": "Appliance Repair", "slug": "appliance-repair", "avg_lead_value": 50.0, "emergency_level": "medium", "description": "Refrigerator, washer, dryer, and oven diagnostic and repair."},
    {"name": "Locksmith Services", "slug": "locksmith-services", "avg_lead_value": 60.0, "emergency_level": "critical", "description": "24/7 lockout, key cutting, and commercial access hardware."},
    {"name": "Concrete Services", "slug": "concrete-services", "avg_lead_value": 115.0, "emergency_level": "medium", "description": "Driveways, decorative stamping, and concrete patio pouring."},
    {"name": "Basement Waterproofing", "slug": "basement-waterproofing", "avg_lead_value": 160.0, "emergency_level": "high", "description": "Sump pumps, French drains, and interior vapor barriers."},
    {"name": "Insulation Services", "slug": "insulation-services", "avg_lead_value": 85.0, "emergency_level": "low", "description": "Spray foam, blown-in attic insulation, and soundproofing."}
]


async def seed_market_defaults(db: AsyncSession):
    """Seed initial countries, states, and 25 core service niches if not present."""
    # Seed US, GB, CA, AU, DE
    countries_data = [
        {"code": "US", "name": "United States", "currency": "USD", "phone_prefix": "+1"},
        {"code": "GB", "name": "United Kingdom", "currency": "GBP", "phone_prefix": "+44"},
        {"code": "CA", "name": "Canada", "currency": "CAD", "phone_prefix": "+1"},
        {"code": "AU", "name": "Australia", "currency": "AUD", "phone_prefix": "+61"},
        {"code": "DE", "name": "Germany", "currency": "EUR", "phone_prefix": "+49"},
    ]
    for c_info in countries_data:
        res = await db.execute(select(Country).where(Country.code == c_info["code"]))
        if not res.scalars().first():
            db.add(Country(**c_info))
    
    await db.flush()

    # Seed US default states and test city (Fort Wayne, IN)
    us_res = await db.execute(select(Country).where(Country.code == "US"))
    us = us_res.scalars().first()
    if us:
        in_state_res = await db.execute(select(State).where(State.country_id == us.id, State.code == "IN"))
        in_state = in_state_res.scalars().first()
        if not in_state:
            in_state = State(country_id=us.id, code="IN", name="Indiana")
            db.add(in_state)
            await db.flush()
        
        fw_city_res = await db.execute(select(City).where(City.state_id == in_state.id, City.name == "Fort Wayne"))
        if not fw_city_res.scalars().first():
            fw_city = City(
                state_id=in_state.id,
                name="Fort Wayne",
                latitude=41.079273,
                longitude=-85.139351,
                population=265000,
                median_income=54000.0,
                homeownership_rate=62.5,
                is_active=True,
            )
            db.add(fw_city)

    # Seed 25 Niches
    for niche_data in INITIAL_NICHES:
        res = await db.execute(select(Niche).where(Niche.slug == niche_data["slug"]))
        if not res.scalars().first():
            db.add(Niche(**niche_data))

    await db.commit()


def calculate_opportunity_score(
    population: int,
    avg_lead_value: float,
    contractor_count: int,
    median_income: float,
) -> Dict[str, float]:
    """
    Computes deterministic multi-factor opportunity score:
    Score = (0.20 * Demand) + (0.20 * Commercial Value) + (0.15 * Contractor Availability)
          + (0.15 * Competition Opp) + (0.15 * Acquisition Cost) + (0.10 * Demand Stability)
          + (0.05 * Data Confidence)
    """
    # 1. Demand Score based on population and scale (normalized 0-100)
    if population > 500000:
        demand_score = 90.0
    elif population > 200000:
        demand_score = 78.0
    elif population > 50000:
        demand_score = 65.0
    else:
        demand_score = 45.0

    # 2. Commercial Value Score based on avg ticket price & median income (0-100)
    ticket_factor = min(avg_lead_value / 2.0, 60.0)  # max 60
    income_factor = min((median_income / 80000.0) * 40.0, 40.0)  # max 40
    commercial_value_score = round(ticket_factor + income_factor, 2)

    # 3. Contractor Availability Score (0-100)
    if contractor_count >= 10:
        contractor_score = 95.0
    elif contractor_count >= 5:
        contractor_score = 80.0
    elif contractor_count >= 1:
        contractor_score = 60.0
    else:
        contractor_score = 30.0

    # 4. Competition Opportunity Score (sweet spot: moderate competition, high arbitrage)
    if 3 <= contractor_count <= 15:
        competition_score = 85.0
    elif contractor_count > 15:
        competition_score = 60.0
    else:
        competition_score = 70.0

    # 5. Acquisition Cost Score (lower CAC in mid-size cities)
    cac_score = 75.0 if population < 500000 else 60.0

    # 6. Demand Stability Score
    stability_score = 80.0

    # 7. Data Confidence Score
    confidence_score = 90.0

    # Overall Weighted Calculation
    overall = (
        (0.20 * demand_score)
        + (0.20 * commercial_value_score)
        + (0.15 * contractor_score)
        + (0.15 * competition_score)
        + (0.15 * cac_score)
        + (0.10 * stability_score)
        + (0.05 * confidence_score)
    )

    return {
        "demand_score": round(demand_score, 2),
        "commercial_value_score": round(commercial_value_score, 2),
        "contractor_availability_score": round(contractor_score, 2),
        "competition_score": round(competition_score, 2),
        "cac_score": round(cac_score, 2),
        "stability_score": round(stability_score, 2),
        "confidence_score": round(confidence_score, 2),
        "overall_score": round(overall, 2),
    }
