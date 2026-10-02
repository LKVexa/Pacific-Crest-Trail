[CmdletBinding()]
param(
    [ValidateRange(0, 65535)][int]$Port = 0,
    [string]$Python = '',
    [switch]$NoBrowser,
    [switch]$Status,
    [switch]$NoPause,
    [ValidateRange(3, 180)][int]$BrowserTimeoutSeconds = 120
)

$ErrorActionPreference = 'Stop'
$projectRoot = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$dataDirectory = Join-Path $projectRoot 'data'
$metadataPath = Join-Path $dataDirectory 'service.json'
$launchId = [guid]::NewGuid().ToString()
$ownedMutex = $null
$mutexAcquired = $false
$launchRecorded = $false
$finalExit = 0
$repositoryHash = ''

function Write-LaunchRecord([string]$Phase, [string]$Message = '') {
    $entry = [ordered]@{
        launch_id = $launchId
        at_utc = [DateTimeOffset]::UtcNow.ToString('o')
        at_local = [DateTimeOffset]::Now.ToString('o')
        phase = $Phase
        message = $Message
    }
    $line = ($entry | ConvertTo-Json -Compress) + [Environment]::NewLine
    [System.IO.File]::AppendAllText((Join-Path $dataDirectory 'launcher.jsonl'), $line, [System.Text.UTF8Encoding]::new($false))
}

function Get-VerifiedService {
    if (-not (Test-Path -LiteralPath $metadataPath -PathType Leaf)) { return $null }
    try {
        $metadata = Get-Content -LiteralPath $metadataPath -Raw | ConvertFrom-Json
        if ($metadata.application -ne 'pct-daily-dossiers' -or $metadata.protocol_version -ne 1 -or $metadata.repository_id -ne $repositoryHash) { return $null }
        $servicePort = [int]$metadata.port
        if ($servicePort -lt 1 -or $servicePort -gt 65535) { return $null }
        $serviceUrl = "http://127.0.0.1:$servicePort"
        if ($metadata.url -ne $serviceUrl) { return $null }
        $health = Invoke-RestMethod -Uri "$serviceUrl/api/health" -TimeoutSec 2 -UseBasicParsing
        if ($health.application -ne 'pct-daily-dossiers' -or $health.protocol_version -ne 1 -or $health.instance_id -ne $metadata.instance_id -or $health.repository_id -ne $repositoryHash -or $health.port -ne $servicePort -or -not $health.ready) { return $null }
        $bootstrap = Invoke-RestMethod -Uri "$serviceUrl/api/bootstrap" -TimeoutSec 3 -UseBasicParsing
        if ($bootstrap.instance_id -ne $metadata.instance_id -or -not $bootstrap.nonce) { return $null }
        return [pscustomobject]@{ Url = $serviceUrl; Metadata = $metadata; Bootstrap = $bootstrap }
    }
    catch { return $null }
}

function Get-PythonExecutable([string]$ConfiguredPython) {
    $choices = @($Python, $env:PCT_PYTHON, $ConfiguredPython)
    $pythonCommand = Get-Command python.exe -ErrorAction SilentlyContinue
    if ($pythonCommand) { $choices += $pythonCommand.Source }
    $choices += (Join-Path $env:USERPROFILE '.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe')
    foreach ($choice in $choices) {
        if (-not $choice) { continue }
        $candidate = [string]$choice
        if (-not [System.IO.Path]::IsPathRooted($candidate)) {
            $found = Get-Command $candidate -CommandType Application -ErrorAction SilentlyContinue
            if ($found) { $candidate = $found.Source }
            else { $candidate = Join-Path $projectRoot $candidate }
        }
        if (-not (Test-Path -LiteralPath $candidate -PathType Leaf)) { continue }
        try {
            $check = & $candidate -c 'import sys,sqlite3; raise SystemExit(0 if sys.version_info >= (3, 9) else 2)' 2>$null
            if ($LASTEXITCODE -eq 0) { return [System.IO.Path]::GetFullPath($candidate) }
        }
        catch { continue }
    }
    throw 'Python 3.9 or newer with sqlite3 is required. Set PCT_PYTHON, use -Python, or set config/local.json python_executable to its executable path.'
}

