<#
.SYNOPSIS
    LABREX Database Operations Automation Script for PowerShell.

.DESCRIPTION
    Provides standardized, repeatable operations for migrations, seeding,
    diagnostics, and automated test execution against the LABREX PostgreSQL instance.
    Enforces strict FAIL-FAST behavior on any command failure.
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory = $true, Position = 0)]
    [ValidateSet("migrate", "current", "seed", "test", "check")]
    [string]$Action
)

$ErrorActionPreference = "Stop"
$RepoRoot = Split-Path -Parent $PSScriptRoot
Set-Location -Path $RepoRoot

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " LABREX Database Operations CLI [Action: $Action]" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

$env:PYTHONPATH = $RepoRoot

function Assert-LastExitCode {
    param([string]$StepName)
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[-] ERROR: $StepName failed with exit code $LASTEXITCODE. Aborting." -ForegroundColor Red
        exit $LASTEXITCODE
    }
}

switch ($Action) {
    "migrate" {
        Write-Host ">> Executing Alembic migrations: alembic upgrade head..." -ForegroundColor Green
        alembic upgrade head
        Assert-LastExitCode "Alembic migration (alembic upgrade head)"

        Write-Host ">> Migration complete. Active revision:" -ForegroundColor Green
        alembic current
        Assert-LastExitCode "Checking revision (alembic current)"
    }

    "current" {
        Write-Host ">> Checking current active migration revision..." -ForegroundColor Green
        alembic current
        Assert-LastExitCode "alembic current"
    }

    "seed" {
        Write-Host ">> Executing idempotent reference and fixture seed..." -ForegroundColor Green
        python -m backend.app.services.data.seed_runner
        Assert-LastExitCode "Database seed runner"
        Write-Host ">> Seed completed successfully." -ForegroundColor Green
    }

    "test" {
        Write-Host ">> Running backend test suite with pytest..." -ForegroundColor Green
        pytest backend/tests -v
        Assert-LastExitCode "Test suite execution"
        Write-Host ">> All tests passed successfully." -ForegroundColor Green
    }

    "check" {
        Write-Host ">> Checking database connectivity, extensions, and migration revision..." -ForegroundColor Green
        python scripts/db_check.py
        Assert-LastExitCode "Database check (scripts/db_check.py)"
        Write-Host ">> Database check passed." -ForegroundColor Green
    }
}
