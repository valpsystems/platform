# VALP SYSTEMS — Infrastructure as Code (IaC) Interview Guide

> Side-by-side Q&A covering **Terraform**, **Terragrunt**, **CloudFormation**
> and **Bicep**. Each answer shows one Terraform syntax first, then the
> equivalent in the other tools.

---

## Quick Reference — Concepts Across Tools

| Concept | Terraform | Terragrunt | CloudFormation | Bicep |
|---------|-----------|------------|----------------|-------|
| **Language** | HCL (`.tf`) | HCL (`.hcl`) | JSON / YAML (`.json`/`.yaml`) | Bicep DSL (`.bicep`) |
| **State** | Local or remote (S3, etc.) | Remote (S3 + DynamoDB lock) | Managed by AWS (stack state) | Managed by Azure (resource group) |
| **Module reuse** | `module` block + directory | `terraform { source = }` in config | Nested Stacks / Modules | `module` declaration |
| **Parameterization** | `variable` + `terraform.tfvars` | `inputs = { }` in `terragrunt.hcl` | `Parameters` + `Ref` | `param` / `var` |
| **Plan before apply** | `terraform plan` / `apply` | `terragrunt plan` / `apply` | Change Set or direct deploy | `what-if` preview |
| **Drift detection** | `terraform plan` (diff) | `terragrunt plan` | Drift Detection API | `what-if` |
| **Environments** | Workspaces or folder layout | Folder strategy (`env.hcl`) | Separate stacks | Resource scopes / modules |
| **DAG / dependencies** | `depends_on` | `dependency` blocks | Implicit (logical IDs) or `DependsOn` | Implicit or `depends` keyword |

---

## Questions & Answers

### 1. What is IaC and why use it?

**A.** Infrastructure as Code defines and provisions resources via versioned
configuration files instead of manual clicks. Benefits: reproducibility,
reviewability (PRs), drift detection, roll-back and documentation-in-code.

---

### 2. Resource definition — Terraform

```hcl
provider "aws" {
  region = "us-east-1"
}

resource "aws_s3_bucket" "data" {
  bucket = "valp-data-bucket"
  tags   = { Environment = "production" }
}
```

### Resource definition — CloudFormation

```yaml
Resources:
  DataBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: valp-data-bucket
      Tags:
        - Key: Environment
          Value: production
```

### Resource definition — Bicep

```bicep
param location string = resourceGroup().location

resource dataBucket 'Microsoft.Storage/storageAccounts@2023-01-01' = {
  name: 'valpdataprod'
  location: location
  kind: 'StorageV2'
  sku: { name: 'Standard_LRS' }
  tags: { Environment: 'production' }
}
```

### Resource definition — Terragrunt

Terragrunt wraps Terraform — the resource block above stays identical;
`terragrunt.hcl` adds remote state config:

```hcl
remote_state {
  backend = "s3"
  config = {
    bucket = "valp-terraform-state"
    key    = "${path_relative_to_include()}/terraform.tfstate"
    region = "us-east-1"
  }
}
```

---

### 3. Variables and parameters

**Terraform (`variables.tf`):**

```hcl
variable "env" {
  type        = string
  default     = "staging"
  description = "Environment name"
}

resource "aws_s3_bucket" "this" {
  bucket = "valp-${var.env}"
}
```

`terraform.tfvars`:
```
env = "production"
```

**CloudFormation:**

```yaml
Parameters:
  Env:
    Type: String
    Default: staging

Resources:
  DataBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !Sub "valp-${Env}"
```

**Bicep:**

```bicep
@allowed(['staging', 'production'])
param env string = 'staging'

resource dataBucket 'Microsoft.Storage/storageAccounts@2023-01-01' = {
  name: 'valp${env}'
  location: resourceGroup().location
  kind: 'StorageV2'
  sku: { name: 'Standard_LRS' }
}
```

**Terragrunt — inputs:**

```hcl
inputs = {
  env = "production"
}
```

---

### 4. Outputs / Exports

**Terraform:**

```hcl
output "bucket_arn" {
  value = aws_s3_bucket.this.arn
}
```

**CloudFormation:**

```yaml
Outputs:
  BucketArn:
    Value: !Ref DataBucket
    Export:
      Name: DataBucketArn
```

