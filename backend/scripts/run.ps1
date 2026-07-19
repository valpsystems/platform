# VALP SYSTEMS Backend - Run Script (PowerShell)
# Usage: .\scripts\run.ps1 [dev|prod]

param(
    [string]$Mode = "dev"
)

$Env:APP_ENV = if ($Mode -eq "prod") { "production" } else { "development" }
$Env:APP_DEBUG = if ($Mode -eq "prod") { "false" } else { "true" }

Write-Host "Starting VALP SYSTEMS Backend ($Mode mode)" -ForegroundColor Green

if ($Mode -eq "prod") {
    uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
} else {
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
}
