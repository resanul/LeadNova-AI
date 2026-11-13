from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.database import get_db
from app.models.entities import Wallet, LedgerEntry, Contractor
from app.schemas.all_schemas import WalletResponse, LedgerEntryResponse, DepositRequest
from app.services.billing_service import deposit_funds
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/billing", tags=["Financial Engine & Wallets"])


@router.get("/wallets", response_model=List[WalletResponse])
async def list_wallets(
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    res = await db.execute(select(Wallet))
    return res.scalars().all()


@router.get("/wallets/{contractor_id}", response_model=WalletResponse)
async def get_contractor_wallet(
    contractor_id: str,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    res = await db.execute(select(Wallet).where(Wallet.contractor_id == contractor_id))
    wallet = res.scalars().first()
    if not wallet:
        raise HTTPException(status_code=404, detail="Contractor wallet not found")
    return wallet


@router.post("/wallets/{contractor_id}/deposit", response_model=LedgerEntryResponse)
async def topup_contractor_wallet(
    contractor_id: str,
    req: DepositRequest,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    entry = await deposit_funds(
        db=db,
        contractor_id=contractor_id,
        amount=req.amount,
        description=req.description,
        idempotency_key=req.idempotency_key,
    )
    return entry


@router.get("/ledger", response_model=List[LedgerEntryResponse])
async def list_ledger_entries(
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    res = await db.execute(
        select(LedgerEntry).order_by(LedgerEntry.created_at.desc()).limit(limit)
    )
    return res.scalars().all()
