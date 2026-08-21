# VALP SYSTEMS — Ops & Debugging Notes

Hard-won notes from the first deployment (Aug 2026). Apply these when deploying
the frontend **and** when we move to containerized applications later.

---

## 1. Golden Rules

| Rule | Why |
|------|-----|
| Services must bind `0.0.0.0`, never `127.0.0.1`, if anything external proxies to them | uvicorn on `127.0.0.1:8080` caused 502 — nginx reached the box but nothing listened on the VPC interface |
| Security comes from Security Groups, not bind addresses | `0.0.0.0` + sg-app allowing only sg-proxy = same protection |
| All environment-specific values live in `.env` / env vars — zero hardcoding | Public IP changed twice already; only `.env` edits were needed |
| Verify actual IPs with `hostname -I` — don't trust docs/memory | App server had TWO private IPs (`10.0.2.50`, `10.0.2.236`) |

## 2. Symptom → Cause → Fix (learned the hard way)

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| `502 Bad Gateway` | Upstream unreachable: wrong IP, service down, or bound to `127.0.0.1` | From proxy: `curl -m 5 http://<APP_IP>:<PORT>/...`; on target: `sudo ss -tlnp \| grep <PORT>` |
| curl *times out* | Security Group blocking | Add inbound rule (e.g., sg-app ← sg-proxy on 8080/3000) |
| curl *connection refused* | Service not running or wrong port | `systemctl status <svc>`, check port with `ss -tlnp` |
| `Invalid host header` | FastAPI `TrustedHostMiddleware` — Host not in `TRUSTED_HOSTS` | Update `.env`: `TRUSTED_HOSTS`, `CORS_ORIGINS`, `APP_URL`, restart service |
| `{"detail":"Not Found"}` | Reached FastAPI but wrong path (e.g., `/health` instead of `/api/v1/health`) | Fix nginx `proxy_pass` URI rewriting |
| `405 Method Not Allowed` on `/` | Everything routed to an API GET-only endpoint — nginx routing broken | Restore correct `location` blocks (`curl -I` sends HEAD; test with plain `curl`) |
| `conflicting server name "_"` warning | Duplicate `server_name _` on :80 — on AL2023 it's the inline default block **inside `nginx.conf`**, not `conf.d/default.conf` | Comment out the default `server {}` in `/etc/nginx/nginx.conf` |
| `No space left on device` during dnf/pip/npm | Small EBS volume fills up | `df -h /` → clean caches → grow EBS (`growpart` + `xfs_growfs`) |

## 3. Public IP Change Checklist (auto-assigned IP changes every stop/start)

1. Local SSH config: `~/.ssh/config` → proxy-server `HostName`
2. App server `/opt/platform/backend/.env` → replace old IP in
   `APP_URL`, `CORS_ORIGINS`, `TRUSTED_HOSTS` → `sudo systemctl restart valp-backend`
3. Browser/curl sanity: `curl http://<NEW_IP>/api/v1/health`

NGINX needs **no** changes — it uses `server_name _` + private IPs only.

## 4. NGINX Gotchas

- **`proxy_pass` URI matters**: no trailing URI = path passed as-is;
  with a URI (`.../api/v1/health`) the matched location prefix is replaced.
- `limit_req_zone` must be at **http context** — top of a `conf.d/*.conf` file
  works (it's included inside `http{}`); inside `server{}` it fails.
- Keep one source of truth for the config; avoid hand-editing fragments —
  paste the whole file (see `DEPLOYMENT.md` §7).

## 5. Cheat Sheet

```bash
# What is listening where?
sudo ss -tlnp | grep <PORT>

# Any hardcoded IPs in configs?
sudo grep -RE '[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}' /etc/nginx/

# End-to-end tests (GET, not HEAD)
curl -m 5 http://<PUBLIC_IP>/api/v1/health     # API
curl -m 5 http://<PUBLIC_IP>/health            # shortcut
curl -m 5 -o /dev/null -w "%{http_code}\n" http://<PUBLIC_IP>/   # frontend

# Service logs
sudo journalctl -u valp-backend -f --no-pager
pm2 logs valp-frontend
```

## 6. Carrying These Lessons Into Container Deployments

When we wrap services in Docker:

- **Containers must listen on `0.0.0.0`** inside the container (e.g., `uvicorn --host 0.0.0.0`).
  `EXPOSE`/`-p` publishing does NOT change the app's bind address.
- Same failure modes appear as today: 502 (container not listening / wrong port),
  timeouts (SG), host-header rejections (`TRUSTED_HOSTS` env must include the proxy/public host).
- Config stays env-driven: pass `.env` via compose `env_file` / `-e` flags —
  rebuild-free IP changes, exactly like today.
- Health checks: reuse `/api/v1/health` as the Docker/compose `healthcheck`;
  nginx upstreams can then use it too.
- One network namespace lesson from today: "localhost" means different things —
  between containers use service names, from host to container use published ports,
  never assume `127.0.0.1` crosses that boundary.
