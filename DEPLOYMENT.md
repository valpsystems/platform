# VALP SYSTEMS — Deployment Guide

Single-source deployment reference for the VALP SYSTEMS stack
(FastAPI + Next.js + PostgreSQL) on the existing 3-tier AWS infrastructure.

> **Current status:** Repo already cloned on the App Server. Remaining work: DB server
> setup/verification, backend venv + systemd, frontend build + PM2, proxy NGINX config.

---

## 1. Architecture

```
Internet ──► [IGW] ──► Public Subnet ──► Proxy (NGINX) [EIP: 174.129.16.36]
                                            │
                                    (VPC private routing)
                                            ▼
                                  Private Subnet ──► App Server [10.0.2.236:8080 / :3000]
                                                            │
                                                            ▼
                                                     DB Server [<DB_PRIVATE_IP>:5432]
```

| Component | IP | OS | Runs |
|-----------|----|----|------|
| Proxy | `174.129.16.36` (EIP) | Amazon Linux 2023 | NGINX reverse proxy |
| App Server | `10.0.2.236` (private) | Amazon Linux 2023 | FastAPI (uvicorn :8080) + Next.js (:3000) |
| DB Server | `<DB_PRIVATE_IP>` (private) | Amazon Linux 2023 | PostgreSQL 15 |

## 2. Prerequisites (Local Machine)

| Item | Status |
|------|--------|
| AWS key pair `learning-key.pem` | `C:\Users\vyju1\.ssh\learning-key.pem` |
| SSH config (`C:\Users\vyju1\.ssh\config`) | proxy-server + app-server aliases |
| Key permissions | `icacls C:\Users\vyju1\.ssh\learning-key.pem /inheritance:r /grant "$($env:USERNAME):(R)"` |

**SSH config entries:**
```
Host proxy-server
    HostName 174.129.16.36
    User ec2-user
    IdentityFile C:\Users\vyju1\.ssh\learning-key.pem

Host app-server
    HostName 10.0.2.236
    User ec2-user
    IdentityFile C:\Users\vyju1\.ssh\learning-key.pem
    ProxyJump proxy-server
```

Test: `ssh proxy-server` then `ssh app-server` (jump via proxy).

## 3. DB Server — Setup & Verification Checklist

> Commands run on the **DB Server**. Reach it by jumping through proxy → app → db
> (`ssh -J proxy-server,app-server ec2-user@<DB_PRIVATE_IP>`).

### 3.1 Verify PostgreSQL Installed & Running

```bash
sudo dnf install -y postgresql15 postgresql15-server   # if not already installed
sudo postgresql-setup --initdb                          # first run only
sudo systemctl enable --now postgresql
sudo systemctl status postgresql                        # must be "active (running)"
```

### 3.2 Verify DB Role, Database & Privileges

```bash
sudo -i -u postgres
psql -c "\du"                                   # check appuser exists
psql -c "\l"                                    # check appdb exists
# If missing:
psql -c "CREATE USER appuser WITH PASSWORD '<DB_PASSWORD>';"
psql -c "CREATE DATABASE appdb OWNER appuser;"
psql -c "GRANT ALL PRIVILEGES ON DATABASE appdb TO appuser;"
exit
```

### 3.3 Verify Authentication Config (pg_hba.conf)

```bash
SHOW hba_file;          # via: sudo -u postgres psql
# Path: /var/lib/pgsql/15/data/pg_hba.conf

# Required lines (md5 for local + host from app server):
# local   all   all                       md5
# host    appdb appuser  10.0.2.236/32   md5

sudo systemctl restart postgresql
```

### 3.4 Verify Listen Addresses (postgresql.conf)

```bash
sudo nano /var/lib/pgsql/15/data/postgresql.conf
# listen_addresses = '10.0.2.236'   # allow app server only
# (or keep 'localhost' + connect from app-server only)
sudo systemctl restart postgresql
```

### 3.5 Verify Network / Firewall