function Quote-ProcessArgument([string]$Value) {
    # Windows paths cannot contain quotes; all path arguments here are resolved files.
    if ($Value.Contains('"')) { throw 'A process argument contains an unsupported quote.' }
    return '"' + $Value + '"'
}

function Get-HouseBootStage([string]$BootLog, [DateTimeOffset]$StartedAt) {
    try {
        if (-not (Test-Path -LiteralPath $BootLog -PathType Leaf)) { return $null }
        $lines = @(Get-Content -LiteralPath $BootLog -Tail 8)
        for ($index = $lines.Count - 1; $index -ge 0; $index--) {
            $parts = $lines[$index] -split "`t", 3
            if ($parts.Count -lt 2) { continue }
            try { $stamp = [DateTimeOffset]::Parse($parts[0], [Globalization.CultureInfo]::InvariantCulture) }
            catch { continue }
            if ($stamp -ge $StartedAt) { return [string]$parts[1] }
        }
    } catch { }
    return $null
}

function Get-HouseStartupStatus([string]$StatusPath, [string]$ExpectedLaunchId, [int]$ExpectedProcessId, [DateTimeOffset]$StartedAt) {
    try {
        if (-not $StatusPath -or -not $ExpectedLaunchId -or -not (Test-Path -LiteralPath $StatusPath -PathType Leaf)) { return $null }
        if ((Get-Item -LiteralPath $StatusPath).Length -gt 65536) { return $null }
        $record = Get-Content -LiteralPath $StatusPath -Raw -Encoding UTF8 | ConvertFrom-Json
        if (($record.version -isnot [int] -and $record.version -isnot [long]) -or ($record.process_id -isnot [int] -and $record.process_id -isnot [long]) -or $record.launch_id -isnot [string]) { return $null }
        if ($record.version -ne 1 -or $record.launch_id -cne $ExpectedLaunchId -or $record.process_id -ne $ExpectedProcessId -or $record.stage -notin @('window-visible', 'dossier-ready', 'failed')) { return $null }
        # Newer PowerShell versions deserialize ISO JSON dates automatically;
        # Windows PowerShell retains the same timestamp as a string.
        if ($record.at_utc -is [DateTimeOffset]) { $stamp = $record.at_utc }
        elseif ($record.at_utc -is [DateTime]) { $stamp = [DateTimeOffset]::new($record.at_utc) }
        elseif ($record.at_utc -is [string]) { $stamp = [DateTimeOffset]::Parse($record.at_utc, [Globalization.CultureInfo]::InvariantCulture) }
        else { return $null }
        if ($stamp -lt $StartedAt) { return $null }
        return [string]$record.stage
    } catch { return $null }
}

