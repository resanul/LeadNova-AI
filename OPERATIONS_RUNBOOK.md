# GLOBALLEAD AI - OPERATIONS RUNBOOK

## 1. Routine Service Management

### 1.1 Starting Services Locally
```bash
# Terminal 1: Backend API Gateway
cd apps/api
.\venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --port 8000

# Terminal 2: Admin Dashboard
cd apps/admin-web
npm run dev
```

### 1.2 Running System Tests
```bash
cd apps/api
.\venv\Scripts\Activate.ps1
pytest -v
```

---

## 2. Emergency Procedures & Kill Switch

### 2.1 Pausing Autonomous Agents
If an autonomous agent exhibits erratic behavior or external API rate limits are exceeded:
1. Access the Admin Command Center: Navigate to `/agents`.
2. Toggle the agent status switch from `Active` to `Paused`.
3. Alternatively, execute via API:
   ```bash
   curl -X PATCH http://localhost:8000/api/v1/agents/{agent_id} -H "Authorization: Bearer <TOKEN>" -d '{"is_active": false}'
   ```

### 2.2 Reversing Erroneous Lead Deductions
To issue an audit-approved contractor refund:
```bash
curl -X POST http://localhost:8000/api/v1/billing/wallets/{contractor_id}/deposit \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"amount": 75.0, "description": "Refund for disputed lead #UUID", "idempotency_key": "refund_uuid"}'
```
