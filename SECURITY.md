# GLOBALLEAD AI - SECURITY, PRIVACY & COMPLIANCE ARCHITECTURE

## 1. Zero-Trust Security Posture
GlobalLead AI is designed from the ground up for strict data integrity, zero unauthorized lateral movement, and bulletproof financial safety.

### 1.1 Network Boundary Isolation
- **No Direct Database Exposure:** The primary PostgreSQL/PostGIS database and Redis broker listen strictly on localhost or private internal Docker bridge networks (`127.0.0.1` or overlay network). Neither port `5432` nor `6379` is ever exposed to the public internet.
- **Worker Execution Plane Isolation:** The self-hosted Rocky Linux background workers connect **outbound-only** to the Cloud Control Plane via TLS 1.3 with pre-shared HMAC authorization headers or mTLS. No incoming ports are opened on the Rocky Linux execution host.

### 1.2 Authentication & Role-Based Access Control (RBAC)
- **Token Security:** JWT tokens signed using `HS256` or `RS256` with strict expiration windows (15 minutes for access tokens, 7 days for secure HttpOnly refresh tokens).
- **Password Hashing:** Industry-standard `bcrypt` with work factor 12.
- **Role Hierarchy:**
  1. `super_admin`: Full system control, financial adjustments, system kill switch.
  2. `admin`: Market research, contractor management, campaign deployment.
  3. `analyst`: Read-only reporting and market intelligence exploration.
  4. `contractor`: Strictly isolated tenant portal; cannot read global stats, other contractors, or administrative endpoints.

### 1.3 Financial Integrity & Anti-Fraud
- **Immutable Append-Only Ledger:** Financial records are strictly append-only. No `UPDATE` or `DELETE` statements are ever executed against the `ledger_entries` table.
- **Database Row-Level Locking:** During wallet deductions, `SELECT ... FOR UPDATE` row locks are acquired to eliminate race conditions, preventing double-spending even under high concurrent call volume.
- **Idempotency Keys:** Every billing event requires a unique UUID idempotency key (`hash(lead_id + contractor_id + timestamp_bucket)`). Replays are automatically rejected.

### 1.4 Regulatory Compliance
- **GDPR & UK GDPR:** Right-to-be-forgotten deletion workflows, PII masking in analytics, consent logging for lead capture forms.
- **TCPA (Telephone Consumer Protection Act):** Form leads require explicit affirmative checkbox consent before lead submission.
- **Call Recording Compliance:** Two-party consent disclosure message injected by default before call bridging if recording is enabled.