- **Security Group `sg-db`** inbound: TCP 5432, source = `sg-app` (group ID) only.
- **iptables** (if enabled): allow 5432 from `10.0.2.236` only.

```bash
# On DB server, test local auth:
sudo -i -u postgres psql -c "ALTER ROLE appuser WITH PASSWORD '<DB_PASSWORD>';"
PGPASSWORD='<DB_PASSWORD>' psql -h 127.0.0.1 -U appuser -d appdb -c "SELECT 1;"
```

### 3.6 Verify From App Server

```bash
# On app server:
PGPASSWORD='<DB_PASSWORD>' psql -h <DB_PRIVATE_IP> -U appuser -d appdb -c "SELECT 1;"
# Must return: ?column? → 1
```

> If this fails: check pg_hba.conf, listen_addresses, SG ingress, and iptables on DB server.

## 4. App Server — System Prep

> Repo already cloned at `/opt/platform`. Commands run on **App Server** (`ssh app-server`).

```bash
# Update & install required packages
sudo dnf upgrade -y
sudo dnf install -y python3 python3-pip python3-venv git nginx
node --version   # 18+, else: sudo dnf install -y nodejs npm

# Verify repo location
ls /opt/platform
```

## 5. Backend — Deploy (FastAPI)

```bash
cd /opt/platform/backend

# 1. Virtual environment
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# 2. Verify imports
python -c "from app.main import app; print(len(app.routes))"

# 3. Logs dir
mkdir -p app/logs

# 4. Environment
cp .env.example .env
nano .env
```

### 5.1 `.env` production values

```ini
APP_NAME=VALP SYSTEMS
APP_VERSION=1.0.0
APP_ENV=production
APP_DEBUG=false
APP_HOST=127.0.0.1
APP_PORT=8080
APP_SECRET_KEY=<openssl rand -hex 48>
APP_URL=http://174.129.16.36

DATABASE_URL=postgresql+asyncpg://appuser:<DB_PASSWORD>@<DB_PRIVATE_IP>:5432/appdb
DATABASE_ECHO=false

CORS_ORIGINS=["http://174.129.16.36"]
TRUSTED_HOSTS=["174.129.16.36","10.0.2.236","localhost"]

JWT_SECRET_KEY=<openssl rand -hex 48>
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7

LOG_LEVEL=INFO
LOG_FORMAT=json
RATE_LIMIT_ENABLED=false
```

> `APP_SECRET_KEY` and `JWT_SECRET_KEY` **must differ**. Note: `/docs` is enabled
> only in development — with `APP_ENV=production` Swagger is disabled (by design).

### 5.2 Migrations

```bash
source .venv/bin/activate
cd /opt/platform/backend
alembic upgrade head

# Verify 19 tables
PGPASSWORD='<DB_PASSWORD>' psql -h <DB_PRIVATE_IP> -U appuser -d appdb -c "\dt"
```

### 5.3 Seed data

```bash
# Idempotent — seeds services/tech/solutions/resources
source .venv/bin/activate
python -c "
import asyncio
from app.database.seed import seed_database
from app.database.session import async_session_factory

async def run():
    async with async_session_factory() as session:
        await seed_database(session)

asyncio.run(run())
"
```

### 5.4 Test backend locally

```bash
uvicorn app.main:app --host 127.0.0.1 --port 8080 &
curl http://127.0.0.1:8080/api/v1/health
```

### 5.5 systemd service

```bash
sudo tee /etc/systemd/system/valp-backend.service << 'EOF'
[Unit]
Description=VALP SYSTEMS Backend API
After=network.target postgresql.service
Wants=postgresql.service

[Service]
Type=simple
User=ec2-user
Group=ec2-user
WorkingDirectory=/opt/platform/backend
Environment=PATH=/opt/platform/backend/.venv/bin:/usr/bin:/usr/local/bin
EnvironmentFile=/opt/platform/backend/.env
ExecStart=/opt/platform/backend/.venv/bin/uvicorn app.main:app \
  --host 127.0.0.1 --port 8080 --workers 4 --log-level info
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable --now valp-backend
sudo systemctl status valp-backend
sudo journalctl -u valp-backend -f
```

