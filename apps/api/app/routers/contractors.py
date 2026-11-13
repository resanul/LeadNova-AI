from typing import List, Optional
import io
import csv
from fastapi import APIRouter, Depends, HTTPException, status, Response
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.database import get_db
from app.models.entities import Contractor, ContractorAgreement, Wallet
from app.schemas.all_schemas import (
    ContractorResponse, ContractorCreate, ContractorUpdate,
    AgreementResponse, AgreementCreate,
)
from app.services.contractor_service import register_contractor, normalize_phone_number
from app.services.contractor_discovery_service import ContractorDiscoveryPipeline
from app.services.outreach_service import generate_contractor_pitch
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/contractors", tags=["Contractor Operations"])


class DiscoveryRequest(BaseModel):
    city_id: str
    niche_id: str
    source: str = "OPENSTREETMAP"
    max_results: int = 10


class PitchRequest(BaseModel):
    niche_id: Optional[str] = None


@router.post("/{id}/generate-pitch")
async def create_contractor_pitch(
    id: str,
    req: PitchRequest = PitchRequest(),
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    """Generates customized B2B partnership proposal (Email, SMS, Cold Call script)."""
    try:
        pitch = await generate_contractor_pitch(db=db, contractor_id=id, niche_id=req.niche_id)
        return pitch
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("", response_model=List[ContractorResponse])
async def list_contractors(
    city: Optional[str] = None,
    partner_status: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    query = select(Contractor)
    if city:
        query = query.where(Contractor.city.ilike(f"%{city}%"))
    if partner_status:
        query = query.where(Contractor.partner_status == partner_status)
    res = await db.execute(query.order_by(Contractor.created_at.desc()))
    return res.scalars().all()


@router.post("", response_model=ContractorResponse)
async def create_contractor(
    contractor_in: ContractorCreate,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    contractor = await register_contractor(db, contractor_in.model_dump())
    return contractor


@router.post("/discover")
async def trigger_contractor_discovery(
    req: DiscoveryRequest,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    """
    Executes automated contractor discovery from OpenStreetMap / Google Places.
    Normalizes phones, deduplicates, and populates the contractor CRM database.
    """
    try:
        result = await ContractorDiscoveryPipeline.discover_contractors(
            db=db,
            city_id=req.city_id,
            niche_id=req.niche_id,
            source=req.source,
            max_results=req.max_results,
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/export/csv")
async def export_contractors_csv(
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    """Exports all contractor records as CSV format with verification statuses."""
    res = await db.execute(select(Contractor).order_by(Contractor.business_name))
    contractors = res.scalars().all()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "ID", "Business Name", "Owner", "Primary Phone", "Email", "Website",
        "City", "State", "Rating", "Reviews", "Verification Status", "Partner Status", "Source"
    ])
    for c in contractors:
        writer.writerow([
            c.id, c.business_name, c.owner_name or "", c.primary_phone,
            c.email or "", c.website or "", c.city, c.state,
            float(c.rating), c.review_count, c.verification_status,
            c.partner_status, c.discovery_source
        ])

    csv_content = output.getvalue()
    return Response(
        content=csv_content,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=contractors_export.csv"}
    )


@router.get("/{id}", response_model=ContractorResponse)
async def get_contractor(id: str, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Contractor).where(Contractor.id == id))
    contractor = res.scalars().first()
    if not contractor:
        raise HTTPException(status_code=404, detail="Contractor not found")
    return contractor


@router.patch("/{id}", response_model=ContractorResponse)
async def update_contractor(
    id: str,
    update_data: ContractorUpdate,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    res = await db.execute(select(Contractor).where(Contractor.id == id))
    contractor = res.scalars().first()
    if not contractor:
        raise HTTPException(status_code=404, detail="Contractor not found")

    for field, val in update_data.model_dump(exclude_unset=True).items():
        setattr(contractor, field, val)

    await db.commit()
    await db.refresh(contractor)
    return contractor


@router.post("/{id}/verify", response_model=ContractorResponse)
async def verify_contractor_phone(
    id: str,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    res = await db.execute(select(Contractor).where(Contractor.id == id))
    contractor = res.scalars().first()
    if not contractor:
        raise HTTPException(status_code=404, detail="Contractor not found")

    phone_info = normalize_phone_number(contractor.primary_phone, contractor.country)
    contractor.verification_status = phone_info["status"]
    if phone_info["is_valid"]:
        contractor.primary_phone = phone_info["formatted"]
        contractor.verification_notes = f"Verified international E.164: {phone_info['national_format']}"
    else:
        contractor.verification_notes = f"Phone verification failed: {phone_info.get('error', 'Invalid syntax')}"

    await db.commit()
    await db.refresh(contractor)
    return contractor


@router.post("/agreements", response_model=AgreementResponse)
async def create_agreement(
    agreement_in: AgreementCreate,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    agreement = ContractorAgreement(**agreement_in.model_dump())
    db.add(agreement)
    await db.commit()
    await db.refresh(agreement)
    return agreement
