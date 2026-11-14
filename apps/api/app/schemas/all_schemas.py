from datetime import datetime, date
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, EmailStr, Field, ConfigDict


# --- Auth & User ---
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class TokenPayload(BaseModel):
    sub: Optional[str] = None
    role: Optional[str] = None
    email: Optional[str] = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    role: str = "admin"
    tenant_id: Optional[str] = None


class UserResponse(BaseModel):
    id: str
    email: str
    full_name: str
    role: str
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# --- Market Intelligence ---
class CountryCreate(BaseModel):
    code: str = Field(..., min_length=2, max_length=2)
    name: str
    currency: str = "USD"
    phone_prefix: str = "+1"


class CountryResponse(BaseModel):
    id: str
    code: str
    name: str
    currency: str
    phone_prefix: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class CityCreate(BaseModel):
    state_id: str
    name: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    population: int = 0
    median_income: float = 0.0
    homeownership_rate: float = 0.0


class CityResponse(BaseModel):
    id: str
    name: str
    latitude: Optional[float]
    longitude: Optional[float]
    population: int
    median_income: float
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class NicheCreate(BaseModel):
    name: str
    slug: str
    avg_lead_value: float = 50.0
    emergency_level: str = "high"
    description: Optional[str] = None


class NicheResponse(BaseModel):
    id: str
    name: str
    slug: str
    avg_lead_value: float
    emergency_level: str
    description: Optional[str]
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class OpportunityEvaluateRequest(BaseModel):
    city_id: str
    niche_id: str


class OpportunityResponse(BaseModel):
    id: str
    city_id: str
    niche_id: str
    city_name: Optional[str] = None
    niche_name: Optional[str] = None
    demand_score: float
    commercial_value_score: float
    contractor_availability_score: float
    competition_score: float
    cac_score: float
    stability_score: float
    confidence_score: float
    overall_score: float
    status: str
    metrics_data: Dict[str, Any] = {}

    model_config = ConfigDict(from_attributes=True)


# --- Contractors ---
class ContractorCreate(BaseModel):
    business_name: str
    owner_name: Optional[str] = None
    primary_phone: str
    secondary_phone: Optional[str] = None
    email: Optional[EmailStr] = None
    website: Optional[str] = None
    address: Optional[str] = None
    city: str
    state: str
    country: str = "US"
    postal_code: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    discovery_source: str = "MANUAL_ENTRY"


class ContractorUpdate(BaseModel):
    business_name: Optional[str] = None
    owner_name: Optional[str] = None
    primary_phone: Optional[str] = None
    email: Optional[EmailStr] = None
    website: Optional[str] = None
    address: Optional[str] = None
    rating: Optional[float] = None
    verification_status: Optional[str] = None
    partner_status: Optional[str] = None
    verification_notes: Optional[str] = None


class ContractorResponse(BaseModel):
    id: str
    business_name: str
    owner_name: Optional[str]
    primary_phone: str
    secondary_phone: Optional[str]
    email: Optional[str]
    website: Optional[str]
    address: Optional[str]
    city: str
    state: str
    country: str
    rating: float
    review_count: int
    verification_status: str
    partner_status: str
    discovery_source: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AgreementCreate(BaseModel):
    contractor_id: str
    niche_id: str
    lead_type: str = "EXCLUSIVE_CALL"
    price_per_lead: float = 75.0
    min_call_duration_seconds: int = 60
    auto_recharge_threshold: float = 100.0
    auto_recharge_amount: float = 500.0


class AgreementResponse(BaseModel):
    id: str
    contractor_id: str
    niche_id: str
    lead_type: str
    price_per_lead: float
    min_call_duration_seconds: int
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


# --- Websites & Landing Pages ---
class WebsiteCreate(BaseModel):
    domain: str
    title: str
    theme_config: Dict[str, Any] = {}


class WebsiteResponse(BaseModel):
    id: str
    domain: str
    title: str
    is_published: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class LandingPageCreate(BaseModel):
    website_id: str
    city_id: str
    niche_id: str
    slug: str
    headline: str
    content_body: str
    seo_title: Optional[str] = None
    seo_description: Optional[str] = None
    tracking_phone: Optional[str] = None


class LandingPageResponse(BaseModel):
    id: str
    website_id: str
    city_id: str
    niche_id: str
    slug: str
    headline: str
    content_body: str
    seo_title: Optional[str]
    tracking_phone: Optional[str]
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# --- Leads & Telephony ---
class LeadCaptureRequest(BaseModel):
    city_id: str
    niche_id: str
    customer_name: Optional[str] = None
    customer_phone: str
    customer_email: Optional[EmailStr] = None
    lead_source: str = "WEB_FORM"
    details: Optional[str] = None


class LeadResponse(BaseModel):
    id: str
    city_id: str
    niche_id: str
    customer_name: Optional[str]
    customer_phone: str
    customer_email: Optional[str]
    lead_source: str
    qualification_status: str
    details: Optional[str]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CallWebhookRequest(BaseModel):
    CallSid: str
    From: str
    To: str
    CallDuration: Optional[int] = 0
    CallStatus: str = "completed"


class CallRoutingResult(BaseModel):
    destination_phone: str
    contractor_id: Optional[str] = None
    business_name: Optional[str] = None
    route_status: str  # ROUTED, FALLBACK, UNASSIGNED


# --- Billing & Wallets ---
class DepositRequest(BaseModel):
    amount: float = Field(..., gt=0.0)
    description: str = "Prepaid wallet top-up"
    idempotency_key: str


class WalletResponse(BaseModel):
    id: str
    contractor_id: str
    currency: str
    balance: float
    reserved_balance: float
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class LedgerEntryResponse(BaseModel):
    id: str
    wallet_id: str
    entry_type: str
    amount: float
    balance_after: float
    description: str
    idempotency_key: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# --- Agents & Analytics ---
class AgentResponse(BaseModel):
    id: str
    name: str
    purpose: str
    model_name: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class AgentRunRequest(BaseModel):
    input_payload: Dict[str, Any] = {}


class AgentRunResponse(BaseModel):
    run_id: str
    agent_name: str
    status: str
    output_payload: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None


class SystemHealthResponse(BaseModel):
    status: str
    database: str
    version: str
    timestamp: datetime


class AnalyticsOverviewResponse(BaseModel):
    total_countries: int
    total_cities: int
    total_niches: int
    total_contractors: int
    verified_contractors: int
    active_contractors: int
    total_leads: int
    qualified_leads: int
    total_revenue_usd: float
    total_calls_routed: int