**Bicep:**

```bicep
output bucketName string = dataBucket.name
```

**Terragrunt:** outputs come from Terraform; Terragrunt can read them with
`dependency {}` blocks.

---

### 5. Modules / Reusable components

**Terraform (`modules/s3-bucket/main.tf`):**

```hcl
variable "name" { type = string }

resource "aws_s3_bucket" "this" {
  bucket = var.name
}
```

Caller:

```hcl
module "data_bucket" {
  source = "./modules/s3-bucket"
  name   = "valp-data"
}
```

**CloudFormation (Nested Stack):**

```yaml
Resources:
  DataStack:
    Type: AWS::CloudFormation::Stack
    Properties:
      TemplateURL: https://s3.amazonaws.com/my-templates/s3-bucket.yaml
      Parameters:
        BucketName: valp-data
```

**Bicep module (`modules/s3.bicep`):**

```bicep
param name string
resource bucket 'Microsoft.Storage/storageAccounts@2023-01-01' = {
  name: name
  location: resourceGroup().location
  kind: 'StorageV2'
  sku: { name: 'Standard_LRS' }
}
```

Caller:

```bicep
module dataBucket './modules/s3.bicep' = {
  name: 'dataBucket'
  params: { name: 'valp-data' }
}
```

**Terragrunt:**

```hcl
terraform {
  source = "../modules/s3-bucket"
}

inputs = {
  name = "valp-data"
}
```

---

### 6. Dependencies & ordering

**Terraform (`depends_on`):**

```hcl
resource "aws_iam_role" "ecs" {
  name = "ecs-role"
}

resource "aws_ecs_task_definition" "app" {
  depends_on = [aws_iam_role.ecs]
  # ...
}
```

**CloudFormation (explicit or implicit):**

```yaml
Resources:
  AppTask:
    Type: AWS::ECS::TaskDefinition
    DependsOn: EcsRole          # explicit
  EcsRole:
    Type: AWS::IAM::Role
```

**Bicep (implicit or explicit `depends`):**

```bicep
resource ecsRole 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: 'ecs-role'
}
resource app 'Microsoft.ContainerInstance/containerGroups@2023-05-01' = {
  name: 'app'
  depends: [ ecsRole ]
}
```

**Terragrunt (dependency blocks):**

```hcl
dependency "ecs_role" {
  config_path = "../ecs-role"
}

inputs = {
  ecs_role_arn = dependency.ecs_role.outputs.arn
}
```

---

### 7. Environments strategy

**Terraform — folders:**

```
infra/
  modules/
  envs/
    staging/       # backend.hcl + *.tf
    production/    # backend.hcl + *.tf
```

**Terragrunt — `env.hcl`:**

```
infra/
  envs/
    staging/
      terragrunt.hcl    # includes common env.hcl
    production/
      terragrunt.hcl
```

**CloudFormation — separate stacks:**

One stack per environment (parametrised or duplicated templates).

**Bicep — resource scopes + modules:**

Deploy modules into different resource groups or subscriptions per environment,
or use parameter files per environment.

---

### 8. State management

| Tool | State |
|------|-------|
| **Terraform** | Local file by default; remote backends: S3+DynamoDB, Terraform Cloud, Azure Blob |
| **Terragrunt** | Always remote — configures Terraform remote_state (S3 + DynamoDB lock) |
| **CloudFormation** | Managed by AWS per stack (no files to manage) |
| **Bicep** | Managed by Azure per deployment / resource group |

**Terraform remote backend (S3):**

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

### 9. Plan / preview before apply

| Tool | Command |
|------|---------|
| **Terraform** | `terraform plan` then `terraform apply` |
| **Terragrunt** | `terragrunt plan` then `terragrunt apply` |
| **CloudFormation** | Create a Change Set to preview, then Execute |
| **Bicep** | `az deployment group what-if --template-file main.bicep` |

---

### 10. Destroying / teardown

| Tool | Command |
|------|---------|
| **Terraform** | `terraform destroy` |
| **Terragrunt** | `terragrunt destroy` |
| **CloudFormation** | Delete stack via console/CLI |
| **Bicep** | `az group delete` or delete individual resources |

---