function Wait-HouseBrowserWindow([object]$Process, [string]$BootLog, [DateTimeOffset]$StartedAt, [int]$TimeoutSeconds, [string]$StatusPath = '', [string]$ExpectedLaunchId = '') {
    $deadline = $StartedAt.AddSeconds($TimeoutSeconds)
    $lastStage = ''
    $nextProgress = $StartedAt.AddSeconds(5)
    while ([DateTimeOffset]::UtcNow -lt $deadline) {
        $Process.Refresh()
        if ($Process.HasExited) { throw "The house browser exited before its dossier window was confirmed (exit $($Process.ExitCode)). See browser\workspace\logs\boot-latest.log." }
        $confirmedStage = Get-HouseStartupStatus $StatusPath $ExpectedLaunchId $Process.Id $StartedAt
        if ($confirmedStage -eq 'failed') { throw 'The house browser reported a dossier startup failure. See its launch status and browser\workspace\logs\boot-latest.log.' }
        if ($confirmedStage -in @('window-visible', 'dossier-ready')) { return $true }
        $windowHandle = [IntPtr]$Process.MainWindowHandle
        if ($windowHandle.ToInt64() -ne 0 -and $Process.MainWindowTitle -eq 'Trail Dossier') { return $true }
        $stage = Get-HouseBootStage $BootLog $StartedAt
        if ($stage -and $stage -ne $lastStage) {
            $lastStage = $stage
            if ($stage -eq 'FAILED') { throw 'The house browser reported a startup failure. See browser\workspace\logs\boot-latest.log.' }
            Write-LaunchRecord 'presentation-stage' $stage
            $copy = switch ($stage) {
                'live-web-provision-begin' { 'Loading the house browser renderer.' }
                'presenter-cache-hit' { 'Using the saved house browser build.' }
                'presenter-cache-miss' { 'Preparing the house browser build for this installation.' }
                'presenter-compile-begin' { 'Building the house browser; the first launch can take longer.' }
                'presenter-compile-complete' { 'The house browser build is ready.' }
                'presenter-run-begin' { 'Opening the house browser window.' }
                default { 'Preparing the house browser.' }
            }
            Write-Host $copy
        }
        if ([DateTimeOffset]::UtcNow -ge $nextProgress) {
            Write-Host 'Waiting for the house browser window. Your saved hike is ready.'
            $nextProgress = [DateTimeOffset]::UtcNow.AddSeconds(5)
        }
        Start-Sleep -Milliseconds 200
    }
    throw "The house browser window was not confirmed within $TimeoutSeconds seconds. It may still be building. See browser\workspace\logs\boot-latest.log; the local service and saved hike are preserved."
}

