# Vercel production cutover
# Run from repo root after: npx vercel login

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot\..

Write-Host "JG Mart — Vercel cutover" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Ensure Vercel Dashboard → Settings → Git → Root Directory is EMPTY (repo root)"
Write-Host "2. Linking project..."
npx vercel link --yes 2>$null
if ($LASTEXITCODE -ne 0) {
  Write-Host "Run: npx vercel login" -ForegroundColor Yellow
  exit 1
}

Write-Host "3. Deploying production..."
npx vercel --prod --yes
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host ""
Write-Host "Verify:" -ForegroundColor Green
@(
  "https://jg-mart.vercel.app/",
  "https://jg-mart.vercel.app/src/web/catalog/defaults.js",
  "https://jg-mart.vercel.app/dashboard",
  "https://jg-mart.vercel.app/admin"
) | ForEach-Object { Write-Host "  $_" }
