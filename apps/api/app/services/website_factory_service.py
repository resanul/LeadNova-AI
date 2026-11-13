import json
from typing import Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.entities import Website, LandingPage, City, Niche, PhoneNumber


def generate_seo_content(city_name: str, niche_name: str, state_code: str = "IN") -> Dict[str, Any]:
    """
    Generates high-converting, compliant local service landing page copy,
    SEO metadata, and Schema.org structured data.
    """
    clean_city = city_name.strip()
    clean_niche = niche_name.strip()

    seo_title = f"{clean_niche} in {clean_city}, {state_code} | 24/7 Rapid Dispatch"
    seo_description = (
        f"Need urgent {clean_niche.lower()} in {clean_city}, {state_code}? "
        f"Connect immediately with local, licensed & verified specialists. 24/7 response."
    )

    headline = f"Emergency {clean_niche} in {clean_city}"
    subheadline = f"Fast, Reliable & Certified Local Specialists Dispatched Directly to Your Property in {clean_city}."

    content_body = f"""## Trusted 24/7 {clean_niche} in {clean_city}, {state_code}

When unexpected property emergencies happen, fast response times make all the difference. Our verified network of licensed local technicians serves all neighborhoods across {clean_city} and surrounding areas.

### Why Choose Our Verified Local Partner Network?
- **Rapid Response Dispatch:** Local technicians ready 24/7, 365 days a year.
- **Licensed & Screened:** Every contractor is phone-verified, insured, and experienced.
- **Transparent Estimates:** Free initial telephone consultations and upfront pricing.
- **Direct Local Communication:** Speak directly with an on-call specialist within minutes.

### Services Provided Across {clean_city}:
1. Emergency Diagnostic & Rapid Assessment
2. Complete Containment and Damage Mitigation
3. Residential & Commercial Restoration
4. Insurance Claims Assistance and Direct Documentation

### Frequently Asked Questions

**Q: How quickly can a specialist arrive at my property in {clean_city}?**  
A: In most emergency cases, a local specialist can be dispatched to your location in {clean_city} within 45 to 90 minutes of your call.

**Q: Are estimates provided upfront?**  
A: Yes, our partner technicians provide full assessments and transparent quotes prior to commencing any major structural or repair work.

**Q: Is emergency service available on holidays and weekends?**  
A: Yes, our call routing connects you directly with on-duty technicians available 24 hours a day, 7 days a week.
"""

    schema_org = {
        "@context": "https://schema.org",
        "@type": "HomeAndConstructionBusiness",
        "name": f"{clean_city} {clean_niche} Network",
        "description": seo_description,
        "areaServed": {
            "@type": "City",
            "name": clean_city,
            "addressRegion": state_code,
        },
        "openingHours": "Mo-Su 00:00-24:00",
        "priceRange": "$$",
    }

    return {
        "seo_title": seo_title,
        "seo_description": seo_description,
        "headline": headline,
        "subheadline": subheadline,
        "content_body": content_body,
        "schema_org": schema_org,
    }


async def generate_and_publish_page(
    db: AsyncSession,
    website_id: str,
    city_id: str,
    niche_id: str,
    slug_override: Optional[str] = None,
) -> LandingPage:
    """
    Automates landing page generation with Schema.org markup, SEO metadata,
    and automatic assignment of virtual tracking numbers.
    """
    site_res = await db.execute(select(Website).where(Website.id == website_id))
    site = site_res.scalars().first()
    if not site:
        raise ValueError("Website not found")

    city_res = await db.execute(select(City).where(City.id == city_id))
    city = city_res.scalars().first()
    if not city:
        raise ValueError("City not found")

    niche_res = await db.execute(select(Niche).where(Niche.id == niche_id))
    niche = niche_res.scalars().first()
    if not niche:
        raise ValueError("Niche not found")

    seo_data = generate_seo_content(city.name, niche.name)
    slug = slug_override or f"{city.name.lower().replace(' ', '-')}-{niche.slug}"

    # Find or allocate tracking phone number
    phone_res = await db.execute(
        select(PhoneNumber).where(PhoneNumber.status == "ACTIVE").limit(1)
    )
    phone_rec = phone_res.scalars().first()
    tracking_phone = phone_rec.phone_number if phone_rec else "+18005550199"

    # Check for existing landing page
    existing_res = await db.execute(
        select(LandingPage).where(LandingPage.website_id == website_id, LandingPage.slug == slug)
    )
    page = existing_res.scalars().first()
    if not page:
        page = LandingPage(
            website_id=website_id,
            city_id=city_id,
            niche_id=niche_id,
            slug=slug,
            headline=seo_data["headline"],
            content_body=seo_data["content_body"],
            seo_title=seo_data["seo_title"],
            seo_description=seo_data["seo_description"],
            tracking_phone=tracking_phone,
            is_active=True,
        )
        db.add(page)
    else:
        page.headline = seo_data["headline"]
        page.content_body = seo_data["content_body"]
        page.seo_title = seo_data["seo_title"]
        page.seo_description = seo_data["seo_description"]
        page.tracking_phone = tracking_phone
        page.is_active = True

    await db.commit()
    await db.refresh(page)
    return page