try {
    if (-not (Test-Path -LiteralPath $dataDirectory -PathType Container)) {
        New-Item -ItemType Directory -Path $dataDirectory | Out-Null
    }
    $canonicalRoot = $projectRoot.ToLowerInvariant()
    $hasher = [System.Security.Cryptography.SHA256]::Create()
    try { $repositoryHash = ([BitConverter]::ToString($hasher.ComputeHash([Text.Encoding]::UTF8.GetBytes($canonicalRoot)))).Replace('-', '').ToLowerInvariant() }
    finally { $hasher.Dispose() }
    $ownedMutex = [System.Threading.Mutex]::new($false, "Local\PCTDailyDossiers_$repositoryHash")
    try { $mutexAcquired = $ownedMutex.WaitOne([TimeSpan]::FromSeconds(25)) }
    catch [System.Threading.AbandonedMutexException] { $mutexAcquired = $true }
    if (-not $mutexAcquired) { throw 'Another launcher is still preparing this repository. Wait for it to finish, then relaunch.' }
    if (-not $Status) { Write-LaunchRecord 'started'; $launchRecorded = $true }

    $configPath = Join-Path $projectRoot 'config\defaults.json'
    $config = Get-Content -LiteralPath $configPath -Raw | ConvertFrom-Json
    if ($config.schema_version -ne 1) { throw 'The configuration schema is unsupported.' }
    $localConfigPath = Join-Path $projectRoot 'config\local.json'
    if (Test-Path -LiteralPath $localConfigPath -PathType Leaf) {
        $overrides = Get-Content -LiteralPath $localConfigPath -Raw | ConvertFrom-Json
        foreach ($property in $overrides.PSObject.Properties) {
            if ($property.Name -notin @('schema_version', 'port', 'python_executable', 'startup_timeout_seconds', 'open_browser')) { throw "Unknown local configuration property: $($property.Name)" }
            $config | Add-Member -NotePropertyName $property.Name -NotePropertyValue $property.Value -Force
        }
    }
    $portIsInteger = ($config.port -is [int]) -or ($config.port -is [long])
    $timeoutIsInteger = ($config.startup_timeout_seconds -is [int]) -or ($config.startup_timeout_seconds -is [long])
    if ($config.schema_version -ne 1 -or -not $portIsInteger -or $config.port -lt 1 -or $config.port -gt 65535 -or -not $timeoutIsInteger -or $config.startup_timeout_seconds -lt 3 -or $config.startup_timeout_seconds -gt 60 -or $config.open_browser -isnot [bool]) { throw 'The local configuration has an invalid port, timeout, browser setting, or schema version.' }
    $selectedPort = if ($Port -eq 0) { [int]$config.port } else { $Port }
    $service = Get-VerifiedService
    if ($Status) {
        if ($service) {
            Write-Host "Local hike is running at $($service.Url)"
            Write-Host "Completed sections: $($service.Bootstrap.completed_day_ids.Count) / $($service.Bootstrap.total_days)"
        }
        else { Write-Host 'No verified local hike service is running.'; $finalExit = 1 }
    }
    else {
        if ($service) {
            if ($Port -ne 0 -and $selectedPort -ne $service.Metadata.port) { throw "This repository already runs on port $($service.Metadata.port). Use its existing instance or stop it before selecting another port." }
            $headers = @{ 'Origin' = $service.Url; 'X-PCT-Nonce' = $service.Bootstrap.nonce }
            $body = @{ launch_id = $launchId } | ConvertTo-Json -Compress
            $null = Invoke-RestMethod -Method Post -Uri "$($service.Url)/api/launch" -Headers $headers -ContentType 'application/json' -Body $body -TimeoutSec 8 -UseBasicParsing
            Write-LaunchRecord 'reused' 'Verified existing repository instance.'
        }
        else {
            $pythonExecutable = Get-PythonExecutable ([string]$config.python_executable)
            $serverScript = Join-Path $projectRoot 'app\server.py'
            if (-not (Test-Path -LiteralPath $serverScript -PathType Leaf) -or -not (Test-Path -LiteralPath (Join-Path $projectRoot 'content\itinerary.json') -PathType Leaf)) { throw 'The application or published itinerary is missing. Restore these files before launching.' }
            $probePath = Join-Path $dataDirectory "probe-$launchId.tmp"
            [System.IO.File]::WriteAllText($probePath, 'write-check')
            Remove-Item -LiteralPath $probePath
            $instanceId = [guid]::NewGuid().ToString()
            $arguments = @((Quote-ProcessArgument $serverScript), '--root', (Quote-ProcessArgument $projectRoot), '--port', [string]$selectedPort, '--instance-id', $instanceId, '--launch-id', $launchId)
            $stdoutPath = Join-Path $dataDirectory "service-$instanceId.stdout.log"
            $stderrPath = Join-Path $dataDirectory "service-$instanceId.stderr.log"
            $process = Start-Process -FilePath $pythonExecutable -ArgumentList $arguments -WorkingDirectory $projectRoot -WindowStyle Hidden -RedirectStandardOutput $stdoutPath -RedirectStandardError $stderrPath -PassThru
            $deadline = [DateTime]::UtcNow.AddSeconds([int]$config.startup_timeout_seconds)
            while ([DateTime]::UtcNow -lt $deadline) {
                $service = Get-VerifiedService
                if ($service -and $service.Metadata.instance_id -eq $instanceId) { break }
                $process.Refresh()
                if ($process.HasExited) {
                    $detail = if (Test-Path -LiteralPath $stderrPath) { (Get-Content -LiteralPath $stderrPath -Raw).Trim() } else { 'No startup diagnostic was written.' }
                    throw "The local service could not start. $detail"
                }
                Start-Sleep -Milliseconds 250
            }
            if (-not $service -or $service.Metadata.instance_id -ne $instanceId) { throw 'The local service did not reach verified readiness before the startup timeout. Review data/service-*.stderr.log and use Stop-Hike.ps1 for a verified instance; no process was killed.' }
            Write-LaunchRecord 'ready' 'New repository instance reached verified readiness.'
        }
        Write-Host "Your daily trail dossier: $($service.Url)"
        if ($service.Bootstrap.expedition_complete) { Write-Host 'All virtual daily sections are complete. Your history remains available.' }
        else { Write-Host "Resuming virtual day $($service.Bootstrap.current_day_number) of $($service.Bootstrap.total_days)." }
        Write-Host 'Opening or reopening the application never completes a section or records exercise.'
        if (-not $NoBrowser -and $config.open_browser) {
            $browserRoot = Join-Path $projectRoot 'browser'
            $browserHost = Join-Path $browserRoot 'host\Start-JA21Browser.ps1'
            if (-not (Test-Path -LiteralPath $browserHost -PathType Leaf)) { throw 'The house browser launcher is missing. Restore browser\host\Start-JA21Browser.ps1, or use -NoBrowser to start only the saved local hike.' }
            if ($service.Metadata.port -ne 8765) { throw 'The house browser uses port 8765. Stop this owned service before returning to that port, or use -NoBrowser to keep this service without opening a window.' }
            Write-Host 'Starting the house browser. This console stays visible until its window appears.'
            Write-Host 'Startup details: browser\workspace\logs\boot-latest.log'
            Write-LaunchRecord 'presentation-requested' 'Requested the copied house browser dossier window.'
            $presentationStartedAt = [DateTimeOffset]::UtcNow
            # Preserve the copied house browser's existing hosting policy.
            # Machine policy and the original browser are never changed here.
            $presentationStart = [Diagnostics.ProcessStartInfo]::new()
            $presentationStart.FileName = Join-Path $env:SystemRoot 'System32\WindowsPowerShell\v1.0\powershell.exe'
            $presentationStart.Arguments = '-NoLogo -NoProfile -STA -ExecutionPolicy Bypass -File "' + $browserHost + '" -Root "' + $browserRoot + '" -Mode TrailDossier'
            $presentationStart.WorkingDirectory = $browserRoot
            $presentationStart.UseShellExecute = $false
            $presentationStart.CreateNoWindow = $true
            $presentationStart.WindowStyle = [Diagnostics.ProcessWindowStyle]::Hidden
            $presentationStart.EnvironmentVariables['JA21_PORTABLE_ROOT'] = Join-Path $browserRoot 'workspace'
            $startupStatusPath = Join-Path $browserRoot "workspace\logs\launch-$launchId.json"
            $presentationStart.EnvironmentVariables['JA21_DOSSIER_STARTUP_STATUS'] = $startupStatusPath
            $presentationStart.EnvironmentVariables['JA21_DOSSIER_LAUNCH_ID'] = $launchId
            $presentationProcess = [Diagnostics.Process]::Start($presentationStart)
            if ($null -eq $presentationProcess) { throw 'The house browser process could not be started.' }
            $bootLog = Join-Path $browserRoot 'workspace\logs\boot-latest.log'
            $null = Wait-HouseBrowserWindow $presentationProcess $bootLog $presentationStartedAt $BrowserTimeoutSeconds $startupStatusPath $launchId
            Write-LaunchRecord 'presentation-visible' 'Confirmed the owned house browser dossier window.'
            Write-Host 'The house browser window is open. The dossier may still be loading.'
        }
    }
}
catch {
    $finalExit = 1
    $failureMessage = $_.Exception.Message
    if ($launchRecorded) {
        try { Write-LaunchRecord 'failed' $failureMessage } catch { }
    }
    Write-Host $failureMessage -ForegroundColor Red
    Write-Host 'Launch details: data\launcher.jsonl' -ForegroundColor Yellow
}
finally {
    if ($mutexAcquired -and $ownedMutex) { $ownedMutex.ReleaseMutex() }
    if ($ownedMutex) { $ownedMutex.Dispose() }
}
exit $finalExit
