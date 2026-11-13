from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.database import get_db
from app.models.entities import Website, LandingPage, City, Niche
from app.schemas.all_schemas import (
    WebsiteResponse, WebsiteCreate,
    LandingPageResponse, LandingPageCreate,
)
from app.services.auth_service import get_current_user

router = APIRouter(prefix="", tags=["Digital Assets & Websites"])


@router.get("/websites", response_model=List[WebsiteResponse])
async def list_websites(db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Website))
    return res.scalars().all()


@router.post("/websites", response_model=WebsiteResponse)
async def create_website(
    site_in: WebsiteCreate,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    website = Website(**site_in.model_dump())
    db.add(website)
    await db.commit()
    await db.refresh(website)
    return website


@router.get("/landing-pages", response_model=List[LandingPageResponse])
async def list_landing_pages(db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(LandingPage))
    return res.scalars().all()


@router.post("/landing-pages/generate", response_model=LandingPageResponse)
async def generate_landing_page(
    page_in: LandingPageCreate,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    # Verify website, city, and niche
    site_res = await db.execute(select(Website).where(Website.id == page_in.website_id))
    site = site_res.scalars().first()
    if not site:
        raise HTTPException(status_code=404, detail="Website not found")

    city_res = await db.execute(select(City).where(City.id == page_in.city_id))
    city = city_res.scalars().first()
    if not city:
        raise HTTPException(status_code=404, detail="City not found")

    niche_res = await db.execute(select(Niche).where(Niche.id == page_in.niche_id))
    niche = niche_res.scalars().first()
    if not niche:
        raise HTTPException(status_code=404, detail="Niche not found")

    page = LandingPage(**page_in.model_dump())
    db.add(page)
    await db.commit()
    await db.refresh(page)
    return page
