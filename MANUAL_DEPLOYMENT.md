# VALP SYSTEMS — Manual EC2 Deployment SOP

> **Standard Operating Procedure** — Deploy VALP SYSTEMS (FastAPI + Next.js) on existing 3-tier AWS infrastructure  
> **Reference Architecture:** [`EC2_deployment_plan.md`](../EC2_deployment_plan.md) — Phase 1 Manual Deployment  
> **Last Updated:** July 2026

---

## Architecture Overview

```
Internet ──► [IGW] ──► Public Subnet ──► Proxy (NGINX) [EIP: 174.129.16.36]
                                            │
                                     (VPC private routing)
                                            ▼
                                  Private Subnet ──► App Server [10.0.2.236]
                                                            │
                                                            ▼
                                                     DB Server [<DB_PRIVATE_IP>]
```

| Component | IP | OS | Role |
|-----------|----|----|------|
| **Proxy** | `174.129.16.36` (EIP) | Amazon Linux 2023 | NGINX reverse proxy |
| **App Server** | `10.0.2.236` (private) | Amazon Linux 2023 | FastAPI + Next.js |
| **DB Server** | `<DB_PRIVATE_IP>` (private) | Amazon Linux 2023 | PostgreSQL |

---

## Prerequisites

| Item | Status |
|------|--------|
| [ ] AWS key pair (`learning-key.pem`) already downloaded on local machine |
| [ ] GitHub account with access to `valpsystems` private repo |
| [ ] Windows Terminal / PowerShell |
| [ ] Proxy and App servers are running (verify in AWS Console) |

---

## Phase 1: Local Machine Setup

### 1.1 Locate Your AWS Key Pair

The `.pem` file was downloaded when you launched the EC2 instances.

```powershell
# If you know its location, move it to .ssh folder
# If missing, create a new key pair:
# AWS Console → EC2 → Key Pairs → Create key pair → "learning-key" → .pem
# Then download and copy to:
# C:\Users\vyju1\.ssh\learning-key.pem
```

**Set permissions (Windows):**
```powershell
icacls C:\Users\vyju1\.ssh\learning-key.pem /inheritance:r /grant "$($env:USERNAME):(R)"
```

### 1.2 Configure SSH (Windows)

Edit `C:\Users\vyju1\.ssh\config`:

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

Host github.com
    HostName github.com
    User git
    IdentityFile C:\Users\vyju1\.ssh\github_key
```

### 1.3 Test SSH Access

```powershell
ssh proxy-server                    # Direct — should connect
ssh app-server                      # Via jump host — should connect
```

### 1.4 Generate GitHub SSH Key (Local Machine)

```powershell
# Generate a dedicated key for GitHub (do NOT use the AWS key)
ssh-keygen -t ed25519 -C "your-email@example.com" -f C:\Users\vyju1\.ssh\github_key

# Copy public key to clipboard
Get-Content C:\Users\vyju1\.ssh\github_key.pub | Set-Clipboard
```

**Add to GitHub:**
1. Go to **GitHub.com → Settings → SSH and GPG keys → New SSH key**
2. Title: `Windows Laptop`
3. Key: Paste from clipboard
4. Click **Add SSH key**

### 1.5 Clone the Repository (Local)

```powershell
cd D:\ProjectsPersonalUse
git clone git@github.com:<your-org>/valpsystems.git
```

---

## Phase 2: App Server — System Preparation

> All commands in Phase 2 run on the **App Server** (`ssh app-server`)

### 2.1 Update System Packages

```bash
sudo dnf update -y
sudo dnf upgrade -y
```

### 2.2 Install Dependencies

Per `EC2_deployment_plan.md` Section 5 — App Server user data installs `git nodejs npm`:

```bash
sudo dnf install -y python3 python3-pip python3-venv git nodejs nginx

