from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Response, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.database import get_db
from app.models.entities import PhoneNumber, LandingPage
from app.services.telephony_service import route_inbound_call

router = APIRouter(prefix="", tags=["Telephony & Call Routing"])


@router.get("/phone-numbers")
async def list_phone_numbers(db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(PhoneNumber))
    return res.scalars().all()


@router.post("/phone-numbers/assign")
async def assign_phone_number(
    phone_number: str,
    landing_page_id: str,
    db: AsyncSession = Depends(get_db),
):
    res = await db.execute(select(PhoneNumber).where(PhoneNumber.phone_number == phone_number))
    num = res.scalars().first()
    if not num:
        num = PhoneNumber(phone_number=phone_number, landing_page_id=landing_page_id)
        db.add(num)
    else:
        num.landing_page_id = landing_page_id
    await db.commit()
    await db.refresh(num)
    return num


@router.post("/webhooks/twilio/voice")
async def twilio_voice_webhook(
    To: str = Form(...),
    From: str = Form(...),
    CallSid: Optional[str] = Form(None),
    db: AsyncSession = Depends(get_db),
):
    """
    Twilio voice webhook for live call forwarding to assigned contractor.
    Returns standard TwiML XML.
    """
    result = await route_inbound_call(db, called_number=To, caller_phone=From)
    return Response(content=result["twiml"], media_type="application/xml")


@router.post("/webhooks/telnyx/voice")
async def telnyx_voice_webhook(
    payload: dict,
    db: AsyncSession = Depends(get_db),
):
    """Telnyx webhook for call routing."""
    data = payload.get("data", {}).get("payload", {})
    to_number = data.get("to")
    from_number = data.get("from")
    result = await route_inbound_call(db, called_number=to_number, caller_phone=from_number)
    return {"status": "success", "routing": result}
