from typing import Dict, Any, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.entities import Contractor


async def analyze_market_competitors(
    db: AsyncSession,
    city_name: str,
    niche_name: str,
) -> Dict[str, Any]:
    """
    Analyzes existing local competitor footprint, rating distributions, and market saturation.
    """
    query = select(Contractor).where(Contractor.city.ilike(city_name))
    res = await db.execute(query)
    contractors = res.scalars().all()

    total_competitors = len(contractors)
    avg_rating = 0.0
    total_reviews = 0
    with_website = 0

    if total_competitors > 0:
        avg_rating = sum(float(c.rating) for c in contractors) / total_competitors
        total_reviews = sum(c.review_count for c in contractors)
        with_website = sum(1 for c in contractors if c.website)

    # Calculate competitor saturation & opportunity gap
    if total_competitors == 0:
        market_barrier = "LOW"
        opportunity_verdict = "PRIME_TARGET_UNCONTESTED"
    elif total_competitors < 10:
        market_barrier = "MODERATE"
        opportunity_verdict = "HIGH_OPPORTUNITY_HEALTHY_DEMAND"
    else:
        market_barrier = "HIGH"
        opportunity_verdict = "COMPETITIVE_ARBITRAGE_VIABLE"

    return {
        "city": city_name,
        "niche": niche_name,
        "total_competitors_mapped": total_competitors,
        "average_competitor_rating": round(avg_rating, 2),
        "total_competitor_reviews": total_reviews,
        "competitors_with_websites_pct": round((with_website / total_competitors * 100), 1) if total_competitors > 0 else 0.0,
        "market_barrier": market_barrier,
        "opportunity_verdict": opportunity_verdict,
        "recommended_organic_strategy": "Target long-tail emergency landing pages + local Schema.org markup",
    }
