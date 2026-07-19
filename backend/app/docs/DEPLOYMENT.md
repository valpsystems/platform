# VALP SYSTEMS Backend — Deployment Guide

## Architecture Overview

```
Browser/Client
     │
     ▼
  Nginx (reverse proxy, port 443)
     │
     ▼
  Uvicorn (ASGI server, port 8000)
     │
     ├── FastAPI Application
     │
     ▼
  PostgreSQL (port 5432)
```

---

## 1. Local Development Setup (Windows / macOS / Linux)

### 1.1 Prerequisites

| Tool | Version | Check Command |
|------|---------|---------------|
| Python | 3.13+ | `python --version` |
| pip | latest | `pip --version` |

### 1.2 Clone & Prepare

```bash
git clone <repo-url> valpsystems
cd valpsystems/backend

# Create virtual environment (recommended)
python -m venv .venv

# Activate
# Windows (PowerShell):
.venv\Scripts\Activate.ps1
# macOS / Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 1.3 Environment File

```bash
cp .env.example .env
```

Edit `.env` for **local development** — use SQLite so no PostgreSQL is needed:

```ini
# .env  (local dev — SQLite, no external DB needed)
APP_ENV=development
APP_DEBUG=true
APP_HOST=0.0.0.0
APP_PORT=8000

# Use SQLite for local dev (comment out PostgreSQL URL)
DATABASE_URL=sqlite+aiosqlite:///./app.db

# JWT — generate a random key
JWT_SECRET_KEY=generate-a-random-secret-key-here

# SMTP — leave empty to skip emails in dev
SMTP_HOST=
```

> **Important**: Set `DATABASE_URL` to SQLite for local testing. PostgreSQL is only needed for EC2/production.

### 1.4 Create Database Tables (Migration)

```bash
# Apply all migrations (creates tables in SQLite)
alembic upgrade head

# Verify tables were created
# You should see 19 tables (9 business + 10 auth)
```

> If you get an error about `async` engines, run the migration in sync mode:
> ```bash
> # Edit alembic.ini temporarily:
> # sqlalchemy.url = sqlite:///./app.db
> # Then run:
> alembic upgrade head
> # Revert the change afterwards
> ```

### 1.5 Seed Default Data

```bash
# Creates default roles (admin, user) and permissions
python scripts/seed.py
```

### 1.6 Run Locally

```bash
# Development mode (auto-reload)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Or use the helper script:
.\scripts\run.ps1 dev    # PowerShell
./scripts/run.sh dev      # Bash
```

Open: http://localhost:8000/docs (Swagger UI)

### 1.7 Run Tests

```bash
# All tests
pytest tests/ -v

# Auth-specific tests
pytest tests/api/v1/test_auth.py -v

# With coverage
pytest tests/ --cov=app/
```

### 1.8 Quick Verification Checklist

```bash
# 1. App starts without errors
uvicorn app.main:app --host 0.0.0.0 --port 8000

# 2. Health endpoint works
curl http://localhost:8000/api/v1/health

# 3. Register a test user
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","username":"testuser","password":"TestPass123","confirm_password":"TestPass123"}'

# 4. Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"TestPass123"}'

# 5. All tests pass
pytest tests/ -v
```

---

## 2. EC2 Production Deployment (Ubuntu / Amazon Linux)

### 2.1 EC2 Instance Setup

**Recommended Instance:**
- Type: `t3.medium` or larger
- OS: Ubuntu 22.04 LTS or Amazon Linux 2023
- Storage: 20 GB gp3
- Security Group:

| Type | Protocol | Port | Source |
|------|----------|------|--------|
| SSH | TCP | 22 | Your IP |
| HTTP | TCP | 80 | 0.0.0.0/0 |
| HTTPS | TCP | 443 | 0.0.0.0/0 |
| Custom | TCP | 8000 | 0.0.0.0/0 (temporary, for testing) |

### 2.2 Connect to EC2

```bash
# From your local machine
ssh -i your-key.pem ubuntu@<ec2-public-ip>
```

### 2.3 Install System Dependencies

```bash
# Ubuntu
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-pip python3-venv git nginx postgresql postgresql-contrib certbot python3-certbot-nginx

# Amazon Linux 2023
sudo dnf update -y
sudo dnf install -y python3 python3-pip git nginx postgresql15 postgresql15-server
```

### 2.4 PostgreSQL Database Setup (Step-by-Step)

#### Step 1: Start PostgreSQL

```bash
# Ubuntu
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Amazon Linux
sudo postgresql-setup --initdb
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

#### Step 2: Create Database & User

```bash
# Switch to postgres user
sudo -i -u postgres

# Create database user (replace 'valp_user' and 'YourStrongPassword')
psql -c "CREATE USER valp_user WITH PASSWORD 'YourStrongPassword';"

# Create database
psql -c "CREATE DATABASE valp_systems OWNER valp_user;"

# Grant all privileges
psql -c "GRANT ALL PRIVILEGES ON DATABASE valp_systems TO valp_user;"

# Exit postgres user
exit
```

