import uuid
from datetime import datetime, timezone
from sqlalchemy import (
    Column,
    String,
    Boolean,
    Integer,
    Numeric,
    Text,
    DateTime,
    ForeignKey,
    JSON,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from app.core.database import Base


def generate_uuid() -> str:
    return str(uuid.uuid4())


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class Tenant(Base):
    __tablename__ = "tenants"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(255), nullable=False)
    slug = Column(String(100), unique=True, nullable=False)
    plan = Column(String(50), default="standard")
    status = Column(String(50), default="active")
    settings = Column(JSON, default=dict)
    created_at = Column(DateTime(timezone=True), default=utc_now)
    updated_at = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now)

    users = relationship("User", back_populates="tenant", cascade="all, delete-orphan")


class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    tenant_id = Column(String(36), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    role = Column(String(50), default="admin")  # super_admin, admin, analyst, contractor
    contractor_id = Column(String(36), nullable=True)
    is_active = Column(Boolean, default=True)
    last_login_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), default=utc_now)
    updated_at = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now)

    tenant = relationship("Tenant", back_populates="users")


class Country(Base):
    __tablename__ = "countries"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    code = Column(String(2), unique=True, index=True, nullable=False)  # US, GB, CA, AU, etc.
    name = Column(String(100), nullable=False)
    currency = Column(String(3), default="USD")
    phone_prefix = Column(String(10), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=utc_now)

    states = relationship("State", back_populates="country", cascade="all, delete-orphan")


class State(Base):
    __tablename__ = "states"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    country_id = Column(String(36), ForeignKey("countries.id", ondelete="CASCADE"), nullable=False)
    code = Column(String(10), nullable=False)
    name = Column(String(100), nullable=False)
    created_at = Column(DateTime(timezone=True), default=utc_now)

    country = relationship("Country", back_populates="states")
    cities = relationship("City", back_populates="state", cascade="all, delete-orphan")

    __table_args__ = (UniqueConstraint("country_id", "code", name="uq_country_state_code"),)


class City(Base):
    __tablename__ = "cities"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    state_id = Column(String(36), ForeignKey("states.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(150), index=True, nullable=False)
    latitude = Column(Numeric(10, 7), nullable=True)
    longitude = Column(Numeric(10, 7), nullable=True)
    population = Column(Integer, default=0)
    median_income = Column(Numeric(12, 2), default=0.0)
    homeownership_rate = Column(Numeric(5, 2), default=0.0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=utc_now)

    state = relationship("State", back_populates="cities")
    opportunities = relationship("Opportunity", back_populates="city", cascade="all, delete-orphan")


class Niche(Base):
    __tablename__ = "niches"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(150), unique=True, index=True, nullable=False)
    slug = Column(String(150), unique=True, index=True, nullable=False)
    avg_lead_value = Column(Numeric(10, 2), default=50.00)
    emergency_level = Column(String(20), default="high")
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=utc_now)

    opportunities = relationship("Opportunity", back_populates="niche", cascade="all, delete-orphan")


class Opportunity(Base):
    __tablename__ = "opportunities"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    city_id = Column(String(36), ForeignKey("cities.id", ondelete="CASCADE"), nullable=False)
    niche_id = Column(String(36), ForeignKey("niches.id", ondelete="CASCADE"), nullable=False)
    demand_score = Column(Numeric(5, 2), default=0.0)
    commercial_value_score = Column(Numeric(5, 2), default=0.0)
    contractor_availability_score = Column(Numeric(5, 2), default=0.0)
    competition_score = Column(Numeric(5, 2), default=0.0)
    cac_score = Column(Numeric(5, 2), default=0.0)
    stability_score = Column(Numeric(5, 2), default=0.0)
    confidence_score = Column(Numeric(5, 2), default=0.0)
    overall_score = Column(Numeric(5, 2), default=0.0)
    status = Column(String(50), default="discovered")  # discovered, researching, viable, activated, paused
    metrics_data = Column(JSON, default=dict)
    created_at = Column(DateTime(timezone=True), default=utc_now)
    updated_at = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now)

    city = relationship("City", back_populates="opportunities")
    niche = relationship("Niche", back_populates="opportunities")

    __table_args__ = (UniqueConstraint("city_id", "niche_id", name="uq_city_niche_opp"),)


