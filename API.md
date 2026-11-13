# GLOBALLEAD AI - REST API SPECIFICATION

## 1. Overview
All endpoints are versioned under `/api/v1/`. All request and response bodies use JSON (`Content-Type: application/json`).
All authenticated endpoints require a Bearer token in the `Authorization` header:
```http
Authorization: Bearer <jwt_access_token>
```

---

## 2. Core API Route Registry

### 2.1 Authentication & Profile (`/api/v1/auth`)
| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :---: |
| `POST` | `/api/v1/auth/login` | Exchange email and password for JWT access token | No |
| `GET` | `/api/v1/auth/me` | Retrieve profile of the currently authenticated user | Yes |
| `POST` | `/api/v1/auth/refresh` | Refresh an expiring session token | Yes |

### 2.2 Market Intelligence (`/api/v1/market`)
| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :---: |
| `GET` | `/api/v1/countries` | List supported countries with dialing codes & currencies | Yes |
| `POST` | `/api/v1/countries` | Register or enable a new country | Yes (Admin) |
| `GET` | `/api/v1/cities` | List cities with optional filter by country / state | Yes |
| `POST` | `/api/v1/cities` | Create a new city entry with population metrics | Yes (Admin) |
| `GET` | `/api/v1/niches` | List high-value local service niches | Yes |
| `POST` | `/api/v1/niches` | Add a new niche with estimated lead values | Yes (Admin) |
| `GET` | `/api/v1/opportunities` | List ranked market opportunities with multi-factor scores | Yes |
| `POST` | `/api/v1/opportunities/evaluate` | Trigger AI/Data score calculation for a city & niche | Yes (Admin) |

### 2.3 Contractor Operations & CRM (`/api/v1/contractors`)
| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :---: |
| `GET` | `/api/v1/contractors` | Search, filter, and paginate contractors | Yes |
| `POST` | `/api/v1/contractors` | Manually register a new contractor | Yes |
| `GET` | `/api/v1/contractors/{id}` | Retrieve comprehensive contractor dossier & CRM history | Yes |
| `PATCH`| `/api/v1/contractors/{id}` | Update contractor partner status, coverage, or notes | Yes |
| `POST` | `/api/v1/contractors/discover` | Trigger automated discovery job (Google Places / OSM) | Yes (Admin) |
| `POST` | `/api/v1/contractors/{id}/verify`| Run phone format (E.164) & reachability verification | Yes |
| `GET` | `/api/v1/contractors/{id}/agreement`| Get contractor active pricing and lead agreements | Yes |
| `POST` | `/api/v1/contractors/{id}/agreement`| Create or update pricing agreement | Yes (Admin) |

### 2.4 Digital Assets & Landing Pages (`/api/v1/websites`)
| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :---: |
| `GET` | `/api/v1/websites` | List managed multi-site domain properties | Yes |
| `POST` | `/api/v1/websites` | Provision a new website property | Yes (Admin) |
| `GET` | `/api/v1/landing-pages` | List generated landing pages with city/niche filters | Yes |
| `POST` | `/api/v1/landing-pages/generate`| Generate AI SEO content & publish local landing page | Yes (Admin) |

### 2.5 Lead Ingestion & Qualification (`/api/v1/leads`)
| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :---: |
| `GET` | `/api/v1/leads` | List ingested leads with qualification and delivery status | Yes |
| `POST` | `/api/v1/leads/capture` | Public endpoint to capture customer form submissions | No (API Key/CORS) |
| `GET` | `/api/v1/leads/{id}` | Get lead details, customer inquiry, and audit trail | Yes |
| `POST` | `/api/v1/leads/{id}/qualify` | Run qualification and duplicate detection engine | Yes |
| `POST` | `/api/v1/leads/{id}/route` | Execute deterministic contractor matching & dispatch | Yes |
| `POST` | `/api/v1/leads/{id}/dispute` | Submit contractor dispute for invalid lead | Yes (Contractor) |

### 2.6 Telephony & Call Arbitrage (`/api/v1/telephony`)
| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :---: |
| `GET` | `/api/v1/phone-numbers` | List virtual tracking numbers and assignments | Yes |
| `POST` | `/api/v1/phone-numbers/assign`| Assign tracking number to landing page & niche | Yes (Admin) |
| `POST` | `/api/v1/webhooks/twilio/voice`| Twilio voice webhook handling live call routing | No (Sig Verified) |
| `POST` | `/api/v1/webhooks/telnyx/voice`| Telnyx voice webhook handling live call routing | No (Sig Verified) |

### 2.7 Financial Engine & Wallets (`/api/v1/billing`)
| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :---: |
| `GET` | `/api/v1/wallets` | List contractor wallet balances | Yes (Admin) |
| `GET` | `/api/v1/wallets/{contractor_id}` | Retrieve specific contractor wallet & ledger history | Yes |
| `POST` | `/api/v1/wallets/{contractor_id}/deposit` | Record prepaid credit deposit (Stripe / Wire) | Yes (Admin) |
| `GET` | `/api/v1/ledger` | Inspect immutable audit ledger entries | Yes (Admin) |

### 2.8 AI Orchestration & System Health (`/api/v1/agents` & `/api/v1/system`)
| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :---: |
| `GET` | `/api/v1/agents` | List 17 autonomous agents and their execution status | Yes |
| `POST` | `/api/v1/agents/{name}/run` | Manually dispatch an agent task | Yes (Admin) |
| `GET` | `/api/v1/system/health` | Service health check (DB, Redis, Celery workers) | No |
| `GET` | `/api/v1/analytics/overview` | Executive KPI dashboard (Revenue, Leads, P&L) | Yes |
