# GLOBALLEAD AI
### Global Autonomous Pay-Per-Lead, Local Service Arbitrage, Contractor Intelligence, Lead Generation & Business Automation Platform

---

## 🌟 Overview
**GlobalLead AI** is an enterprise-grade, multi-tenant, autonomous Pay-Per-Lead (PPL) and local service business operating system. The platform automates the entire local service lifecycle:
1. **Global Market Intelligence:** Discovers profitable countries, cities, and high-value niches (Water Damage, Roofing, Plumbing, HVAC, etc.).
2. **Contractor Intelligence & Discovery:** Integrates public directories, Google Places, OpenStreetMap, and business registries with strict phone & reachability verification.
3. **AI Website Factory & SEO:** Generates high-converting, compliant local service landing pages with dynamic click-to-call, contact forms, schema markup, and performance tracking.
4. **Telephony & Call Routing:** Multi-provider VoIP engine (Twilio, Telnyx) with virtual tracking numbers, real-time geographic/capacity-based contractor forwarding, and failover routing.
5. **Smart Lead Ingestion & Qualification:** Automated duplicate detection, spam filtering, intent verification, and matching algorithm.
6. **Financial Ledger & Billing:** Double-entry wallet architecture, pricing rule engines (Per-Call, Per-Form, Exclusive/Shared, Subscriptions), automated invoicing, and dispute management.
7. **Autonomous AI Orchestration:** 17 specialized AI agents coordinated with strict permission boundaries, safety guardrails, and budget caps.

---

## 🏛️ Architecture & Deployment

### Hybrid Architecture:
- **Cloud Control Plane:** Admin Dashboard (Next.js 14, Tailwind, shadcn/ui), Contractor Portal, FastAPI API Gateway, Primary PostgreSQL/PostGIS database, Redis Cache, Stripe/Payment webhooks.
- **Self-Hosted Execution Plane (RHEL/Rocky Linux):** Distributed Celery & asyncio background workers for market research, contractor scraping/verification, SEO crawling, and scheduled automation without exposing internal worker databases to the public internet.

---

## 🚀 Repository Structure
```
globallead-ai/
├── apps/
│   ├── admin-web/              # Next.js Admin Command Center
│   ├── contractor-portal/      # Contractor Self-Service Portal
│   ├── public-websites/        # Dynamic Local Lead Landing Pages
│   └── api/                    # FastAPI Backend Gateway & REST APIs
├── services/
│   ├── market-intelligence/    # City/Niche discovery & Opportunity scoring
│   ├── contractor-discovery/   # Multi-source scraper & normalization
│   ├── data-verification/      # Phone validation (E.164) & email syntax
│   ├── website-factory/        # Page generator & SEO metadata
│   ├── lead-engine/            # Qualification, deduplication & ingestion
│   ├── telephony-engine/       # Twilio/Telnyx routing & call tracking
│   ├── billing-engine/         # Wallet ledger, invoices & payments
│   ├── ai-orchestrator/        # 17 Autonomous agents & LLM Gateway
│   └── analytics-engine/       # P&L, CAC, lead velocity & market reports
├── workers/
│   ├── research-worker/        # Market & keyword scraping workers
│   ├── discovery-worker/       # Business directory data collectors
│   ├── verification-worker/    # Asynchronous verification queues
│   ├── seo-worker/             # Technical SEO audits & rank monitoring
│   ├── lead-worker/            # Lead routing & qualification jobs
│   ├── webhook-worker/         # Inbound telephony & payment event processing
│   └── reporting-worker/       # Daily/Weekly/Monthly financial rollups
├── packages/
│   ├── shared-types/           # Common data contracts & schemas
│   ├── api-client/             # Typed SDK for frontends
│   ├── ui-components/          # Shared design system components
│   ├── validation/             # Form & data validators
│   └── configuration/          # App settings & environment policies
├── database/
│   ├── migrations/             # Alembic database migrations
│   ├── seeds/                  # Initial seed data (countries, niches)
│   └── schemas/                # SQL definitions & PostGIS extensions
├── integrations/
│   ├── business-data/          # Google Places, OSM, Business Registries
│   ├── telephony/              # Twilio, Telnyx, CallRail adapters
│   ├── payments/               # Stripe, PayPal, Wire Transfer
│   ├── email/                  # SendGrid, Postmark, SMTP
│   └── analytics/              # Prometheus, OpenTelemetry
├── infrastructure/
│   ├── docker/                 # Container definitions
│   ├── cloud/                  # Cloud Control Plane configurations
│   ├── rocky-linux/            # Self-hosted systemd & worker configurations
│   ├── nginx/                  # Reverse proxy & TLS termination
│   ├── monitoring/             # Prometheus & Grafana dashboards
│   ├── backup/                 # Automated PostgreSQL backup & restore scripts
│   └── ci-cd/                  # GitHub Actions CI/CD workflows
├── tests/
│   ├── unit/                   # Model, financial & routing tests
│   ├── integration/            # API endpoints & database integration
│   ├── security/               # RBAC, tenant isolation & injection tests
│   ├── performance/            # Throughput & load benchmarks
│   └── e2e/                    # Complete business lifecycle simulations
├── docs/                       # Technical & operational documentation
└── docker-compose.yml          # Local multi-service orchestration
```

---

## ⚡ Quick Start

### 1. Prerequisites
- Python 3.12+
- Node.js 20+ & npm 10+
- Docker & Docker Compose (for containerized deployment) or local Python/Node environments.

### 2. Backend Setup
```bash
cd apps/api
python -m venv venv
# On Windows:
.\venv\Scripts\Activate.ps1
# On Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
cp .env.example .env
alembic upgrade head
uvicorn main:app --reload --port 8000
```
Backend API will be running at `http://localhost:8000` with Swagger Docs at `http://localhost:8000/docs`.

### 3. Admin Frontend Setup
```bash
cd apps/admin-web
npm install
cp .env.example .env.local
npm run dev
```
Admin Dashboard will be running at `http://localhost:3000`.

---

## 🔒 Security & Compliance
- **Zero-Trust Network:** Worker execution planes communicate strictly outbound via mTLS/HTTPS.
- **Data Compliance:** Built-in configurable GDPR, CCPA, and TCPA consent capture & retention management.
- **Financial Integrity:** Append-only immutable double-entry ledger with database row-level locking.
- **Call Recording Safety:** Recordings disabled by default until two-party consent mechanisms are activated.

---

## 📄 License
Commercial Enterprise License — All rights reserved.
