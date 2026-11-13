import uuid
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app, lifespan
from app.services.website_factory_service import generate_seo_content


def test_seo_content_generation():
    seo = generate_seo_content(city_name="Fort Wayne", niche_name="Water Damage Restoration", state_code="IN")
    assert "Water Damage Restoration in Fort Wayne, IN" in seo["seo_title"]
    assert "24/7" in seo["seo_description"]
    assert "schema_org" in seo
    assert seo["schema_org"]["@type"] == "HomeAndConstructionBusiness"
    assert seo["schema_org"]["areaServed"]["name"] == "Fort Wayne"


@pytest.mark.asyncio
async def test_auto_generate_and_preview_landing_page():
    async with lifespan(app):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://testserver") as client:
            # 1. Login as Admin
            login_res = await client.post(
                "/api/v1/auth/login",
                data={"username": "admin@globallead.ai", "password": "AdminPassword123!"},
                headers={"Content-Type": "application/x-www-form-urlencoded"},
            )
            tokens = login_res.json()
            auth_headers = {"Authorization": f"Bearer {tokens['access_token']}"}

            # 2. Create Website Property with unique domain
            site_domain = f"fortwayne-{uuid.uuid4().hex[:6]}-pros.com"
            site_res = await client.post(
                "/api/v1/websites",
                json={
                    "domain": site_domain,
                    "title": "Fort Wayne Emergency Restoration Network",
                },
                headers=auth_headers,
            )
            assert site_res.status_code == 200
            website = site_res.json()

            # 3. Retrieve City and Niche
            cities = (await client.get("/api/v1/cities", headers=auth_headers)).json()
            city = cities[0]
            niches = (await client.get("/api/v1/niches", headers=auth_headers)).json()
            water_damage = next(n for n in niches if n["slug"] == "water-damage-restoration")

            # 4. Trigger Autonomous Landing Page Generation
            page_res = await client.post(
                "/api/v1/landing-pages/generate-auto",
                json={
                    "website_id": website["id"],
                    "city_id": city["id"],
                    "niche_id": water_damage["id"],
                },
                headers=auth_headers,
            )
            assert page_res.status_code == 200
            page = page_res.json()
            assert page["slug"] == "fort-wayne-water-damage-restoration"
            assert page["is_active"] is True
            assert page["tracking_phone"] is not None

            # 5. Test Public Preview Endpoint
            preview_res = await client.get(f"/api/v1/landing-pages/{page['slug']}/preview")
            assert preview_res.status_code == 200
            preview_data = preview_res.json()
            assert preview_data["headline"].startswith("Emergency")
            assert "tel:" in preview_data["click_to_call_href"]
            assert preview_data["schema_org"]["@type"] == "HomeAndConstructionBusiness"
