from typing import Dict, Any, Optional
from datetime import datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.models.entities import Lead, LeadAssignment, Contractor, ContractorAgreement, Wallet
from app.services.contractor_service import normalize_phone_number
from app.services.billing_service import charge_lead


async def process_incoming_lead(
    db: AsyncSession,
    city_id: str,
    niche_id: str,
    raw_phone: str,
    customer_name: Optional[str] = None,
    customer_email: Optional[str] = None,
    lead_source: str = "WEB_FORM",
    details: Optional[str] = None,
) -> Lead:
    """
    Ingests and qualifies a new lead with duplicate checking and smart contractor matching.
    """
    # 1. Normalize phone
    phone_info = normalize_phone_number(raw_phone)
    clean_phone = phone_info["formatted"] if phone_info["is_valid"] else raw_phone

    # 2. Duplicate Detection (check within past 72 hours)
    three_days_ago = datetime.now(timezone.utc) - timedelta(hours=72)
    dup_query = select(Lead).where(
        Lead.customer_phone == clean_phone,
        Lead.niche_id == niche_id,
        Lead.created_at >= three_days_ago,
    )
    dup_res = await db.execute(dup_query)
    is_duplicate = dup_res.scalars().first() is not None

    # 3. Spam Detection Check
    is_spam = False
    if details:
        spam_signals = ["free backlink", "seo service", "viagra", "crypto casino", "test spam 123"]
        if any(signal in details.lower() for signal in spam_signals):
            is_spam = True

    # Assign qualification status
    if is_spam:
        qual_status = "SPAM"
    elif is_duplicate:
        qual_status = "DUPLICATE"
    elif not phone_info["is_valid"]:
        qual_status = "REJECTED"
    else:
        qual_status = "QUALIFIED"

    # Save lead
    lead = Lead(
        city_id=city_id,
        niche_id=niche_id,
        customer_name=customer_name,
        customer_phone=clean_phone,
        customer_email=customer_email,
        lead_source=lead_source,
        qualification_status=qual_status,
        details=details,
    )
    db.add(lead)
    await db.commit()
    await db.refresh(lead)

    # 4. If Qualified, execute deterministic Smart Contractor Matching
    if qual_status == "QUALIFIED":
        await match_and_deliver_lead(db, lead)

    return lead


async def match_and_deliver_lead(db: AsyncSession, lead: Lead) -> Optional[LeadAssignment]:
    """
    Finds the highest-ranked eligible contractor with an active agreement and sufficient wallet balance.
    """
    from app.models.entities import City
    city_res = await db.execute(select(City).where(City.id == lead.city_id))
    city = city_res.scalars().first()
    city_name = city.name if city else ""

    # Query contractors with active agreement for this niche in the city
    query = (
        select(Contractor, ContractorAgreement, Wallet)
        .join(ContractorAgreement, ContractorAgreement.contractor_id == Contractor.id)
        .join(Wallet, Wallet.contractor_id == Contractor.id)
        .where(
            Contractor.partner_status == "ACTIVE",
            Contractor.city.ilike(city_name),
            ContractorAgreement.niche_id == lead.niche_id,
            ContractorAgreement.is_active == True,
        )
        .order_by(Contractor.rating.desc(), Contractor.created_at.desc())
    )
    res = await db.execute(query)
    matches = res.all()

    for contractor, agreement, wallet in matches:
        price = float(agreement.price_per_lead)
        # Check wallet balance
        if float(wallet.balance) >= price:
            # Create delivery assignment
            assignment = LeadAssignment(
                lead_id=lead.id,
                contractor_id=contractor.id,
                agreement_id=agreement.id,
                delivery_status="DELIVERED",
                charged_amount=price,
            )
            db.add(assignment)
            await db.flush()

            # Execute atomic wallet deduction
            idempotency_key = f"charge_{lead.id}_{contractor.id}"
            await charge_lead(
                db=db,
                contractor_id=contractor.id,
                assignment_id=assignment.id,
                amount=price,
                description=f"Qualified lead delivery for {lead.customer_phone}",
                idempotency_key=idempotency_key,
            )

            await db.commit()
            return assignment

    return None