# Verify
python3 --version     # 3.9+ (Amazon Linux 2023 default)
node --version         # 18+
npm --version
```

### 2.3 Database Setup

**If using RDS** (recommended per plan):
- DB endpoint: `<DB_ENDPOINT>` (from AWS RDS Console)
- Username: `admin` (per plan default)
- Password: `<DB_PASSWORD>`
- Database: `appdb` (per plan default)

**If using EC2-hosted PostgreSQL:**

```bash
# Install PostgreSQL
sudo dnf install -y postgresql15-server
sudo postgresql-setup --initdb
sudo systemctl enable postgresql
sudo systemctl start postgresql

# Create database and user (per EC2_deployment_plan.md Section 6 Option B)
sudo -i -u postgres
psql -c "CREATE DATABASE appdb;"
psql -c "CREATE USER appuser WITH PASSWORD '<DB_PASSWORD>';"
psql -c "GRANT ALL PRIVILEGES ON DATABASE appdb TO appuser;"
exit

# Configure auth
sudo nano /var/lib/pgsql/15/data/pg_hba.conf
# Change: local   all   all   peer  →  local   all   all   md5
# Add: host  appdb  appuser  127.0.0.1/32  md5

sudo systemctl restart postgresql
```

---

## Phase 3: GitHub Deploy Key (App Server Access)

### 3.1 Generate Deploy Key on App Server

```bash
# On app server
ssh app-server

ssh-keygen -t ed25519 -C "valp-deploy" -f ~/.ssh/deploy_key -N ""
cat ~/.ssh/deploy_key.pub
```

### 3.2 Add to GitHub

1. Go to **GitHub.com → Repository: `valpsystems` → Settings → Deploy Keys → Add deploy key**
2. Title: `EC2 App Server`
3. Key: Paste the output from `cat ~/.ssh/deploy_key.pub`
4. Check: **Allow write access** (required for `git pull` during updates)
5. Click **Add key**

### 3.3 Configure SSH for GitHub

```bash
cat > ~/.ssh/config << 'EOF'
Host github.com
    HostName github.com
    User git
    IdentityFile ~/.ssh/deploy_key
    StrictHostKeyChecking accept-new
EOF

chmod 600 ~/.ssh/deploy_key ~/.ssh/config
```

### 3.4 Test Authentication

```bash
ssh -T git@github.com
# Expected: "Hi <org>/valpsystems! You've successfully authenticated..."
```

---

## Phase 4: Backend Deployment (FastAPI)

### 4.1 Clone Repository on App Server

```bash
sudo mkdir -p /opt
sudo chown ec2-user:ec2-user /opt
cd /opt
git clone git@github.com:<your-org>/valpsystems.git
cd valpsystems/backend
```

### 4.2 Create Python Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 4.3 Verify Imports

```bash
python -c "from app.main import app; print(f'App OK — {len(app.routes)} routes')"
```

Expected: `App OK — 22 routes`

### 4.4 Create Logs Directory

```bash
mkdir -p app/logs
```

### 4.5 Configure Production Environment

```bash
cp .env.example .env
nano .env
```

Set these values:

```ini
APP_NAME=VALP SYSTEMS
APP_VERSION=1.0.0
APP_ENV=production
APP_DEBUG=false
APP_HOST=127.0.0.1
APP_PORT=8080
APP_SECRET_KEY=<generate below>
APP_URL=http://174.129.16.36

# Database — use your DB server private IP or RDS endpoint
DATABASE_URL=postgresql+asyncpg://appuser:<DB_PASSWORD>@<DB_PRIVATE_IP>:5432/appdb
DATABASE_ECHO=false
DATABASE_POOL_SIZE=10
DATABASE_MAX_OVERFLOW=20

CORS_ORIGINS=["http://174.129.16.36"]
TRUSTED_HOSTS=["174.129.16.36","10.0.2.236","localhost"]

LOG_LEVEL=INFO
LOG_FORMAT=json

JWT_SECRET_KEY=<run: python3 -c "import secrets; print(secrets.token_urlsafe(48))" — different from APP_SECRET_KEY>
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7

PASSWORD_MIN_LENGTH=8
PASSWORD_REQUIRE_UPPERCASE=true
PASSWORD_REQUIRE_LOWERCASE=true
PASSWORD_REQUIRE_DIGIT=true
PASSWORD_REQUIRE_SPECIAL=false

