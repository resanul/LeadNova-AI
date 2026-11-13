from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from sqlalchemy.future import select
from app.core.config import settings
from app.core.database import engine, Base, AsyncSessionLocal
from app.core.security import get_password_hash
from app.models.entities import User
from app.services.market_service import seed_market_defaults
from app.services.agent_orchestrator import seed_agents
from app.routers import (
    auth,
    market,
    contractors,
    websites,
    leads,
    telephony,
    billing,
    agents,
    analytics,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize DB tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Seed Super Admin, Market Defaults, and 17 AI Agents
    async with AsyncSessionLocal() as session:
        # 1. Super Admin
        admin_res = await session.execute(
            select(User).where(User.email == settings.FIRST_SUPERUSER_EMAIL)
        )
        if not admin_res.scalars().first():
            admin_user = User(
                email=settings.FIRST_SUPERUSER_EMAIL,
                hashed_password=get_password_hash(settings.FIRST_SUPERUSER_PASSWORD),
                full_name="GlobalLead Super Administrator",
                role="super_admin",
                is_active=True,
            )
            session.add(admin_user)
            await session.commit()

        # 2. Market defaults
        await seed_market_defaults(session)

        # 3. 17 AI Agents
        await seed_agents(session)

    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Enterprise Multi-Tenant Pay-Per-Lead (PPL) and Business Operating System API",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Router Registrations
api_prefix = settings.API_V1_STR
app.include_router(auth.router, prefix=api_prefix)
app.include_router(market.router, prefix=api_prefix)
app.include_router(contractors.router, prefix=api_prefix)
app.include_router(websites.router, prefix=api_prefix)
app.include_router(leads.router, prefix=api_prefix)
app.include_router(telephony.router, prefix=api_prefix)
app.include_router(billing.router, prefix=api_prefix)
app.include_router(agents.router, prefix=api_prefix)
app.include_router(analytics.router, prefix=api_prefix)


@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")
