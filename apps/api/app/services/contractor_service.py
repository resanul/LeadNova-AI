from typing import Optional, Dict, Any, List
import phonenumbers
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.entities import Contractor, Wallet

VERIFICATION_LEVELS = [
    "NOT_AVAILABLE",
    "DISCOVERED",
    "FORMAT_VALID",
    "PROVIDER_VALIDATED",
    "REACHABILITY_CHECKED",
    "BUSINESS_CONFIRMED",
    "FAILED_VERIFICATION",
]


def normalize_phone_number(raw_phone: str, default_country: str = "US") -> Dict[str, Any]:
    """
    Parses and normalizes a phone number to standard E.164 format.
    Does NOT claim reachability; sets verification status to FORMAT_VALID if syntax passes.
    """
    if not raw_phone:
        return {"is_valid": False, "formatted": None, "status": "NOT_AVAILABLE"}
    
    try:
        parsed = phonenumbers.parse(raw_phone, default_country)
        if phonenumbers.is_valid_number(parsed):
            formatted_e164 = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
            return {
                "is_valid": True,
                "formatted": formatted_e164,
                "status": "FORMAT_VALID",
                "national_format": phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.NATIONAL),
            }
        else:
            return {"is_valid": False, "formatted": raw_phone, "status": "FAILED_VERIFICATION"}
    except Exception as e:
        return {"is_valid": False, "formatted": raw_phone, "status": "FAILED_VERIFICATION", "error": str(e)}


async def find_existing_contractor(
    db: AsyncSession,
    business_name: str,
    normalized_phone: Optional[str],
    city: str,
) -> Optional[Contractor]:
    """Check for duplicate contractor records by phone or business name in the same city."""
    if normalized_phone:
        query_by_phone = select(Contractor).where(Contractor.primary_phone == normalized_phone)
        res = await db.execute(query_by_phone)
        existing = res.scalars().first()
        if existing:
            return existing

    query_by_name = select(Contractor).where(
        Contractor.business_name.ilike(business_name),
        Contractor.city.ilike(city),
    )
    res_name = await db.execute(query_by_name)
    return res_name.scalars().first()


async def register_contractor(
    db: AsyncSession,
    data: Dict[str, Any],
    auto_create_wallet: bool = True,
) -> Contractor:
    """Creates a new contractor and initializes their financial ledger wallet."""
    # Normalize phone
    phone_info = normalize_phone_number(data.get("primary_phone", ""), data.get("country", "US"))
    clean_phone = phone_info["formatted"] if phone_info["is_valid"] else data.get("primary_phone", "")
    verification_status = phone_info["status"]

    contractor = Contractor(
        business_name=data["business_name"],
        owner_name=data.get("owner_name"),
        primary_phone=clean_phone,
        secondary_phone=data.get("secondary_phone"),
        email=data.get("email"),
        website=data.get("website"),
        address=data.get("address"),
        city=data["city"],
        state=data["state"],
        country=data.get("country", "US"),
        postal_code=data.get("postal_code"),
        latitude=data.get("latitude"),
        longitude=data.get("longitude"),
        rating=data.get("rating", 0.0),
        review_count=data.get("review_count", 0),
        verification_status=verification_status,
        partner_status=data.get("partner_status", "PROSPECT"),
        discovery_source=data.get("discovery_source", "MANUAL_ENTRY"),
    )
    db.add(contractor)
    await db.flush()

    if auto_create_wallet:
        wallet = Wallet(contractor_id=contractor.id, balance=0.00, reserved_balance=0.00)
        db.add(wallet)

    await db.commit()
    await db.refresh(contractor)
    return contractor