class Contractor(Base):
    __tablename__ = "contractors"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    tenant_id = Column(String(36), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=True)
    business_name = Column(String(255), index=True, nullable=False)
    owner_name = Column(String(255), nullable=True)
    primary_phone = Column(String(50), index=True, nullable=False)
    secondary_phone = Column(String(50), nullable=True)
    email = Column(String(255), nullable=True)
    website = Column(String(255), nullable=True)
    address = Column(String(255), nullable=True)
    city = Column(String(150), index=True, nullable=False)
    state = Column(String(50), nullable=False)
    country = Column(String(10), default="US")
    postal_code = Column(String(20), nullable=True)
    latitude = Column(Numeric(10, 7), nullable=True)
    longitude = Column(Numeric(10, 7), nullable=True)
    rating = Column(Numeric(3, 2), default=0.0)
    review_count = Column(Integer, default=0)
    verification_status = Column(String(50), default="DISCOVERED")
    verification_notes = Column(Text, nullable=True)
    partner_status = Column(String(50), default="PROSPECT")  # PROSPECT, CONTACTED, ACTIVE, PAUSED, REJECTED
    discovery_source = Column(String(100), default="GOOGLE_PLACES")
    created_at = Column(DateTime(timezone=True), default=utc_now)
    updated_at = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now)

    agreements = relationship("ContractorAgreement", back_populates="contractor", cascade="all, delete-orphan")
    wallet = relationship("Wallet", back_populates="contractor", uselist=False, cascade="all, delete-orphan")


class ContractorAgreement(Base):
    __tablename__ = "contractor_agreements"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    contractor_id = Column(String(36), ForeignKey("contractors.id", ondelete="CASCADE"), nullable=False)
    niche_id = Column(String(36), ForeignKey("niches.id", ondelete="CASCADE"), nullable=False)
    lead_type = Column(String(50), default="EXCLUSIVE_CALL")  # EXCLUSIVE_CALL, SHARED_CALL, FORM_LEAD
    price_per_lead = Column(Numeric(10, 2), default=75.00)
    min_call_duration_seconds = Column(Integer, default=60)
    auto_recharge_threshold = Column(Numeric(10, 2), default=100.00)
    auto_recharge_amount = Column(Numeric(10, 2), default=500.00)
    is_active = Column(Boolean, default=True)
    valid_from = Column(DateTime(timezone=True), default=utc_now)
    valid_until = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), default=utc_now)

    contractor = relationship("Contractor", back_populates="agreements")
    niche = relationship("Niche")


class Website(Base):
    __tablename__ = "websites"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    tenant_id = Column(String(36), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=True)
    domain = Column(String(255), unique=True, index=True, nullable=False)
    title = Column(String(255), nullable=False)
    theme_config = Column(JSON, default=dict)
    is_published = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), default=utc_now)

    landing_pages = relationship("LandingPage", back_populates="website", cascade="all, delete-orphan")


class LandingPage(Base):
    __tablename__ = "landing_pages"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    website_id = Column(String(36), ForeignKey("websites.id", ondelete="CASCADE"), nullable=False)
    city_id = Column(String(36), ForeignKey("cities.id", ondelete="CASCADE"), nullable=False)
    niche_id = Column(String(36), ForeignKey("niches.id", ondelete="CASCADE"), nullable=False)
    slug = Column(String(255), nullable=False)
    headline = Column(String(255), nullable=False)
    content_body = Column(Text, nullable=False)
    seo_title = Column(String(255), nullable=True)
    seo_description = Column(Text, nullable=True)
    tracking_phone = Column(String(50), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=utc_now)

    website = relationship("Website", back_populates="landing_pages")
    city = relationship("City")
    niche = relationship("Niche")

    __table_args__ = (UniqueConstraint("website_id", "slug", name="uq_website_slug"),)


class PhoneNumber(Base):
    __tablename__ = "phone_numbers"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    phone_number = Column(String(50), unique=True, index=True, nullable=False)
    provider = Column(String(50), default="TWILIO")  # TWILIO, TELNYX
    landing_page_id = Column(String(36), ForeignKey("landing_pages.id"), nullable=True)
    status = Column(String(50), default="ACTIVE")
    monthly_cost = Column(Numeric(6, 2), default=1.00)
    created_at = Column(DateTime(timezone=True), default=utc_now)


