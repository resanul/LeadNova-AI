import pytest
from app.core.security import get_password_hash, verify_password, create_access_token, decode_token
from app.services.contractor_service import normalize_phone_number
from app.services.market_service import calculate_opportunity_score


def test_password_hashing():
    raw = "SuperSecretPassword123!"
    hashed = get_password_hash(raw)
    assert hashed != raw
    assert verify_password(raw, hashed) is True
    assert verify_password("WrongPassword", hashed) is False


def test_jwt_token_creation_and_decoding():
    payload = {"sub": "user-uuid-123", "role": "admin", "email": "test@globallead.ai"}
    token = create_access_token(payload)
    decoded = decode_token(token)
    assert decoded["sub"] == "user-uuid-123"
    assert decoded["role"] == "admin"
    assert decoded["email"] == "test@globallead.ai"


def test_phone_normalization_valid_us():
    res = normalize_phone_number("260-555-0199", "US")
    assert res["is_valid"] is True
    assert res["status"] == "FORMAT_VALID"
    assert res["formatted"].startswith("+1")


def test_phone_normalization_invalid():
    res = normalize_phone_number("12345", "US")
    assert res["is_valid"] is False
    assert res["status"] == "FAILED_VERIFICATION"


def test_opportunity_scoring_calculation():
    scores = calculate_opportunity_score(
        population=265000,
        avg_lead_value=150.0,
        contractor_count=8,
        median_income=54000.0,
    )
    assert "overall_score" in scores
    assert scores["overall_score"] > 60.0
    assert scores["demand_score"] == 78.0
    assert scores["contractor_availability_score"] == 80.0
