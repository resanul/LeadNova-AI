import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app, lifespan
from app.services.geo_expansion_service import haversine_distance_miles


def test_haversine_distance():
    # Distance between Fort Wayne (41.0793, -85.1394) and New Haven (41.0706, -85.0319) is ~5.6 miles
    dist = haversine_distance_miles(41.0793, -85.1394, 41.0706, -85.0319)
    assert 4.0 <= dist <= 7.0


@pytest.mark.asyncio
async def test_market_intelligence_and_discovery_pipeline():
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

            # 2. Retrieve City and Niche
            cities_res = await client.get("/api/v1/cities", headers=auth_headers)
            city = cities_res.json()[0]

            niches_res = await client.get("/api/v1/niches", headers=auth_headers)
            water_damage = next(n for n in niches_res.json() if n["slug"] == "water-damage-restoration")

            # 3. Test Keyword Intelligence API
            kw_res = await client.get(
                f"/api/v1/market/keywords?city_id={city['id']}&niche_id={water_damage['id']}",
                headers=auth_headers,
            )
            assert kw_res.status_code == 200
            kw_data = kw_res.json()
            assert "primary_keywords" in kw_data
            assert "emergency_keywords" in kw_data
            assert kw_data["estimated_cpc_usd"] == 45.0

            # 4. Test Competitor Analysis API
            comp_res = await client.get(
                f"/api/v1/market/competitors?city_id={city['id']}&niche_id={water_damage['id']}",
                headers=auth_headers,
            )
            assert comp_res.status_code == 200
            comp_data = comp_res.json()
            assert "market_barrier" in comp_data
            assert "opportunity_verdict" in comp_data

            # 5. Test Surrounding Cities Expansion
            surround_res = await client.get(
                f"/api/v1/market/surrounding-cities?city_id={city['id']}&radius_miles=30",
                headers=auth_headers,
            )
            assert surround_res.status_code == 200
            surrounding = surround_res.json()
            assert len(surrounding) >= 1
            assert any(s["name"] == "New Haven" for s in surrounding)

            # 6. Test Automated Contractor Discovery Execution
            discovery_res = await client.post(
                "/api/v1/contractors/discover",
                json={
                    "city_id": city["id"],
                    "niche_id": water_damage["id"],
                    "source": "OPENSTREETMAP",
                    "max_results": 3,
                },
                headers=auth_headers,
            )
            assert discovery_res.status_code == 200
            disc_data = discovery_res.json()
            assert disc_data["total_queried"] >= 1
            assert "contractors" in disc_data

            # 7. Test Opportunity Ranking
            rank_res = await client.get("/api/v1/opportunities/rank", headers=auth_headers)
            assert rank_res.status_code == 200

            # 8. Test CSV Export
            csv_res = await client.get("/api/v1/contractors/export/csv", headers=auth_headers)
            assert csv_res.status_code == 200
            assert "text/csv" in csv_res.headers["content-type"]
            assert "Business Name" in csv_res.text
