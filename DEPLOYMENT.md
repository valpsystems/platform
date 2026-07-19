# VALP SYSTEMS — Deployment Guide

This document is the top-level entry point for deploying the full VALP SYSTEMS stack.

## Architecture

```
Internet → Nginx → Backend (FastAPI/Uvicorn) → PostgreSQL
                                    ↕
                             Frontend (React/Next.js)
```

## Repositories

| Directory | Tech | Deployment Doc |
|-----------|------|----------------|
| `backend/` | FastAPI + PostgreSQL | [Backend Guide](./backend/app/docs/DEPLOYMENT.md) |
| `frontend/` | (TBD) | (TBD) |

## Quick Links

- **Local Development**: See [Backend Guide → Section 1](./backend/app/docs/DEPLOYMENT.md#1-local-development-setup)
- **EC2 Production**: See [Backend Guide → Section 2](./backend/app/docs/DEPLOYMENT.md#2-ec2-production-deployment)
- **Environment Config**: [`backend/.env.example`](./backend/.env.example)
- **API Docs** (running): `http://localhost:8000/docs`

## Deployment Order

1. **Database** — Set up PostgreSQL (local or RDS)
2. **Backend** — Deploy FastAPI app, run migrations
3. **Frontend** — Build and deploy static assets / SSR
4. **Nginx** — Configure reverse proxy for both
5. **SSL** — Certbot / CloudFront / ALB
6. **Monitor** — Set up logging and health checks

> For complete step-by-step backend instructions, see [`backend/app/docs/DEPLOYMENT.md`](./backend/app/docs/DEPLOYMENT.md).