class Lead(Base):
    __tablename__ = "leads"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    tenant_id = Column(String(36), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=True)
    niche_id = Column(String(36), ForeignKey("niches.id"), nullable=False)
    city_id = Column(String(36), ForeignKey("cities.id"), nullable=False)
    customer_name = Column(String(255), nullable=True)
    customer_phone = Column(String(50), index=True, nullable=False)
    customer_email = Column(String(255), nullable=True)
    lead_source = Column(String(50), default="PHONE_CALL")  # PHONE_CALL, WEB_FORM
    qualification_status = Column(String(50), default="NEW")  # NEW, QUALIFIED, SPAM, DUPLICATE, REJECTED
    details = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=utc_now)

    niche = relationship("Niche")
    city = relationship("City")
    assignments = relationship("LeadAssignment", back_populates="lead", cascade="all, delete-orphan")


class LeadAssignment(Base):
    __tablename__ = "lead_assignments"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    lead_id = Column(String(36), ForeignKey("leads.id", ondelete="CASCADE"), nullable=False)
    contractor_id = Column(String(36), ForeignKey("contractors.id", ondelete="CASCADE"), nullable=False)
    agreement_id = Column(String(36), ForeignKey("contractor_agreements.id"), nullable=True)
    delivery_status = Column(String(50), default="DELIVERED")  # DELIVERED, ACCEPTED, DISPUTED, REFUNDED
    charged_amount = Column(Numeric(10, 2), default=0.0)
    delivered_at = Column(DateTime(timezone=True), default=utc_now)

    lead = relationship("Lead", back_populates="assignments")
    contractor = relationship("Contractor")


class Wallet(Base):
    __tablename__ = "wallets"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    contractor_id = Column(String(36), ForeignKey("contractors.id", ondelete="CASCADE"), unique=True, nullable=False)
    currency = Column(String(3), default="USD")
    balance = Column(Numeric(12, 2), default=0.00)
    reserved_balance = Column(Numeric(12, 2), default=0.00)
    version = Column(Integer, default=1)
    created_at = Column(DateTime(timezone=True), default=utc_now)
    updated_at = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now)

    contractor = relationship("Contractor", back_populates="wallet")
    entries = relationship("LedgerEntry", back_populates="wallet", cascade="all, delete-orphan")


class LedgerEntry(Base):
    __tablename__ = "ledger_entries"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    wallet_id = Column(String(36), ForeignKey("wallets.id", ondelete="RESTRICT"), nullable=False)
    assignment_id = Column(String(36), ForeignKey("lead_assignments.id"), nullable=True)
    entry_type = Column(String(50), nullable=False)  # PREPAID_DEPOSIT, LEAD_CHARGE, REFUND, ADJUSTMENT
    amount = Column(Numeric(12, 2), nullable=False)  # Negative for charge, positive for deposit/refund
    balance_after = Column(Numeric(12, 2), nullable=False)
    description = Column(Text, nullable=False)
    idempotency_key = Column(String(255), unique=True, index=True, nullable=False)
    created_at = Column(DateTime(timezone=True), default=utc_now)

    wallet = relationship("Wallet", back_populates="entries")


class Agent(Base):
    __tablename__ = "agents"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(100), unique=True, index=True, nullable=False)
    purpose = Column(Text, nullable=False)
    model_name = Column(String(100), default="gemini-1.5-flash")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=utc_now)

    runs = relationship("AgentRun", back_populates="agent", cascade="all, delete-orphan")


class AgentRun(Base):
    __tablename__ = "agent_runs"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    agent_id = Column(String(36), ForeignKey("agents.id", ondelete="CASCADE"), nullable=False)
    status = Column(String(50), default="RUNNING")  # RUNNING, COMPLETED, FAILED
    input_payload = Column(JSON, default=dict)
    output_payload = Column(JSON, nullable=True)
    tokens_consumed = Column(Integer, default=0)
    cost_usd = Column(Numeric(8, 4), default=0.0)
    error_message = Column(Text, nullable=True)
    started_at = Column(DateTime(timezone=True), default=utc_now)
    completed_at = Column(DateTime(timezone=True), nullable=True)

    agent = relationship("Agent", back_populates="runs")


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), nullable=True)
    action = Column(String(100), index=True, nullable=False)
    entity_name = Column(String(100), nullable=False)
    entity_id = Column(String(36), nullable=True)
    details = Column(JSON, default=dict)
    ip_address = Column(String(50), nullable=True)
    created_at = Column(DateTime(timezone=True), default=utc_now)
