# GLOBALLEAD AI - HYBRID DEPLOYMENT GUIDE

## 1. Cloud Control Plane Deployment

### 1.1 Docker Compose Production Topology
The Cloud Control Plane runs:
1. `api`: FastAPI application (Uvicorn / Gunicorn workers)
2. `admin-web`: Next.js 14 Production standalone build
3. `db`: PostgreSQL 16 + PostGIS
4. `redis`: Redis 7 Alpine with persistent append-only file (AOF)
5. `nginx`: Reverse proxy with Let's Encrypt TLS

### 1.2 Quick Launch Command
```bash
docker compose -f docker-compose.yml up -d --build
```

---

## 2. Self-Hosted Execution Plane (Rocky Linux 9 / RHEL)

### 2.1 Hardware Requirements
- **CPU:** 4 vCPU (Intel Xeon / AMD EPYC)
- **RAM:** 8 GB minimum (16 GB recommended)
- **Storage:** 100 GB NVMe SSD
- **OS:** Rocky Linux 9.4 (Minimal Install)

### 2.2 Host Preparation
```bash
sudo dnf update -y
sudo dnf install -y python3.12 python3.12-pip git redis-tools
sudo mkdir -p /opt/globallead-ai/{app,config,workers,logs,backups}
sudo useradd -r -s /sbin/nologin globallead
sudo chown -R globallead:globallead /opt/globallead-ai
```

### 2.3 Systemd Service Definition (`/etc/systemd/system/globallead-worker.service`)
```ini
[Unit]
Description=GlobalLead AI Distributed Worker
After=network.target

[Service]
Type=simple
User=globallead
WorkingDirectory=/opt/globallead-ai/app
ExecStart=/opt/globallead-ai/app/venv/bin/celery -A workers.celery_app worker --loglevel=INFO -c 4
Restart=always
RestartSec=10
EnvironmentFile=/opt/globallead-ai/config/worker.env

[Install]
WantedBy=multi-user.target
```

---

## 3. Automated Database Backup & Disaster Recovery

### 3.1 Backup Script (`/opt/globallead-ai/backups/backup_db.sh`)
```bash
#!/bin/bash
BACKUP_DIR="/opt/globallead-ai/backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="${BACKUP_DIR}/globallead_backup_${TIMESTAMP}.sql.gz"

pg_dump -U globallead -h 127.0.0.1 globallead_db | gzip > "${BACKUP_FILE}"
# Retain last 30 daily backups
find "${BACKUP_DIR}" -type f -name "*.sql.gz" -mtime +30 -exec rm {} \;
```

### 3.2 Restore Verification Command
```bash
gunzip -c /opt/globallead-ai/backups/globallead_backup_LATEST.sql.gz | psql -U globallead -d globallead_restore_test
```
