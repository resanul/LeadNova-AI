# GLOBALLEAD AI - CHANGELOG

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
