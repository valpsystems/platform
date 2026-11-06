# Terraform — Interview Preparation Guide

Complete interview prep for Terraform: core concepts, syntax, hands-on
scenario-based Q&As, and rapid-fire one-liners. Every answer includes real
HCL syntax so you can talk code in the interview.

---

## Table of Contents

1. [Core Concepts Q&A](#part-1-core-concepts-questions--answers)
2. [Syntax Cheat Sheet](#part-2-syntax-cheat-sheet)
3. [Scenario-Based Questions & Answers](#part-3-scenario-based-questions--answers)
4. [Configuration Lifecycle Q&A](#part-4-configuration-lifecycle-questions--answers)
5. [Rapid-Fire One-Liners](#part-5-rapid-fire-one-liners)
6. [Common Pitfalls & Debugging](#part-6-common-pitfalls--debugging)
7. [Answers Matrix for Resumes](#part-7-resume-answer-templates)

---

## Part 1: Core Concepts Questions & Answers

### Q1. What is Terraform and what problem does it solve?

**A.** Terraform is HashiCorp's Infrastructure as Code (IaC) tool. It lets you
define infrastructure declaratively in HCL (HashiCorp Configuration Language),
then plan and apply those definitions across providers (AWS, Azure, GCP, etc.).

It solves: manual console clicks -> human error, no reproducibility, no review
of infra changes, no drift visibility. Terraform gives you versioned,
reviewable, reproducible infra with a diff (plan) before change (apply).

---

### Q2. What are the phases of `terraform apply`?

**A.**
1. **init** — downloads providers/modules, configures backend.
2. **validate** — syntax + internal consistency check.
3. **plan** — builds a graph of resources, compares desired state vs current
   state (in state file), outputs an execution plan.
4. **apply** — executes the plan in dependency order (DAG) and updates state.
5. **destroy** — applies a plan that deletes all managed resources.

---

### Q3. What is the difference between `terraform plan` and `terraform apply`?

**A.**
- `plan` is **read-only** — shows what would change, no modifications.
- `apply` actually creates/updates/destroys resources and writes state.
- `terraform apply` without args will re-run a plan interactively. Best
  practice: `terraform plan -out=tfplan` then `terraform apply tfplan` so
  apply uses the exact reviewed plan.

---

### Q4. What is state and why is it important?

**A.** `terraform.tfstate` is the JSON record of every resource Terraform
manages — the mapping between config (`aws_instance.web`) and the real cloud
object ID (`i-0abc123`). Terraform uses it to:
- compute diffs during plan,
- know what to delete on destroy,
- store outputs and metadata.

State is the **source of truth** — without it Terraform can't know what it
owns. This is why you must use a **remote backend** in team environments.

---

### Q5. What is a backend? Compare local vs remote.

| | Local | Remote (e.g., S3 + DynamoDB) |
|---|---|---|
| State file | `terraform.tfstate` on disk | Stored in bucket |
| Team collaboration | Not safe — conflicts | Shared single source of truth |
| Locking | None | DynamoDB lock prevents concurrent runs |
| Drift between machines | Yes | No |

Syntax:
```hcl
terraform {
  backend "s3" {
    bucket         = "valp-terraform-state"
    key            = "infra/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "tf-lock"
    encrypt        = true
  }
}
```

---

### Q6. What is a provider and how is it configured?

**A.** A provider is a plugin that lets Terraform talk to a cloud API (aws,
azurerm, google, etc.). It translates HCL resource blocks into API calls and
tracks state.

```hcl
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"   # allows 5.x, not 6.x
    }
  }
}

provider "aws" {
  region = var.region
}
```

`terraform init` downloads the provider binaries from the registry.

---

### Q7. What are variables and their types in Terraform?

```hcl
variable "env" {
  type        = string
  default     = "staging"
  description = "Environment name"
}

variable "count"       { type = number }
variable "enabled"     { type = bool }
variable "tags"        { type = map(string) }
variable "subnets"     { type = list(string) }
variable "resources"   { type = object({ cpu = number, mem = number }) }
variable "any_value"   { type = any }
```

Set values in order of precedence (lowest to highest):
1. default in `variable` block
2. `terraform.tfvars` / `terraform.tfvars.json`
3. `*.auto.tfvars` (alphabetical)
4. `-var-file=file.tfvars`
5. CLI: `-var="env=production"`
6. Environment variable `TF_VAR_env`

---

### Q8. What is the difference between `locals`, `variables`, and `outputs`?

| | Purpose | Syntax |
|---|---|---|
| `variable` | Input from user/CI | `variable "env" { type = string }` |
| `local` | Computed intermediate values | `local { name = "valp-${var.env}" }` |
| `output` | Expose values to caller/CI | `output "bucket" { value = aws_s3_bucket.b.id }` |

```hcl
locals {
  bucket_name = "valp-${var.env}-data"
}

resource "aws_s3_bucket" "b" {
  bucket = local.bucket_name
}

output "bucket_name" {
  value = aws_s3_bucket.b.id
}
```

---

### Q9. What is a module and why use them?

**A.** A module is a reusable, self-contained folder of `.tf` files with its own
variables and outputs. It's the "function call" of Terraform. Benefits: DRY,
versioned reuse, consistent standards, easier testing.

```hcl
module "web" {
  source  = "github.com/valp/infra//modules/web?ref=v1.2.0"
  env     = var.env
  size    = "t3.micro"
}
```

Use the **root module** (current directory) or **child modules** (every `module`
block). For registry modules pin a version; for git modules pin with `?ref=`.

---

### Q10. What is the resource graph / dependency handling?

**A.** Terraform builds a dependency graph from resource references. Implicit
dependencies come from referencing (`aws_subnet.web.id`). Explicit dependencies
use `depends_on`.

```hcl
resource "aws_instance" "app" {
  depends_on = [aws_db_instance.db]   # explicit even though no reference
}
```

Useful when: wait-for ordering that isn't captured via references, or nullary
resources (e.g., IAM policies that must exist first).

---

### Q11. What is `count` and `for_each`? When do you use each?

| | `count` | `for_each` |
|---|---|---|
| Works with | list (fixed index) | map or set of strings |
| Reference | `aws_x.y[0]` | `aws_x.y["key"]` |
| Deletion behavior | shifting index can destroy wrong resource | safe key-based |
| Best for | simple, numeric sequences | anything with meaningful keys |

```hcl
# count
resource "aws_subnet" "sub" {
  count = length(var.cidrs)
  cidr_block = var.cidrs[count.index]
}

# for_each (map key becomes the identifier)
resource "aws_s3_bucket" "b" {
  for_each = toset(["logs", "data", "tmp"])
  bucket   = "valp-${each.key}"
}
```

Interview tip: `for_each` is preferred when the order could change because it
uses keys not indexes.

---

### Q12. What are data sources?

**A.** `data` blocks read existing infrastructure (or external facts) **without
managing it**. Use to reference resources created outside Terraform or to avoid
duplicating output pls from another stack.

```hcl
data "aws_ami" "ubuntu" {
  most_recent = true
  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-22.04-amd64-server-*"]
  }
  owners = ["099720109477"]
}

resource "aws_instance" "web" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = "t3.micro"
}
```

---

### Q13. What is the difference between `terraform import`, `state mv`, and `state rm`?

| Command | Purpose | Example |
|---|---|---|
| `import` | Bring existing resource under Terraform management | `terraform import aws_s3_bucket.b my-bucket` |
| `state mv` | Re-map state without re-creating (e.g., rename resource, move to module, array index change) | `terraform state mv aws_x.old aws_x.new` |
| `state rm` | Remove a resource from state (Terraform stops managing; cloud object stays) | `terraform state rm aws_x.volatile` |

---

### Q14. How does Terraform handle secrets?

**A.**
- Never commit secrets in `.tf` files or `.tfvars`.
- Use `TF_VAR_*` env vars, GitHub/AWS Secrets, Vault, or a backend with
  encryption (S3 server-side encryption, KMS).
- Mark sensitive outputs so plan/apply doesn't print them:

```hcl
output "db_password" {
  value     = aws_db_instance.db.password
  sensitive = true
}
```

- Consider `sops` for encrypting `.tfvars` at rest.

---

### Q15. What locking mechanism prevents state corruption?

**A.** Remote backends support **state locking**. With S3 + DynamoDB, Terraform
creates a lock item in the DynamoDB table before running plan/apply/destroy and
deletes it after. If another process holds the lock, you get:

```
Error: Error acquiring the state lock
```

A stale lock can be force-cleared (only when you're sure nothing is running):
```sh
terraform force-unlock <LOCK_ID>
```

---

### Q16. What is `terraform validate` vs `terraform plan` vs `terraform fmt`?

| Command | What it checks |
|---|---|
| `terraform fmt` | Formatting/style (whitespace, alignment) — automatable, does not touch logic |
| `terraform validate` | Syntax + internal consistency (no provider/API calls) |
| `terraform plan` | Real diff against actual cloud state — needs init + credentials |
| `terraform tflint` (external) | Best-practice linting rules on top of validate |

---

### Q17. What is Terraform Cloud / Terraform Enterprise?

**A.** HashiCorp's managed platform for Terraform: remote state, remote
plan/apply runs, policy as code (Sentinel/OPA), private module registry,
variable sets, and run triggers. TFE is the self-hosted version for enterprises.

---

### Q18. How do you migrate between backends?

**A.** Use `terraform init -migrate-state` when the backend block changes:
```sh
terraform init -migrate-state
```
Interactive prompt copies state to the new backend. Use `-force-copy` in CI to
skip the prompt.

---

## Part 2: Syntax Cheat Sheet

### Lifecycle

```hcl
resource "aws_instance" "web" {
  ami           = "ami-123"
  instance_type = "t3.micro"

  lifecycle {
    create_before_destroy = true   # create new before deleting old
    prevent_destroy       = true   # block accidental deletion
    ignore_changes        = [tags] # ignore out-of-band tag changes
  }
}
```

### Conditionals & dynamic blocks

```hcl
resource "aws_instance" "web" {
  instance_type = var.env == "prod" ? "t3.large" : "t3.micro"

  dynamic "tag" {
    for_each = var.extra_tags
    content {
      key   = tag.key
      value = tag.value
    }
  }
}
```

### Functions

```terraform
lower("VALP")          # "valp"
upper("valp")          # "VALP"
join("-", ["a","b"])   # "a-b"
split("-", "a-b")      # ["a","b"]
length(["a","b"])      # 2
element(["a","b"], 0)  # "a"
lookup(map, "k", "default")
fileset("${path.module}/px", "*.conf")
merge(map1, map2)      # combine maps
cidrsubnet("10.0.0.0/16", 8, 1)  # "10.0.0.0/24"
```

### Providers (multi-region / alias)

```hcl
provider "aws" {
  alias  = "west"
  region = "us-west-2"
}

resource "aws_instance" "west" {
  provider = aws.west
}
```

### Provisioners (last resort — prefer data sources / remote-exec rarely)

```hcl
resource "null_resource" "run" {
  provisioner "local-exec" {
    command = "echo ${self.id}"
  }
}
```

### Terragrunt wrapper (if mentioned)

```hcl
terraform {
  source = "../../modules/vpc"
}

inputs = {
  env    = "prod"
  region = "us-east-1"
}

remote_state {
  backend = "s3"
  config = {
    bucket = "valp-tfstate"
    key    = "${path_relative_to_include()}/terraform.tfstate"
  }
}
```

---

## Part 3: Scenario-Based Questions & Answers

### S1. "An engineer manually created an S3 bucket in AWS. Now they want it managed by Terraform. What do you do?"

**A.**
1. Write the matching `aws_s3_bucket` config.
2. `terraform import aws_s3_bucket.b bucket-name`
3. Run `terraform plan` — it should show a **clean or minimal diff**, not
   deletion. If it wants to delete settings, tweak config / `ignore_changes`.
4. Apply. The bucket is now managed; future changes flow through Terraform.

```sh
terraform import aws_s3_bucket.data valp-data-bucket
```

---

### S2. "Two engineers ran `terraform apply` at the same time and state got corrupted / a lock error appeared."

**A.**
- With S3 + DynamoDB locking this is prevented. Investigate who holds the lock.
- Verify no run is actually in progress (check terminal/CI logs), then
  `terraform force-unlock <LOCK_ID>`.
- Root fix: always use remote backend + locking + CI to serialize? apply (or
  `-lock-timeout=300s` to wait rather than fail).

---

### S3. "You changed a resource's name (e.g., bucket). Terraform plan wants to destroy the old one and create a new one with data loss risk."

**A.**
- If the tool supports it, prefer rename option: S3 supports `force_destroy`
  only for contents — the bucket itself can often be renamed in place.
- General solution: avoid renames of stateful resources; use `terraform state mv`
  to remap:
  ```sh
  terraform state mv 'aws_s3_bucket.old' 'aws_s3_bucket.new'
  ```
  Then fix config and plan again — it should show a no-op or minor diff.
- If resources must be recreated, plan a **destroy/create** strategy with
  `create_before_destroy` coalesced with a migration window.

---

### S4. "A resource drifted — someone changed the security group rules in the console. How do you detect and fix?"

**A.**
1. Detect: `terraform plan` shows the diff between state and reality.
2. Fix: `terraform apply` re-applies desired config (options: revert console
   change) — or if the console change is desired, update config to match.
3. Prevent: enable **drift detection alerts** (AWS Config rules), restrict
   console IAM permissions, and treat console as "read-only".

---

### S5. "Your CI/CD workflow must not fail mid-way when many resources depend on each other. How does Terraform handle ordering / failures?"

**A.**
- Terraform builds a **DAG**; resources with dependencies wait.
- `-parallelism` controls concurrent operations (`terraform apply -parallelism=10`).
- On failure, apply stops; re-run `terraform apply` (with `-auto-approve` in CI)
  to continue/complete — apply is **idempotent** and resumes from state.
- Use `create_before_destroy` to reduce downtime for replacements.

---

### S6. "You must roll back a bad deployment. How with IaC?"

**A.**
- **State rollback (preferred):** restore the previous state file from the S3
  versioning history / Terraform Cloud, then `terraform apply` to rebuild it.
- **Config rollback:** revert the PR, re-apply — Terraform reconciles to the
  last good config.
- For app code (not infra): deploy previous Docker image / commit — infra
  (as long as versions are parameterized) stays untouched.
- Best: tag state versions and enable versioning on the state bucket.

---

### S7. "Which backend would you pick for a stateful production AWS workload and why?"

**A.** **S3 with DynamoDB locking, versioning, and encryption.**

```hcl
terraform {
  backend "s3" {
    bucket         = "valp-terraform-state-prod"
    key            = "prod/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "tfstate-locks"
    encrypt        = true
  }
}
```
Why: shared team access, locking, version history (rollback), encryption,
and cheap. Terraform Cloud is the higher-governance alternative.

---

### S8. "A team needs identical VPC + subnets across 5 environments. How do you structure it?"

**A.** A module with parameters:

```hcl
module "vpc" {
  source = "./modules/vpc"
  env    = each.key
  cidr   = var.cidrs[each.key]
}

variable "cidrs" {
  type = map(string)
  default = {
    dev  = "10.0.0.0/16"
    stg  = "10.1.0.0/16"
    prd  = "10.2.0.0/16"
  }
}
```
Call from a config per environment folder (or Terragrunt for DRY inputs):

```
infra/
  environments/
    dev/     main.tf, backend.hcl, tfvars
    staging/ main.tf, backend.hcl, tfvars
    prod/    main.tf, backend.hcl, tfvars
```

---

### S9. "Your CI/CD must apply an environment only when its plan passes review. How do you do this?"

**A.** Split plan and apply into separate jobs/steps. Save the plan artifact in
plan, review via PR comments or approvals (Terraform Cloud run approvals /
GitHub environment protection rules), then apply using the saved plan:

```sh
terraform plan -out=tfplan
# ... review ...
terraform apply tfplan
```
In GitHub Actions, grant apply job `environment: production` with required
reviewers — the job is gated.

---

### S10. "A module needs to compute a VPC ID that exists in another Terraform stack. How do you share it?"

**A.**
- **Option 1 — Data source reading remote state:**
  ```hcl
  data "terraform_remote_state" "vpc" {
    backend = "s3"
    config = {
      bucket = "valp-tfstate"
      key    = "network/terraform.tfstate"
      region = "us-east-1"
    }
  }
  # vpc_id = data.terraform_remote_state.vpc.outputs.vpc_id
  ```
- **Option 2 — share via outputs + a config/database** (SSM Parameter Store
  `aws_ssm_parameter`, or a central config.
- Data-source cross-stack reads are the standard pattern; beware it creates a
  coupling — run dependency stack first.

---

### S11. "How do you version modules and keep environments on fixed versions?"

**A.** Pin module sources:

```hcl
module "web" {
  source = "github.com/valp/terraform-modules//web?ref=v1.4.2"
}
```
- Git tags (`?ref=v1.4.2`) or registry module versions.
- Use a module registry, review `modules` update as a PR, and bump versions
  deliberately per environment rather than auto-latest on all.

---

### S12. "An entire apply failed at resource 40 of 100. What do you do?"

**A.**
1. Read the error; fix root cause (config or dependency).
2. Re-run `terraform plan` then `terraform apply` — Terraform works off state,
   so it only does remaining work; already-created resources are untouched
   (they're in state).
3. If a resource is in a half-state, re-apply may need `terraform state mv` or
   targeted apply: `terraform apply -target=aws_x.broken`.

---

### S13. "You need to provision the same config but each module call slightly different values."

**A.** Use `for_each` on the module:

```hcl
module "team_s3" {
  for_each = var.teams
  source   = "./modules/s3"
  name     = "valp-${each.key}"
  policy   = each.value
}
```
Each module instance is addressed as `module.team_s3["sales"]`.

---

### S14. "How do you destroy only a subset of infra (e.g., the ECS cluster, not the DB)? What are the dangers?"

**A.**
- Targeted: `terraform destroy -target=aws_ecs_cluster.main`
- Or `terraform state rm` / use separate stacks (split infra so each has its own
  lifecycle).
- Dangers: targeted destroy can break dependent resources or leave orphaned
  references; always run a `plan` first to review exactly what will go.

---

### S15. "Your provider API is rate-limited during big applies. How do you overcome it?"

**A.**
- Reduce parallelism: `terraform apply -parallelism=5`
- Add retry logic / retryable errors (Terraform retries 429/5xx by default).
- Split the run across targeted applies or time the release.
- Use provider `retry` settings / increase `max_retries` in provider blocks
  where supported.

---

### S16. "GitHub Actions runs `terraform plan` but you want the diff inside a PR comment."

**A.** Use `terraform-plan-commenter` or store the plan output; simplest is:

```yaml
- name: Plan
  id: plan
  run: |
    export TF_VAR_env=${{ github.ref_name }}
    terraform plan -no-color -out=tfplan 2>&1 | tee plan.txt
  env:
    AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
    AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
```

Later: parse `plan.txt` with the `dflook/terraform-plan` action or
`hashicorp/terraform-github-actions`, which posts the plan to the PR.

---

## Part 4: Configuration Lifecycle Questions & Answers

### Q19. What happens on `terraform init`?

**A.** Downloads provider plugins and modules, initializes the backend
(state location), creates `.terraform/` directory. Can be run repeatedly; safe.

### Q20. `terraform refresh` — what is it?

**A.** Updates state against real infra **without changing resources** (no
config change). Modern Terraform (0.15+) uses `terraform apply -refresh-only`.

```sh
terraform apply -refresh-only
```

### Q21. What are workspaces? When do you prefer workspaces vs folders?

**A.** Workspaces give multiple named state files for the same config:

```sh
terraform workspace new dev
terraform workspace select dev
```
- Workspaces: quick env splits, same structure, but hard to attribute resources
  per env later; state key auto-appends workspace name.
- Folders (`dev/`, `prod/` separate dirs): preable for big differences in config
  or strict separation of state & permissions. Prefer folders in production.

### Q22. How do you handle secrets in plan/apply logs?

**A.** Mark outputs `sensitive = true`; use `-no-color` to avoid ANSI noise;
never log `TF_VAR_secret`; use vault/secret managers and reference by ID
(`data.aws_secretsmanager_secret_version.x.secret_string`).

### Q23. What does `-auto-approve` do and why is it risky?

**A.** Skips the confirmation prompt:
```sh
terraform apply -auto-approve
```
Risk: validates state changes without human review. Only use in CI after a plan
+ review stage — never for manual prod consoles.

---

## Part 5: Rapid-Fire One-Liners

| Question | Short answer |
|---|---|
| What's HCL? | HashiCorp Configuration Language — Terraform DSL |
| `init`? | Downloads providers/modules, configures backend |
| `plan`? | Read-only diff (desired vs current/state) |
| `apply`? | Executes plan, writes state |
| `destroy`? | Removes all managed resources |
| `validate`? | Static syntax check |
| `fmt`? | Auto-formatting |
| `refresh`? | Sync state to real infra |
| `import`? | Adopt existing resource into state |
| `state`? | JSON file = source of truth for managed resources |
| Backend? | Where state is stored (local / S3 / Terraform Cloud) |
| State lock? | Prevents concurrent runs from corrupting state |
| Provider? | Plugin to talk to a cloud API |
| Module? | Reusable folder of tf code with vars/outputs |
| Data source? | Read existing resources, don't manage them |
| `count` vs `for_each` | Index vs key-based multiple instances |
| `create_before_destroy` | Replacement strategy to reduce downtime |
| `prevent_destroy` | Guard against accidental deletion |
| `ignore_changes` | Ignore selected attributes for drift |
| `depends_on` | Explicit ordering between resources |
| Sensitive output? | Hides value in plan/apply (`sensitive = true`) |
| Workspace? | Multiple state files for same config |
| `TF_VAR_x`? | Env var to set variable `x` |
| `-var-file` | Load values from a tfvars file |
| `terraform force-unlock` | Remove a stale state lock |
| Sentinel/OPA? | Policy as code gates for Terraform Cloud |

---

## Part 6: Common Pitfalls & Debugging

| Symptom | Root cause / fix |
|---|---|
| `Error acquiring the state lock` | Concurrent run / stale lock → `force-unlock` after verifying |
| `Invalid function call` | Wrong syntax: use `()` not `=` for functions in expressions |
| `Cycle: ...` dependency loop | Remove circular refs; restructure with locals/data instead of `depends_on` |
| Plan wants to replace a resource you didn't change | `ignore_changes` or a provider bump changed schema; read diff |
| `Resource not found` on apply | Resource deleted outside Terraform; re-import or recreate |
| `Error: ... not found` on `init` | Wrong AWS creds / missing backend bucket |
| Changes always showing in plan (drift) | Someone (or config) touches resources → restrict IAM, use `ignore_changes` |
| State corrupted during apply | Restore from S3 versioned backup; fix locking |
| Provider version mismatch | Pin `required_providers` versions; `terraform init -upgrade` deliberately |

---

## Part 7: Resume Answer Templates

### "Tell me about a Terraform project you managed."
- State what: multi-env infra (S3, VPC, ECS) with modules.
- State how: remote S3 + DynamoDB state, module per component, CI/CD plans via
  GitHub Actions.
- State win: self-service env provisioning, reduced setup from days to minutes,
  PR-reviewable infra, rollback via state versioning.

### "What would you improve in a new Terraform adoption?"
- Remote state + lock on day one.
- Module library + version pinning.
- PR plan/comment workflow so everyone reviews infra like code.
- Policy gates (Sentinel/OPA) + drift detection.
- Split state per environment for blast-radius control.

---

*Practice tips: run `terraform init && plan && apply` against free-tier AWS/Azure,
create a module, import an existing resource, corrupt a state file, and restore
it from versioning. Interviewers love candidates who can demo recovery flows.*