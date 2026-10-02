[CmdletBinding()]
param()
$ErrorActionPreference = 'Stop'
$projectRoot = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$metadataPath = Join-Path $projectRoot 'data\service.json'
try {
    if (-not (Test-Path -LiteralPath $metadataPath -PathType Leaf)) { Write-Host 'No repository service is recorded.'; exit 0 }
    $metadata = Get-Content -LiteralPath $metadataPath -Raw | ConvertFrom-Json
    $hasher = [System.Security.Cryptography.SHA256]::Create()
    try { $repositoryHash = ([BitConverter]::ToString($hasher.ComputeHash([Text.Encoding]::UTF8.GetBytes($projectRoot.ToLowerInvariant())))).Replace('-', '').ToLowerInvariant() }
    finally { $hasher.Dispose() }
    if ($metadata.application -ne 'pct-daily-dossiers' -or $metadata.protocol_version -ne 1 -or $metadata.repository_id -ne $repositoryHash) { throw 'The recorded service does not belong to this repository. No shutdown was attempted.' }
    $servicePort = [int]$metadata.port
    if ($servicePort -lt 1 -or $servicePort -gt 65535) { throw 'The recorded service port is invalid.' }
    $serviceUrl = "http://127.0.0.1:$servicePort"
    if ($metadata.url -ne $serviceUrl) { throw 'The recorded service URL is invalid.' }
    $health = Invoke-RestMethod -Uri "$serviceUrl/api/health" -TimeoutSec 3 -UseBasicParsing
    if ($health.application -ne 'pct-daily-dossiers' -or $health.protocol_version -ne 1 -or $health.instance_id -ne $metadata.instance_id -or $health.repository_id -ne $repositoryHash -or -not $health.ready) { throw 'The running service identity could not be verified. No shutdown was attempted.' }
    $bootstrap = Invoke-RestMethod -Uri "$serviceUrl/api/bootstrap" -TimeoutSec 3 -UseBasicParsing
    if ($bootstrap.instance_id -ne $metadata.instance_id -or -not $bootstrap.nonce) { throw 'The service ownership token could not be verified.' }
    $headers = @{ 'Origin' = $serviceUrl; 'X-PCT-Nonce' = $bootstrap.nonce }
    $body = @{ instance_id = $metadata.instance_id } | ConvertTo-Json -Compress
    $null = Invoke-RestMethod -Method Post -Uri "$serviceUrl/api/shutdown" -Headers $headers -ContentType 'application/json' -Body $body -TimeoutSec 8 -UseBasicParsing
    $deadline = [DateTime]::UtcNow.AddSeconds(12)
    while ([DateTime]::UtcNow -lt $deadline) {
        if (-not (Test-Path -LiteralPath $metadataPath -PathType Leaf)) { Write-Host 'The local hike service closed. Your repository history is preserved.'; exit 0 }
        Start-Sleep -Milliseconds 250
    }
    throw 'The service accepted shutdown but has not confirmed closure yet. Preserve the data directory and check again; no process was killed.'
}
catch { Write-Host $_.Exception.Message -ForegroundColor Red; exit 1 }
