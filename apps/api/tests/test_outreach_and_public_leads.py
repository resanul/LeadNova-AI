import uuid
import random
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app, lifespan


@pytest.mark.asyncio
async def test_contractor_pitch_generation():
    async with lifespan(app):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://testserver") as client:
            # 1. Login
            login_res = await client.post(
                "/api/v1/auth/login",
                data={"username": "admin@globallead.ai", "password": "AdminPassword123!"},
                headers={"Content-Type": "application/x-www-form-urlencoded"},
            )
            auth_headers = {"Authorization": f"Bearer {login_res.json()['access_token']}"}

            # 2. Get registered contractor
            contractors = (await client.get("/api/v1/contractors", headers=auth_headers)).json()
            assert len(contractors) > 0
            target_contractor = contractors[0]

            # 3. Generate B2B Outreach Pitch
            pitch_res = await client.post(
                f"/api/v1/contractors/{target_contractor['id']}/generate-pitch",
                json={},
                headers=auth_headers,
            )
            assert pitch_res.status_code == 200
            pitch = pitch_res.json()

            assert "cold_email" in pitch
            assert "sms_pitch" in pitch
            assert "cold_call_script" in pitch
            assert target_contractor["business_name"] in pitch["cold_email"]["body"]
            assert "exclusive" in pitch["sms_pitch"].lower()
            assert target_contractor["city"] in pitch["cold_call_script"]
            assert "Emergency Contractor Dispatch" in pitch["cold_call_script"]


@pytest.mark.asyncio
async def test_public_lead_capture_and_routing():
    async with lifespan(app):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://testserver") as client:
            # 1. Fetch City and Niche
            cities = (await client.get("/api/v1/cities")).json()
            niches = (await client.get("/api/v1/niches")).json()
            assert len(cities) > 0
            assert len(niches) > 0

            city = cities[0]
            water_damage = next(n for n in niches if n["slug"] == "water-damage-restoration")

            # Unique valid US phone (NANP valid central office code 2-9)
            unique_phone = f"+1260{random.randint(2000000, 8999999)}"

            # 2. Simulate customer submitting lead via public landing page
            payload = {
                "city_id": city["id"],
                "niche_id": water_damage["id"],
                "customer_name": "Sarah Connor",
                "customer_phone": unique_phone,
                "customer_email": f"sarah_{uuid.uuid4().hex[:6]}@cyberdyne-defense.com",
                "lead_source": "LANDING_PAGE_FORM",
                "details": "Major basement pipe burst, 4 inches of standing water. Need immediate extraction!",
            }

            lead_res = await client.post("/api/v1/leads/capture", json=payload)
            assert lead_res.status_code == 200
            lead_data = lead_res.json()

            assert lead_data["customer_name"] == "Sarah Connor"
            # Normalized E.164 phone
            assert lead_data["customer_phone"].startswith("+1260")
            assert lead_data["qualification_status"] == "QUALIFIED"
            assert lead_data["id"] is not None