#### Step 3: Configure Remote Access (if needed)

```bash
# Edit pg_hba.conf (find the path first)
sudo -u postgres psql -c "SHOW hba_file;"
# Typically: /etc/postgresql/16/main/pg_hba.conf

# Add or update this line (for local app connections):
# local   valp_systems   valp_user   md5
# host    valp_systems   valp_user   127.0.0.1/32   md5

# Restart PostgreSQL
sudo systemctl restart postgresql
```

#### Step 4: Verify Connection

```bash
# Test connection
PGPASSWORD='YourStrongPassword' psql -h 127.0.0.1 -U valp_user -d valp_systems -c "SELECT 1;"
# Should return: ?column? → 1
```

### 2.5 Clone Application

```bash
cd /opt
sudo git clone <repo-url> valpsystems
sudo chown -R ubuntu:ubuntu valpsystems
cd valpsystems/backend
```

### 2.6 Create Production Environment File

```bash
cp .env.example .env
```

Edit `.env`:

```ini
# .env  (EC2 production)
APP_NAME=VALP SYSTEMS
APP_VERSION=1.0.0
APP_DESCRIPTION=VALP SYSTEMS Enterprise Backend API
APP_ENV=production
APP_DEBUG=false
APP_HOST=0.0.0.0
APP_PORT=8000
APP_SECRET_KEY=<generate-a-secure-random-64-char-key>
APP_URL=https://yourdomain.com

# PostgreSQL (use 127.0.0.1 to connect via local socket)
DATABASE_URL=postgresql+asyncpg://valp_user:YourStrongPassword@127.0.0.1:5432/valp_systems
DATABASE_ECHO=false
DATABASE_POOL_SIZE=10
DATABASE_MAX_OVERFLOW=20

# CORS — allow your frontend domain
CORS_ORIGINS=["https://yourdomain.com","https://www.yourdomain.com"]

# Trusted Hosts
TRUSTED_HOSTS=["yourdomain.com","www.yourdomain.com"]

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json

# JWT
JWT_SECRET_KEY=<generate-a-different-secure-random-64-char-key>
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7

# Password Policy
PASSWORD_MIN_LENGTH=8
PASSWORD_REQUIRE_UPPERCASE=true
PASSWORD_REQUIRE_LOWERCASE=true
PASSWORD_REQUIRE_DIGIT=true
PASSWORD_REQUIRE_SPECIAL=false

# Email Verification
EMAIL_VERIFICATION_TOKEN_EXPIRE_HOURS=24
PASSWORD_RESET_TOKEN_EXPIRE_HOURS=1

# SMTP — configure your email provider
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_USE_TLS=true
SMTP_FROM_EMAIL=noreply@yourdomain.com
SMTP_FROM_NAME=VALP SYSTEMS

# Redis (optional)
REDIS_URL=redis://localhost:6379/0
```

> Generate secret keys with: `python -c "import secrets; print(secrets.token_urlsafe(48))"`

### 2.7 Create Python Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 2.8 Run Database Migrations

```bash
# Ensure PostgreSQL is running
sudo systemctl status postgresql

# Apply migrations
alembic upgrade head

# Verify tables
PGPASSWORD='YourStrongPassword' psql -h 127.0.0.1 -U valp_user -d valp_systems -c "\dt"
# You should see 19 tables
```

### 2.9 Seed Default Data

The `scripts/seed.py` script may need to be updated for Phase 5 to create default roles and permissions. For now, run:

```bash
python scripts/seed.py
```

> **Note**: You may need to update `scripts/seed.py` to seed default roles (admin, user) and permissions if not already done.

### 2.10 Create Systemd Service (Auto-start on Boot)

```bash
sudo nano /etc/systemd/system/valp-backend.service
```

Paste the following (adjust paths and user as needed):

```ini
[Unit]
Description=VALP SYSTEMS Backend API
After=network.target postgresql.service
Wants=postgresql.service

[Service]
Type=simple
User=ubuntu
Group=ubuntu
WorkingDirectory=/opt/valpsystems/backend
Environment=PATH=/opt/valpsystems/backend/.venv/bin:/usr/bin
EnvironmentFile=/opt/valpsystems/backend/.env
ExecStart=/opt/valpsystems/backend/.venv/bin/uvicorn app.main:app \
  --host 0.0.0.0 \
  --port 8000 \
  --workers 4 \
  --log-level info
Restart=always
RestartSec=5
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

Enable and start the service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable valp-backend
sudo systemctl start valp-backend

# Check status
sudo systemctl status valp-backend

# View logs
sudo journalctl -u valp-backend -f
```

### 2.11 Configure Nginx as Reverse Proxy

