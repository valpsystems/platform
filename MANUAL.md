# VALP SYSTEMS — Complete Deployment Manual

A full record of what was done to bring the stack live on AWS, why each failure
happened, the underlying concepts, and the best practices that came out of it.
Written so that any future deployment — bare-metal or containerized — can follow
the same reasoning instead of re-learning the same lessons.

**Final status (2026-08-21): LIVE** — frontend `200`, API healthy, all through
`http://23.20.14.94/`

---

## Table of Contents

1. [Architecture & Current State](#1-architecture--current-state)
2. [Deployment Journal — What We Did](#2-deployment-journal--what-we-did)
3. [Root-Cause Deep Dives](#3-root-cause-deep-dives)
   - 3.1 [502 Bad Gateway → bind address](#31-502-bad-gateway--bind-address)
   - 3.2 ["Invalid host header" → TrustedHostMiddleware](#32-invalid-host-header--trustedhostmiddleware)
   - 3.3 [`{"detail":"Not Found"}` → nginx URI rewriting](#33-detailnot-found--nginx-uri-rewriting)
   - 3.4 [405 Method Not Allowed → mangled config](#34-405-method-not-allowed--mangled-config)
   - 3.5 [Conflicting server name → AL2023 layout](#35-conflicting-server-name--al2023-layout)
   - 3.6 [`Invalid Version` / `ENOSPC` → /tmp is tmpfs](#36-invalid-version--enospc---tmp-is-tmpfs)
   - 3.7 [504 vs 502 → Security Group semantics](#37-504-vs-502--security-group-semantics)
   - 3.8 [Disk & memory sizing](#38-disk--memory-sizing)
4. [Standard Operating Procedures](#4-standard-operating-procedures)
5. [Best Practices Going Forward](#5-best-practices-going-forward)
6. [Command Reference](#6-command-reference)

---

## 1. Architecture & Current State

```
Internet ──► IGW ──► Public Subnet (10.0.1.0/24) ──► Proxy [NGINX :80]
                                                       │ private VPC routing
                                                       ▼
                     Private Subnet (10.0.2.0/24) ──► App Server [:8080 API, :3000 UI]
                                                       │
                                                       ▼
                                                  DB Server [PostgreSQL :5432]
```

| Component | Value | Notes |
|-----------|-------|-------|
| Proxy public IP | `23.20.14.94` | auto-assigned; **changes on stop/start** (EIP deferred for cost) |
| Proxy instance | `ip-10-0-1-121`, Amazon Linux 2023 | NGINX 1.30.3 |
| App server | `10.0.2.50` + `10.0.2.236` (two private IPs) | FastAPI via systemd, Next.js via PM2 |
| DB server | private only | PostgreSQL 15 |
| Proxy SG | `vlap-public-sg` (`sg-0903e7ff9a9b3cb76`) | 80 open to world, 22 restricted |
| App/DB SG | `valp-prv-sg` (`sg-0eb288b2ae6fb781b`) | 22, **8080**, **3000** from `10.0.1.0/24` |
| DB SG | `valp-db-sg` (`sg-03ee5463695e92c58`) | 5432 from app only |
| App disk | 20 GB gp3 (grown from 8) | `growpart` + `xfs_growfs` |
| App swap | 2 GB `/swapfile` | essential on ~1 GB RAM micro instance |

**Source-of-truth files in repo:**

| File | Purpose |
|------|---------|
| `deploy/nginx/app.conf` | The exact NGINX config running on the proxy — edit here, scp up |
| `DEPLOYMENT.md` | Step-by-step deploy guide (+ status notes at top) |
| `TROUBLESHOOTING.md` | Quick symptom→cause→fix tables |
| `MANUAL.md` | This document |

---

## 2. Deployment Journal — What We Did

Chronological account of the session:

1. **EIP decision** — Elastic IP discarded to avoid idle hourly cost; documented
   that an EIP will be attached later if a static IP is needed. Consequence:
   public IP changes on every stop/start → update checklist required (§4.1).
2. **Proxy NGINX setup** — config applied on proxy; early versions were hand-edited
   and drifted from the guide (this caused problems later).
3. **First request → 502 Bad Gateway.**
   Backend was bound to `127.0.0.1:8080`; NGINX could reach the *machine* but not
   the *service*. Fixed: systemd unit changed to `--host 0.0.0.0`. (§3.1)
4. **Second request → "Invalid host header".**
   `.env` still listed the old EIP in `TRUSTED_HOSTS`. Fixed with:
   `sed -i 's/174\.129\.16\.36/23.20.14.94/g' .env` + service restart. (§3.2)
5. **Third request → `{"detail":"Not Found"}` on `/health`.**
   Request reached FastAPI but as path `/health`, which doesn't exist — the real
   route is `/api/v1/health`. NGINX `proxy_pass` URI rewriting was wrong. (§3.3)
6. **Config drift disaster** — repeated manual edits/heredoc pastes over SSH left
   `app.conf` routing *everything* to the health endpoint → `405 Method Not Allowed`
   on `/`. Resolution: stopped hand-editing on the server; committed
   `deploy/nginx/app.conf` to the repo and pushed it with `scp`. (§3.4)
7. **`conflicting server name "_"` warning** — traced to AL2023's inline default
   server block inside `/etc/nginx/nginx.conf` (there is no `conf.d/default.conf`
   on AL2023). Harmless but noisy; clean fix is commenting out that block. (§3.5)
8. **Frontend build failures** — `npm install` failed with `Invalid Version:` then
   `ENOSPC`. Root cause chain: 8 GB disk nearly full earlier → grew EBS to 20 GB;
   but the real killer was npm cache placed in `/tmp`, which on AL2023 is a
   **RAM-backed tmpfs (~450 MB)**. Plain `npm install` (cache in `~/.npm`) worked. (§3.6)
9. **Instance sizing** — grew disk 8→20 GB online (`growpart` + `xfs_growfs`),
   added 2 GB swapfile for the ~1 GB RAM micro instance before `next build`.
10. **PM2 duplicates** — frontend had been started 5×; three processes were
    crash-looping fighting over port 3000 (restart counts >1200), pinning CPU at
    99.9%. Fixed with `pm2 delete` + single start + `pm2 save`.
11. **Public URL → 504 Gateway Time-out.**
    NGINX → `10.0.2.50:3000` packets silently dropped: `valp-prv-sg` had no rule
    for port 3000. Added via AWS CLI:
    `authorize-security-group-ingress --port 3000 --cidr 10.0.1.0/24`. (§3.7)
12. **Verification** — all three endpoints green:
    `/` → 200 · `/api/v1/health` → healthy JSON · `/health` → 200.

---

## 3. Root-Cause Deep Dives

### 3.1 502 Bad Gateway → bind address

**Symptom:** `curl http://23.20.14.94/health` → 502 from nginx.

**Diagnosis chain:**

```bash
sudo ss -tlnp | grep 8080     # showed 127.0.0.1:8080  ← the smoking gun
```

**Concept:** a listening socket has a *bind address*. `127.0.0.1` means "accept
connections only from this machine". The app server has interfaces `10.0.2.50`
and `10.0.2.236`; NGINX arrives over the network targeting one of those IPs —
nothing is listening there, so the kernel refuses, and nginx reports 502.

**Fix:** `--host 0.0.0.0` ("listen on ALL interfaces") in the systemd unit +
`daemon-reload` + restart.

**Best practice:** never use the bind address as your security control. Bind
`0.0.0.0` and restrict *who can reach the port* with Security Groups
(`valp-prv-sg` allows 8080 only from `10.0.1.0/24`). Defense lives at the network
layer; the app just listens.

> Container translation: same rule — apps inside containers must listen on
> `0.0.0.0`. `EXPOSE`/`-p` publishing does **not** change the app's bind address;
> a container app bound to `127.0.0.1` is unreachable even with perfect port
> mapping. This exact bug is the #1 first-time Docker mistake.

### 3.2 "Invalid host header" → TrustedHostMiddleware

**Symptom:** after fixing 3.1, requests returned plain-text `Invalid host header`.

**Concept:** FastAPI's `TrustedHostMiddleware` compares the HTTP `Host:` header
against `TRUSTED_HOSTS`. NGINX forwards `Host: $host` = whatever the browser sent
= `23.20.14.94`. The `.env` only knew the old EIP `174.129.16.36`.

**Why this design exists:** host-header validation blocks cache-poisoning and
password-reset poisoning attacks where attackers send arbitrary Host headers.

**Fix:** keep environment-specific values in `.env` only:

```bash
grep -E 'APP_URL|CORS_ORIGINS|TRUSTED_HOSTS' .env      # inspect
sed -i 's/OLD_IP/NEW_IP/g' .env                        # replace
sudo systemctl restart valp-backend                    # env is read at startup
```

**Best practice:** when infrastructure changes (new IP, new domain), grep the
whole repo/server for the old value: `grep -r "OLD_VALUE"`. Config should never
be baked into code — this is precisely what makes containerized deploys easy
later (same image, different env).

### 3.3 `{"detail":"Not Found"}` → nginx URI rewriting

**Symptom:** `/health` reached FastAPI but 404'd.

**Concept — `proxy_pass` has two modes:**

```nginx
location /health {
    proxy_pass http://backend;                  # A: no URI → original path sent (/health)
}
location = /health {
    proxy_pass http://backend/api/v1/health;    # B: URI → matched prefix replaced
}
```

With **B**, nginx swaps the location-matched part of the request path for the URI
in `proxy_pass`. Our final config uses `location = /health` (exact match) mapping
to the real API route — a convenience alias only; the canonical endpoint stays
`/api/v1/health`.

**Debugging trick:** the JSON error body tells you which layer answered.
`{"detail": ...}` = FastAPI spoke → networking is fine, look at paths.
HTML nginx error pages = look at connectivity/config.

### 3.4 405 Method Not Allowed → mangled config

**Symptom:** `curl -I /` returned 405 with `allow: GET` and API-style headers.

**What happened:** after several manual edit attempts, `app.conf` had a single
`location / { proxy_pass .../api/v1/health; }` — every request on the site became
a health check. `curl -I` sends HEAD; FastAPI's route allows GET only → 405.

**Lessons:**

1. **Configs belong in the repo**, not typed into servers. Hand-editing under
   fatigue produced three broken variants in one afternoon.
2. **Heredoc pastes over SSH truncate silently** — a long paste lost its tail,
   bash sat at the continuation prompt `>`, Ctrl+C aborted, leaving confusion
   about whether the file changed. Prefer `scp` of a repo file.
3. **`curl -I` sends HEAD**, which many endpoints reject with 405 even when GET
   works. Test with `curl -o /dev/null -w "%{http_code}"`.
4. Failed reloads are safe by design: `systemctl reload nginx` keeps the old
   config in memory if the new one fails `nginx -t`. The site kept serving while
   we fixed the file.

### 3.5 Conflicting server name → AL2023 layout

**Symptom:** `nginx: [warn] conflicting server name "_" on 0.0.0.0:80, ignored`.

**Concept:** two server blocks claimed `server_name _` on port 80. On RHEL-family
systems the default site lives at `/etc/nginx/conf.d/default.conf` — but Amazon
Linux 2023 instead embeds a default server block **directly inside
`/etc/nginx/nginx.conf`**. Deleting a nonexistent `default.conf` did nothing.

**Impact:** low — nginx ignores the duplicate and our block wins — but warnings
hide real problems. Clean fix: comment out the inline default `server {}` in
`nginx.conf`.

**Lesson:** distro layouts differ; verify assumptions with
`sudo grep -Rn 'server_name' /etc/nginx/` instead of following muscle memory.

### 3.6 `Invalid Version` / `ENOSPC` → /tmp is tmpfs

**Symptoms:** `npm install` failed with `npm error Invalid Version:` (empty
version!), then later `ENOSPC: no space left on device` — while `df -h /` showed
15 GB free.

**Root cause:** on AL2023, `/tmp` is a **tmpfs** — a filesystem backed by RAM/swap,
sized ~450 MB on a micro instance. Running `npm install --cache /tmp/npmcache`
wrote hundreds of MB of cache into RAM until it exploded. The truncated/corrupt
cache also explains the bizarre `Invalid Version` error (semver choking on empty
strings from damaged metadata). An earlier near-full 8 GB disk had contributed
partial-install corruption too.

**Fixes applied:**

```bash
# grow disk online (after AWS Console volume modify 8→20GB)
lsblk                                  # confirm new size visible
sudo growpart /dev/nvme0n1 1           # resize partition
sudo xfs_growfs /                      # resize XFS filesystem

# add swap BEFORE next build (build needs more than 1GB RAM)
sudo fallocate -l 2G /swapfile && sudo chmod 600 /swapfile
sudo mkswap /swapfile && sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab

# install with cache on REAL disk
rm -rf node_modules
npm install                            # default cache ~/.npm — never --cache /tmp/...
```

**Best practices:** check `df -h` *and* `df -h /tmp` (they're different
filesystems!); give micro instances swap before any JS build; treat
`Invalid Version` as "corrupted package state", not a version problem.

> Container translation: builds belong outside tmpfs there too, and CI runners
> need explicit disk/RAM sizing — same failure, different costume.

### 3.7 504 vs 502 → Security Group semantics

**Symptom:** locally `curl 127.0.0.1:3000` → 200, publicly → 504 Gateway Time-out.

**Concept — the timeout IS the diagnosis:**

| Response | Meaning | Network layer answer |
|----------|---------|---------------------|
| `502 Bad Gateway` (fast) | upstream actively refused / reset | "service down or wrong port" |
| `504 Gateway Time-out` (slow) | upstream never answered — packets dropped | "firewall blocking" |
| `000` from curl `-m N` | client-side timeout | same as 504 |

SG rules that don't exist cause silent DROP (no RST packet) → nginx waits for its
connect timeout → 504. That's how we knew *before opening the console* that
`valp-prv-sg` lacked a 3000 rule — confirmed via CLI:

```bash
aws ec2 describe-security-groups --group-ids sg-0eb288b2ae6fb781b \
  --query "SecurityGroups[0].IpPermissions[].{Port:FromPort,CIDR:IpRanges[].CidrIp}" --output table

aws ec2 authorize-security-group-ingress --group-id sg-0eb288b2ae6fb781b \
  --protocol tcp --port 3000 --cidr 10.0.1.0/24
```

**Best practice:** every new port a component listens on needs a matching SG rule
in the same change. Write the rule into the runbook *when you add the listener*,
not when something breaks.

### 3.8 Disk & memory sizing

Observed consumption on the app server: OS+packages ≈ 5.3 GB, `node_modules` ≈
400–600 MB, `.next` build output ≈ 200–500 MB, plus logs/backups. An 8 GB volume
was never realistic; 20 GB gives comfortable headroom. The ~912 MB RAM micro
instance cannot run `next build` (multi-hundred-MB RSS spikes) without swap —
with 2 GB swap the build passed.

**Rule of thumb adopted:** minimum 20 GB gp3 + 2 GB swap for any node-building
host; revisit if builds move to CI (preferred long-term).

---

## 4. Standard Operating Procedures

### 4.1 Public IP changed (stop/start without EIP)

1. Local: `~/.ssh/config` → proxy-server `HostName` → new IP
2. App server:
   ```bash
   sudo sed -i 's/<OLD_IP>/<NEW_IP>/g' /opt/platform/backend/.env
   sudo systemctl restart valp-backend
   ```
3. Verify: `curl http://<NEW_IP>/api/v1/health` and `/`
4. Update the current-IP note at top of `DEPLOYMENT.md`

NGINX needs nothing — it uses `server_name _` + private IPs.

### 4.2 Code update / redeploy

```bash
cd /opt/platform && git pull origin main
cd backend && source .venv/bin/activate && pip install -r requirements.txt \
  && alembic upgrade head && sudo systemctl restart valp-backend
cd ../frontend && npm install && npm run build && pm2 restart valp-frontend
```

### 4.3 NGINX config change

Edit `deploy/nginx/app.conf` in the repo → commit → push to server:

```powershell
scp .\deploy\nginx\app.conf proxy-server:/tmp/app.conf
ssh proxy-server "sudo mv /tmp/app.conf /etc/nginx/conf.d/app.conf && sudo chown root:root /etc/nginx/conf.d/app.conf && sudo nginx -t && sudo systemctl reload nginx"
```

Never hand-edit on the server; never paste heredocs over SSH.

### 4.4 Adding a new service/port

Checklist: app binds `0.0.0.0` → SG rule added (source = proxy subnet) → nginx
location/upstream added in repo config → scp + reload → curl test through public IP.

---

## 5. Best Practices Going Forward

**Adopted during this deployment:**

1. Single source of truth for configs (repo), pushed via scp — no server-side edits
2. Environment-specific values only in `.env`; code reads them at startup
3. Security Groups are the firewall; apps bind `0.0.0.0` freely inside
4. Diagnose by response shape: JSON=app layer, HTML=nginx, timeout=network drop
5. Swap before JS builds on small instances; 20 GB minimum disk
6. One PM2 process per name — `pm2 save` AFTER cleanup, or reboot resurrects junk

**Recommended next steps:**

| Item | Why | Effort |
|------|-----|--------|
| Attach EIP when stable | stops the per-restart IP churn entirely | 5 min |
| Move `next build` to CI, ship artifacts | faster deploys, no build load on prod | medium |
| HTTPS via Let's Encrypt (needs domain) | currently plain HTTP | small |
| Structured monitoring (pm2 metrics, journald retention, uptime ping) | detect before users do | medium |
| Containerize (compose: web/api/db) | reproducibility; apply §3.1/§3.6 lessons directly | larger |

---

## 6. Command Reference

```bash
# --- sockets & services ---
sudo ss -tlnp | grep <PORT>            # who listens where (bind address!)
systemctl status valp-backend --no-pager
pm2 status && pm2 logs valp-frontend
sudo journalctl -u valp-backend -f

# --- connectivity ladder (run in order) ---
curl http://127.0.0.1:<PORT>/...       # on target: is the app alive?
curl -m 5 http://10.0.2.50:<PORT>/...  # from proxy: is the path open?
curl -m 5 http://23.20.14.94/...       # from anywhere: full chain

# --- nginx ---
sudo nginx -t && sudo systemctl reload nginx
sudo grep -RE '[0-9]{1,3}(\.[0-9]{1,3}){3}' /etc/nginx/   # hardcoded IPs?
sudo tail -f /var/log/nginx/valp-error.log

# --- disk / memory ---
df -h / ; df -h /tmp                   # DIFFERENT filesystems on AL2023!
free -h                                # swap present?
sudo du -xh --max-depth=1 / | sort -rh | head

# --- AWS CLI ---
aws ec2 describe-security-groups --region us-east-1 \
  --group-ids sg-0eb288b2ae6fb781b \
  --query "SecurityGroups[0].IpPermissions[].{Port:FromPort,CIDR:IpRanges[].CidrIp}" --output table
```

---

*Written 2026-08-21 from the live deployment session. Companion docs:
`DEPLOYMENT.md` (how-to), `TROUBLESHOOTING.md` (quick fixes).*
