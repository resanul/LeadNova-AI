# GLOBALLEAD AI - CHANGELOG

## [1.3.0] - 2026-11-14
### Added
- **Interactive Business Operating System Engine:** Full real-time operational workflows connecting Market Selection, Contractor Discovery, Asset Generation, B2B Outreach, and Inbound Lead Arbitrage:
  - `MarketLaunchModal.tsx`: 4-step wizard to evaluate markets, discover contractors, and publish landing pages.
  - `OutreachModal.tsx`: Generates 1-click tailored B2B Cold Email, Direct SMS, and 60-second Cold Call pitch scripts.
  - `LeadSimulatorModal.tsx`: Interactive tool to test live lead capture, duplicate filtering, smart contractor matching, and atomic wallet deductions.
  - `DashboardClient.tsx`: Real-time state management and immediate UI action dispatching.
- **Public Customer Emergency Landing Page (`/p/[slug]`):**
  - Schema.org `LocalBusiness` / `HomeAndConstructionBusiness` JSON-LD structured data for Google Search snippet indexing.
  - Emergency 24/7 click-to-call banner with virtual tracking phone number.
  - Client-side Lead Capture Form (`LeadCaptureForm.tsx`) submitting directly to `POST /api/v1/leads/capture`.
- **Pilot Market Seeded:**
  - Seeded primary pilot market in Fort Wayne, IN (Water Damage Restoration).
  - Seeded pilot contractor (*Fort Wayne Elite Water Restoration*) with $500 funded prepaid wallet and active agreement.
- **Test Automation & Quality Assurance:**
  - Expanded test suite to 12 automated unit and integration tests (100% pass rate in `apps/api/tests`).
  - Next.js 14 production build verified with 5/5 static/dynamic routes.

## [1.1.0] - 2026-11-14
### Added
- **GitHub Actions CI/CD Pipeline:** Complete automated continuous integration (`.github/workflows/ci.yml`) and continuous deployment workflow (`.github/workflows/deploy.yml`) covering:
  - Backend Python 3.12 dependency installation, Pytest suite execution.
  - Frontend Node.js 20 build verification (`next build`).
  - Container build verification for `apps/api` and `apps/admin-web` Dockerfiles.
- **Keyword Intelligence Engine (`keyword_service.py`):** Structured generator for primary, emergency, commercial, and long-tail keywords with estimated CPC indicators, search intent, and seasonal demand.
- **Competitor Analysis Service (`competitor_service.py`):** Calculates competitor density, rating distributions, website penetration percentages, and market entry barrier scores.
- **Geographic Expansion Engine (`geo_expansion_service.py`):** Autonomous discovery of surrounding satellite municipalities using Haversine great-circle distance (e.g. Fort Wayne -> New Haven, Auburn, Huntington, Columbia City).
- **Automated Contractor Discovery Pipeline (`contractor_discovery_service.py`):** Pluggable adapters for OpenStreetMap (Nominatim search) and Google Places with phone normalization and duplicate protection.
- **CSV Data Export:** Added streaming CSV export endpoint (`/api/v1/contractors/export/csv`) with verification details.
- **Extended Test Suite:** Added `tests/test_phase3_4.py`, expanding automated test coverage to 8 comprehensive tests (100% pass rate).

## [1.0.0] - 2026-11-14
### Added
- **Monorepo Architecture:** Established enterprise monorepo containing `apps/api`, `apps/admin-web`, `packages/`, `database/`, and `infrastructure/`.
- **FastAPI Core Gateway:** Implemented versioned REST API (`/api/v1`) with full async SQLAlchemy 2.0 and Pydantic v2 schemas.
- **Relational & Spatial Database:** Complete schema definition for PostgreSQL/PostGIS with standalone SQLite async dev engine.
- **Identity & RBAC:** JWT authentication, bcrypt work factor 12 password hashing, and role-based permissions (`super_admin`, `admin`, `analyst`, `contractor`).
- **Global Market Intelligence:** Seeded 5 countries (US, GB, CA, AU, DE) and 25 core service niches with multi-factor opportunity scoring algorithm.
- **Contractor Discovery & Phone Verification:** International phone normalization using Google's `libphonenumber` to E.164 with 7 verification levels.
- **Deterministic Lead Qualification & Dispatch:** 72-hour duplicate detection, spam filtering, and smart contractor matching.
- **Double-Entry Financial Ledger:** Immutable ledger table with row-level locking (`SELECT ... FOR UPDATE`) and idempotency key enforcement.
- **17 Autonomous AI Agents Subsystem:** Registered and initialized all 17 agents with token accounting and execution runner.
- **Next.js 14 Admin Dashboard:** Modern command center with Tailwind CSS, KPI metric cards, agent status grid, contractor directory, and lead feed.
- **Automated Testing Suite:** 100% passing Pytest unit and integration test suite covering the entire business lifecycle.
- **Hybrid Infrastructure:** Docker Compose topology for Cloud Control Plane and systemd specifications for Rocky Linux execution workers.