## 6. Frontend — Deploy (Next.js)

```bash
cd /opt/platform/frontend
npm install
npm run build

# Process manager
sudo npm install -g pm2
pm2 start npm --name "valp-frontend" -- start -- --port 3000
pm2 save
sudo pm2 startup systemd -u ec2-user --hp /home/ec2-user
```

Verify: `pm2 status` and `curl http://localhost:3000`.

## 7. Proxy — NGINX Config

> Commands run on the **Proxy server** (`ssh proxy-server`).

```bash
sudo tee /etc/nginx/conf.d/app.conf << 'EOF'
upstream backend {
    server 10.0.2.236:8080;
}

server {
    listen 80;
    server_name _;
    client_max_body_size 10M;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # API
    location /api/ {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 90s;
    }

    # Health
    location /health {
        proxy_pass http://backend/api/v1/health;
        proxy_set_header Host $host;
    }

    # Rate limiting (login)
    limit_req_zone $binary_remote_addr zone=login:10m rate=5r/s;
    location /api/v1/auth/login {
        limit_req zone=login burst=3 nodelay;
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # Frontend
    location / {
        proxy_pass http://10.0.2.236:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Deny sensitive files
    location ~ /\.(env|git|venv|next) {
        deny all;
        return 404;
    }

    access_log /var/log/nginx/valp-access.log;
    error_log /var/log/nginx/valp-error.log;
}
EOF

sudo rm -f /etc/nginx/conf.d/default.conf
sudo nginx -t
sudo systemctl reload nginx
```

## 8. Verification (End-to-End)

```powershell
# From local machine
curl http://174.129.16.36/api/v1/health
start http://174.129.16.36          # frontend

# Register + login
curl -X POST http://174.129.16.36/api/v1/auth/register `
  -H "Content-Type: application/json" `
  -d '{"email":"admin@valpsystems.com","username":"admin","password":"AdminPass123","confirm_password":"AdminPass123"}'

# On app server: service status
sudo systemctl status valp-backend --no-pager
pm2 status
```

## 9. Maintenance

```bash
# Code update (app server)
cd /opt/platform
git pull origin main
cd backend && source .venv/bin/activate && pip install -r requirements.txt && alembic upgrade head && sudo systemctl restart valp-backend
cd ../frontend && npm install && npm run build && pm2 restart valp-frontend

# Logs
sudo journalctl -u valp-backend -f
pm2 logs valp-frontend
sudo tail -f /var/log/nginx/valp-access.log   # proxy
```

### DB backup (cron on DB server)

```bash
sudo tee /opt/platform/scripts/backup.sh << 'SCRIPT'
#!/bin/bash
BACKUP_DIR="/opt/platform/backups"
mkdir -p $BACKUP_DIR
PGPASSWORD='<DB_PASSWORD>' pg_dump -h 127.0.0.1 -U appuser -d appdb > "$BACKUP_DIR/backup_$(date +%Y%m%d_%H%M%S).sql"
find $BACKUP_DIR -name "*.sql" -mtime +7 -delete
SCRIPT
chmod +x /opt/platform/scripts/backup.sh
sudo crontab -e        # 0 3 * * * /opt/platform/scripts/backup.sh
```

## 10. Troubleshooting

| Problem | Check |
|---------|-------|
| DB `connection refused` | PG running? pg_hba.conf? listen_addresses? SG/iptables 5432? |
| 502 Bad Gateway | `pm2 status` (frontend), `systemctl status valp-backend`, nginx error log |
| DB auth failed | User/password in `.env` vs DB; md5 line in pg_hba.conf |
| Frontend blank page | CORS_ORIGINS / TRUSTED_HOSTS in backend `.env` |
| Auth broken after redeploy | Same JWT_SECRET_KEY across restarts (keep in `.env`) |
| Log permission errors | `sudo chown -R ec2-user:ec2-user /opt/platform/backend/app/logs` |