SMTP_HOST=
SMTP_PORT=587
SMTP_USER=
SMTP_PASSWORD=
SMTP_USE_TLS=true
SMTP_FROM_EMAIL=noreply@valpsystems.com
SMTP_FROM_NAME=VALP SYSTEMS

RATE_LIMIT_ENABLED=false
RATE_LIMIT_REQUESTS=10
RATE_LIMIT_WINDOW_SECONDS=60
```

### 4.6 Generate Secret Keys

```bash
# Run these two commands SEPARATELY — use different outputs for each key
python3 -c "import secrets; print(secrets.token_urlsafe(48))"   # → APP_SECRET_KEY
python3 -c "import secrets; print(secrets.token_urlsafe(48))"   # → JWT_SECRET_KEY
```

### 4.7 Run Database Migrations

```bash
source .venv/bin/activate
cd /opt/valpsystems/backend
alembic upgrade head
```

Verify 19 tables:
```bash
PGPASSWORD='<DB_PASSWORD>' psql -h <DB_PRIVATE_IP> -U appuser -d appdb -c "\dt"
```

### 4.8 Seed Default Data

```bash
python scripts/seed.py
```

### 4.9 Test Backend Locally

```bash
uvicorn app.main:app --host 127.0.0.1 --port 8080 &
sleep 3
curl http://127.0.0.1:8080/api/v1/health
kill %1 2>/dev/null
```

Expected: `{"success":true,"message":"Service is healthy",...}`

### 4.10 Create Systemd Service (Auto-Start)

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
WorkingDirectory=/opt/valpsystems/backend
Environment=PATH=/opt/valpsystems/backend/.venv/bin:/usr/bin:/usr/local/bin
EnvironmentFile=/opt/valpsystems/backend/.env
ExecStart=/opt/valpsystems/backend/.venv/bin/uvicorn app.main:app \
  --host 127.0.0.1 \
  --port 8080 \
  --workers 4 \
  --log-level info
Restart=always
RestartSec=5
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable valp-backend
sudo systemctl start valp-backend
sudo systemctl status valp-backend
```

---

## Phase 5: Frontend Deployment (Next.js)

### 5.1 Install Dependencies & Build

```bash
cd /opt/valpsystems/frontend
npm install
npm run build
```

### 5.2 Install PM2 for Process Management

```bash
sudo npm install -g pm2

pm2 start npm --name "valp-frontend" -- start -- --port 3000
pm2 save
sudo pm2 startup systemd -u ec2-user --hp /home/ec2-user
```

### 5.3 Verify

```bash
pm2 status
curl http://localhost:3000  # Should return HTML
```

---

## Phase 6: Proxy — NGINX Configuration

> All commands in Phase 6 run on the **Proxy Server** (`ssh proxy-server`)

Per `EC2_deployment_plan.md` Section 4.2 — the proxy already has NGINX + NAT configured. We just update the NGINX config.

### 6.1 Replace NGINX Config

```bash
sudo tee /etc/nginx/conf.d/app.conf << 'EOF'
upstream backend {
    server 10.0.2.236:8080;
}

server {
    listen 80;
    server_name _;

    client_max_body_size 10M;

    # ─── Security Headers ───
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    add_header Permissions-Policy "camera=(), microphone=(), geolocation=()" always;

    # ─── API Routes ───
    location /api/ {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 90s;
        proxy_connect_timeout 10s;
    }

    # ─── Swagger / Docs ───
    location /docs {
        proxy_pass http://backend/docs;
        proxy_set_header Host $host;
    }

    location /redoc {
        proxy_pass http://backend/redoc;
        proxy_set_header Host $host;
    }

    location /openapi.json {
        proxy_pass http://backend/openapi.json;
        proxy_set_header Host $host;
    }

    # ─── Health Check ───
    location /health {
        proxy_pass http://backend/api/v1/health;
        proxy_set_header Host $host;
    }

    # ─── Rate Limiting (Login endpoint) ───
    limit_req_zone $binary_remote_addr zone=login:10m rate=5r/s;
    location /api/v1/auth/login {
        limit_req zone=login burst=3 nodelay;
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # ─── Frontend ───
    location / {
        proxy_pass http://10.0.2.236:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 90s;
    }

    # ─── Deny sensitive files ───
    location ~ /\.(env|git|venv|next) {
        deny all;
        return 404;
    }

    # ─── Logs ───
    access_log /var/log/nginx/valp-access.log;
    error_log /var/log/nginx/valp-error.log;
}
EOF

# Remove default config
sudo rm -f /etc/nginx/conf.d/default.conf

# Test and reload
sudo nginx -t
sudo systemctl reload nginx
```

