import uuid
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app, lifespan


@pytest.mark.asyncio
async def test_full_business_lifecycle():
    async with lifespan(app):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://testserver") as client:
            # 1. Health check
            health_res = await client.get("/api/v1/system/health")
            assert health_res.status_code == 200
            assert health_res.json()["status"] == "OPERATIONAL"

            # 2. Login as Super Admin
            login_data = {
                "username": "admin@globallead.ai",
                "password": "AdminPassword123!",
            }
            login_res = await client.post(
                "/api/v1/auth/login",
                data=login_data,
                headers={"Content-Type": "application/x-www-form-urlencoded"},
            )
            assert login_res.status_code == 200
            tokens = login_res.json()
            access_token = tokens["access_token"]
            auth_headers = {"Authorization": f"Bearer {access_token}"}

            # 3. Verify Profile
            me_res = await client.get("/api/v1/auth/me", headers=auth_headers)
            assert me_res.status_code == 200
            assert me_res.json()["email"] == "admin@globallead.ai"

            # 4. Check Seeded Niches
            niches_res = await client.get("/api/v1/niches", headers=auth_headers)
            assert niches_res.status_code == 200
            niches = niches_res.json()
            assert len(niches) >= 25
            water_damage = next(n for n in niches if n["slug"] == "water-damage-restoration")

            # 5. Check Seeded Countries & Cities
            countries_res = await client.get("/api/v1/countries", headers=auth_headers)
            assert countries_res.status_code == 200
            assert any(c["code"] == "US" for c in countries_res.json())

            cities_res = await client.get("/api/v1/cities", headers=auth_headers)
            assert cities_res.status_code == 200
            cities = cities_res.json()
            assert len(cities) >= 1
            fw_city = cities[0]

            # 6. Register a Contractor in Fort Wayne
            contractor_payload = {
                "business_name": "Fort Wayne Elite Water Restoration",
                "owner_name": "John Miller",
                "primary_phone": "260-555-0188",
                "email": "contact@fwwaterrestoration.com",
                "website": "https://fwwaterrestoration.example.com",
                "address": "1200 E Washington Blvd",
                "city": "Fort Wayne",
                "state": "IN",
                "country": "US",
                "postal_code": "46802",
                "discovery_source": "GOOGLE_PLACES",
            }
            contractor_res = await client.post(
                "/api/v1/contractors", json=contractor_payload, headers=auth_headers
            )
            assert contractor_res.status_code == 200
            contractor = contractor_res.json()
            contractor_id = contractor["id"]
            assert contractor["verification_status"] == "FORMAT_VALID"

            # Mark contractor as ACTIVE with highest rating to guarantee primary matching
            patch_res = await client.patch(
                f"/api/v1/contractors/{contractor_id}",
                json={"partner_status": "ACTIVE", "rating": 5.0},
                headers=auth_headers,
            )
            assert patch_res.status_code == 200

            # 7. Add Pricing Agreement ($75 per lead)
            agreement_payload = {
                "contractor_id": contractor_id,
                "niche_id": water_damage["id"],
                "lead_type": "EXCLUSIVE_CALL",
                "price_per_lead": 75.0,
                "min_call_duration_seconds": 60,
            }
            agreement_res = await client.post(
                "/api/v1/contractors/agreements",
                json=agreement_payload,
                headers=auth_headers,
            )
            assert agreement_res.status_code == 200

            # 8. Top-up Contractor Wallet ($500.00)
            dep_key = f"dep_test_{uuid.uuid4()}"
            deposit_payload = {
                "amount": 500.0,
                "description": "Initial prepaid balance deposit",
                "idempotency_key": dep_key,
            }
            deposit_res = await client.post(
                f"/api/v1/billing/wallets/{contractor_id}/deposit",
                json=deposit_payload,
                headers=auth_headers,
            )
            assert deposit_res.status_code == 200
            assert deposit_res.json()["balance_after"] == 500.0

            # 9. Ingest an Emergency Customer Lead
            customer_phone = f"+1260555{uuid.uuid4().int % 9000 + 1000}"
            lead_payload = {
                "city_id": fw_city["id"],
                "niche_id": water_damage["id"],
                "customer_name": "Sarah Connor",
                "customer_phone": customer_phone,
                "customer_email": "sarah@example.com",
                "lead_source": "WEB_FORM",
                "details": "Basement pipe burst, urgent water extraction needed immediately!",
            }
            lead_res = await client.post("/api/v1/leads/capture", json=lead_payload)
            assert lead_res.status_code == 200
            lead = lead_res.json()
            assert lead["qualification_status"] == "QUALIFIED"

            # 10. Check Contractor Wallet Balance after automatic lead dispatch & charge ($500 - $75 = $425)
            wallet_res = await client.get(
                f"/api/v1/billing/wallets/{contractor_id}", headers=auth_headers
            )
            assert wallet_res.status_code == 200
            assert wallet_res.json()["balance"] == 425.0

            # 11. Run an Autonomous AI Agent Task
            agent_run_res = await client.post(
                "/api/v1/agents/City Discovery Agent/run",
                json={"input_payload": {"city": "Fort Wayne", "niche": "Water Damage"}},
                headers=auth_headers,
            )
            assert agent_run_res.status_code == 200
            assert agent_run_res.json()["status"] == "COMPLETED"

            # 12. Check Analytics Dashboard Overview
            analytics_res = await client.get("/api/v1/analytics/overview", headers=auth_headers)
            assert analytics_res.status_code == 200
            metrics = analytics_res.json()
            assert metrics["total_contractors"] >= 1
            assert metrics["total_leads"] >= 1
            assert metrics["total_revenue_usd"] >= 75.0
