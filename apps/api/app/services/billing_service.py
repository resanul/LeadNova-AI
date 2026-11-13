from typing import Dict, Any, Optional
from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException, status
from app.models.entities import Wallet, LedgerEntry


async def deposit_funds(
    db: AsyncSession,
    contractor_id: str,
    amount: float,
    description: str,
    idempotency_key: str,
) -> LedgerEntry:
    """
    Credits a contractor wallet atomically using row-level locking.
    Creates an immutable append-only ledger entry.
    """
    if amount <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Deposit amount must be positive")

    # Check idempotency
    existing_entry = await db.execute(select(LedgerEntry).where(LedgerEntry.idempotency_key == idempotency_key))
    if existing_entry.scalars().first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Idempotency key has already been executed")

    # Lock wallet row for update
    wallet_query = select(Wallet).where(Wallet.contractor_id == contractor_id).with_for_update()
    res = await db.execute(wallet_query)
    wallet = res.scalars().first()
    if not wallet:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contractor wallet not found")

    new_balance = float(wallet.balance) + amount
    wallet.balance = new_balance
    wallet.version += 1

    entry = LedgerEntry(
        wallet_id=wallet.id,
        entry_type="PREPAID_DEPOSIT",
        amount=amount,
        balance_after=new_balance,
        description=description,
        idempotency_key=idempotency_key,
    )
    db.add(entry)
    await db.commit()
    await db.refresh(entry)
    return entry


async def charge_lead(
    db: AsyncSession,
    contractor_id: str,
    assignment_id: str,
    amount: float,
    description: str,
    idempotency_key: str,
) -> LedgerEntry:
    """
    Deducts qualified lead fee from contractor wallet atomically with row-level locking.
    Rejects if wallet balance is insufficient.
    """
    if amount <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Charge amount must be positive")

    # Check idempotency
    existing_entry = await db.execute(select(LedgerEntry).where(LedgerEntry.idempotency_key == idempotency_key))
    if existing_entry.scalars().first():
        return existing_entry.scalars().first()

    # Lock wallet row for update
    wallet_query = select(Wallet).where(Wallet.contractor_id == contractor_id).with_for_update()
    res = await db.execute(wallet_query)
    wallet = res.scalars().first()
    if not wallet:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contractor wallet not found")

    if float(wallet.balance) < amount:
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail=f"Insufficient wallet balance (${wallet.balance}) for lead charge (${amount})",
        )

    new_balance = float(wallet.balance) - amount
    wallet.balance = new_balance
    wallet.version += 1

    entry = LedgerEntry(
        wallet_id=wallet.id,
        assignment_id=assignment_id,
        entry_type="LEAD_CHARGE",
        amount=-amount,
        balance_after=new_balance,
        description=description,
        idempotency_key=idempotency_key,
    )
    db.add(entry)
    await db.commit()
    await db.refresh(entry)
    return entry
