# VALP SYSTEMS — EC2 Production Deployment

> Free Tier friendly | Ubuntu 22.04 on EC2 | PostgreSQL | FastAPI | Nginx | SSL

---

## Table of Contents

1. [Architecture Overview](#1-architecture-overview)
2. [Prerequisites](#2-prerequisites)
3. [Step 1 — Launch EC2 Instance (Free Tier)](#3-step-1--launch-ec2-instance-free-tier)
4. [Step 2 — Connect to EC2](#4-step-2--connect-to-ec2)
5. [Step 3 — Install System Dependencies](#5-step-3--install-system-dependencies)
6. [Step 4 — PostgreSQL Database Setup](#6-step-4--postgresql-database-setup)
7. [Step 5 — Deploy the Application](#7-step-5--deploy-the-application)
8. [Step 6 — Environment Configuration](#8-step-6--environment-configuration)
9. [Step 7 — Run Migrations & Seed](#9-step-7--run-migrations--seed)
10. [Step 8 — Systemd Service (Auto-start)](#10-step-8--systemd-service-auto-start)
11. [Step 9 — Nginx Reverse Proxy](#11-step-9--nginx-reverse-proxy)
12. [Step 10 — SSL Certificate (HTTPS)](#12-step-10--ssl-certificate-https)
13. [Step 11 — Verify Everything](#13-step-11--verify-everything)
14. [Security Checklist](#14-security-checklist)
15. [Maintenance](#15-maintenance)
16. [CI/CD Future Plan](#16-cicd-future-plan)
17. [Troubleshooting](#17-troubleshooting)

---

## 1. Architecture Overview

```
                           AWS Cloud
                        ┌──────────────┐
                        │   EC2 Instance   │
                        │  (t2.micro/t3.micro — Free Tier)  │
                        │                      │
  Browser ──HTTPS──►  Nginx (port 443)        │
                        │      │                  │
                        │  Uvicorn (port 8000)    │
                        │      │                  │
                        │  FastAPI Application    │
                        │      │                  │
                        │  PostgreSQL (port 5432) │
                        └──────────────────┘
```

| Component | What it does |
|-----------|-------------|
| **EC2** | Virtual server (free tier: 750 hrs/month for 12 months) |
| **Ubuntu 22.04** | OS on the EC2 |
| **PostgreSQL** | Production database |
| **FastAPI / Uvicorn** | Python web server |
| **Nginx** | Reverse proxy — handles HTTPS, rate limiting, serves as shield |
| **Certbot** | Free SSL certificates from Let's Encrypt |
| **Systemd** | Keeps the app running, auto-starts on reboot |

---

## 2. Prerequisites

### From your Local Machine (Windows or Linux/macOS)

| Tool | Why | Check |
|------|-----|-------|
| Git | Push code to GitHub/GitLab | `git --version` |
| SSH client | Connect to EC2 | `ssh` (built into Windows 10/11, Linux, macOS) |
| AWS account | Free tier eligible | Sign up at https://aws.amazon.com/free |

### From AWS

- An **AWS account** (credit card required, but free tier costs $0 if you stay within limits)
- A **key pair** (.pem file) for SSH access — created during EC2 launch below
- A **domain name** (optional but recommended — use Route53, Namecheap, etc.)

### Free Tier Limits (Important)

| Resource | Free Tier Limit |
|----------|----------------|
| EC2 | 750 hours/month (one t2.micro or t3.micro) |
| EBS | 30 GB GP2/GP3 storage |
| Data transfer | 100 GB/month outbound |

> **⚠️ Warning**: You will NOT be charged if you stay within these limits for 12 months. After 12 months, standard rates apply (~$8-15/month for this setup).

---

## 3. Step 1 — Launch EC2 Instance (Free Tier)

### 3.1 Login to AWS Console

Go to https://console.aws.amazon.com → **EC2** → **Launch Instance**

### 3.2 Instance Configuration

| Setting | Value |
|---------|-------|
| **Name** | `valp-systems-prod` |
| **OS** | Ubuntu Server 22.04 LTS (HVM), SSD Volume Type |
| **Architecture** | 64-bit (x86) |
| **Instance type** | `t2.micro` or `t3.micro` (free tier eligible) |
| **Key pair** | Select "Create new key pair" → name it `valp-key` → download the `.pem` file → **SAVE IT SAFELY** |

### 3.3 Network Settings

Click **Edit**:

| Setting | Value |
|---------|-------|
| **VPC** | Default VPC |
| **Auto-assign public IP** | Enable |
| **Firewall / Security group** | Create new |

**Add these security group rules:**

| Type | Protocol | Port Range | Source | Description |
|------|----------|-----------|--------|-------------|
| SSH | TCP | 22 | Your home IP (or `0.0.0.0/0` if dynamic) | SSH access |
| HTTP | TCP | 80 | `0.0.0.0/0` | Web traffic |
| HTTPS | TCP | 443 | `0.0.0.0/0` | Secure web traffic |

> **Security tip**: For SSH, set Source to your specific IP (e.g., `103.xxx.xxx.xxx/32`). You can find your IP by searching "what is my ip" in Google. If your IP changes often, use `0.0.0.0/0` but enable SSM Session Manager instead.

### 3.4 Configure Storage

| Setting | Value |
|---------|-------|
| **Size** | 20 GB (free tier: up to 30 GB) |
| **Volume type** | gp3 (free tier eligible) |
| **Delete on termination** | Yes |

### 3.5 Launch

Click **Launch instance**. Wait 2-3 minutes for it to be ready.

### 3.6 Get Your EC2 Public IP

In EC2 Dashboard → **Instances** → Select your instance → Copy **Public IPv4 address** (looks like `54.123.45.67`)

> If you have a domain, create an **A record** pointing `yourdomain.com` → this IP in your DNS provider (Route53, Namecheap, Cloudflare, etc.)

---

## 4. Step 2 — Connect to EC2

### Windows (PowerShell)

```powershell
# Navigate to where you saved the .pem file
cd C:\Users\YourName\Downloads

# Set proper permissions (required on Windows)
icacls .\valp-key.pem /inheritance:r /grant:r "$($env:USERNAME):(R)"

# Connect
ssh -i .\valp-key.pem ubuntu@54.123.45.67

# Replace 54.123.45.67 with your EC2 public IP
```

### Linux / macOS

```bash
cd ~/Downloads
chmod 400 valp-key.pem
ssh -i valp-key.pem ubuntu@54.123.45.67
```

### First-time login check

```bash
# You should see something like:
# Welcome to Ubuntu 22.04 LTS ...
# ubuntu@ip-xx-xx-xx-xx:~$
```

---

## 5. Step 3 — Install System Dependencies

Run these commands one by one on the EC2:

```bash
# Update packages
sudo apt update && sudo apt upgrade -y

# Install everything needed
sudo apt install -y python3 python3-pip python3-venv git nginx postgresql postgresql-contrib certbot python3-certbot-nginx

# Verify installations
python3 --version     # Should be 3.10+
psql --version        # Should be 14+
nginx -v              # Should be 1.18+
```

---

## 6. Step 4 — PostgreSQL Database Setup

### 6.1 Start PostgreSQL

```bash
sudo systemctl start postgresql
sudo systemctl enable postgresql  # Auto-start on reboot
sudo systemctl status postgresql   # Should show "active (running)"
```

### 6.2 Create Database User

```bash
# Switch to postgres system user
sudo -i -u postgres

# Create a database user (replace password with a strong one)
psql -c "CREATE USER valp_admin WITH PASSWORD 'Y0ur$trong!Passw0rd';"

# Create the database
psql -c "CREATE DATABASE valp_systems OWNER valp_admin;"

# Grant all permissions
psql -c "GRANT ALL PRIVILEGES ON DATABASE valp_systems TO valp_admin;"

# Exit postgres user
exit
```

### 6.3 Configure PostgreSQL to Trust Local Connections

```bash
# Find the pg_hba.conf file
sudo -u postgres psql -c "SHOW hba_file;"
# Typically: /etc/postgresql/14/main/pg_hba.conf

# Edit it
sudo nano /etc/postgresql/14/main/pg_hba.conf
```

Find this line:
```
local   all             all                                     peer
```

Change it to:
```
local   all             all                                     md5
```

Also add (or ensure this exists):
```
host    valp_systems    valp_admin      127.0.0.1/32            md5
```

```bash
# Restart PostgreSQL to apply changes
sudo systemctl restart postgresql
```

### 6.4 Test the Connection

```bash
PGPASSWORD='Y0ur$trong!Passw0rd' psql -h 127.0.0.1 -U valp_admin -d valp_systems -c "SELECT 1;"
```

You should see:
```
 ?column?
----------
        1
(1 row)
```

---

## 7. Step 5 — Deploy the Application

### 7.1 Clone the Repository

```bash
cd /opt
sudo git clone <your-repo-url> valpsystems
sudo chown -R ubuntu:ubuntu valpsystems
cd valpsystems/backend
```

> If your repo is private, use:
> ```bash
> git clone https://<username>:<token>@github.com/yourorg/valpsystems.git
> ```

### 7.2 Create Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 7.3 Verify App Imports

```bash
python -c "from app.main import app; print(f'App OK — {len(app.routes)} routes')"
```

Expected output:
```
App OK — 22 routes
```

### 7.4 Create Logs Directory

```bash
mkdir -p app/logs
```

---

## 8. Step 6 — Environment Configuration

### 8.1 Create .env File

```bash
cp .env.example .env
nano .env
```

### 8.2 Production Settings

Paste this into `.env` (replace all values marked `<>`):

```ini
# ─── Application ───
APP_NAME=VALP SYSTEMS
APP_VERSION=1.0.0
APP_DESCRIPTION=VALP SYSTEMS Enterprise Backend API
APP_ENV=production
APP_DEBUG=false
APP_HOST=0.0.0.0
APP_PORT=8000
APP_SECRET_KEY=<run: python3 -c "import secrets; print(secrets.token_urlsafe(48))">
APP_URL=https://yourdomain.com

# ─── Database (PostgreSQL) ───
DATABASE_URL=postgresql+asyncpg://valp_admin:Y0ur$trong!Passw0rd@127.0.0.1:5432/valp_systems
DATABASE_ECHO=false
DATABASE_POOL_SIZE=10
DATABASE_MAX_OVERFLOW=20

# ─── Testing (not used in production) ───
TEST_DATABASE_URL=sqlite+aiosqlite:///./test.db

# ─── CORS (allow your frontend domain) ───
CORS_ORIGINS=["https://yourdomain.com","https://www.yourdomain.com"]

# ─── Trusted Hosts ───
TRUSTED_HOSTS=["yourdomain.com","www.yourdomain.com"]

# ─── Logging ───
LOG_LEVEL=INFO
LOG_FORMAT=json

# ─── JWT ───
JWT_SECRET_KEY=<run: python3 -c "import secrets; print(secrets.token_urlsafe(48))" — DIFFERENT from APP_SECRET_KEY>
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7

# ─── Password Policy ───
PASSWORD_MIN_LENGTH=8
PASSWORD_REQUIRE_UPPERCASE=true
PASSWORD_REQUIRE_LOWERCASE=true
PASSWORD_REQUIRE_DIGIT=true
PASSWORD_REQUIRE_SPECIAL=false

# ─── Email Verification ───
EMAIL_VERIFICATION_TOKEN_EXPIRE_HOURS=24
PASSWORD_RESET_TOKEN_EXPIRE_HOURS=1

# ─── SMTP (Email sending — Gmail example) ───
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-gmail-app-password
SMTP_USE_TLS=true
SMTP_FROM_EMAIL=noreply@yourdomain.com
SMTP_FROM_NAME=VALP SYSTEMS

# ─── Rate Limiting ───
RATE_LIMIT_ENABLED=false
RATE_LIMIT_REQUESTS=10
RATE_LIMIT_WINDOW_SECONDS=60

# ─── Redis (optional) ───
REDIS_URL=redis://localhost:6379/0

# ─── AWS (optional) ───
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_REGION=us-east-1
```

### 8.3 Generate Secret Keys

Run these two commands separately on the EC2:

```bash
# For APP_SECRET_KEY
python3 -c "import secrets; print(secrets.token_urlsafe(48))"
# Copy the output and paste into .env for APP_SECRET_KEY

# For JWT_SECRET_KEY
python3 -c "import secrets; print(secrets.token_urlsafe(48))"
# Copy the output and paste into .env for JWT_SECRET_KEY
```

> **Important**: These two keys must be **different** from each other.

### 8.4 Save & Exit

In `nano`: `Ctrl+X` → `Y` → `Enter`

---

## 9. Step 7 — Run Migrations & Seed

```bash
# Activate virtual env (if not already)
source /opt/valpsystems/backend/.venv/bin/activate
cd /opt/valpsystems/backend

# Run database migrations
alembic upgrade head
```

Expected output:
```
INFO  [alembic.runtime.migration] Running upgrade  -> 0e9497533b08, initial
INFO  [alembic.runtime.migration] Running upgrade 0e9497533b08 -> a1b2c3d4e5f6, auth_tables
```

**Verify tables were created:**

```bash
PGPASSWORD='Y0ur$trong!Passw0rd' psql -h 127.0.0.1 -U valp_admin -d valp_systems -c "\dt"
```

You should see 19 tables:
```
               List of relations
 Schema |        Name         | Type  |  Owner
--------+---------------------+-------+----------
 public | audit_logs          | table | valp_admin
 public | career_applications | table | valp_admin
 public | contacts            | table | valp_admin
 public | email_verifications  | table | valp_admin
 public | feedbacks           | table | valp_admin
 public | login_history       | table | valp_admin
 public | newsletters         | table | valp_admin
 public | password_resets     | table | valp_admin
 public | permissions         | table | valp_admin
 public | quote_requests      | table | valp_admin
 public | refresh_tokens      | table | valp_admin
 public | resources           | table | valp_admin
 public | role_permissions    | table | valp_admin
 public | roles               | table | valp_admin
 public | services            | table | valp_admin
 public | solutions           | table | valp_admin
 public | technologies        | table | valp_admin
 public | user_roles          | table | valp_admin
 public | users               | table | valp_admin
(19 rows)
```

**Test that the app starts correctly:**

```bash
cd /opt/valpsystems/backend
source .venv/bin/activate
uvicorn app.main:app --host 127.0.0.1 --port 8000 &
sleep 3
curl http://127.0.0.1:8000/api/v1/health
kill %1 2>/dev/null
```

Expected output:
```json
{"success":true,"message":"Service is healthy","data":{"status":"healthy",...}}
```

---

## 10. Step 8 — Systemd Service (Auto-start)

This keeps your app running **even after reboot** or if it crashes.

### 10.1 Create the Service File

```bash
sudo nano /etc/systemd/system/valp-backend.service
```

### 10.2 Paste This Configuration

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
Environment=PATH=/opt/valpsystems/backend/.venv/bin:/usr/bin:/usr/local/bin
EnvironmentFile=/opt/valpsystems/backend/.env
ExecStart=/opt/valpsystems/backend/.venv/bin/uvicorn app.main:app \
  --host 127.0.0.1 \
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

### 10.3 Enable & Start

```bash
sudo systemctl daemon-reload
sudo systemctl enable valp-backend
sudo systemctl start valp-backend
```

### 10.4 Check Status

```bash
sudo systemctl status valp-backend
```

Expected output:
```
● valp-backend.service - VALP SYSTEMS Backend API
     Loaded: loaded (/etc/systemd/system/valp-backend.service; enabled; vendor preset: enabled)
     Active: active (running) since ...
```

### 10.5 View Logs

```bash
# Live log stream
sudo journalctl -u valp-backend -f

# Last 50 lines
sudo journalctl -u valp-backend -n 50 --no-pager
```

---

## 11. Step 9 — Nginx Reverse Proxy

### 11.1 Create Nginx Config

```bash
sudo nano /etc/nginx/sites-available/valp-backend
```

### 11.2 Paste This Configuration

```nginx
# Upstream — the FastAPI backend
upstream valp_backend {
    server 127.0.0.1:8000;
}

# HTTP → HTTPS redirect (only if you have a domain)
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    # For certbot (SSL setup)
    location /.well-known/acme-challenge/ {
        root /var/www/html;
    }

    # Redirect everything else to HTTPS
    location / {
        return 301 https://$server_name$request_uri;
    }
}

# HTTPS server
server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    # SSL — will be filled by certbot in Step 10
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

    # Request size limit
    client_max_body_size 10M;

    # ─── API Routes ───

    location /api/ {
        proxy_pass http://valp_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 90s;
        proxy_connect_timeout 10s;
    }

    # ─── Swagger UI ───
    location /docs {
        proxy_pass http://valp_backend/docs;
        proxy_set_header Host $host;
    }

    location /redoc {
        proxy_pass http://valp_backend/redoc;
        proxy_set_header Host $host;
    }

    location /openapi.json {
        proxy_pass http://valp_backend/openapi.json;
        proxy_set_header Host $host;
    }

    # ─── Health Check ───
    location / {
        proxy_pass http://valp_backend/;
        proxy_set_header Host $host;
    }

    # ─── Rate Limiting for Login ───
    limit_req_zone $binary_remote_addr zone=login:10m rate=5r/s;
    location /api/v1/auth/login {
        limit_req zone=login burst=3 nodelay;
        proxy_pass http://valp_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # ─── Deny access to .env and .git ───
    location ~ /\.(env|git) {
        deny all;
        return 404;
    }

    # ─── Logs ───
    access_log /var/log/nginx/valp-access.log;
    error_log /var/log/nginx/valp-error.log;
}
```

### 11.3 Enable & Test

```bash
# If you DON'T have a domain yet, use this simpler config first:
sudo nano /etc/nginx/sites-available/valp-backend
```

Replace the above with this **no-domain version** (HTTP only):

```nginx
upstream valp_backend {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name _;  # Any domain or IP

    client_max_body_size 10M;

    location /api/ {
        proxy_pass http://valp_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 90s;
    }

    location /docs {
        proxy_pass http://valp_backend/docs;
    }

    location /redoc {
        proxy_pass http://valp_backend/redoc;
    }

    location /openapi.json {
        proxy_pass http://valp_backend/openapi.json;
    }

    location / {
        proxy_pass http://valp_backend/;
    }

    location ~ /\.(env|git) {
        deny all;
        return 404;
    }
}
```

```bash
# Enable the site
sudo ln -s /etc/nginx/sites-available/valp-backend /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default  # Remove default

# Test config
sudo nginx -t

# If test passes, restart Nginx
sudo systemctl restart nginx
```

### 11.4 Verify Nginx

```bash
curl http://localhost/api/v1/health
# Should return the health check JSON
```

---

## 12. Step 10 — SSL Certificate (HTTPS)

> **Skip this step if you don't have a domain yet.** You can test with HTTP first.

### 12.1 Install SSL

```bash
# Replace with your actual domain
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

### 12.2 Follow the Prompts

```
Enter email for urgent renewal notices: you@email.com
Agree to terms of service: A
Share email with EFF: N (optional)
```

### 12.3 Verify Auto-Renewal

```bash
# Test that renewal works (doesn't actually renew)
sudo certbot renew --dry-run

# Check the timer
sudo systemctl list-timers | grep certbot
```

Certbot creates a systemd timer that auto-renews every 60 days. No manual action needed.

---

## 13. Step 11 — Verify Everything

### 13.1 From EC2 itself

```bash
# Health check
curl https://yourdomain.com/api/v1/health
# OR (if no domain)
curl http://localhost/api/v1/health

# Register a user
curl -X POST https://yourdomain.com/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@yourdomain.com","username":"admin","password":"AdminPass1","confirm_password":"AdminPass1"}'

# Login
curl -X POST https://yourdomain.com/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@yourdomain.com","password":"AdminPass1"}'
```

### 13.2 From Your Local Browser

- **Swagger UI**: `https://yourdomain.com/docs`
- **Health**: `https://yourdomain.com/api/v1/health`

### 13.3 Final Status Check

```bash
# Service status
sudo systemctl status valp-backend --no-pager

# Nginx status
sudo systemctl status nginx --no-pager

# PostgreSQL status
sudo systemctl status postgresql --no-pager

# Disk space
df -h

# Memory
free -h
```

---

## 14. Security Checklist

After deployment, verify each item:

- [ ] **`APP_DEBUG=false`** in `.env`
- [ ] **`JWT_SECRET_KEY`** is a long random string (different from `APP_SECRET_KEY`)
- [ ] **`APP_SECRET_KEY`** is a long random string
- [ ] **PostgreSQL password** is strong (16+ chars, mixed case, numbers, special)
- [ ] **PostgreSQL bound to 127.0.0.1** only (not accessible from outside)
- [ ] **Security group** — SSH allowed only from your IP
- [ ] **Nginx** blocks access to `.env` and `.git` files (already in config above)
- [ ] **SSL/HTTPS** active (if domain is configured)
- [ ] **Rate limiting** on login endpoint (already in config above)
- [ ] **Regular updates** — run weekly:
  ```bash
  sudo apt update && sudo apt upgrade -y
  sudo systemctl restart valp-backend  # If Python packages updated
  ```

---

## 15. Maintenance

### 15.1 Update Application Code

```bash
cd /opt/valpsystems/backend
source .venv/bin/activate
sudo -u ubuntu git pull origin main
pip install -r requirements.txt  # If new dependencies
alembic upgrade head             # If new migrations
sudo systemctl restart valp-backend
```

### 15.2 View Application Logs

```bash
# Live stream
sudo journalctl -u valp-backend -f

# Last 100 lines
sudo journalctl -u valp-backend -n 100

# Filter by date
sudo journalctl -u valp-backend --since "2026-01-01" --until "2026-01-02"
```

### 15.3 Database Backup (Recommended)

Create a backup script:

```bash
sudo nano /opt/valpsystems/scripts/backup.sh
```

```bash
#!/bin/bash
BACKUP_DIR="/opt/valpsystems/backups"
mkdir -p $BACKUP_DIR
PGPASSWORD='Y0ur$trong!Passw0rd' pg_dump -h 127.0.0.1 -U valp_admin -d valp_systems > "$BACKUP_DIR/backup_$(date +%Y%m%d_%H%M%S).sql"
# Keep only last 7 days of backups
find $BACKUP_DIR -name "*.sql" -mtime +7 -delete
```

```bash
chmod +x /opt/valpsystems/scripts/backup.sh

# Schedule daily at 3 AM
sudo crontab -e
# Add this line:
0 3 * * * /opt/valpsystems/scripts/backup.sh
```

### 15.4 Reboot Test

```bash
sudo reboot
# Wait 2 minutes, then SSH back in
sudo systemctl status valp-backend  # Should show "active (running)"
```

---

## 16. CI/CD Future Plan

This section covers how to automate deployments in the future.

### 16.1 Current Manual Flow

```
Local Dev ──git push──► GitHub ──ssh──► EC2 ──git pull──► Deploy
```

### 16.2 Future Automated Flow

```
Local Dev ──git push──► GitHub ──webhook──► GitHub Actions ──ssh──► EC2
                                              │
                                              ├── Run tests
                                              ├── Build
                                              ├── Copy files
                                              ├── Install deps
                                              ├── Run migrations
                                              └── Restart service
```

### 16.3 GitHub Actions Workflow (when ready)

Create `.github/workflows/deploy.yml` in your repo root:

```yaml
name: Deploy to EC2

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.13'
      - name: Install dependencies
        run: pip install -r backend/requirements.txt
      - name: Run tests
        run: pytest backend/tests/ -v
        env:
          APP_ENV: testing

  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to EC2 via SSH
        uses: appleboy/ssh-action@v1.0.3
        with:
          host: ${{ secrets.EC2_HOST }}
          username: ubuntu
          key: ${{ secrets.EC2_SSH_KEY }}
          script: |
            cd /opt/valpsystems/backend
            git pull origin main
            source .venv/bin/activate
            pip install -r requirements.txt
            alembic upgrade head
            sudo systemctl restart valp-backend
```

### 16.4 What You Need to Set Up for CI/CD

| Item | How |
|------|-----|
| GitHub repo | Push your code to GitHub |
| `EC2_HOST` secret | Your EC2 public IP or domain |
| `EC2_SSH_KEY` secret | Your private key (the `.pem` file content) |
| GitHub Actions | Enabled on your repo (free for public repos) |

### 16.5 Deployment Options Comparison

| Method | Effort | Best For |
|--------|--------|----------|
| **Manual (current)** | Low | MVP, learning |
| **GitHub Actions** | Medium | Solo dev, small team |
| **Docker + ECS** | High | Scalable production |
| **Terraform + Ansible** | High | Infrastructure as Code |

> **Recommendation**: Start with `Manual`. Once you're comfortable, add `GitHub Actions` (takes ~1 hour to set up). Move to `Docker` only when you need multiple servers.

---

## 17. Troubleshooting

### App won't start

```bash
# Check the service logs
sudo journalctl -u valp-backend -n 50 --no-pager

# Common fixes:
# 1. .env file missing — check /opt/valpsystems/backend/.env exists
# 2. PostgreSQL not running — sudo systemctl restart postgresql
# 3. Port 8000 already in use — sudo lsof -i :8000
```

### 502 Bad Gateway from Nginx

```bash
# 1. Is the app running?
sudo systemctl status valp-backend

# 2. Is it listening on port 8000?
curl http://127.0.0.1:8000/api/v1/health

# 3. Check Nginx error log
sudo tail -f /var/log/nginx/valp-error.log
```

### Database connection failed

```bash
# Test manually
PGPASSWORD='Y0ur$trong!Passw0rd' psql -h 127.0.0.1 -U valp_admin -d valp_systems -c "SELECT 1;"

# Check if PostgreSQL is running
sudo systemctl status postgresql

# Check the .env DATABASE_URL is correct
grep DATABASE_URL /opt/valpsystems/backend/.env
```

### Permission denied

```bash
# Fix ownership
sudo chown -R ubuntu:ubuntu /opt/valpsystems

# Fix log directory
sudo chown -R ubuntu:ubuntu /opt/valpsystems/backend/app/logs
```

### Domain not resolving

```bash
# Check DNS
nslookup yourdomain.com

# Wait — DNS changes can take 5 minutes to 48 hours to propagate
# Test with IP directly: curl http://54.123.45.67/api/v1/health
```

---

## Quick Reference Sheet

```bash
# ─── Service Management ───
sudo systemctl start valp-backend
sudo systemctl stop valp-backend
sudo systemctl restart valp-backend
sudo systemctl status valp-backend
sudo journalctl -u valp-backend -f

# ─── Nginx ───
sudo systemctl restart nginx
sudo nginx -t

# ─── PostgreSQL ───
sudo systemctl restart postgresql
PGPASSWORD='password' psql -h 127.0.0.1 -U valp_admin -d valp_systems

# ─── App Update ───
cd /opt/valpsystems/backend
git pull
source .venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
sudo systemctl restart valp-backend

# ─── Logs ───
sudo journalctl -u valp-backend -n 100
sudo tail -f /var/log/nginx/valp-access.log
```

---

> **Next Step**: After deployment, build the frontend login page to connect to this backend. See the existing frontend at `frontend/` in this repo.
