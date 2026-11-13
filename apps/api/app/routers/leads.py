from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.database import get_db
from app.models.entities import Lead, LeadAssignment
from app.schemas.all_schemas import LeadResponse, LeadCaptureRequest
from app.services.lead_service import process_incoming_lead
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/leads", tags=["Lead Management"])


@router.get("", response_model=List[LeadResponse])
async def list_leads(
    status_filter: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    query = select(Lead)
    if status_filter:
        query = query.where(Lead.qualification_status == status_filter)
    res = await db.execute(query.order_by(Lead.created_at.desc()))
    return res.scalars().all()


@router.post("/capture", response_model=LeadResponse)
async def capture_lead(lead_in: LeadCaptureRequest, db: AsyncSession = Depends(get_db)):
    """Public customer-facing lead capture endpoint."""
    lead = await process_incoming_lead(
        db=db,
        city_id=lead_in.city_id,
        niche_id=lead_in.niche_id,
        raw_phone=lead_in.customer_phone,
        customer_name=lead_in.customer_name,
        customer_email=lead_in.customer_email,
        lead_source=lead_in.lead_source,
        details=lead_in.details,
    )
    return lead


@router.post("/{id}/dispute")
async def dispute_lead(
    id: str,
    reason: str,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    res = await db.execute(select(Lead).where(Lead.id == id))
    lead = res.scalars().first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    lead.qualification_status = "DISPUTED"
    await db.commit()
    return {"status": "DISPUTE_SUBMITTED", "lead_id": lead.id, "reason": reason}
