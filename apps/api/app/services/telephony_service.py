from typing import Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.entities import PhoneNumber, LandingPage, Contractor, ContractorAgreement, Wallet
from app.services.lead_service import process_incoming_lead


async def route_inbound_call(
    db: AsyncSession,
    called_number: str,
    caller_phone: str,
) -> Dict[str, Any]:
    """
    Looks up tracking number and returns the forwarding destination phone number.
    Generates TwiML compliant dial response.
    """
    # Find active tracking phone number
    query = (
        select(PhoneNumber, LandingPage)
        .join(LandingPage, LandingPage.id == PhoneNumber.landing_page_id)
        .where(PhoneNumber.phone_number == called_number)
    )
    res = await db.execute(query)
    record = res.first()

    if not record:
        # Default unassigned response
        return {
            "action": "reject",
            "destination_phone": None,
            "twiml": "<Response><Say>Thank you for calling. This number is currently not in service.</Say><Hangup/></Response>",
        }

    phone_num, landing_page = record

    # Find active contractor for this city & niche with positive wallet balance
    contractor_query = (
        select(Contractor, ContractorAgreement, Wallet)
        .join(ContractorAgreement, ContractorAgreement.contractor_id == Contractor.id)
        .join(Wallet, Wallet.contractor_id == Contractor.id)
        .where(
            Contractor.city == landing_page.city_id,  # Or city match
            ContractorAgreement.niche_id == landing_page.niche_id,
            Contractor.partner_status == "ACTIVE",
            ContractorAgreement.is_active == True,
            Wallet.balance > 0,
        )
        .order_by(Contractor.rating.desc())
    )
    contractor_res = await db.execute(contractor_query)
    match = contractor_res.first()

    if match:
        contractor, agreement, wallet = match
        dest_phone = contractor.primary_phone
        twiml = f"""<Response>
    <Say>Connecting your call to a local verified specialist. This call may be recorded for quality assurance.</Say>
    <Dial timeout="30" record="false">{dest_phone}</Dial>
</Response>"""
        return {
            "action": "dial",
            "contractor_id": contractor.id,
            "destination_phone": dest_phone,
            "twiml": twiml,
        }

    # Fallback message
    return {
        "action": "voicemail",
        "destination_phone": None,
        "twiml": "<Response><Say>All specialists are currently assisting other customers. Please leave a message or try again later.</Say><Hangup/></Response>",
    }
