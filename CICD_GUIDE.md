# VALP SYSTEMS — CI/CD Learning Guide

A complete, hands-on guide to learning GitHub Actions CI/CD using the VALP SYSTEMS
project. Every concept is explained from scratch — what it is, why it matters, how
it works — then demonstrated with real workflow code that runs against our FastAPI
backend and Next.js frontend. All examples are for reference — you will create
your own workflow files as you practice.

> **Prerequisites:** Basic Git knowledge, GitHub account, the VALP SYSTEMS repo
> cloned locally. No prior CI/CD experience required.

> **Target:** By the end of this guide you will understand and be able to implement
> enterprise-grade GitHub Actions pipelines with concurrency, caching, matrix builds,
> composite actions, reusable workflows, self-hosted runners, OIDC authentication,
> and deployment gates.

---

## Table of Contents

1. [What is CI/CD?](#1-what-is-cicd)
2. [GitHub Actions Architecture](#2-github-actions-architecture)
3. [Workflow File Anatomy](#3-workflow-file-anatomy)
4. [Lesson 01 — Workflow Basics](#4-lesson-01--workflow-basics)
5. [Lesson 02 — Backend CI Pipeline](#5-lesson-02--backend-ci-pipeline)
6. [Lesson 03 — Frontend CI Pipeline](#6-lesson-03--frontend-ci-pipeline)
7. [Lesson 04 — Composite Actions](#7-lesson-04--composite-actions)
8. [Lesson 05 — Reusable Workflows](#8-lesson-05--reusable-workflows)
9. [Lesson 06 — Deployment Pipeline](#9-lesson-06--deployment-pipeline)
10. [Lesson 07 — Full Orchestration](#10-lesson-07--full-orchestration)
11. [Enterprise Patterns Reference](#11-enterprise-patterns-reference)
12. [Self-Hosted Runners](#12-self-hosted-runners)
13. [Configuration Reference](#13-configuration-reference)
14. [Learning Checklist](#14-learning-checklist)

---

## 1. What is CI/CD?

### 1.1 Definitions

**CI (Continuous Integration)** is the practice of automatically building and
testing code every time a developer pushes a change. Instead of manually running
`pytest` and `npm run build` on your laptop before merging, a server does it for
you — every single time — in a clean, reproducible environment.

**CD (Continuous Delivery)** extends CI by automatically preparing release
artifacts (Docker images, build folders, deployment packages) after tests pass.

**CD (Continuous Deployment)** goes one step further: if all checks pass, the
change is deployed to production automatically — no human clicks required.

```
Developer pushes code
        |
        v
+------------------- CI -------------------+
|  Lint -> Type Check -> Test -> Build     |
+-------------------------------------------+
        | (all pass)
        v
+------------------- CD -------------------+
|  Package -> Deploy to Staging -> Approve |
+-------------------------------------------+
        | (approved)
        v
   Deploy to Production
```

### 1.2 Why CI/CD Matters

| Without CI/CD | With CI/CD |
|---------------|------------|
| "Works on my machine" bugs reach production | Tests catch bugs before merge |
| Manual deployment takes 30+ minutes, error-prone | Deployment takes 5 minutes, repeatable |
| No one knows if the code is shippable | Green check = shippable |
| Fear of deploying on Fridays | Deploy any time, any day |
| Security scans forgotten | Automated security gates |

### 1.3 What We Will Build

By the end of this guide, our pipeline will look like this:

```
+-----------------------------------------------------------------------+
|                     VALP SYSTEMS CI/CD Pipeline                        |
+-----------------------------------------------------------------------+
|                                                                       |
|   Push/PR ---> Backend Lint ---+                                      |
|                Frontend Lint --+---> Backend Test (3.11, 3.12, 3.13) |
|                Type Check ------         |                             |
|                Security Scan ----------- |                             |
|                                         v                             |
|                               Frontend Build                          |
|                                         |                             |
|                               +---------+---------+                   |
|                               v                   v                   |
|                      Deploy Staging         Deploy Production         |
|                      (develop branch)       (main branch + approval) |
|                                                                       |
+-----------------------------------------------------------------------+
```

---

## 2. GitHub Actions Architecture

### 2.1 How GitHub Actions Works

GitHub Actions is a CI/CD platform built into GitHub. When you push code,
GitHub spins up a virtual machine (called a **runner**), clones your repo,
and executes the steps you defined in YAML workflow files.

```
+-------------------------------------------------------------------+
|                    GitHub Actions Architecture                     |
+-------------------------------------------------------------------+
|                                                                    |
|  GitHub Repository                                                 |
|  +-- .github/workflows/           <- Workflow definitions (YAML)  |
|  +-- .github/actions/             <- Custom actions (optional)     |
|                                                                    |
|         | trigger (push, PR, schedule, manual)                     |
|         v                                                          |
|  +----------------------------------------------+                 |
|  |  Runner (Virtual Machine)                    |                 |
|  |  +-- Ubuntu / Windows / macOS                |                 |
|  |  +-- GitHub-hosted or Self-hosted            |                 |
|  |  +-- Fresh VM for each job                   |                 |
|  |  +-- Executes steps sequentially             |                 |
|  +----------------------------------------------+                 |
|         |                                                          |
|         v                                                          |
|  +----------------------------------------------+                 |
|  |  Actions (Reusable packages)                 |                 |
|  |  +-- actions/checkout@v4                     |                 |
|  |  +-- actions/setup-python@v5                 |                 |
|  |  +-- actions/cache@v4                        |                 |
|  |  +-- Custom composite actions                |                 |
|  +----------------------------------------------+                 |
|                                                                    |
+-------------------------------------------------------------------+
```

### 2.2 Key Terminology

| Term | What It Is | Analogy |
|------|-----------|---------|
| **Workflow** | An automated process defined in a YAML file | A recipe card |
| **Job** | A group of steps that run on the same runner | A station in a factory |
| **Step** | A single task (run a command or use an action) | A single instruction |
| **Action** | A reusable package of steps | A tool you pick up |
| **Runner** | The VM that executes your jobs | The factory worker |
| **Trigger** | The event that starts the workflow | The button you press |
| **Matrix** | Running the same job with different parameters | Testing on multiple devices |
| **Artifact** | Files passed between jobs or saved after a run | A package you ship |

### 2.3 Free Tier Limits

GitHub Actions provides **2,000 minutes/month** for free (public repos are
unlimited). A typical workflow run for our project takes 3-8 minutes.

| Runner Type | Free Minutes | Cost After |
|-------------|-------------|------------|
| Linux (ubuntu-latest) | 2,000 min/month | $0.008/min |
| Windows | 2,000 min/month (counts 2x) | $0.016/min |
| macOS | 2,000 min/month (counts 10x) | $0.08/min |

---

## 3. Workflow File Anatomy

Every workflow file lives in `.github/workflows/` and is a YAML file.
Here is the skeleton with every possible section explained:

```yaml
# =============================================================================
# Workflow Name — displayed in the GitHub Actions tab
# =============================================================================
name: "My Workflow"

# =============================================================================
# TRIGGERS — When should this workflow run?
# =============================================================================
on:
  # push: When code is pushed to these branches
  push:
    branches: [main, develop]
    paths: ["backend/**"]  # Only if files in backend/ changed

  # pull_request: When a PR targets these branches
  pull_request:
    branches: [main]

  # schedule: Cron-based (runs on default branch only)
  schedule:
    - cron: "0 2 * * 1"  # Every Monday at 2:00 AM UTC

  # workflow_dispatch: Manual trigger from GitHub UI
  workflow_dispatch:
    inputs:
      environment:
        description: "Target environment"
        required: true
        type: choice
        options: [staging, production]

  # workflow_call: Can be called from other workflows
  workflow_call:
    inputs:
      python-version:
        type: string
        default: "3.13"

# =============================================================================
# ENV — Global environment variables (available to all jobs)
# =============================================================================
env:
  APP_NAME: "VALP-SYSTEMS"
  PYTHON_VERSION: "3.13"

# =============================================================================
# JOBS — The main units of work
# =============================================================================
jobs:

  # -------------------------------------------------------------------------
  # JOB: A named unit of work
  # -------------------------------------------------------------------------
  my-job:
    # runs-on: The VM to use
    runs-on: ubuntu-latest

    # environment: GitHub environment (for protection rules)
    environment:
      name: production
      url: https://valpsystems.com

    # permissions: Fine-grained access control
    permissions:
      contents: read
      id-token: write  # For OIDC

    # outputs: Values this job exposes to other jobs
    outputs:
      build-url: ${{ steps.deploy.outputs.url }}

    # strategy: Matrix configuration
    strategy:
      matrix:
        python-version: ["3.11", "3.12", "3.13"]
      fail-fast: false

    # concurrency: Prevent duplicate runs
    concurrency:
      group: my-job-${{ github.ref }}
      cancel-in-progress: true

    # services: Docker containers to run alongside
    services:
      postgres:
        image: postgres:15
        ports: ["5432:5432"]

    steps:
      - name: "Checkout"
        uses: actions/checkout@v4

      - name: "Run tests"
        run: pytest tests/

      - name: "Setup Python"
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
```

### 3.1 Understanding the `on:` Triggers

| Trigger | When It Fires | Use Case |
|---------|--------------|----------|
| `push` | Code pushed to a branch | CI on every commit |
| `pull_request` | PR opened/updated/merged | Validate before merge |
| `schedule` | Cron schedule | Nightly security scans |
| `workflow_dispatch` | Manual button click | Deployment, hotfixes |
| `workflow_call` | Called by another workflow | Reusable CI logic |

### 3.2 Understanding `steps` Execution

Steps within a job run **sequentially** (one after another). Jobs run
**in parallel** by default (unless connected with `needs:`).

```
Job A: [Step 1] -> [Step 2] -> [Step 3]     <- runs in parallel with Job B
Job B: [Step 1] -> [Step 2]                  <- runs in parallel with Job A
Job C: [Step 1]                              <- waits for Job A + Job B (needs:)
```

---

## 4. Lesson 01 — Workflow Basics

**Concepts covered:** Triggers, jobs, steps, actions, outputs, conditions,
matrix strategy.

### 4.1 What We Are Learning

This lesson teaches the absolute fundamentals. You will learn how to write
a workflow file, define triggers, run commands, pass data between steps,
and use conditions.

### 4.2 The Complete Workflow

```yaml
# .github/workflows/01-basic-ci.yml

name: "Lesson 01 - Workflow Basics"

# TRIGGER: This workflow runs on push to main/develop AND on pull requests
# to main. It can also be triggered manually from the Actions tab.
on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]
  workflow_dispatch:

# ENV: Global variables. These are available in ALL jobs and ALL steps.
# Access them with ${{ env.APP_NAME }}
env:
  APP_NAME: "VALP-SYSTEMS"
  PYTHON_VERSION: "3.13"

# JOBS: Each job runs on its own fresh VM. Jobs run in PARALLEL by default.
jobs:

  # -------------------------------------------------------------------------
  # JOB 1: Demonstrates basics — checkout, commands, outputs
  # -------------------------------------------------------------------------
  hello-world:
    # runs-on: The operating system of the runner VM.
    # Options: ubuntu-latest, ubuntu-22.04, windows-latest, macos-latest
    runs-on: ubuntu-latest

    steps:
      # STEP: actions/checkout clones your repo into the runner VM.
      # Without this, the runner has no code to work with.
      # @v4 means "use version 4" (pinned for stability).
      - name: "Checkout repository"
        uses: actions/checkout@v4

      # STEP: Run a shell command.
      # 'run:' executes bash (on Linux/Mac) or PowerShell (on Windows).
      # The '|' allows multi-line commands.
      - name: "Print environment info"
        run: |
          echo "App Name: ${{ env.APP_NAME }}"
          echo "Runner OS: ${{ runner.os }}"
          echo "Runner Arch: ${{ runner.arch }}"
          echo "GitHub Ref: ${{ github.ref }}"
          echo "Triggered by: ${{ github.event_name }}"

      # STEP: Setting outputs.
      # GitHub Actions allows steps to produce outputs that other steps/jobs
      # can read. You write to $GITHUB_OUTPUT file.
      - name: "Set a variable"
        id: my-output  # 'id' is REQUIRED to reference outputs later
        run: |
          echo "build_number=$GITHUB_RUN_NUMBER" >> "$GITHUB_OUTPUT"
          echo "timestamp=$(date -u +%Y-%m-%dT%H:%M:%SZ)" >> "$GITHUB_OUTPUT"

      # STEP: Using outputs from a previous step.
      # Reference with: steps.<id>.outputs.<name>
      - name: "Use output from previous step"
        run: |
          echo "Build number: ${{ steps.my-output.outputs.build_number }}"
          echo "Timestamp: ${{ steps.my-output.outputs.timestamp }}"

  # -------------------------------------------------------------------------
  # JOB 2: Conditional execution with 'if:'
  # -------------------------------------------------------------------------
  conditional-job:
    runs-on: ubuntu-latest
    steps:
      - name: "Checkout"
        uses: actions/checkout@v4

      # if: Controls whether this step runs.
      # Common expressions:
      #   github.event_name == 'push'        -> only on push
      #   github.ref == 'refs/heads/main'    -> only on main branch
      #   github.event_name == 'pull_request' -> only on PRs
      - name: "Only on push to main"
        if: github.event_name == 'push' && github.ref == 'refs/heads/main'
        run: echo "This only runs on push to main branch"

      - name: "Only on PR"
        if: github.event_name == 'pull_request'
        run: echo "This only runs on pull requests"

  # -------------------------------------------------------------------------
  # JOB 3: Matrix strategy — test across multiple versions in parallel
  # -------------------------------------------------------------------------
  matrix-example:
    runs-on: ubuntu-latest

    # STRATEGY: Define variables that create multiple parallel jobs.
    # With 3 python versions, this creates 3 parallel jobs.
    strategy:
      matrix:
        python-version: ["3.11", "3.12", "3.13"]
      # fail-fast: false means if one job fails, the others keep running.
      # Default is true (cancel all on first failure).
      fail-fast: false

    steps:
      - name: "Checkout"
        uses: actions/checkout@v4

      # Use matrix variable: ${{ matrix.python-version }}
      # This is how each parallel job gets a different Python version.
      - name: "Setup Python ${{ matrix.python-version }}"
        uses: actions/setup-python@v5
        with:
          # 'with:' provides inputs to an action.
          # setup-python@v5 needs to know which version to install.
          python-version: ${{ matrix.python-version }}

      - name: "Python version check"
        run: python --version
```

### 4.3 Key Concepts Explained

**`uses:` vs `run:`**
- `uses:` runs a pre-built action (a package from GitHub Marketplace or a local path)
- `run:` executes a shell command directly on the runner

**`id:` on Steps**
- Every step can have an `id` (a short string identifier)
- Without an `id`, you cannot reference that step's outputs later
- The `id` is used in `steps.<id>.outputs.<name>` and `steps.<id>.outcome`

**GitHub Context Object**
- `github` is a built-in context object with information about the workflow run
- `github.event_name` — what triggered the run (push, pull_request, etc.)
- `github.ref` — the branch or tag that triggered the run
- `github.sha` — the commit SHA that triggered the run
- `github.actor` — the user who triggered the run

**Matrix Strategy**
- A matrix creates N x M x ... jobs from combinations of variables
- Each combination runs as a separate job on its own VM
- Great for testing across multiple Python versions, Node versions, or OS types

---

## 5. Lesson 02 — Backend CI Pipeline

**Concepts covered:** Pip caching, concurrency groups, service containers,
linting, type checking, testing, artifacts.

### 5.1 What We Are Learning

This lesson builds a real CI pipeline for our Python/FastAPI backend. You will
learn how to cache dependencies to speed up runs, use concurrency groups to
prevent duplicate runs, run PostgreSQL as a service container for tests, and
upload test coverage as artifacts.

### 5.2 Why Caching Matters

Every time a workflow runs, it starts with a fresh VM — no installed packages,
no cached files. Without caching, `pip install` downloads and installs every
dependency from scratch (takes 30-60 seconds). With caching, GitHub stores
the pip cache between runs and restores it instantly (takes 2-5 seconds).

```
Without cache: checkout (5s) -> pip install (45s) -> lint (5s) = 55 seconds
With cache:    checkout (5s) -> pip install (3s)  -> lint (5s) = 13 seconds
```

### 5.3 Why Concurrency Groups Matter

Without concurrency groups, pushing twice quickly creates two parallel runs
that waste minutes and may produce conflicting results. Concurrency groups
tell GitHub: "if a run is already in progress for this branch, cancel it
and start the new one."

### 5.4 The Complete Workflow

```yaml
# .github/workflows/02-backend-ci.yml

name: "Lesson 02 - Backend CI"

on:
  push:
    branches: [main, develop]
    paths:
      - "backend/**"  # Only run when backend files change
  pull_request:
    branches: [main]
    paths:
      - "backend/**"
  workflow_dispatch:

# CONCURRENCY: Prevent duplicate runs for the same branch.
# Group key: combines workflow name + branch ref.
# If a new push happens to the same branch, cancel the previous run.
concurrency:
  group: backend-${{ github.ref }}
  cancel-in-progress: true  # Cancel the old run immediately

env:
  PYTHON_VERSION: "3.13"

jobs:

  # -------------------------------------------------------------------------
  # JOB 1: Linting with Ruff + Black
  #
  # What is linting? Linting checks your code for style errors and potential
  # bugs WITHOUT running the code. Ruff checks for Python best practices.
  # Black checks for consistent formatting (indentation, spacing, etc.)
  # -------------------------------------------------------------------------
  lint:
    runs-on: ubuntu-latest
    steps:
      - name: "Checkout"
        uses: actions/checkout@v4

      - name: "Setup Python"
        uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}

      # CACHING: Store pip's download cache between workflow runs.
      # Key components:
      #   path: Where pip stores downloaded packages
      #   key: Unique identifier for this cache (based on requirements.txt hash)
      #   restore-keys: Fallback keys if exact match not found
      #
      # When requirements.txt changes -> new cache key -> fresh download
      # When requirements.txt is same -> same cache key -> use cached
      - name: "Cache pip dependencies"
        uses: actions/cache@v4
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('backend/requirements.txt') }}
          restore-keys: |
            ${{ runner.os }}-pip-

      - name: "Install dependencies"
        run: |
          python -m pip install --upgrade pip
          pip install -r backend/requirements.txt

      # Ruff: Fast Python linter (replaces flake8, isort, pyflakes)
      # Checks: unused imports, undefined variables, code style violations
      - name: "Run Ruff linter"
        working-directory: backend  # Changes to backend/ before running
        run: ruff check .

      # Black: Code formatter (makes all code look consistent)
      # --check: Only CHECK, don't modify. Fails if formatting is needed.
      - name: "Check Black formatting"
        working-directory: backend
        run: black --check .

  # -------------------------------------------------------------------------
  # JOB 2: Type checking with mypy
  #
  # What is type checking? mypy analyzes your Python code to find type errors
  # WITHOUT running it. For example: passing a string where an int is expected.
  # -------------------------------------------------------------------------
  typecheck:
    runs-on: ubuntu-latest
    steps:
      - name: "Checkout"
        uses: actions/checkout@v4

      - name: "Setup Python"
        uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}

      - name: "Cache pip dependencies"
        uses: actions/cache@v4
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('backend/requirements.txt') }}
          restore-keys: |
            ${{ runner.os }}-pip-

      - name: "Install dependencies"
        run: |
          python -m pip install --upgrade pip
          pip install -r backend/requirements.txt

      # mypy: Static type checker for Python
      # app/ is the directory to check (our main application code)
      - name: "Run mypy"
        working-directory: backend
        run: mypy app/

  # -------------------------------------------------------------------------
  # JOB 3: Run tests with PostgreSQL service container
  #
  # What are service containers? Docker containers that run alongside your job.
  # They start before your steps run and stop after your job completes.
  # Perfect for databases, Redis, message queues, etc.
  # -------------------------------------------------------------------------
  test:
    runs-on: ubuntu-latest

    # SERVICES: Docker containers that run in parallel with your job.
    # GitHub pulls the image, starts the container, and maps ports.
    # The 'options' field runs health checks to ensure the service is ready.
    services:
      postgres:
        image: postgres:15  # Docker image to use
        env:
          POSTGRES_USER: test_user
          POSTGRES_PASSWORD: test_password
          POSTGRES_DB: test_db
        ports:
          - 5432:5432  # Map container port 5432 to runner port 5432
        # HEALTH CHECK: Wait until PostgreSQL is ready to accept connections.
        # Without this, your tests might start before the DB is ready.
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - name: "Checkout"
        uses: actions/checkout@v4

      - name: "Setup Python"
        uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}

      - name: "Cache pip dependencies"
        uses: actions/cache@v4
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('backend/requirements.txt') }}
          restore-keys: |
            ${{ runner.os }}-pip-

      - name: "Install dependencies"
        run: |
          python -m pip install --upgrade pip
          pip install -r backend/requirements.txt

      # Run tests with coverage report
      # --cov=app/ measures how much of our code is covered by tests
      # --cov-report=xml generates a machine-readable report
      # --cov-report=html generates a human-readable HTML report
      - name: "Run tests with coverage"
        working-directory: backend
        env:
          # DATABASE_URL: Points to the PostgreSQL service container above.
          # 'localhost' works because the service port is mapped to the runner.
          DATABASE_URL: postgresql+asyncpg://test_user:test_password@localhost:5432/test_db
        run: pytest tests/ -v --cov=app/ --cov-report=xml --cov-report=html

      # ARTIFACTS: Save files from the runner for later download.
      # Useful for test reports, build outputs, coverage reports.
      # Files are kept for 'retention-days' then deleted.
      - name: "Upload coverage report"
        if: always()  # Run even if previous steps failed
        uses: actions/upload-artifact@v4
        with:
          name: coverage-report
          path: backend/htmlcov/
          retention-days: 7

  # -------------------------------------------------------------------------
  # JOB 4: Security scanning
  #
  # What is security scanning? Checking your dependencies for known
  # vulnerabilities (CVEs). 'safety' checks Python packages against
  # the vulnerability database.
  # -------------------------------------------------------------------------
  security:
    runs-on: ubuntu-latest
    steps:
      - name: "Checkout"
        uses: actions/checkout@v4

      - name: "Setup Python"
        uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}

      - name: "Install safety"
        run: pip install safety

      # continue-on-error: true means this step won't fail the job.
      # We want to SEE the vulnerabilities but not BLOCK the build.
      - name: "Check for vulnerabilities"
        working-directory: backend
        run: safety check -r requirements.txt
        continue-on-error: true
```

### 5.5 Key Concepts Explained

**Caching Strategy**
| What to Cache | Where | Key Formula |
|--------------|-------|-------------|
| Python packages | `~/.cache/pip` | `pip-${{ hashFiles('requirements.txt') }}` |
| Node modules | `~/.npm` | `npm-${{ hashFiles('package-lock.json') }}` |
| Build outputs | Custom path | `build-${{ github.sha }}` |

**Service Containers**
- Run Docker containers alongside your job
- Start before steps, stop after job
- Health checks ensure readiness
- Ports are mapped to the runner (localhost access)

**Artifacts**
- Files saved from the runner VM
- Available for download in the GitHub UI
- Useful for: test reports, build outputs, logs
- Retention: 1-90 days (configurable)

**`working-directory:`**
- Changes the directory before running the command
- Equivalent to `cd backend && command`
- Cleaner than chaining `cd` commands in `run:`

**`if: always()`**
- By default, a step only runs if ALL previous steps succeeded
- `if: always()` forces the step to run regardless of previous outcomes
- Essential for cleanup steps and artifact uploads

---

## 6. Lesson 03 — Frontend CI Pipeline

**Concepts covered:** npm caching, build verification, ESLint, TypeScript
type checking, build artifacts.

### 6.1 What We Are Learning

This lesson builds a CI pipeline for our Next.js frontend. The frontend
has different tooling (npm instead of pip, ESLint instead of Ruff) but
the same principles apply.

### 6.2 The Complete Workflow

```yaml
# .github/workflows/03-frontend-ci.yml

name: "Lesson 03 - Frontend CI"

on:
  push:
    branches: [main, develop]
    paths:
      - "frontend/**"  # Only run when frontend files change
  pull_request:
    branches: [main]
    paths:
      - "frontend/**"
  workflow_dispatch:

# CONCURRENCY: Same pattern as backend, but separate group.
# Backend and frontend concurrency groups are INDEPENDENT.
concurrency:
  group: frontend-${{ github.ref }}
  cancel-in-progress: true

env:
  NODE_VERSION: "20"

jobs:

  # -------------------------------------------------------------------------
  # JOB 1: Lint and type check
  # -------------------------------------------------------------------------
  lint:
    runs-on: ubuntu-latest
    steps:
      - name: "Checkout"
        uses: actions/checkout@v4

      # setup-node@v4 with cache: "npm" handles npm caching automatically.
      # No need for actions/cache — setup-node does it for you.
      # cache-dependency-path: Points to the lockfile for cache key generation.
      - name: "Setup Node.js"
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: "npm"
          cache-dependency-path: frontend/package-lock.json

      # npm ci: Install dependencies from lockfile.
      # 'ci' is faster and more reliable than 'npm install' for CI.
      # It deletes node_modules first and installs exactly what lockfile says.
      - name: "Install dependencies"
        working-directory: frontend
        run: npm ci

      # ESLint: JavaScript/TypeScript linter
      # Checks: unused variables, import order, code style, etc.
      - name: "Run ESLint"
        working-directory: frontend
        run: npm run lint

      # TypeScript type check (without emitting files)
      # --noEmit: Check types but don't generate .js files
      - name: "TypeScript type check"
        working-directory: frontend
        run: npx tsc --noEmit

  # -------------------------------------------------------------------------
  # JOB 2: Build verification
  # -------------------------------------------------------------------------
  build:
    runs-on: ubuntu-latest
    steps:
      - name: "Checkout"
        uses: actions/checkout@v4

      - name: "Setup Node.js"
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: "npm"
          cache-dependency-path: frontend/package-lock.json

      - name: "Install dependencies"
        working-directory: frontend
        run: npm ci

      # Next.js build: Compiles TypeScript, optimizes assets, generates static pages
      # If this fails, the build is broken and cannot be deployed.
      - name: "Build Next.js"
        working-directory: frontend
        run: npm run build
        env:
          NEXT_PUBLIC_APP_URL: https://valpsystems.com

      # Upload the build output as an artifact.
      # This can be downloaded or used by deployment jobs.
      - name: "Upload build output"
        uses: actions/upload-artifact@v4
        with:
          name: frontend-build
          path: frontend/.next/
          retention-days: 7
```

### 6.3 Key Concepts Explained

**`npm ci` vs `npm install`**
| Command | What It Does | When to Use |
|---------|-------------|-------------|
| `npm ci` | Installs exactly what lockfile says, deletes node_modules first | CI/CD (deterministic) |
| `npm install` | May update lockfile, respects package.json ranges | Local development |

**Automatic npm Caching**
- `actions/setup-node@v4` with `cache: "npm"` handles caching automatically
- It caches `~/.npm` (npm's download cache)
- The cache key is derived from `package-lock.json`
- No need for manual `actions/cache` steps

**Build Artifacts**
- `.next/` contains the compiled Next.js application
- Upload as artifact to pass between jobs or save for deployment
- Deployment jobs can download this artifact instead of rebuilding

---

## 7. Lesson 04 — Composite Actions

**Concepts covered:** Composite actions, reusable step sequences, DRY principle,
action inputs and outputs.

### 7.1 What Are Composite Actions?

A composite action is a reusable sequence of steps that you can call from
any workflow. Think of it as a "function" — you define it once and call
it many times.

**Why use them?**
- Our backend CI repeats: checkout -> setup Python -> cache pip -> install deps
- Without composites: copy-paste these 4 steps into every workflow
- With composites: write once, call with `uses: ./.github/actions/setup-python-env`

### 7.2 The Setup Python Composite Action

Create this file at `.github/actions/setup-python-env/action.yml`:

```yaml
# .github/actions/setup-python-env/action.yml

# =============================================================================
# COMPOSITE ACTION: Reusable Python Environment Setup
# =============================================================================
# What it does:
#   1. Installs the specified Python version
#   2. Caches pip dependencies
#   3. Upgrades pip
#   4. Installs project dependencies
#
# Why use it:
#   - DRY: Write once, use in every Python workflow
#   - Consistent: Same setup everywhere
#   - Maintainable: Change in one place, updates everywhere
# =============================================================================

name: "Setup Python Environment"
description: "Sets up Python, caches pip, and installs project dependencies"

# INPUTS: Parameters the caller can provide.
# Each input has a name, description, whether it's required, and a default.
inputs:
  python-version:
    description: "Python version to install"
    required: false
    default: "3.13"
  cache-dependency:
    description: "Path to requirements.txt for cache key"
    required: false
    default: "backend/requirements.txt"

# OUTPUTS: Values this action exposes to the caller.
outputs:
  python-version:
    description: "The installed Python version"
    value: ${{ steps.setup.outputs.python-version }}

# RUNS: The steps this composite action executes.
# 'using: "composite"' means this is a composite action (not JavaScript/Docker).
runs:
  using: "composite"
  steps:
    # Each step must have 'shell:' specified (unlike regular workflow steps)
    - name: "Setup Python"
      id: setup
      uses: actions/setup-python@v5
      with:
        python-version: ${{ inputs.python-version }}

    - name: "Cache pip dependencies"
      uses: actions/cache@v4
      with:
        path: ~/.cache/pip
        key: ${{ runner.os }}-pip-${{ hashFiles(inputs.cache-dependency) }}
        restore-keys: |
          ${{ runner.os }}-pip-

    - name: "Upgrade pip"
      shell: bash  # REQUIRED in composite actions
      run: python -m pip install --upgrade pip

    - name: "Install dependencies"
      shell: bash
      run: pip install -r ${{ inputs.cache-dependency }}

    - name: "Set output"
      shell: bash
      run: echo "python-version=${{ inputs.python-version }}" >> "$GITHUB_OUTPUT"
```

### 7.3 The Setup Node Composite Action

Create this file at `.github/actions/setup-node-env/action.yml`:

```yaml
# .github/actions/setup-node-env/action.yml

name: "Setup Node Environment"
description: "Sets up Node.js, caches npm, and installs project dependencies"

inputs:
  node-version:
    description: "Node.js version to install"
    required: false
    default: "20"
  working-directory:
    description: "Directory containing package.json"
    required: false
    default: "frontend"

outputs:
  node-version:
    description: "The installed Node.js version"
    value: ${{ steps.setup.outputs.node-version }}

runs:
  using: "composite"
  steps:
    - name: "Setup Node.js"
      id: setup
      uses: actions/setup-node@v4
      with:
        node-version: ${{ inputs.node-version }}
        cache: "npm"
        cache-dependency-path: ${{ inputs.working-directory }}/package-lock.json

    - name: "Install dependencies"
      shell: bash
      working-directory: ${{ inputs.working-directory }}
      run: npm ci

    - name: "Set output"
      shell: bash
      run: echo "node-version=${{ inputs.node-version }}" >> "$GITHUB_OUTPUT"
```

### 7.4 Using Composite Actions in Workflows

```yaml
# Example: Using our composite actions in a workflow
name: "Using Composite Actions"

on: push

jobs:
  demo:
    runs-on: ubuntu-latest
    steps:
      # Call our composite action with custom inputs
      - name: "Setup Python environment"
        uses: ./.github/actions/setup-python-env
        with:
          python-version: "3.13"
          cache-dependency: backend/requirements.txt

      # Call our Node composite action
      - name: "Setup Node environment"
        uses: ./.github/actions/setup-node-env
        with:
          node-version: "20"
          working-directory: frontend

      # Both environments are now ready!
      - name: "Verify setup"
        run: |
          python --version
          node --version
```

### 7.5 Key Concepts Explained

**Composite vs Reusable Workflows**
| Feature | Composite Action | Reusable Workflow |
|---------|-----------------|-------------------|
| Trigger | Called with `uses:` in a step | Called with `uses:` in a job |
| Runs in | Same job as caller | Separate job (own runner) |
| Outputs | Available via `outputs:` | Available via `job.outputs` |
| Use case | Shared step sequences | Shared job configurations |
| Isolation | Same runner VM | Separate runner VM |

**`shell:` Requirement**
- In regular workflow steps, `shell:` defaults to `bash` on Linux/Mac
- In composite actions, you MUST specify `shell:` explicitly
- Common options: `bash`, `pwsh` (PowerShell), `sh`

---

## 8. Lesson 05 — Reusable Workflows

**Concepts covered:** Reusable workflows (workflow_call), workflow inputs,
workflow outputs, calling reusable workflows, sharing CI logic.

### 8.1 What Are Reusable Workflows?

A reusable workflow is a complete workflow that can be called from another
workflow. Unlike composite actions (which run as steps in a job), reusable
workflows run as **separate jobs** on their own runners.

**When to use reusable workflows:**
- Multiple repos need the same CI pipeline
- Multiple workflows in the same repo share job configurations
- You want to enforce standardization (security, testing, etc.)

### 8.2 Defining a Reusable Workflow

```yaml
# .github/workflows/05-reusable-workflow.yml

# =============================================================================
# REUSABLE WORKFLOW: Can be called from other workflows
# =============================================================================
# This workflow defines a backend CI pipeline that other workflows can invoke.
# The caller provides inputs (Python version, whether to run tests, etc.)
# and this workflow executes the jobs.
# =============================================================================

name: "Reusable Backend CI"

# workflow_call: Makes this workflow callable from other workflows.
# It can accept inputs (parameters) and secrets from the caller.
on:
  workflow_call:

    # INPUTS: Parameters the caller must/should provide.
    # These become available as ${{ inputs.<name> }}
    inputs:
      python-version:
        description: "Python version to use"
        required: false
        default: "3.13"
        type: string
      run-tests:
        description: "Whether to run tests"
        required: false
        default: true
        type: boolean
      run-security:
        description: "Whether to run security scan"
        required: false
        default: false
        type: boolean

    # SECRETS: Secrets the caller must pass.
    # Reusable workflows cannot access the caller's secrets automatically.
    secrets:
      DATABASE_URL:
        required: false
        description: "Database URL for tests"

    # OUTPUTS: Values this workflow returns to the caller.
    outputs:
      test-result:
        description: "Test job result (success/failure/cancelled)"
        value: ${{ jobs.test.result }}

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ inputs.python-version }}
      - run: pip install ruff black
      - run: ruff check .
        working-directory: backend
      - run: black --check .
        working-directory: backend

  test:
    # if: Conditionally run this job based on caller's input.
    if: ${{ inputs.run-tests }}
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ inputs.python-version }}
      - run: pip install -r backend/requirements.txt
      - run: pytest tests/ -v
        working-directory: backend

  security:
    if: ${{ inputs.run-security }}
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pip install safety
      - run: safety check -r backend/requirements.txt
        continue-on-error: true
```

### 8.3 Calling a Reusable Workflow

```yaml
# .github/workflows/caller-example.yml

name: "Caller Workflow"

on: push

jobs:
  # Call the reusable workflow with custom inputs
  backend-ci:
    # 'uses:' at the job level calls a reusable workflow.
    # Format: ./.github/workflows/<filename>.yml or <org>/<repo>/.github/workflows/<file>.yml@ref
    uses: ./.github/workflows/05-reusable-workflow.yml
    with:
      python-version: "3.13"
      run-tests: true
      run-security: true
    # Pass secrets to the reusable workflow
    secrets:
      DATABASE_URL: ${{ secrets.DATABASE_URL }}

  # Use the output from the reusable workflow
  deploy:
    needs: [backend-ci]
    runs-on: ubuntu-latest
    steps:
      - run: echo "Test result: ${{ needs.backend-ci.outputs.test-result }}"
```

### 8.4 Reusable Workflow vs Composite Action

| Scenario | Use Composite Action | Use Reusable Workflow |
|----------|---------------------|----------------------|
| Shared setup steps (cache, install) | Yes | No |
| Shared job configurations | No | Yes |
| Need separate runner isolation | No | Yes |
| Need to pass secrets | No | Yes |
| Need job-level outputs | No | Yes |
| Cross-repo reuse | No | Yes |

---

## 9. Lesson 06 — Deployment Pipeline

**Concepts covered:** SSH deployment, GitHub Secrets, environment protection,
deployment gates, OIDC vs static credentials.

### 9.1 Deployment Concepts

**GitHub Secrets:**
- Encrypted variables stored in your repo settings
- Never exposed in logs (replaced with `***`)
- Used for: API keys, SSH keys, database passwords
- Configure at: Settings > Secrets and variables > Actions

**Environment Protection:**
- GitHub Environments allow you to configure protection rules
- Rules: required reviewers, wait timers, branch restrictions
- Deployment jobs can target specific environments
- Environments track deployment history

**OIDC vs Static Credentials:**
| Feature | Static Credentials (IAM Keys) | OIDC (Keyless) |
|---------|------------------------------|-----------------|
| Setup | Create IAM user, get access keys | Create OIDC provider + IAM role |
| Security | Keys stored as secrets (can be leaked) | No long-lived credentials |
| Rotation | Manual rotation needed | Automatic (tokens expire in 1hr) |
| Audit | Hard to track per-workflow | Easy (each run gets unique token) |
| Use case | Legacy, simple setups | Modern, enterprise setups |

### 9.2 The Deployment Workflow

```yaml
# .github/workflows/06-deploy-ec2.yml

name: "Lesson 06 - Deploy to AWS EC2"

on:
  push:
    branches: [main]
  workflow_dispatch:
    inputs:
      environment:
        description: "Target environment"
        required: true
        type: choice
        options:
          - staging
          - production

# CONCURRENCY: Prevent overlapping deployments.
# cancel-in-progress: false for deployments (don't cancel mid-deploy!).
concurrency:
  group: deploy-${{ inputs.environment || 'production' }}
  cancel-in-progress: false

jobs:

  # -------------------------------------------------------------------------
  # JOB 1: Deploy using static IAM credentials
  #
  # This approach uses AWS IAM access keys stored as GitHub secrets.
  # Simpler to set up but less secure (long-lived credentials).
  # -------------------------------------------------------------------------
  deploy-static:
    runs-on: ubuntu-latest

    # ENVIRONMENT: Targets a GitHub Environment.
    # If the environment has protection rules (e.g., required reviewers),
    # the job will PAUSE until the rules are satisfied.
    environment:
      name: ${{ inputs.environment || 'production' }}
      url: https://valpsystems.com

    steps:
      - name: "Checkout"
        uses: actions/checkout@v4

      # Configure AWS credentials from GitHub secrets.
      # These secrets must be set in: Settings > Secrets > Actions
      - name: "Configure AWS credentials (Static)"
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1

      # SSH into the app server and deploy
      - name: "Deploy backend"
        uses: appleboy/ssh-action@v1
        with:
          host: ${{ secrets.APP_SERVER_HOST }}
          username: ${{ secrets.SERVER_USERNAME }}
          key: ${{ secrets.SSH_PRIVATE_KEY }}
          script: |
            cd /opt/platform
            git pull origin main
            cd backend
            source venv/bin/activate
            pip install -r requirements.txt
            alembic upgrade head
            sudo systemctl restart valp-backend

      - name: "Deploy frontend"
        uses: appleboy/ssh-action@v1
        with:
          host: ${{ secrets.APP_SERVER_HOST }}
          username: ${{ secrets.SERVER_USERNAME }}
          key: ${{ secrets.SSH_PRIVATE_KEY }}
          script: |
            cd /opt/platform/frontend
            npm install
            npm run build
            pm2 restart valp-frontend

      # SCP: Copy NGINX config to proxy server
      - name: "Update NGINX config"
        uses: appleboy/scp-action@v0.1.7
        with:
          host: ${{ secrets.PROXY_SERVER_HOST }}
          username: ${{ secrets.SERVER_USERNAME }}
          key: ${{ secrets.SSH_PRIVATE_KEY }}
          source: "deploy/nginx/app.conf"
          target: "/etc/nginx/conf.d/app.conf"

      - name: "Reload NGINX"
        uses: appleboy/ssh-action@v1
        with:
          host: ${{ secrets.PROXY_SERVER_HOST }}
          username: ${{ secrets.SERVER_USERNAME }}
          key: ${{ secrets.SSH_PRIVATE_KEY }}
          script: sudo nginx -t && sudo systemctl reload nginx

  # -------------------------------------------------------------------------
  # JOB 2: Deploy using OIDC (Keyless)
  #
  # This approach uses OpenID Connect for authentication.
  # No static credentials needed — GitHub and AWS establish trust.
  #
  # Setup required:
  #   1. Create OIDC provider in AWS IAM
  #   2. Create IAM role with trust policy for GitHub
  #   3. Store role ARN as GitHub secret
  # -------------------------------------------------------------------------
  deploy-oidc:
    runs-on: ubuntu-latest
    if: false  # Disable by default — enable when OIDC is configured

    environment:
      name: ${{ inputs.environment || 'production' }}
      url: https://valpsystems.com

    # OIDC requires these permissions.
    # 'id-token: write' allows the workflow to request an OIDC token.
    permissions:
      id-token: write
      contents: read

    steps:
      - name: "Checkout"
        uses: actions/checkout@v4

      # OIDC: No access keys needed!
      # GitHub provides a JWT token, AWS validates it via the OIDC provider.
      - name: "Configure AWS credentials (OIDC)"
        uses: aws-actions/configure-aws-credentials@v4
        with:
          # The role ARN is the only "secret" needed.
          role-to-assume: ${{ secrets.AWS_OIDC_ROLE_ARN }}
          aws-region: us-east-1

      - name: "Verify identity"
        run: aws sts get-caller-identity
```

### 9.3 Setting Up Environment Protection

1. Go to your repo on GitHub
2. Navigate to **Settings > Environments**
3. Click **New environment** and create `production`
4. Configure protection rules:
   - **Required reviewers:** Add people who must approve deployments
   - **Wait timer:** Add a delay (e.g., 5 minutes) before deployment starts
   - **Branch restrictions:** Only allow deployments from `main`
5. Click **Save protection rules**

---

## 10. Lesson 07 — Full Orchestration

**Concepts covered:** Complete pipeline orchestration, job dependencies,
parallel vs sequential execution, branch-based deployment.

### 10.1 What We Are Building

This lesson combines everything into a production-ready pipeline that:
1. Runs linting, type checking, and security scans in parallel
2. Runs backend tests across multiple Python versions
3. Builds the frontend
4. Deploys to staging on `develop` branch
5. Deploys to production on `main` branch (with approval gate)

### 10.2 The Complete Pipeline

```yaml
# .github/workflows/07-full-pipeline.yml

name: "Lesson 07 - Full Pipeline"

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

concurrency:
  group: pipeline-${{ github.ref }}
  cancel-in-progress: true

# ============================================================================
# PIPELINE FLOW:
#
# STAGE 1 (Parallel): Backend Lint, Frontend Lint, Type Check, Security
# STAGE 2 (Parallel): Backend Test (3 versions), Frontend Build
# STAGE 3: Deploy Staging (develop) or Production (main)
# ============================================================================
jobs:

  # ==========================================================================
  # STAGE 1: Code Quality (all run in parallel)
  # ==========================================================================

  backend-lint:
    name: "Backend Lint"
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: ./.github/actions/setup-python-env
        with:
          cache-dependency: backend/requirements.txt
      - run: ruff check .
        working-directory: backend
      - run: black --check .
        working-directory: backend

  frontend-lint:
    name: "Frontend Lint"
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: ./.github/actions/setup-node-env
        with:
          working-directory: frontend
      - run: npm run lint
        working-directory: frontend

  typecheck:
    name: "Type Check"
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: ./.github/actions/setup-python-env
        with:
          cache-dependency: backend/requirements.txt
      - run: mypy app/
        working-directory: backend

  # ==========================================================================
  # STAGE 2: Tests & Build (depends on Stage 1, runs in parallel)
  # ==========================================================================

  backend-test:
    name: "Backend Test (Python ${{ matrix.python-version }})"
    # needs: Wait for backend-lint to pass before running tests.
    # If lint fails, tests won't run (saves time and compute).
    needs: [backend-lint]
    runs-on: ubuntu-latest

    # Matrix: Test across 3 Python versions simultaneously.
    strategy:
      matrix:
        python-version: ["3.11", "3.12", "3.13"]
      fail-fast: false

    # Service container: PostgreSQL for integration tests
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_USER: test
          POSTGRES_PASSWORD: test
          POSTGRES_DB: test_db
        ports: ["5432:5432"]
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      - uses: actions/cache@v4
        with:
          path: ~/.cache/pip
          key: pip-${{ matrix.python-version }}-${{ hashFiles('backend/requirements.txt') }}
      - run: pip install -r backend/requirements.txt
      - run: pytest tests/ -v --cov=app/
        working-directory: backend
        env:
          DATABASE_URL: postgresql+asyncpg://test:test@localhost:5432/test_db

  frontend-build:
    name: "Frontend Build"
    needs: [frontend-lint]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: ./.github/actions/setup-node-env
        with:
          working-directory: frontend
      - run: npm run build
        working-directory: frontend
      - uses: actions/upload-artifact@v4
        with:
          name: frontend-build
          path: frontend/.next/

  # ==========================================================================
  # STAGE 3: Deployment (depends on ALL Stage 2 jobs)
  # ==========================================================================

  deploy-staging:
    name: "Deploy to Staging"
    # needs: ALL tests must pass before deploying.
    needs: [backend-test, frontend-build, typecheck]
    # if: Only deploy to staging on develop branch.
    if: github.ref == 'refs/heads/develop'
    runs-on: ubuntu-latest
    environment:
      name: staging
      url: https://staging.valpsystems.com
    steps:
      - uses: actions/checkout@v4
      - run: echo "Deploying to staging..."

  deploy-production:
    name: "Deploy to Production"
    needs: [backend-test, frontend-build, typecheck]
    # if: Only deploy to production on main branch.
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment:
      name: production  # This environment has approval gates
      url: https://valpsystems.com
    steps:
      - uses: actions/checkout@v4
      - run: echo "Deploying to production..."
```

### 10.3 Understanding Job Dependencies

```
backend-lint ----------> backend-test (3 versions)
frontend-lint ---------> frontend-build
typecheck -------------> deploy-staging (develop branch only)
                         deploy-production (main branch only)
```

**`needs:` Behavior:**
- Job runs only after ALL listed dependencies complete successfully
- If any dependency fails, the dependent job is skipped
- Dependencies run in parallel unless they also have `needs:` chains

**Branch-Based Deployment:**
- `if: github.ref == 'refs/heads/develop'` → staging only
- `if: github.ref == 'refs/heads/main'` → production only
- PRs run tests but skip deployment (no deploy job matches)

---

## 11. Enterprise Patterns Reference

### 11.1 Concurrency Groups

**What:** Prevents duplicate workflow runs for the same branch/PR.

**Why:** Without concurrency, pushing twice quickly creates two parallel runs
that waste compute and may produce conflicting results.

```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
```

| Component | What It Does |
|-----------|-------------|
| `group` | Unique identifier for the concurrency group |
| `cancel-in-progress: true` | Cancel the old run when a new one starts |
| `cancel-in-progress: false` | Queue the new run (wait for old to finish) |

**Best practices:**
- Use `true` for CI (lint, test) — fast feedback is more important
- Use `false` for deployments — never cancel a mid-deployment
- Include workflow name + branch in the group key

### 11.2 Path-Based Triggers

**What:** Only run workflows when specific files change.

**Why:** If you only changed backend code, there's no need to run frontend CI.

```yaml
on:
  push:
    paths:
      - "backend/**"        # Only if files in backend/ changed
      - "!backend/logs/**"  # But NOT if only logs changed (negation)
    paths-ignore:
      - "docs/**"           # Skip if only docs changed
      - "*.md"              # Skip if only markdown files changed
```

### 11.3 Caching Strategies

| Stack | Cache Path | Key Formula |
|-------|-----------|-------------|
| Python (pip) | `~/.cache/pip` | `pip-${{ hashFiles('requirements.txt') }}` |
| Node.js (npm) | `~/.npm` | `npm-${{ hashFiles('package-lock.json') }}` |
| Go | `~/go/pkg/mod` | `go-${{ hashFiles('go.sum') }}` |
| Rust (cargo) | `~/.cargo/registry` | `cargo-${{ hashFiles('Cargo.lock') }}` |

### 11.4 Secret Management Best Practices

| Practice | Description |
|----------|-------------|
| Never hardcode | Always use `${{ secrets.SECRET_NAME }}` |
| Minimal scope | Create separate secrets for dev/staging/prod |
| Rotate regularly | Change secrets every 90 days |
| Use OIDC when possible | Avoid long-lived credentials entirely |
| Audit access | Review who can modify secrets in repo settings |

### 11.5 Branch Protection Integration

Configure in GitHub repo settings to enforce CI checks:

1. Go to **Settings > Branches > Branch protection rules**
2. Add rule for `main` branch
3. Enable:
   - **Require status checks to pass** — blocks merge if CI fails
   - **Require branches to be up to date** — ensures latest code is tested
   - **Require pull request reviews** — at least 1 approval required
4. Select required checks: `backend-lint`, `frontend-lint`, `backend-test`, etc.

### 11.6 Notifications

```yaml
# Add to the end of any workflow
- name: "Notify Slack on failure"
  if: failure()
  uses: slackapi/slack-github-action@v1
  with:
    payload: |
      {
        "text": "CI failed for ${{ github.repository }}:${{ github.ref_name }}"
      }
  env:
    SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
```

---

## 12. Self-Hosted Runners

**Concepts covered:** When to use self-hosted runners, setup on EC2/Linux,
registration, labels, running as a systemd service, Docker capability,
targeting self-hosted in workflows, security, updates, troubleshooting.

### 12.1 What Are Self-Hosted Runners?

A **self-hosted runner** is a machine that YOU own and run — instead of using
the ephemeral VMs GitHub provides — to execute your workflows. GitHub sends job
instructions to your machine over a persistent HTTPS connection, and your
machine executes the steps.

```
+----------------+      HTTPS (outbound only)      +--------------------+
|  GitHub        |  <==========================>  |  Your EC2 server  |
|  Actions       |         (runner agent)          |  (runner live)     |
+----------------+                                 +--------------------+
        |                                                    |
        v                                                    v
  Queues jobs                                      Runs steps locally,
  Stores logs                                      uses your CPU/RAM/disk
```

**Key fact:** The runner maintains an **outbound** connection to GitHub.
GitHub never connects into your machine — so no inbound ports are needed.
This means a self-hosted runner works on machines in private subnets (which the
VALP SYSTEMS infrastructure already uses).

### 12.2 When (Not) to Use Self-Hosted Runners

| Factor | GitHub-Hosted | Self-Hosted |
|--------|---------------|-------------|
| Setup effort | Zero (just use `runs-on: ubuntu-latest`) | Must install + register the agent |
| Cost | Free 2,000 min/month, paid after | Time on your VMs (you already pay) |
| Resources | Ephemeral, industry-standard (4 CPU / 16 GB) | Whatever your machine has |
| OS/packages | Fixed set, you cannot install globally | Install anything you want |
| State cleanliness | Fresh VM every run (isolated) | Persistent state between runs |
| Security | Isolated (safe for untrusted code) | **NOT safe for untrusted code** |
| Where it runs | GitHub's cloud | Your network / private subnet |
| Third-party deps | Sometimes slow (NDA/privacy) | Full control, no data leaves your VPC |

**Use self-hosted when:**
- You exceed the free hosted minutes and want to save costs
- You need to install software not available on hosted runners
- You must keep artifacts/secrets inside your VPC (regulatory/NDA)
- Your VMs have more RAM/CPU than hosted runners

**Prefer GitHub-hosted when:**
- You are still learning (this guide's first 10 lessons target hosted runners)
- You process pull requests from forks (untrusted code)
- You want consistent, reproducible, disposable environments

### 12.3 Architecture & Requirements

| Component | Requirement |
|-----------|-------------|
| OS | Linux (Ubuntu/RHEL/Amazon Linux), Windows, or macOS |
| Hardware | 2+ GB RAM, 2+ vCPUs recommended, ~15 GB free disk |
| Network | Outbound HTTPS to `github.com` (port 443) only |
| Software | Runner requires Bash on Linux; Docker optional (for service containers) |
| Permissions | A service account or dedicated user (never run as root ideally) |

**One machine, multiple runners:** You can register several runner instances
on one machine (each in its own directory) — useful for different labels.

### 12.4 Setup on Amazon Linux 2023 (our App Server)

The steps below match our existing EC2 infrastructure. The runner directory
lives under `/opt/actions-runner`.

#### Step 1 — Create the runner in GitHub

1. Repo-level: **Settings > Actions > Runners > New self-hosted runner**
2. Generate a **registration token** (valid ~1 hour; re-generate as needed)
3. The page shows the exact download URL for your platform — copy the
   **Linux x64** commands for an EC2 instance

#### Step 2 — Prepare the machine

```bash
# As ec2-user (or a dedicated 'runner' user — recommended for security)
sudo dnf install -y tar gzip git curl

# Optional: Docker for service containers (PostgreSQL in tests, etc.)
sudo dnf install -y docker
sudo systemctl enable --now docker
sudo usermod -aG docker ec2-user    # avoid sudo for docker commands

# Optional: Java/other toolchains your workflows need — install globally here
```

#### Step 3 — Download, extract, configure

```bash
mkdir -p /opt/actions-runner
cd /opt/actions-runner

# Replace VERSION_SHORT with the version GitHub shows you (e.g. 2.319.1)
curl -o actions-runner-linux-x64.tar.gz -L https://github.com/actions/runner/releases/download/v<VERSION>/actions-runner-linux-x64-<VERSION>.tar.gz

# Optional: verify the SHA256 from GitHub's page for security
echo "<SHA256>  actions-runner-linux-x64.tar.gz" | sha256sum -c -

tar xzf actions-runner-linux-x64.tar.gz

# Configure the runner (token pasted from GitHub UI)
./config.sh --url https://github.com/<OWNER>/<REPO> \
            --token <REGISTRATION_TOKEN> \
            --name valp-app-runner \
            --labels linux,x64,valp \
            --unattended --replace
```

| Flag | Purpose |
|------|---------|
| `--url` | Repo or org to register against |
| `--token` | One-time registration token (from GitHub UI) |
| `--name` | Friendly name shown in GitHub UI |
| `--labels` | Custom labels your workflows use to target this runner |
| `--unattended` | No prompts (good for scripts/automation) |
| `--replace` | Overwrite an existing runner with the same name |

#### Step 4 — Run the runner

```bash
# Foreground (for testing)
./run.sh

# Or install as a systemd service so it starts on boot
sudo ./svc.sh install
sudo ./svc.sh start
sudo ./svc.sh status
```

The service will auto-restart with the machine. Verify it appears as
**"Online"** in **Settings > Actions > Runners**.

### 12.5 Labels — How Workflows Find Your Runner

Labels are tags you assign at registration. Your workflows select runners with
`runs-on: <label>`.

| Label you set | How workflows target it |
|---------------|-------------------------|
| `self-hosted` | Auto-added. Matches `runs-on: self-hosted` |
| `linux`, `x64` | Auto-added (OS/arch). Match `runs-on: [self-hosted, linux, x64]` |
| `valp` | Custom. Match `runs-on: [self-hosted, valp]` |

```yaml
# Use the custom 'valp' runner we registered above
runs-on: [self-hosted, valp]

# Or require only the runner named for this repo
runs-on: self-hosted
```

> **`runs-on: self-hosted` will match ANY self-hosted runner** on that
> repo/org — including ones on other machines. Add distinguishing labels
> (like `valp`) when you have more than one machine.

### 12.6 Using Docker / Service Containers on Self-Hosted

Service containers (`services:` in your workflow, e.g. our PostgreSQL test DB)
run as Docker containers **on the self-hosted machine**. Your runner must:

1. Have Docker installed (Step 2 above)
2. The runner user must be in the `docker` group
3. Workflows targeting self-hosted runners need `runs-on: self-hosted`

```yaml
jobs:
  test:
    runs-on: [self-hosted, valp]   # Docker is required here now
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_USER: test
          POSTGRES_PASSWORD: test
          POSTGRES_DB: test_db
        ports: ["5432:5432"]
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    steps:
      - uses: actions/checkout@v4
      - run: pip install -r backend/requirements.txt
      - run: pytest tests/ -v
        working-directory: backend
        env:
          DATABASE_URL: postgresql+asyncpg://test:test@localhost:5432/test_db
```

**Why Docker matters for us:** Lesson 02/07 rely on a PostgreSQL service
container. On a hosted runner that "just works". On a self-hosted runner,
Docker must exist first — otherwise the job fails with something like:
`Cannot connect to the Docker daemon`.

### 12.7 Business Logic for "Mark as production ready"

**State & caching on self-hosted runners:**
- Unlike hosted runners (fresh VM each run), a self-hosted runner keeps state
  between runs. Installed packages in `~/.npm`, pip caches, git caches — even
  artifacts from a previous run — persist.
- You can set `RUNNER_LOCATION`/home caches manually. Often you can skip the
  `actions/cache` step entirely because dependencies stay installed locally:
   ```yaml
   - name: "Install deps (cached by the runner itself)"
     run: |
       pip install -r backend/requirements.txt || true
   ```
   But be careful — this is **not deterministic**. A clean checkout on a fresh
   hosted runner is sometimes exactly what you want. Use stale-safe patterns.

**Cleaning between runs (recommended):**
- Add a cleanup job/step that resets workspace state you care about
- Or run with `./config.sh` reprovisioned occasionally
- Never rely on leftover files from a previous job in your actual deploy logic

### 12.8 Security — Read This Before You Deploy One

| Threat | Why It's Dangerous | Mitigation |
|--------|--------------------|------------|
| Fork PRs | A fork's code runs ON YOUR MACHINE — a malicious PR shells out and owns your server | Only route trusted branches to self-hosted (`if: github.event.pull_request.head.repo.full_name == 'OWNER/REPO'`), or use hosted runners for PRs |
| Secret exposure | Any code you run can read `${{ secrets.* }}` and env vars | Restrict who can register runners; keep runner on an isolated VM, never on prod DB hosts |
| Supply chain | Compromised dependency installs code into your runner | Pin versions, keep runner patched, isolate network access |
| Lateral movement | Runner on your VPC can reach other servers | Put the runner on its own hardened instance / security group |
| Persistence | Ran as `root`, a malicious step takes over the box | Use a dedicated unprivileged `runner` user |

**The golden rule:**
> A self-hosted runner has access to your machine and your **production
> environment secrets**. Only run **trusted** code on it. GitHub-hosted runners
> are disposable; your machine is not.

Recommended combo for our project:
- Self-hosted runner for the **deploy** job (keeps prod network/secrets in VPC)
- GitHub-hosted runners for **lint/test on pull requests** (untrusted forks safe)

### 12.9 Targeting Self-Hosted in Our Workflows

A mixed strategy for VALP SYSTEMS:

```yaml
jobs:
  # CI on PRs — hosted runners are safe & disposable (untrusted code OK)
  backend-test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        ...
    steps:
      - run: pytest tests/ -v

  # Deploy — run from inside our VPC via self-hosted runner (no SSH needed!)
  deploy-prod:
    needs: [backend-test]
    if: github.ref == 'refs/heads/main'
    runs-on: [self-hosted, valp]
    environment:
      name: production
    steps:
      - uses: actions/checkout@v4
      # Runner lives INSIDE the VPC — deploy directly, no SSH secrets required!
      - run: |
          ssh -i ~/.ssh/learning-key.pem ec2-user@10.0.2.236 'cd /opt/platform && git pull && sudo systemctl restart valp-backend'
```

> **Bonus of running deploy on a self-hosted runner inside your VPC:** you
> don't need GitHub secrets for `APP_SERVER_HOST` / `SSH_PRIVATE_KEY` anymore —
> the runner can reach private IPs directly. That is a major security win.

### 12.10 Updating the Runner

GitHub releases runner updates regularly. The running service will show a
"New runner version available" warning in the Actions settings page.

```bash
cd /opt/actions-runner
./svc.sh stop
./run.sh --version                       # compare with latest from GitHub
wget/or curl new tarball                 # from the releases page
tar xzf actions-runner-linux-x64-<ver>.tar.gz   # overwrites in place
./svc.sh start
./svc.sh status
```

> Never just `git pull` the runner's own directory. Overwrite with the tarball
> exactly as in Step 3.

### 12.11 Troubleshooting Self-Hosted Runners

| Symptom | Likely Cause | Fix |
|---------|--------------|-----|
| Runner shows "Offline" | Agent not running / network blocked | `./svc.sh status`, check `pnpm`/logs in `_diag/` and `_work/_diag/` |
| Job stuck "queued" | No runner matches the requested labels | Check `runs-on:` labels vs runner labels in Settings |
| `Cannot connect to the Docker daemon` | Docker not installed / user not in `docker` group | `sudo dnf install docker`, `sudo usermod -aG docker runner`, re-login |
| Runner disconnects randomly | Outdated agent / firewall | Update with Step (§12.10); allow outbound 443 |
| Registration token expired | Tokens live ~1 hour | Generate a fresh token in the UI |
| Secrets not available | Job ran on a fork | Only run on trusted refs (`github.event.pull_request.head.repo.full_name`) |
| Logs show "Runner was not found" | Deleted from UI but service still running | `./config.sh remove --token <PAT>` then uninstall service |

---

## 13. Configuration Reference

### 13.1 Required GitHub Secrets

Configure these in **Settings > Secrets and variables > Actions**:

| Secret | Description | Used In |
|--------|-------------|---------|
| `AWS_ACCESS_KEY_ID` | AWS IAM access key (static) | Deploy workflows |
| `AWS_SECRET_ACCESS_KEY` | AWS IAM secret key (static) | Deploy workflows |
| `AWS_OIDC_ROLE_ARN` | OIDC role ARN (keyless) | Deploy workflows |
| `APP_SERVER_HOST` | App server public/private IP | SSH deployment |
| `PROXY_SERVER_HOST` | Proxy server public IP | SSH deployment |
| `SERVER_USERNAME` | SSH username (e.g., ec2-user) | SSH deployment |
| `SSH_PRIVATE_KEY` | SSH private key content | SSH deployment |
| `DATABASE_URL` | PostgreSQL connection string | Test workflows |
| `SLACK_WEBHOOK_URL` | Slack incoming webhook URL | Notifications |

### 13.2 Environment Protection Setup

| Environment | Branch | Protection Rules |
|-------------|--------|-----------------|
| `staging` | `develop` | None (auto-deploy) |
| `production` | `main` | Required reviewers, wait timer |

### 13.3 OIDC Setup (AWS)

1. **Create OIDC provider in AWS IAM:**
   ```bash
   aws iam create-open-id-connect-provider \
     --url https://token.actions.githubusercontent.com \
     --thumbprint-list "6938fd4d98bab03faadb97b34396831e3780aea1" \
     --client-id-list "sts.amazonaws.com"
   ```

2. **Create IAM role with trust policy:**
   ```json
   {
     "Version": "2012-10-17",
     "Statement": [{
       "Effect": "Allow",
       "Principal": { "Federated": "arn:aws:iam::<ACCOUNT>:oidc-provider/token.actions.githubusercontent.com" },
       "Action": "sts:AssumeRoleWithWebIdentity",
       "Condition": {
         "StringEquals": { "token.actions.githubusercontent.com:aud": "sts.amazonaws.com" },
         "StringLike": { "token.actions.githubusercontent.com:sub": "repo:<OWNER>/<REPO>:ref:refs/heads/main" }
       }
     }]
   }
   ```

3. **Store role ARN as GitHub secret:** `AWS_OIDC_ROLE_ARN`

---

## 14. Learning Checklist

### Phase 1: Basics (Lessons 01-03)
- [ ] Create `.github/workflows/01-basic-ci.yml` and push
- [ ] Verify workflow appears in GitHub Actions tab
- [ ] Understand triggers, jobs, steps
- [ ] Create `02-backend-ci.yml` with caching
- [ ] Create `03-frontend-ci.yml` with npm caching
- [ ] Verify caching works (check second run speed)

### Phase 2: Intermediate (Lessons 04-05)
- [ ] Create `.github/actions/setup-python-env/action.yml`
- [ ] Create `.github/actions/setup-node-env/action.yml`
- [ ] Use composite actions in a workflow
- [ ] Create `05-reusable-workflow.yml`
- [ ] Call reusable workflow from another workflow

### Phase 3: Advanced (Lessons 06-07)
- [ ] Configure GitHub Secrets (at least SSH keys)
- [ ] Create `06-deploy-ec2.yml` with SSH deployment
- [ ] Create GitHub Environments (staging, production)
- [ ] Configure environment protection rules
- [ ] Create `07-full-pipeline.yml` complete orchestration

### Phase 4: Enterprise
- [ ] Set up branch protection rules
- [ ] Add concurrency groups to all workflows
- [ ] Add path-based triggers
- [ ] Configure Slack notifications
- [ ] Set up OIDC (optional, for production)
- [ ] Install a self-hosted runner on the App Server (§12)
- [ ] Move the deploy job to the self-hosted runner (no SSH secrets needed)

---

## Quick Reference: Common Commands

| Task | Command |
|------|---------|
| Run locally | `act` (GitHub Actions local runner) |
| Validate YAML | `yamllint .github/workflows/*.yml` |
| Check action syntax | `actionlint` |
| List workflow runs | `gh run list` |
| Watch a run | `gh run watch` |
| Re-run a run | `gh run rerun <run-id>` |

---

## Next Steps

1. Start with Lesson 01 and work through sequentially
2. Push each workflow file and verify it runs
3. Break things intentionally to see how GitHub Actions reports errors
4. Experiment with matrix combinations
5. Set up branch protection to enforce CI checks
6. Add notifications for failed runs

---

> **Remember:** CI/CD is a journey, not a destination. Start simple, iterate,
> and add complexity as you need it. The best pipeline is the one your team
> actually uses.
