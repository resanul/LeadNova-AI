from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.database import get_db
from app.models.entities import Country, City, Niche, Opportunity, Contractor, State
from app.schemas.all_schemas import (
    CountryResponse, CountryCreate,
    CityResponse, CityCreate,
    NicheResponse, NicheCreate,
    OpportunityResponse, OpportunityEvaluateRequest,
)
from app.services.market_service import calculate_opportunity_score
from app.services.keyword_service import generate_keyword_intelligence
from app.services.competitor_service import analyze_market_competitors
from app.services.geo_expansion_service import discover_surrounding_cities
from app.services.auth_service import get_current_user

router = APIRouter(prefix="", tags=["Market Intelligence"])


@router.get("/countries", response_model=List[CountryResponse])
async def list_countries(db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Country).where(Country.is_active == True))
    return res.scalars().all()


@router.post("/countries", response_model=CountryResponse)
async def create_country(country_in: CountryCreate, db: AsyncSession = Depends(get_db)):
    country = Country(**country_in.model_dump())
    db.add(country)
    await db.commit()
    await db.refresh(country)
    return country


@router.get("/cities", response_model=List[CityResponse])
async def list_cities(db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(City).where(City.is_active == True))
    return res.scalars().all()


@router.post("/cities", response_model=CityResponse)
async def create_city(city_in: CityCreate, db: AsyncSession = Depends(get_db)):
    city = City(**city_in.model_dump())
    db.add(city)
    await db.commit()
    await db.refresh(city)
    return city


@router.get("/niches", response_model=List[NicheResponse])
async def list_niches(db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Niche).where(Niche.is_active == True))
    return res.scalars().all()


@router.post("/niches", response_model=NicheResponse)
async def create_niche(niche_in: NicheCreate, db: AsyncSession = Depends(get_db)):
    niche = Niche(**niche_in.model_dump())
    db.add(niche)
    await db.commit()
    await db.refresh(niche)
    return niche


@router.get("/opportunities", response_model=List[OpportunityResponse])
async def list_opportunities(db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Opportunity))
    return res.scalars().all()


@router.get("/opportunities/rank", response_model=List[OpportunityResponse])
async def rank_opportunities(db: AsyncSession = Depends(get_db)):
    """Ranks market opportunities by overall multi-factor profitability score."""
    res = await db.execute(select(Opportunity).order_by(Opportunity.overall_score.desc()))
    return res.scalars().all()


@router.post("/opportunities/evaluate", response_model=OpportunityResponse)
async def evaluate_market_opportunity(
    req: OpportunityEvaluateRequest,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    city_res = await db.execute(select(City).where(City.id == req.city_id))
    city = city_res.scalars().first()
    if not city:
        raise HTTPException(status_code=404, detail="City not found")

    niche_res = await db.execute(select(Niche).where(Niche.id == req.niche_id))
    niche = niche_res.scalars().first()
    if not niche:
        raise HTTPException(status_code=404, detail="Niche not found")

    contractor_res = await db.execute(select(Contractor).where(Contractor.city.ilike(city.name)))
    contractors = contractor_res.scalars().all()
    contractor_count = len(contractors)

    scores = calculate_opportunity_score(
        population=city.population,
        avg_lead_value=float(niche.avg_lead_value),
        contractor_count=contractor_count,
        median_income=float(city.median_income),
    )

    opp_res = await db.execute(
        select(Opportunity).where(Opportunity.city_id == city.id, Opportunity.niche_id == niche.id)
    )
    opp = opp_res.scalars().first()
    if not opp:
        opp = Opportunity(
            city_id=city.id,
            niche_id=niche.id,
            status="viable" if scores["overall_score"] >= 70 else "discovered",
            metrics_data=scores,
            **scores,
        )
        db.add(opp)
    else:
        for k, v in scores.items():
            setattr(opp, k, v)
        opp.status = "viable" if scores["overall_score"] >= 70 else "discovered"

    await db.commit()
    await db.refresh(opp)
    return opp


@router.get("/market/keywords")
async def get_market_keywords(
    city_id: str,
    niche_id: str,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    """Returns local keyword intelligence, CPC benchmarks, and search intent."""
    city_res = await db.execute(select(City).where(City.id == city_id))
    city = city_res.scalars().first()
    if not city:
        raise HTTPException(status_code=404, detail="City not found")

    niche_res = await db.execute(select(Niche).where(Niche.id == niche_id))
    niche = niche_res.scalars().first()
    if not niche:
        raise HTTPException(status_code=404, detail="Niche not found")

    return generate_keyword_intelligence(city_name=city.name, niche_name=niche.name)


@router.get("/market/competitors")
async def get_market_competitors(
    city_id: str,
    niche_id: str,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    """Analyzes local competitor saturation and market penetration difficulty."""
    city_res = await db.execute(select(City).where(City.id == city_id))
    city = city_res.scalars().first()
    if not city:
        raise HTTPException(status_code=404, detail="City not found")

    niche_res = await db.execute(select(Niche).where(Niche.id == niche_id))
    niche = niche_res.scalars().first()
    if not niche:
        raise HTTPException(status_code=404, detail="Niche not found")

    return await analyze_market_competitors(db, city_name=city.name, niche_name=niche.name)


@router.get("/market/surrounding-cities")
async def get_surrounding_cities(
    city_id: str,
    radius_miles: float = 30.0,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    """Expands geographic coverage to surrounding satellite cities."""
    return await discover_surrounding_cities(db, base_city_id=city_id, radius_miles=radius_miles)