### 6.2 Verify Proxy Forwarding

```bash
# From proxy server
curl http://localhost/api/v1/health
curl http://localhost/health
curl http://localhost/  # Should return HTML
```

---

## Phase 7: Production Hardening

### 7.1 PostgreSQL Security

```bash
# Ensure PostgreSQL binds only to localhost
sudo nano /var/lib/pgsql/15/data/postgresql.conf
# Set: listen_addresses = 'localhost'
# OR on DB server: listen_addresses = '10.0.2.236' (only allow app server)

sudo systemctl restart postgresql
```

### 7.2 App Server — Firewall

```bash
# Block everything except needed ports
sudo dnf install -y iptables-services

# Default deny incoming
sudo iptables -P INPUT DROP
sudo iptables -P FORWARD DROP
sudo iptables -P OUTPUT ACCEPT

# Allow established connections
sudo iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

# Allow SSH from proxy only
sudo iptables -A INPUT -s 10.0.1.0/24 -p tcp --dport 22 -j ACCEPT

# Allow localhost
sudo iptables -A INPUT -i lo -j ACCEPT

# Allow backend port from proxy only
sudo iptables -A INPUT -s 10.0.1.0/24 -p tcp --dport 8080 -j ACCEPT

# Allow frontend port from proxy only
sudo iptables -A INPUT -s 10.0.1.0/24 -p tcp --dport 3000 -j ACCEPT

# Allow PostgreSQL from app server only (run on DB server)
sudo iptables -A INPUT -s 10.0.2.236 -p tcp --dport 5432 -j ACCEPT

# Save rules
sudo service iptables save
sudo systemctl enable iptables
```

### 7.3 Proxy Server — Harden NGINX

On the proxy server, add to `/etc/nginx/conf.d/app.conf` within the `server` block (already included above):

- Security headers (X-Frame-Options, X-Content-Type-Options, etc.)
- Rate limiting on login endpoint (5 req/s with burst of 3)
- Deny access to `.env`, `.git`, `.venv`, `.next`
- Client max body size limited to 10 MB

### 7.4 Automatic Security Updates

```bash
sudo dnf install -y dnf-automatic
sudo systemctl enable --now dnf-automatic.timer
```

### 7.5 File Permissions

```bash
# Lock down sensitive files
chmod 600 /opt/valpsystems/backend/.env
chmod 700 ~/.ssh
chmod 600 ~/.ssh/*
sudo chown -R ec2-user:ec2-user /opt/valpsystems
```

---

## Phase 8: Verification

### 8.1 End-to-End Test

```powershell
# From local browser
start http://174.129.16.36

# API health
curl http://174.129.16.36/api/v1/health

# Swagger
start http://174.129.16.36/docs
```

### 8.2 Register a User

```powershell
curl -X POST http://174.129.16.36/api/v1/auth/register ^
  -H "Content-Type: application/json" ^
  -d '{"email":"admin@valpsystems.com","username":"admin","password":"AdminPass123","confirm_password":"AdminPass123"}'
```

### 8.3 Login

```powershell
$body = @{email="admin@valpsystems.com";password="AdminPass123"} | ConvertTo-Json
curl -X POST http://174.129.16.36/api/v1/auth/login -H "Content-Type: application/json" -d $body
```

### 8.4 Service Status

