from typing import Dict, Any, Optional
import json
import os
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.entities import Contractor, Niche, City
from app.core.config import settings


async def generate_contractor_pitch(
    db: AsyncSession,
    contractor_id: str,
    niche_id: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Generates high-converting B2B outreach proposals (Email, SMS, Cold Call Script)
    to recruit local contractors into the Pay-Per-Lead partner network.
    """
    res = await db.execute(select(Contractor).where(Contractor.id == contractor_id))
    contractor = res.scalars().first()
    if not contractor:
        raise ValueError("Contractor not found")

    # Determine niche
    niche_name = "Water Damage Restoration"
    avg_price = 75.0
    if niche_id:
        niche_res = await db.execute(select(Niche).where(Niche.id == niche_id))
        niche = niche_res.scalars().first()
        if niche:
            niche_name = niche.name
            avg_price = float(niche.avg_lead_value)

    business_name = contractor.business_name
    contact_name = contractor.owner_name or "Business Owner"
    city = contractor.city
    state = contractor.state

    # 1. Cold B2B Partnership Email
    cold_email_subject = f"Exclusive emergency {niche_name.lower()} inquiries in {city} — can your crew take 5-10 extra jobs/week?"
    cold_email_body = f"""Hi {contact_name},

I came across {business_name} while reviewing licensed service professionals in {city}.

Our local media network generates pre-screened, live inbound phone calls and emergency inquiries from homeowners needing urgent {niche_name.lower()} across {city} and surrounding areas.

We are currently looking for ONE reliable, licensed partner in {city} to receive these inquiries exclusively. 

Here is our model:
- 100% Exclusive: We never send the same customer to multiple contractors.
- Zero Upfront Setup Fees: You only pay a flat fee (${avg_price:.0f}) per qualified, dispatched customer.
- Free First Lead: We'll send your first emergency call on us so you can verify the lead quality and close rate.

Do you have capacity to take on an extra 5 to 10 jobs per week in {city}? 

If so, let me know what phone number is best to reach you or reply to this email, and we can turn on lead routing tomorrow.

Best regards,

Partnership Team | GlobalLead AI Network
service@{city.lower().replace(' ', '')}emergencypros.com
"""

    # 2. Direct SMS Outreach Pitch
    sms_pitch = (
        f"Hi {contact_name}, this is the local {city} home services dispatch network. "
        f"We have live inbound {niche_name.lower()} customer calls in {city} ready to route. "
        f"Can {business_name} take on 5-10 exclusive jobs this week? Reply YES for details."
    )

    # 3. Cold Call Telephone Script (for sales / SDR reps)
    cold_call_script = f"""[Cold Call Script - 60 Seconds]
Rep: "Hi {contact_name}! My name is Alex with the {city} Emergency Contractor Dispatch. Quick question—are you currently accepting new {niche_name.lower()} jobs in {city}?"

[If Yes]:
Rep: "Great! Our local digital platform receives verified emergency homeowner calls every week in {city}. We don't sell shared leads like Angie or HomeAdvisor—every call is exclusive, live, and routed directly to your phone. We'd like to send you 2-3 trial calls this week at zero upfront cost to see if our quality matches your standards. What is the direct cell or dispatch number we should route these calls to?"

[If No / Skeptical]:
Rep: "Totally understand! Keep our number handy. If your schedule opens up next week, let us know and we'll activate your service radius."
"""

    return {
        "contractor_id": contractor.id,
        "business_name": business_name,
        "city": city,
        "niche": niche_name,
        "cold_email": {
            "subject": cold_email_subject,
            "body": cold_email_body,
        },
        "sms_pitch": sms_pitch,
        "cold_call_script": cold_call_script,
    }
