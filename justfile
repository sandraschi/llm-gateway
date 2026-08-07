set windows-shell := ["powershell.exe", "-NoProfile", "-Command"]

default: serve

serve:
    uv run llm-gateway

install:
    uv sync

# Bootstrap: install dev deps + pre-commit hook
bootstrap:
    uv sync --group dev
    uv run pre-commit install
    Write-Host "Pre-commit hooks installed." -ForegroundColor Green