### 11. Drift detection — what changed outside IaC?

- **Terraform / Terragrunt:** `plan` shows diff between state and real infra.
- **CloudFormation:** Enable **Drift Detection** on the stack; review in console.
- **Bicep:** `what-if` compares template to deployed resources; or use Azure
  Policy for continuous compliance.

---

### 12. Sample: S3 bucket + IAM role together

**Terraform:**

```hcl
resource "aws_s3_bucket" "data" {
  bucket = "valp-data"
}

resource "aws_iam_user" "deployer" {
  name = "deployer"
}

resource "aws_iam_user_policy_attachment" "s3" {
  user       = aws_iam_user.deployer.name
  policy_arn = "arn:aws:iam::policy/AmazonS3FullAccess"
}
```

**CloudFormation:**

```yaml
Resources:
  DataBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: valp-data
  DeployerUser:
    Type: AWS::IAM::User
    Properties:
      UserName: deployer
  DeployerPolicy:
    Type: AWS::IAM::UserPolicyAttachment
    Properties:
      UserName: !Ref DeployerUser
      PolicyArn: arn:aws:iam::policy/AmazonS3FullAccess
```

**Bicep (Azure Storage + role):**

```bicep
param location string = resourceGroup().location

resource storage 'Microsoft.Storage/storageAccounts@2023-01-01' = {
  name: 'valpdata'
  location: location
  kind: 'StorageV2'
  sku: { name: 'Standard_LRS' }
}

resource role 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(storage.id)
  scope: storage
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', 'ba92f5b4-2d11-453d-a403-e96b0029c9fe')
    principalId: '<managed-identity-principal-id>'
  }
}
```

---

### 13. CI/CD integration tips

| Step | What to run |
|------|-------------|
| Validate | `terraform validate` / `cfn-lint` / `az bicep build-params` |
| Plan | `terraform plan -out=tfplan` / Change Set / `az deployment group what-if` |
| Apply | `terraform apply tfplan` / execute Change Set / `az deployment group create` |
| Secrets | Never commit; use GitHub Secrets, Vault, or cloud KMS; pass via env vars |

**GitHub Actions sample (Terraform):**

```yaml
- uses: hashicorp/setup-terraform@v3
  with:
    terraform_version: "1.7"

- run: terraform init
- run: terraform validate
- run: terraform plan -out=tfplan
- run: terraform apply tfplan
```

---

### 14. Debugging IaC issues

| Symptom | Check |
|---------|-------|
| `Error: Error acquiring the state lock` | DynamoDB lock stuck (Terraform) or another run in progress |
| `Error: Invalid function call` | HCL syntax: use `()` for functions, not `=` |
| `Circular dependency` | Use `depends_on` sparingly; restructure resource refs |
| Stack create fails | Read CloudFormation event history in console |
| `what-if` shows unexpected changes | Compare current resource properties vs template; check `location` defaults |

---

### 15. When to use which tool?

| Scenario | Best fit |
|----------|----------|
| AWS-only, team already uses AWS | CloudFormation (native, free, deep AWS integration) |
| Multi-cloud or existing Terraform skills | Terraform + Terragrunt |
| Azure-only, .NET team | Bicep (native Azure, no state files, great IDE support) |
| Small team, many environments | Terragrunt folder strategy (DRY configs) |
| Enterprise, state governance | Terraform Cloud / Enterprise + policy as code |

---

### 16. One-liner rapid-fire

| Question | Answer |
|----------|--------|
| Terraform `terraform init` does what? | Downloads providers and initializes backend |
| `terraform plan` vs `apply`? | Plan shows diff; apply makes changes |
| Terragrunt wraps what? | Terraform — same HCL resources, adds DRY configs |
| CloudFormation stack policy? | Prevents accidental deletion/update of critical resources |
| Bicep param vs var? | `param` is input; `var` is a local computed value |
| Terraform module version pinning? | `source = "git::https://...?ref=v1.2"` |
| `import` in Terraform? | Bring existing infra under management |
| CloudFormation drift detection? | API that diffs real vs template state |
| Bicep what-if vs plan? | Both preview changes; what-if shows per-property diffs |
| Remote state lock purpose? | Prevents concurrent runs from overwriting state |
