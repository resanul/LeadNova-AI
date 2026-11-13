from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.database import get_db
from app.models.entities import Website, LandingPage, City, Niche
from app.schemas.all_schemas import (
    WebsiteResponse, WebsiteCreate,
    LandingPageResponse, LandingPageCreate,
)
from app.services.website_factory_service import generate_and_publish_page, generate_seo_content
from app.services.auth_service import get_current_user

router = APIRouter(prefix="", tags=["Digital Assets & Websites"])


class AutoGeneratePageRequest(BaseModel):
    website_id: str
    city_id: str
    niche_id: str
    slug_override: Optional[str] = None


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


@router.post("/landing-pages/generate-auto", response_model=LandingPageResponse)
async def auto_generate_landing_page(
    req: AutoGeneratePageRequest,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    """
    Autonomously generates an optimized local landing page with
    Schema.org JSON-LD, SEO title, FAQs, and virtual tracking number.
    """
    try:
        page = await generate_and_publish_page(
            db=db,
            website_id=req.website_id,
            city_id=req.city_id,
            niche_id=req.niche_id,
            slug_override=req.slug_override,
        )
        return page
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/landing-pages/{slug}/preview")
async def preview_landing_page(slug: str, db: AsyncSession = Depends(get_db)):
    """Public preview endpoint rendering structured landing page metadata and JSON-LD."""
    res = await db.execute(select(LandingPage).where(LandingPage.slug == slug))
    page = res.scalars().first()
    if not page:
        raise HTTPException(status_code=404, detail="Landing page not found")

    city_res = await db.execute(select(City).where(City.id == page.city_id))
    city = city_res.scalars().first()
    city_name = city.name if city else "Local"

    niche_res = await db.execute(select(Niche).where(Niche.id == page.niche_id))
    niche = niche_res.scalars().first()
    niche_name = niche.name if niche else "Emergency Service"

    seo_data = generate_seo_content(city_name, niche_name)

    return {
        "id": page.id,
        "slug": page.slug,
        "seo_title": page.seo_title,
        "seo_description": page.seo_description,
        "headline": page.headline,
        "content_body": page.content_body,
        "tracking_phone": page.tracking_phone,
        "click_to_call_href": f"tel:{page.tracking_phone}",
        "schema_org": seo_data["schema_org"],
        "is_active": page.is_active,
    }
