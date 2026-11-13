from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.database import get_db
from app.models.entities import Contractor, ContractorAgreement, Wallet
from app.schemas.all_schemas import (
    ContractorResponse, ContractorCreate, ContractorUpdate,
    AgreementResponse, AgreementCreate,
)
from app.services.contractor_service import register_contractor, normalize_phone_number
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/contractors", tags=["Contractor Operations"])


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
