# Compare two security scan outputs (CycloneDX SBOM JSON and optional SARIF) and print a concise delta
# Usage examples:
#   pwsh ./scripts/compare_security_artifacts.ps1 -OldSbom .\container-scan-backend\sbom-backend-old.json -NewSbom .\container-scan-backend\sbom-backend.json
#   pwsh ./scripts/compare_security_artifacts.ps1 -OldSarif .\container-scan-backend\trivy-backend-old.sarif -NewSarif .\container-scan-backend\trivy-backend.sarif

[CmdletBinding()]
param(
  [Parameter(Mandatory=$false)] [string]$OldSbom,
  [Parameter(Mandatory=$false)] [string]$NewSbom,
  [Parameter(Mandatory=$false)] [string]$OldSarif,
  [Parameter(Mandatory=$false)] [string]$NewSarif
)

function Read-Json($path) {
  if (-not $path -or -not (Test-Path $path)) { return $null }
  try { Get-Content -Raw -Path $path | ConvertFrom-Json -ErrorAction Stop } catch { return $null }
}

Write-Host "== Compare Security Artifacts ==" -ForegroundColor Cyan

if ($OldSbom -and $NewSbom) {
  Write-Host "\n[SBOM] Comparing: `n  OLD: $OldSbom`n  NEW: $NewSbom" -ForegroundColor Yellow
  $old = Read-Json $OldSbom
  $new = Read-Json $NewSbom
  if ($null -eq $old -or $null -eq $new) {
    Write-Host "SBOM parse error. Skipping SBOM diff." -ForegroundColor Red
  }
  else {
    $oldComps = @{}
    foreach ($c in ($old.components | Where-Object { $_.name })) {
      $key = ($c.name + '|' + ($c.version ?? ''))
      $oldComps[$key] = $true
    }
    $newComps = @{}
    foreach ($c in ($new.components | Where-Object { $_.name })) {
      $key = ($c.name + '|' + ($c.version ?? ''))
      $newComps[$key] = $true
    }
    $removed = @()
    foreach ($k in $oldComps.Keys) { if (-not $newComps.ContainsKey($k)) { $removed += $k } }
    $added = @()
    foreach ($k in $newComps.Keys) { if (-not $oldComps.ContainsKey($k)) { $added += $k } }

    Write-Host "SBOM: Removed components (old → not in new):" -ForegroundColor Green
    if ($removed.Count -eq 0) { Write-Host "  (none)" } else { $removed | Sort-Object | ForEach-Object { Write-Host "  $_" } }

    Write-Host "SBOM: Added components (new only):" -ForegroundColor Green
    if ($added.Count -eq 0) { Write-Host "  (none)" } else { $added | Sort-Object | ForEach-Object { Write-Host "  $_" } }
  }
}

if ($OldSarif -and $NewSarif) {
  Write-Host "\n[SARIF] Comparing: `n  OLD: $OldSarif`n  NEW: $NewSarif" -ForegroundColor Yellow
  $old = Read-Json $OldSarif
  $new = Read-Json $NewSarif
  if ($null -eq $old -or $null -eq $new) {
    Write-Host "SARIF parse error. Skipping SARIF diff." -ForegroundColor Red
  }
  else {
    function Extract-Alerts($sarif) {
      $alerts = @()
      foreach ($run in ($sarif.runs)) {
        foreach ($res in ($run.results)) {
          $ruleId = $res.ruleId
          $sev = $res.level
          $msg = $res.message.text
          if (-not $ruleId) { $ruleId = ($res.rule?.id) }
          $alerts += ("${ruleId}|${sev}|" + ($msg -replace '\s+', ' ') )
        }
      }
      return $alerts
    }
    $oldA = Extract-Alerts $old
    $newA = Extract-Alerts $new
    $oldSet = [System.Collections.Generic.HashSet[string]]::new($oldA)
    $newSet = [System.Collections.Generic.HashSet[string]]::new($newA)

    $removed = $oldA | Where-Object { -not $newSet.Contains($_) }
    $added   = $newA | Where-Object { -not $oldSet.Contains($_) }

    Write-Host "SARIF: Removed alerts:" -ForegroundColor Green
    if (-not $removed) { Write-Host "  (none)" } else { $removed | Sort-Object | ForEach-Object { Write-Host "  $_" } }
    Write-Host "SARIF: Added alerts:" -ForegroundColor Green
    if (-not $added) { Write-Host "  (none)" } else { $added | Sort-Object | ForEach-Object { Write-Host "  $_" } }
  }
}

if (-not ($OldSbom -or $NewSbom -or $OldSarif -or $NewSarif)) {
  Write-Host "No inputs provided. Use -OldSbom/-NewSbom and/or -OldSarif/-NewSarif." -ForegroundColor DarkYellow
}
