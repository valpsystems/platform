# GitHub Actions — Interview Preparation Guide

Complete interview prep for GitHub Actions: core concepts, workflow syntax,
security, and scenario-based Q&As — every answer includes real YAML syntax so
you can write code during the interview.

---

## Table of Contents

1. [Core Concepts Q&A](#part-1-core-concepts-questions--answers)
2. [Syntax Cheat Sheet](#part-2-syntax-cheat-sheet)
3. [Scenario-Based Questions & Answers](#part-3-scenario-based-questions--answers)
4. [Enterprise Patterns Q&A](#part-4-enterprise-patterns-questions--answers)
5. [Security Q&A](#part-5-security-questions--answers)
6. [Rapid-Fire One-Liners](#part-6-rapid-fire-one-liners)
7. [Common Failures & Debugging](#part-7-common-failures--debugging)

---

## Part 1: Core Concepts Questions & Answers

### Q1. What is GitHub Actions? How does it differ from Jenkins?

**A.** GitHub Actions is GitHub's built-in CI/CD engine. Workflows live as YAML
files in `.github/workflows/` and are triggered by GitHub events (push, PR,
schedule, etc.). Unlike Jenkins's installed/served model, Actions runs on
**cloud or self-hosted runners**, is **repository-native** (no separate
server), has **marketplace actions**, and integrates deeply with PRs, secrets,
and environments.

Pros vs Jenkins: zero infrastructure to manage, native GitHub integration,
YAML config in-repo. Cons: more locked to GitHub, marketplace actions are
third-party, debugging limited to logs/artifacts.

---

### Q2. What are the core building blocks?

| Building block | What it is |
|---|---|
| **Workflow** | Top-level YAML file defining automation |
| **Event** | Trigger (push, pull_request, schedule, workflow_dispatch) |
| **Job** | Group of steps running on one runner |
| **Step** | Individual command/action inside a job |
| **Action** | Reusable unit (composite, JS, or Docker) |
| **Runner** | Machine executing jobs (GitHub-hosted or self-hosted) |
| **Runner group / labels** | How jobs select a runner |

---

### Q3. What is the minimum viable workflow?

```yaml
name: CI
on: push

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run a script
        run: echo "Hello from GitHub Actions"
```

---

### Q4. What are events? Name the most used.

**A.** Events trigger workflows. `on:` defines them:
- `push` — branch/commit push
- `pull_request` — PR events (opened, synchronize, closed…)
- `workflow_dispatch` — manual trigger (button / API)
- `schedule` — cron
- `repository_dispatch` — external webhook
- `release`, `issue_comment`, `workflow_run`, `merge_group`…

```yaml
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  workflow_dispatch:
  schedule:
    - cron: '0 2 * * *'
```

---

### Q5. What's the difference between a **workflow**, a **job**, and a **step**?

- **Workflow** = file, `on` triggers, one or more jobs.
- **Job** = sequenced steps + its own runner/OS + own env. Jobs are the unit
  of parallel execution.
- **Step** = one command or action; runs top-to-bottom inside a job; failure by
  default stops subsequent steps (unless `if:` or `continue-on-error`).

---

### Q6. How do jobs communicate data? Jobs don't share a filesystem.

**A.**
1. **Artifacts** — upload/download files (build artifacts, coverage reports).
2. **Outputs** — job `outputs:` map passed via `needs.<job>.outputs.<name>`.
3. **Cache** — dependency caches across runs.
4. **Actions** can persist with `p` paths.

```yaml
jobs:
  build:
    outputs:
      version: ${{ steps.ver.outputs.value }}
    steps:
      - id: ver
        run: echo "value=1.2.3" >> "$GITHUB_OUTPUT"

  deploy:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - run: echo "Deploy version ${{ needs.build.outputs.version }}"
```

---

### Q7. What is an action? Describe the 3 action types.

**A.** A reusable piece of logic:
- **JavaScript action** — Node.js bundled file; fast, runs on runner directly.
- **Composite action** — YAML that groups multiple steps; reusable, no
  packaging. Most common for internal reuse.
- **Docker container action** — full container; slow startup but full env control.

Syntax:
```yaml
uses: actions/checkout@v4
uses: actions/setup-node@v4
  with:
    node-version: '20'
```

You build custom actions in `.github/actions/name/action.yml`.

---

### Q8. What's the difference between a **composite action** and a **reusable workflow**?

| | Composite Action | Reusable Workflow |
|---|---|---|
| Scope | Groups multiple steps into one action | Entire workflow called from another workflow |
| Used via | `uses: ./path/to/action` | `uses: owner/repo/.github/workflows/x.yml@ref` |
| Can contain Jobs | No (steps only) | Yes (jobs) |
| Trigger | none | `on: workflow_call` |

**Reusable workflow (caller):**
```yaml
jobs:
  call:
    uses: valp-org/infra/.github/workflows/deploy.yml@main
    with:
      env: production
    secrets: inherit
```

**Reusable workflow (callee):**
```yaml
on:
  workflow_call:
    inputs:
      env:
        type: string
        required: true
    secrets:
      AWS_ACCESS_KEY_ID:
        required: true
    outputs:
      url:
        value: ${{ jobs.deploy.outputs.url }}

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - run: echo "Deploying to ${{ inputs.env }}"
```

---

### Q9. How do environments work?

**A.** Environments add deployment gates and isolated secrets:
- **Protection rules** — required reviewers, wait timer, deployment branch rules.
- **Environment secrets** — per-env secrets (separate from repo secrets).
- Jobs targeting `environment:` get `environment` URL and concurrency protection.

```yaml
jobs:
  deploy-prod:
    runs-on: ubuntu-latest
    environment:
      name: production
      url: https://valp.example.com
```

Production deploy above would pause for required reviewers if configured.

---

### Q10. What is a runner? GitHub-hosted vs self-hosted?

| | GitHub-hosted | Self-hosted |
|---|---|---|
| Provisioning | Auto (ubuntu/windows/macos) | You provide a VM/container |
| Cost | Included minutes (or paid) | Free (your hardware) |
| Custom hardware/software | Limited | Full control |
| Security | Isolated, short-lived | Persistent — compromise risk; keep isolated |
| Choosing | `runs-on: ubuntu-latest` | `runs-on: [self-hosted, linux, gpu]` |

---

### Q11. How do you pass secrets and why not put them in code?

**A.** Store in Settings → Secrets (repo, env, org levels) and reference via
`${{ secrets.NAME }}`. GitHub masks values in logs. Never hardcode keys in
YAML or committed env files.

```yaml
- run: deploy.sh
  env:
    AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
```

---

### Q12. What is the difference between the `GITHUB_TOKEN` default permissions and fine-grained PATs?

**A.** `GITHUB_TOKEN` is auto-created per run, scoped to the current repo,
expires at job end. Default is read/write; GitHub recommends **read-only** default.

```yaml
permissions:
  contents: read
  pull-requests: write   # enable only what is needed
```

A PAT (personal access token) is a user-level token that can reach other repos —
use it only when cross-repo access is genuinely needed (and prefer fine-grained
PATs / GitHub App tokens).

---

### Q13. How does `if:` deal with a step that fails or succeeds?

**A.** Conditional execution uses context:
- Default: step fails → job fails → subsequent steps skipped.
- `if: always()` — run regardless,
- `if: failure()` — run only on prior failure (cleanup),
- `if: success()` — run only if all prior passed (default),

```yaml
steps:
  - run: ./tests.sh
  - if: failure()
    run: echo "Tests failed"
  - if: always()
    run: echo "Always runs"
```

---

### Q14. What are contexts? Name a few.

**A.** Contexts expose runtime info: `github`, `env`, `job`, `steps`, `runner`,
`secrets`, `inputs`, `needs`, `vars`.

```yaml
- run: echo "Event: ${{ github.event_name }} Branch: ${{ github.ref_name }}"
```

---

### Q15. What is artifact retention and how do you configure it?

**A.** Artifacts store files between runs/jobs. Retention default is 90 days;
set in repo/org settings or via `actions/upload-artifact`.

```yaml
- uses: actions/upload-artifact@v4
  with:
    name: build-output
    path: dist/
    retention-days: 30
```

---

### Q16. What does `continue-on-error` do?

**A.** Marks a step as non-fatal:
```yaml
- run: optional-check
  continue-on-error: true
```
Job continues; a *warning* is shown; job result only fails if the step is the
final status contributor (it becomes neutral). Used for optional checks/lints.

---

### Q17. What is the difference between `GITHUB_OUTPUT`, `GITHUB_ENV`, `GITHUB_STEP_SUMMARY`?

| File | Purpose |
|---|---|
| `GITHUB_OUTPUT` | Set step outputs used later (`${{ steps.x.outputs.y }}`) |
| `GITHUB_ENV` | Set env vars for remaining steps in the job |
| `GITHUB_STEP_SUMMARY` | Write a job summary / fancy report |

```sh
echo "value=foo" >> "$GITHUB_OUTPUT"
echo "MY_VAR=bar" >> "$GITHUB_ENV"
echo "### Deploy summary :rocket:" >> "$GITHUB_STEP_SUMMARY"
```

(`::set-output` is deprecated.)

---

### Q18. What is the workflow file syntax for matrices and concurrency?

**A.**

```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest]
        python: ['3.11', '3.12']
```
- `strategy.matrix` generates one job per combination.
- `strategy.fail-fast: false` lets other matrix jobs continue if one fails.
- `concurrency` prevents overlapping runs of the same group; `cancel-in-progress`
  cancels the older run.

---

## Part 2: Syntax Cheat Sheet

### Full workflow skeleton

```yaml
name: CI/CD
run-name: CI on ${{ github.ref_name }}   # rich run display name
on:
  push:
    branches: [main]
    paths: ['backend/**', '.github/**']  # path filters
  pull_request:

permissions:
  contents: read

env:
  GLOBAL_ENV: hello

jobs:
  backend:
    runs-on: ubuntu-latest
    timeout-minutes: 15
    container:
      image: python:3.12-slim
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
          cache: pip
      - run: pip install -r backend/requirements.txt
      - run: pytest backend/
  deploy:
    needs: [backend]
    if: github.ref == 'refs/heads/main'
    environment: production
    runs-on: ubuntu-latest
    steps:
      - run: ./deploy.sh
        env:
          AWS_CREDS: ${{ secrets.AWS_CREDS }}
```

### Shell on Windows / cross-platform

```yaml
- run: echo "hi"
  shell: bash        # Git Bash on windows runners
- run: dir
  shell: cmd
- run: |
    Write-Host "hi"
  shell: pwsh
```

### Path filters & conditions

```yaml
on:
  pull_request:
    paths:
      - 'frontend/**'
      - '!frontend/**/*.md'   # ignore markdown

jobs:
  deploy:
    if: startsWith(github.head_ref, 'release/')   # only release PRs
```

### Workflow dispatch inputs

```yaml
on:
  workflow_dispatch:
    inputs:
      env:
        description: Target environment
        type: choice
        options: [staging, production]
        default: staging
```
Accessed as `${{ github.event.inputs.env }}`.

### Outputs from a job

```yaml
jobs:
  meta:
    runs-on: ubuntu-latest
    outputs:
      tag: ${{ steps.gen.outputs.tag }}
    steps:
      - id: gen
        run: echo "tag=v1.0-${{ github.run_id }}" >> "$GITHUB_OUTPUT"
```

### Cache

```yaml
- uses: actions/cache@v4
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
    restore-keys: |
      ${{ runner.os }}-pip-
```

### Service containers

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_PASSWORD: postgres
        ports:
          - 5432:5432
    steps:
      - run: pytest backend/        # tests connect to localhost:5432
```

---

## Part 3: Scenario-Based Questions & Answers

### S1. "Our backend pipeline builds, tests, and deploys. It takes 20 min. How do you speed it up?"

**A.**
1. **Caching** dependencies (`actions/cache`, setup-tool caching).
2. **Matrix split** tests and linters in parallel jobs.
3. **Parallel jobs** for stages that don't depend on each other.
4. **Build only on source changes** (`paths:` filters).
5. **Composite actions / reusable workflows** to remove duplicated runs.
6. Upgrade runner image / use larger runners for CPU-heavy builds.
7. Only run full test on main; run fast subset on PR.

---

### S2. "Two pushes to main happened quickly; the second one waits or cancels the first. What do you do?"

**A.** Use `concurrency` — group per branch, cancel the stale one:

```yaml
concurrency:
  group: ci-${{ github.ref }}
  cancel-in-progress: true
```
For **deploy**, set `cancel-in-progress: false` so the last-good deploy always
finishes and you don't lose a running release mid-flight.

---

### S3. "You need to test the same app against Node 18, 20, 22 and both ubuntu + windows."

**A.** Matrix:

```yaml
strategy:
  matrix:
    os: [ubuntu-latest, windows-latest]
    node: [18, 20, 22]
```
16 jobs total (2x3). Use `fail-fast: false` so a Windows-only bug doesn't hide
Linux results. Run on `${{ matrix.os }}`.

---

### S4. "Production deploys must require human approval; staging doesn't."

**A.** Use **environments**. Create `production` env with required reviewers;
reference it in the deploy job:

```yaml
jobs:
  deploy:
    environment:
      name: production
```
Job steps won't run until reviewers approve. `staging` env has no reviewers, so
it deploys automatically. Environment secrets keep env-specific values separate.

---

### S5. "Someone opened a PR from a fork; you don't want secrets available to fork PRs."

**A.** Fork PRs from public repos cannot access secrets (GitHub bakes this in
unless `pull_request_target` misused). Rules to remember:
- Prefer `pull_request` (safe) for CI on the fork's code.
- `pull_request_target` runs on the **base** branch with secrets — security risk;
  never run untrusted build steps from PR branches with it. Validate and check out
  the PR with `actions/checkout@v4` into a trusted, pinned action only.

---

### S6. "A workflow run failed only on Windows; Linux passed. How do you debug?"

**A.**
1. Read logs; add `shell: bash` for consistent behavior or fix env-specific
   steps.
2. Re-run with debug diagnostics: enable **debug logging** by setting secret
   `ACTIONS_STEP_DEBUG=true` and `ACTIONS_RUNNER_DEBUG=true`.
3. Reproduce on a self-hosted or local runner; or push a matrix including only
   Windows with extra diagnostic steps.
4. Use `actions/upload-artifact` to capture test reports + coredumps from the
   failing run

---

### S7. "You need two teams each with their own build, triggered on different paths, but sharing one deploy step."

**A.** Modular workflows: two CI workflows (backend/frontend) with `paths` filters,
plus one centrally owned reusable deploy workflow with `workflow_call` and inputs:

```yaml
# .github/workflows/deploy.yml
on:
  workflow_call:
    inputs:
      service:
        type: string
        required: true

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - run: deploy --service ${{ inputs.service }}
```
Callers: `uses: valp-org/infra/.github/workflows/deploy.yml@main with: service: backend`.

---

### S8. "Your deploy step needs the version/number produced earlier in the build."

**A.** Outputs chain:

```yaml
jobs:
  build:
    outputs:
      image: ${{ steps.tag.outputs.image }}
    steps:
      - id: tag
        run: |
          echo "image=valp/backend:${{ github.sha }}" >> "$GITHUB_OUTPUT"

  deploy:
    needs: build
    steps:
      - run: docker pull ${{ needs.build.outputs.image }}
```

---

### S9. "You must run a workflow only after another workflow succeeds."

**A.** Two approaches:
1. `workflow_run` trigger (separate workflow after target completes):
```yaml
on:
  workflow_run:
    workflows: ["CI"]
    types: [completed]
    branches: [main]
```
2. Within one workflow use `needs:`.

Only option 1 works across **different** workflow files; add an `if: github.event.workflow_run.conclusion == 'success'` guard.

---

### S10. "A scheduled pipeline runs nightly but you occasionally want it without waiting."

**A.** Add `workflow_dispatch` to the same workflow:
```yaml
on:
  schedule:
    - cron: '0 2 * * 1-5'   # weekdays 02:00 UTC
  workflow_dispatch:
```
Manual run via Actions tab → "Run workflow" (or `gh workflow run nightly.yml`).

---

### S11. "You use a self-hosted runner in production. What security practices do you apply?"

**A.**
- Use **runner groups** restricted to the repo/org that needs it.
- Keep runners in an isolated network segment; avoid privileged cloud creds on
  them — use OIDC federation or short-lived tokens.
- No public forks on org-accessible self-hosted runners (classic supply-chain
  attack vector) — require explicit fork handling or use GitHub-hosted for PRs.
- Auto-update runner software, pin actions, regular OS patching, minimal packages.

---

### S12. "How do you implement a blue-green / canary deployment with GitHub Actions?"

**A.**
1. Build & push image (tag `sha`).
2. Deploy green (new) to a different service/ASG target group; wait for health
   check.
3. Smoke test.
4. Switch traffic (weight or target group swap).
5. Rollback = route back to blue/old on failure.

High level:
```yaml
deploy-green:  steps: [tag, push, docker deploy green]
health-check:  needs: deploy-green  run: curl green-alb
route-traffic: needs: health-check  run: update target group weights
# on failure: rollback job routes 100% back to blue
```

---

### S13. "Your repo README says works for Node 18. Your Action uses degraded Node."

**A.** The action runtime is **separate** from the app runtime. GitHub-hosted
runners bundle several Action versions; set your needed one explicitly:
```yaml
uses: actions/setup-node@v5
with:
  node-version: 20
```
For custom **JavaScript actions**, the runner hosts specific Node versions; if
too old for your action runtime, add `runs-on: node20` or check `runs.using` in
`action.yml`. Set `runtime: node20` to raise the action runtime version.

---

### S14. "Terraform plan output must appear as a PR comment."

**A.** Use the `hashicorp/terraform-github-actions` or store plan file:
```yaml
- name: Terraform Plan
  id: plan
  run: terraform plan -no-color -out=tfplan 2>&1 | tee plan.txt
- uses: actions/upload-artifact@v4
  with:
    name: tfplan
    path: tfplan
```
A separate step can post `plan.txt` via an action (e.g., `terraform-plan-commenter`)
with `pull-requests: write` permission. Review the plan, manual approve, then
`terraform apply tfplan`.

---

### S15. "Nightly E2E fails intermittently (flaky). How do you handle flaky tests in CI?"

**A.**
1. **Retry once on known-flaky** step (`if: failure()` + rerun) but track them
   as separate metric.
2. Upload reports + artifacts; link issues when flake detected.
3. Run flaky suite separately / `continue-on-error` with a #[flaky] label,
   investigate and remove.
4. Never silently ignore — flaky tests are bugs in test design: quarantine and
   fix root cause (wait (not sleep), unique data, idempotency).

---

## Part 4: Enterprise Patterns Questions & Answers

### Q19. What are **composite actions** and their `action.yml` structure?

```yaml
name: 'Setup Node & Install'
description: 'Setup node and install deps'
inputs:
  node-version:
    required: true
runs:
  using: 'composite'
  steps:
    - uses: actions/setup-node@v5
      with:
        node-version: ${{ inputs.node-version }}
    - shell: bash
      run: npm ci
```

Note: `shell: bash` is mandatory on composite steps (no default shell).

### Q20. How do you limit permissions and avoid privilege creep?

```yaml
permissions:
  contents: read
  packages: read
  statuses: none
```
"Least privilege": explicit, minimal scopes; avoid default write `GITHUB_TOKEN`;
use environment secrets per deploy; OIDC short-lived cloud creds.

### Q21. What is **OIDC** and why prefer it over long-lived cloud keys?

**A.** GitHub issues an OIDC ID token proving a specific workflow/ref; cloud
(IAM) trusts that token to mint short-lived credentials. No static keys stored:
```yaml
permissions:
  id-token: write
  contents: read
steps:
  - uses: aws-actions/configure-aws-credentials@v4
    with:
      role-to-assume: arn:aws:iam::123:role/github-oidc
      aws-region: us-east-1
```
Advantages: no secret rotation, revocable, scoped, auditable.

### Q22. How do you version/reuse a set of workflows across many repos?

**A.** Publish a central repo of:
- **Reusable workflows** referenced as `owner/repo/.github/workflows/x.yml@v1.2.0`
  (pinned tag).
- **Composite actions** published in the marketplace / internal registry.
- Enforce via renovate/dependabot version bumps; document usage + migration
  notes. Use a service account/GitHub App for cross-org access if needed.

### Q23. What is **matrix `include`/`exclude`** and when useful?

```yaml
strategy:
  matrix:
    os: [ubuntu-latest, windows-latest]
    include:
      - os: ubuntu-latest
        extra: lint
      - os: ubuntu-latest
        node: 20
    exclude:
      - os: windows-latest
        node: 18
```
Lets you add special cases (run lint) or drop combos that fail for known reasons
while keeping the matrix expressive.

---

## Part 5: Security Questions & Answers

### Q24. How would you prevent secret leakage in logs?

**A.**
- Use secrets; never echo them; mask via `${{ secrets.X }}` automatically.
- `::add-mask::` for values that aren't stored as secrets:
```sh
echo '::add-mask::my-common-token'
```
- Keep debug logging off by default (`ACTIONS_STEP_DEBUG`).
- Rotate immediately if leaked; audit `settings/security` & GitHub digests.

### Q25. What is **script injection**? How do you avoid it?

**A.** When attacker-controlled data (PR title, branch name, issue body) is
interpolated directly into `run:`:
```yaml
# BAD: attacker-controlled
run: echo "PR title: ${{ github.event.pull_request.title }}"
```
Mitigations: always pass data via env, never inline:
```yaml
env:
  TITLE: ${{ github.event.pull_request.title }}
run: echo "PR title: $TITLE"
```

### Q26. Scenario: "Fork PR workflows" — the difference between `pull_request` and `pull_request_target`?

- `pull_request` runs on fork's merged (test) code, no secrets — for general CI.
- `pull_request_target` runs on the base branch's workflow (with repo secrets);
  only use it if you check out and build the PR, and **pin** the steps; must
  never trust code/actions from the PR head in secrets context.

### Q27. How do you handle supply-chain (dependency/action) risk?

**A.**
- **Pin actions by SHA** not just tag:
  `uses: actions/checkout@a81bbbf8298c0fa03ea29cdc473d45769f953675`
- Use Dependabot/renovate for actions + npm/pip deps.
- Restrict marketplace action sources (org connector allowlist).
- SBOM + `npm audit`/`osv-scanner`; sign artifacts with [sigstore]/cosign.

---

## Part 6: Rapid-Fire One-Liners

| Question | Short answer |
|---|---|
| Where do workflows live? | `.github/workflows/*.yml` |
| Trigger types? | push, pull_request, schedule, workflow_dispatch, workflow_run… |
| Runners? | GitHub-hosted or self-hosted, `runs-on` |
| Jobs vs steps? | Job = runner unit; step = command inside job |
| How do jobs share data? | artifacts, outputs, caches, service containers |
| `needs:`? | Orders jobs / waits for completion |
| `if:`? | Conditional step/job execution |
| `continue-on-error`? | Step fails but job continues |
| `strategy.matrix`? | Parallel runs over os/version combos |
| `concurrency`? | Prevent parallel duplicate runs (group + cancel) |
| `$GITHUB_OUTPUT`? | Set step outputs (`echo 'x=y' >> "$GITHUB_OUTPUT"`) |
| `$GITHUB_ENV`? | Set env for remaining steps |
| Artifacts vs cache? | Artifacts persist across runs (reports); cache stores deps (fast restore) |
| Default secrets permission? | Read/write; recommended to tighten to read |
| `GITHUB_TOKEN`? | Per-run, short-lived, scoped token |
| Reusable workflows? | Callable via `uses: owner/repo/.github/workflows/x.yml@ref` |
| Composite actions? | Reusable YAML steps packed as an action |
| Environments? | Gates (reviewers), isolated secrets, deployment tracking |
| workflow_dispatch inputs? | Manual parameters for a run |
| Path filters? | `paths:` / `paths-ignore:` limit trigger scope |
| Debug logging? | Secrets `ACTIONS_RUNNER_DEBUG=true`, `ACTIONS_STEP_DEBUG=true` |
| OIDC? | Trusted short-lived cloud creds via ID token |
| `run: echo "$RANDOM"`? | Use random via env context to stay safe |

---

## Part 7: Common Failures & Debugging

| Symptom | Cause / fix |
|---|---|
| Job fails immediately with "runner not found" | No runner matches `runs-on` labels (self-hosted group) |
| "Error: Permission to ... denied" | Wrong `permissions:` or token scope; bump only needed scopes |
| Fork PR doesn't run secrets | By design; use `pull_request`, avoid secrets for untrusted PRs |
| `needs.<job>` empty | Output name typo or step id missing |
| Long-running step killed | `timeout-minutes` / GitHub runner hard limits |
| "Only one ... can run at a time" | Concurrent deploy — use `concurrency` group with `cancel-in-progress: true` |
| Plan applies but workflow times out | Runner timeout; split steps, use larger runner or self-hosted |
| Action `deprecated` node12 warnings | Pin actions to v4/v5, action runtime node20, update refs |
| Cache miss every run | Key mismatch; keep keys derived from lockfile `hashFiles` |
| Secrets visible in logs | Never echo; use `::add-mask::`, rotate immediately |
| Windows paths/line endings break runs | Set `shell: bash`/`checkout` lf line endings, `core.autocrlf` setting |

---

*Practice: build a 2-job pipeline with outputs+artifacts, add a matrix,
protect production behind an environment with reviewers, pin a composite action,
and switch cloud creds to OIDC. These five demos cover the majority of
senior/DevOps interview questions.*
Demo 1 — 2-job pipeline: outputs + artifacts (03-outputs-artifacts.yml)
- Job build: checkout → setup Python → pip install, build a wheel (pip wheel), then set outputs (version=$GITHUB_RUN_NUMBER) and actions/upload-artifact the wheel.
- Job deploy: needs: build, print ${{ needs.build.outputs.version }}, actions/download-artifact the wheel.
Verify: go to Actions → build job shows in deploy the version number; artifact downloader in the Actions UI.
Demo 2 — Matrix (04-test-matrix.yml)
- Extend your existing matrix: python: [3.11, 3.12, 3.13] × os: [ubuntu-latest, windows-latest], each running pytest backend/ and uploading coverage as an artifact.
- Keep fail-fast: false.
Verify: 6 parallel jobs in the run, distributes quickly, all pass.
Demo 3 — Production protected by reviewers (05-environment-gate.yml)
- In repo Settings → Environments → New environment production → enable Required reviewers → add yourself.
- Deploy job uses:
environment:
  name: production
with if: github.ref == 'refs/heads/main'.
Verify: your apply/PR-triggered run shows "Waiting" — approve in Actions UI and it continues. This is the #1 senior/interview demo.
Demo 4 — Pin a composite action (.github/actions/setup-python-dep/action.yml)
- Bundle setup-python + cache + pip install -r backend/requirements.txt into one composite action (remember shell: bash is required).
- Replace the repeated 3-step blocks in 02-backend-ci.yml with:
- uses: ./.github/actions/setup-python-dep
  with:
    python-version: ${{ env.PYTHON_VERSION }}
Verify: run lint/typecheck — many fewer steps, both jobs byte-identical setup.
Demo 5 — Switch cloud creds to OIDC (06-oidc.yml)
This needs a real AWS account (can't fake it locally):
1. Create an IAM OIDC provider for token.actions.githubusercontent.com (thumbprint) + an IAM role trusting it, Condition: StringEquals on sub = your repo:VALPSYSTEMS/*.
2. Workflow:
permissions:
  id-token: write
  contents: read
steps:
  - uses: aws-actions/configure-aws-credentials@v4
    with:
      role-to-assume: arn:aws:iam::<ACCT>:role/github-oidc
      aws-region: us-east-1
  - run: aws sts get-caller-identity
Verify: get-caller-identity returns the assumed role, no static keys anywhere.