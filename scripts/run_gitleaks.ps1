param(
  [string]$Config = ".gitleaks.toml",
  [switch]$StagedOnly
)

$ErrorActionPreference = "Stop"

$Bin = Join-Path $PSScriptRoot "gitleaks"
$IsWin = $IsWindows -or $PSVersionTable.OS -match "Windows"

Write-Host "Downloading gitleaks binary..."
$Url = if ($IsWin) { "https://github.com/gitleaks/gitleaks/releases/latest/download/gitleaks_Windows_x86_64.zip" } else { "https://github.com/gitleaks/gitleaks/releases/latest/download/gitleaks_linux_x64.tar.gz" }
$Tmp = New-Item -ItemType Directory -Force -Path (Join-Path $env:TEMP "gitleaks-dl")
$ZipPath = Join-Path $Tmp "gitleaks.zip"

Invoke-WebRequest -Uri $Url -OutFile $ZipPath -UseBasicParsing

if ($IsWin) {
  Expand-Archive -Path $ZipPath -DestinationPath $Tmp -Force
  Copy-Item (Join-Path $Tmp "gitleaks.exe") $Bin -Force
} else {
  tar -xzf $ZipPath -C $Tmp
  Copy-Item (Join-Path $Tmp "gitleaks") $Bin -Force
  chmod +x $Bin
}

$CliArgs = @("detect", "--no-banner", "--redact", "--report-format", "sarif", "--report-path", "gitleaks.sarif", "--config-path", $Config)
if ($StagedOnly) { $CliArgs += @("--staged") }

& $Bin @CliArgs
$Exit = $LASTEXITCODE

if ($Exit -ne 0) {
  Write-Warning "Gitleaks found issues. See gitleaks.sarif and gitleaks.log"
}

exit 0 # report-only mode
