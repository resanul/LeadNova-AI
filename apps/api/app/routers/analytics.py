from datetime import datetime, timezone
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from app.core.database import get_db
from app.core.config import settings
from app.models.entities import (
    Country, City, Niche, Contractor, Lead, LeadAssignment, LedgerEntry
)
from app.schemas.all_schemas import AnalyticsOverviewResponse, SystemHealthResponse

router = APIRouter(prefix="", tags=["Analytics & System Health"])


@router.get("/analytics/overview", response_model=AnalyticsOverviewResponse)
async def get_analytics_overview(db: AsyncSession = Depends(get_db)):
    # Calculate real aggregates
    countries_count = (await db.execute(select(func.count(Country.id)))).scalar() or 0
    cities_count = (await db.execute(select(func.count(City.id)))).scalar() or 0
    niches_count = (await db.execute(select(func.count(Niche.id)))).scalar() or 0
    contractors_count = (await db.execute(select(func.count(Contractor.id)))).scalar() or 0
    verified_contractors = (await db.execute(
        select(func.count(Contractor.id)).where(Contractor.verification_status == "FORMAT_VALID")
    )).scalar() or 0
    active_contractors = (await db.execute(
        select(func.count(Contractor.id)).where(Contractor.partner_status == "ACTIVE")
    )).scalar() or 0
    leads_count = (await db.execute(select(func.count(Lead.id)))).scalar() or 0
    qualified_leads = (await db.execute(
        select(func.count(Lead.id)).where(Lead.qualification_status == "QUALIFIED")
    )).scalar() or 0
    revenue_sum = (await db.execute(
        select(func.sum(LeadAssignment.charged_amount))
    )).scalar() or 0.0

    return {
        "total_countries": countries_count,
        "total_cities": cities_count,
        "total_niches": niches_count,
        "total_contractors": contractors_count,
        "verified_contractors": verified_contractors,
        "active_contractors": active_contractors,
        "total_leads": leads_count,
        "qualified_leads": qualified_leads,
        "total_revenue_usd": float(revenue_sum),
        "total_calls_routed": qualified_leads,
    }


@router.get("/system/health", response_model=SystemHealthResponse)
async def system_health(db: AsyncSession = Depends(get_db)):
    # Test DB connectivity
    db_status = "HEALTHY"
    try:
        await db.execute(select(1))
    except Exception:
        db_status = "DEGRADED"

    return {
        "status": "OPERATIONAL",
        "database": db_status,
        "version": settings.VERSION,
        "timestamp": datetime.now(timezone.utc),
    }