```bash
# On app server
sudo systemctl status valp-backend --no-pager
pm2 status
sudo systemctl status postgresql --no-pager

# On proxy server
sudo systemctl status nginx --no-pager
```

---

## Phase 9: Maintenance & Operations

### 9.1 Update Application Code

```bash
# On app server
cd /opt/valpsystems

# Pull latest code
git pull origin main

# Update backend
cd backend
source .venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
sudo systemctl restart valp-backend

# Update frontend
cd ../frontend
npm install
npm run build
pm2 restart valp-frontend
```

### 9.2 Database Backup (Cron)

```bash
# Create backup script
sudo tee /opt/valpsystems/scripts/backup.sh << 'SCRIPT'
#!/bin/bash
BACKUP_DIR="/opt/valpsystems/backups"
mkdir -p $BACKUP_DIR
PGPASSWORD='<DB_PASSWORD>' pg_dump -h <DB_PRIVATE_IP> -U appuser -d appdb > "$BACKUP_DIR/backup_$(date +%Y%m%d_%H%M%S).sql"
find $BACKUP_DIR -name "*.sql" -mtime +7 -delete
SCRIPT

chmod +x /opt/valpsystems/scripts/backup.sh

# Schedule daily at 3 AM
sudo crontab -e
# Add: 0 3 * * * /opt/valpsystems/scripts/backup.sh
```

### 9.3 View Logs

```bash
# Backend
sudo journalctl -u valp-backend -f

# Frontend
pm2 logs valp-frontend

# NGINX (on proxy)
sudo tail -f /var/log/nginx/valp-access.log
sudo tail -f /var/log/nginx/valp-error.log
```

---

## Phase 10: SSL/HTTPS (Post-Deployment)

When a domain is available, follow `EC2_deployment_plan.md` Section 9:

```bash
# On proxy server
sudo dnf install -y certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
sudo certbot renew --dry-run
```

---

## Appendix A: Architecture Mapping

| EC2_deployment_plan.md Section | This SOP Phase |
|-------------------------------|----------------|
| Section 1-3 (VPC, SGs, Key) | Already done by user |
| Section 4 (Launch Proxy) | Already done — infra exists |
| Section 5 (Launch App) | Already done — infra exists |
| Section 6 (Database) | Phase 2.3 |
| Section 7 (Sample App) | Phases 4-5 (adapted for FastAPI+Next.js) |
| Section 8 (CI/CD Pipeline) | Future — not in scope |
| Section 9 (SSL) | Phase 10 |
| Section 10 (Monitoring) | Phase 9 |

## Appendix B: Quick Reference Card

```bash
# ─── SSH ───
ssh proxy-server                    # Connect to proxy
ssh app-server                      # Connect to app via jump

# ─── Services ───
sudo systemctl start|stop|restart|status valp-backend
sudo journalctl -u valp-backend -f
pm2 start|stop|restart|status valp-frontend
pm2 logs valp-frontend
sudo systemctl reload nginx
sudo nginx -t

# ─── App Update ───
cd /opt/valpsystems
git pull
cd backend && source .venv/bin/activate && pip install -r requirements.txt && alembic upgrade head && sudo systemctl restart valp-backend
cd ../frontend && npm install && npm run build && pm2 restart valp-frontend

# ─── Database ───
PGPASSWORD='<pass>' psql -h <DB_IP> -U appuser -d appdb
PGPASSWORD='<pass>' pg_dump -h <DB_IP> -U appuser -d appdb > backup.sql

# ─── Logs ───
sudo journalctl -u valp-backend -n 50 --no-pager
sudo tail -f /var/log/nginx/valp-access.log
```

## Appendix C: Variables Reference

| Variable | Your Value |
|----------|-----------|
| Proxy EIP | `174.129.16.36` |
| App Server Private IP | `10.0.2.236` |
| DB Server Private IP | `__________` |
| DB Password | `__________` |
| GitHub Org/Repo | `__________` |
| SSH Key Name | `learning-key` |
| SSH Key Path | `C:\Users\vyju1\.ssh\learning-key.pem` |