```bash
sudo nano /etc/nginx/sites-available/valp-backend
```

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    # Redirect HTTP to HTTPS (if using certbot)
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    # SSL — configure after running certbot
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # API proxy
    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 90s;
    }

    # Swagger / OpenAPI docs
    location /docs {
        proxy_pass http://127.0.0.1:8000/docs;
        proxy_set_header Host $host;
    }

    location /openapi.json {
        proxy_pass http://127.0.0.1:8000/openapi.json;
        proxy_set_header Host $host;
    }

    # Root health check
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
    }

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
    location /api/v1/auth/login {
        limit_req zone=api burst=5 nodelay;
        proxy_pass http://127.0.0.1:8000;
    }
}
```

```bash
# Enable the site
sudo ln -s /etc/nginx/sites-available/valp-backend /etc/nginx/sites-enabled/
sudo nginx -t  # Test config
sudo systemctl restart nginx
```

### 2.12 SSL Certificate (HTTPS)

```bash
# Install certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Auto-renewal (certbot sets this up automatically)
sudo certbot renew --dry-run
```

### 2.13 Testing Production

```bash
# Health check
curl https://yourdomain.com/api/v1/health

# Register a user
curl -X POST https://yourdomain.com/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@yourdomain.com","username":"admin","password":"AdminPass123","confirm_password":"AdminPass123"}'

# Login
curl -X POST https://yourdomain.com/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@yourdomain.com","password":"AdminPass123"}'
```

---

## 3. Common Tasks

### 3.1 View Logs

```bash
# Application logs
sudo journalctl -u valp-backend -f

# Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log

# Application log files (if configured)
tail -f /opt/valpsystems/backend/app/logs/app.log
```

### 3.2 Database Backup & Restore

```bash
# Backup
pg_dump -h 127.0.0.1 -U valp_user -d valp_systems > backup_$(date +%Y%m%d).sql

# Restore
psql -h 127.0.0.1 -U valp_user -d valp_systems < backup_file.sql
```

### 3.3 Create a New Migration

```bash
source .venv/bin/activate
alembic revision --autogenerate -m "description_of_change"
alembic upgrade head
```

### 3.4 Update Application Code

```bash
cd /opt/valpsystems/backend
sudo -u ubuntu git pull origin main
source .venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
sudo systemctl restart valp-backend
```

---

## 4. Troubleshooting

| Problem | Check |
|---------|-------|
| `Connection refused` on DB | Is PostgreSQL running? (`sudo systemctl status postgresql`) |
| `UNIQUE constraint failed` | Check if seed data was already inserted; run idempotent seed |
| `502 Bad Gateway` from Nginx | Is Uvicorn running? (`sudo systemctl status valp-backend`) |
| JWT tokens invalid after deploy | Ensure `JWT_SECRET_KEY` is the same across all app instances |
| Email not sending | Check SMTP settings; ensure port 587 is open outbound |
| Migration fails on `async` engine | Use the sync URL format: `postgresql://user:pass@host/db` |
| Permission denied on log dir | `sudo chown -R ubuntu:ubuntu /opt/valpsystems/backend/app/logs` |

---

## 5. Security Checklist

- [ ] `APP_SECRET_KEY` changed to a long random value
- [ ] `JWT_SECRET_KEY` changed to a different long random value
- [ ] PostgreSQL password is strong and not default
- [ ] `APP_DEBUG=false` in production
- [ ] `CORS_ORIGINS` restricted to your frontend domain
- [ ] `TRUSTED_HOSTS` restricted
- [ ] SSL/HTTPS enabled via certbot
- [ ] Firewall (security group) restricts SSH to your IP only
- [ ] PostgreSQL not exposed to the internet (bound to 127.0.0.1)
- [ ] Nginx rate limiting configured on login endpoint
- [ ] Regular database backups scheduled (cron)
- [ ] OS updates applied (`sudo apt update && sudo apt upgrade`)

---

## 6. Quick Reference: Environment Comparison

| Feature | Local (Dev) | EC2 (Production) |
|---------|-------------|-------------------|
| **Database** | SQLite (`app.db`) | PostgreSQL 16 |
| **Server** | Uvicorn (single worker) | Uvicorn (4 workers) + Nginx |
| **Auto-reload** | Yes | No |
| **HTTPS** | No | Yes (certbot) |
| **Debug mode** | True | False |
| **Log level** | DEBUG | INFO |
| **SMTP** | Not configured (emails skipped) | Configured (real emails) |
| **Service** | Manual `uvicorn` command | systemd service (auto-start) |
| **Domain** | `localhost:8000` | `yourdomain.com` |
| **Install** | `pip install -r requirements.txt` | Same + system packages |

---

## 7. Files & Directories Reference

| Path | Purpose |
|------|---------|
| `.env` | Environment configuration (excluded from git — **do not commit**) |
| `.env.example` | Template for `.env` (committed to git) |
| `alembic/` | Database migration scripts |
| `alembic.ini` | Alembic configuration |
| `app/logs/` | Application log files (auto-created) |
| `scripts/run.ps1` | PowerShell run script |
| `scripts/run.sh` | Bash run script |
| `scripts/seed.py` | Database seeding script |
| `tests/` | Pytest test suite |
| `/etc/systemd/system/valp-backend.service` | systemd service (EC2 only) |
| `/etc/nginx/sites-available/valp-backend` | Nginx config (EC2 only) |
