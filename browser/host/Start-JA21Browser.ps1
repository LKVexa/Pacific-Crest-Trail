param([string]$Root, [string]$StartUrl, [ValidateSet('TrailDossier','GeneralBrowser')][string]$Mode = 'TrailDossier', [switch]$CompileOnly)
if ($Mode -eq 'TrailDossier') {
    if ($StartUrl -and $StartUrl -cne 'http://127.0.0.1:8765/') { throw 'Trail Dossier uses the fixed address http://127.0.0.1:8765/. Use -Mode GeneralBrowser for general navigation.' }
    $env:JA21_DOSSIER_MODE = '1'
    $env:JA21_START_URL = 'http://127.0.0.1:8765/'
} else {
    $env:JA21_DOSSIER_MODE = '0'
    if ($StartUrl) { $env:JA21_START_URL = $StartUrl }
}
$ErrorActionPreference = 'Stop'

function Resolve-JA21PackageRoot {
    param([string]$Candidate)
    if ([string]::IsNullOrWhiteSpace($Candidate)) { $Candidate = Split-Path -Parent $PSScriptRoot }
    $Candidate = [Environment]::ExpandEnvironmentVariables($Candidate.Trim())
    while ($Candidate.Length -gt 0 -and ($Candidate[0] -eq [char]34 -or $Candidate[0] -eq [char]39)) { $Candidate = $Candidate.Substring(1) }
    while ($Candidate.Length -gt 0 -and ($Candidate[$Candidate.Length - 1] -eq [char]34 -or $Candidate[$Candidate.Length - 1] -eq [char]39)) { $Candidate = $Candidate.Substring(0, $Candidate.Length - 1) }
    if ([string]::IsNullOrWhiteSpace($Candidate)) { throw 'JA21 package root resolved to an empty path.' }
    try { $Full = [IO.Path]::GetFullPath($Candidate) } catch { throw "Invalid JA21 package root '$Candidate': $($_.Exception.Message)" }
    if (!(Test-Path -LiteralPath $Full -PathType Container)) { throw "JA21 package root does not exist: $Full" }
    return $Full
}

$Root = Resolve-JA21PackageRoot -Candidate $Root

# JA21 9.8.7 portable desktop contract. All JA21-owned mutable state is rooted beside
# the application, never under the user's real AppData tree. The .cmd launcher sets
# these before PowerShell starts; these assignments are a second fail-safe for direct .ps1 use.
$PortableRoot = if ([string]::IsNullOrWhiteSpace($env:JA21_PORTABLE_ROOT)) { Join-Path $Root 'workspace' } else { [IO.Path]::GetFullPath($env:JA21_PORTABLE_ROOT) }
$env:JA21_PORTABLE_ROOT = $PortableRoot
$portableDirs = @('state','state\webview2','state\vec1','desktop','documents','downloads','uploads','logs','temp','cache','home','host-env\LocalAppData','host-env\RoamingAppData','runtime','evidence','snapshots')
foreach($rel in $portableDirs){ New-Item -ItemType Directory -Force -Path (Join-Path $PortableRoot $rel) | Out-Null }
$env:JA21_WEB_DATA_ROOT = Join-Path $PortableRoot 'state\webview2'
$env:JA21_VEC1_STATE_ROOT = Join-Path $PortableRoot 'state\vec1'
$env:JA21_DOWNLOADS_ROOT = Join-Path $PortableRoot 'downloads'
$env:JA21_TEMP_ROOT = Join-Path $PortableRoot 'temp'
$env:LOCALAPPDATA = Join-Path $PortableRoot 'host-env\LocalAppData'
$env:APPDATA = Join-Path $PortableRoot 'host-env\RoamingAppData'
$env:TEMP = Join-Path $PortableRoot 'temp'
$env:TMP = Join-Path $PortableRoot 'temp'
$env:HOME = Join-Path $PortableRoot 'home'
$env:PYTHONPYCACHEPREFIX = Join-Path $PortableRoot 'cache\pycache'
$env:PYTHONDONTWRITEBYTECODE = '1'

# 9.8.7 boot observability: every startup reaches a durable stage marker before dynamic
# C# compilation.  If Windows PowerShell terminates or Add-Type fails, the operator can
# distinguish setup, live-web binding, compilation and presenter-start failures without
# depending on the console window remaining alive.
$BootLog = Join-Path $PortableRoot 'logs\boot-latest.log'
$BootClock = [Diagnostics.Stopwatch]::StartNew()
$LastBootStageMilliseconds = 0
function Write-JA21BootStage {
    param([string]$Stage, [string]$Detail = '')
    $stamp = [DateTime]::UtcNow.ToString('o')
    $elapsed = $BootClock.ElapsedMilliseconds
    $duration = $elapsed - $script:LastBootStageMilliseconds
    $script:LastBootStageMilliseconds = $elapsed
    $line = "$stamp`t$Stage`telapsed_ms=$elapsed; previous_stage_ms=$duration" + $(if ($Detail) { "`t$Detail" } else { '' })
    try { Add-Content -LiteralPath $BootLog -Value $line -Encoding UTF8 } catch { }
    Write-Host ("JA21 boot · " + $Stage + $(if($Detail){" · "+$Detail}else{""}))
}
try { Set-Content -LiteralPath $BootLog -Value ("JA21 Portable Desktop 9.8.7 boot log`r`nRoot: " + $Root + "`r`nWorkspace: " + $PortableRoot) -Encoding UTF8 } catch { }
trap {
    $detail = ($_ | Out-String).Trim()
    try { Add-Content -LiteralPath $BootLog -Value (([DateTime]::UtcNow.ToString('o')) + "`tFAILED`t" + $detail) -Encoding UTF8 } catch { }
    Write-Host ''
    Write-Host 'JA21 boot failed.' -ForegroundColor Red
    Write-Host $detail -ForegroundColor Red
    Write-Host ("Boot log: " + $BootLog) -ForegroundColor Yellow
    exit 1
}
Write-JA21BootStage 'portable-layout-ready'
$source = Join-Path $Root 'host\JA21VirtualBrowser.cs'
$substrateSource = Join-Path $Root 'host\Vec1Substrate.cs'
$portableDesktop = Join-Path $Root 'host\PortableDesktop.cs'
$liveContracts = Join-Path $Root 'host\LiveWebContracts.cs'
$liveBridge = Join-Path $Root 'host\LiveWebBridge.cs'
$liveStub = Join-Path $Root 'host\LiveWebBridgeStub.cs'
$dossierSource = Join-Path $Root 'host\TrailDossierHost.cs'
$liveProvisioner = Join-Path $Root 'host\Ensure-WebView2Bridge.ps1'
$liveLoader = Join-Path $Root 'host\Import-WebView2Adapter.ps1'
$ir = Join-Path $Root 'engine\ja21\browser.ir.json'
$rendererIr = Join-Path $Root 'engine\ja21\renderer.ir.json'
$rendererSource = Join-Path $Root 'source\renderer.ja'
$webSource = Join-Path $Root 'source\web_engine.ja'
$webIr = Join-Path $Root 'engine\ja21\web_engine.ir.json'
$seal = Join-Path $Root 'engine\ja21\runtime.integrity.json'
$helper = Join-Path $Root 'helper\DF_Small\node\NODE_DESCRIPTOR.json'
$dfMediumDll = Join-Path $Root 'engine\df_medium\native\win-x64\dfmedium-ja21-web.dll'
$dfMediumProv = Join-Path $Root 'engine\df_medium\ENGINE_PROVENANCE.json'
foreach($p in @($source,$substrateSource,$portableDesktop,$liveContracts,$liveBridge,$liveStub,$dossierSource,$liveProvisioner,$liveLoader,$ir,$rendererIr,$rendererSource,$webSource,$webIr,$seal,$helper,$dfMediumDll,$dfMediumProv)){ if (!(Test-Path -LiteralPath $p -PathType Leaf)) { throw "Required JA21 runtime file missing: $p" } }

# WPF shell plus optional explicit WebView2 live-web adapter. Native DF_Medium remains the fallback.
$refResolver = Join-Path $PSScriptRoot 'Wpf-CompileReferences.ps1'
if (!(Test-Path -LiteralPath $refResolver -PathType Leaf)) { throw "WPF compile-reference resolver is missing: $refResolver" }
. $refResolver
Write-JA21BootStage 'framework-references-begin'
$refs = Get-JA21WpfCompileReferences
Write-JA21BootStage 'framework-references-complete'
Write-JA21BootStage 'live-web-provision-begin'
$live = & $liveProvisioner -Root $Root -Quiet
$bridgeSource = $liveStub
$liveLoaded = $null
if($live.Ready){
    $liveLoaded = & $liveLoader -Adapter $live -Quiet
    if($liveLoaded.Ready){
        # Compiler references are still explicit, but the managed DLLs have already been loaded
        # into this AppDomain so Program.Run cannot fail later on a strong-name resolution miss.
        $bridgeSource = $liveBridge
        $refs = @($refs) + @($live.Core,$live.Wpf)
        if($liveLoaded.RuntimeReady){
            Write-Host ("Live web: WebView2 adapter " + $live.Version + " loaded; runtime " + $liveLoaded.RuntimeVersion) -ForegroundColor Green
        } else {
            Write-Warning ("Live web managed adapter loaded, but the Evergreen runtime was not detected; JA21 will open with Native DF_Medium fallback. " + $liveLoaded.RuntimeError)
        }
    } else {
        Write-Warning ("Live web managed adapter could not be loaded; JA21 will open with Native DF_Medium fallback. " + $liveLoaded.Error)
    }
} else { Write-Warning 'Live web adapter could not be provisioned; starting sealed Native DF_Medium mode.' }
Write-JA21BootStage 'live-web-provision-complete' ($(if($live.Ready){'adapter-ready'}else{'native-fallback'}))

# The presenter is two C# compilation units in one namespace: the omni-bin window and the
# VEC1 electron substrate. Add-Type accepts a single -TypeDefinition string, and C# requires
# every using directive to precede the first namespace block in that string. Concatenating
# the files verbatim therefore fails with CS1529 on the second file's usings, so they are
# hoisted here: usings are collected (de-duplicated, first-seen order), everything else is
# appended in a fixed order, and the result is one valid compilation unit.
function Join-JA21CompilationUnits {
    param([string[]]$Sources)
    $usings = New-Object System.Collections.Generic.List[string]
    $bodies = New-Object System.Collections.Generic.List[string]
    foreach ($src in $Sources) {
        $body = New-Object System.Text.StringBuilder
        foreach ($line in ($src -split "`r?`n")) {
            # A using DIRECTIVE only: 'using X;' / 'using X = Y;' / 'using static X;'.
            # A using STATEMENT ('using (var x = ...)') starts with a parenthesis and is left alone.
            if ($line -match '^\s*using\s+(static\s+)?[A-Za-z_@][^();{}]*;\s*$') {
                $u = $line.Trim()
                if (-not $usings.Contains($u)) { [void]$usings.Add($u) }
            } else {
                [void]$body.AppendLine($line)
            }
        }
        [void]$bodies.Add($body.ToString())
    }
    if ($usings.Count -lt 1) { throw 'No using directives were found in the presenter sources; refusing to compile a suspect unit.' }
    return (($usings -join [Environment]::NewLine) + [Environment]::NewLine + [Environment]::NewLine + ($bodies -join [Environment]::NewLine))
}

$code = Join-JA21CompilationUnits @(
    (Get-Content -LiteralPath $source -Raw -Encoding UTF8),
    (Get-Content -LiteralPath $substrateSource -Raw -Encoding UTF8),
    (Get-Content -LiteralPath $portableDesktop -Raw -Encoding UTF8),
    (Get-Content -LiteralPath $liveContracts -Raw -Encoding UTF8),
    (Get-Content -LiteralPath $dossierSource -Raw -Encoding UTF8),
    (Get-Content -LiteralPath $bridgeSource -Raw -Encoding UTF8)
)
$cacheHelper = Join-Path $PSScriptRoot 'Presenter-Cache.ps1'
if (!(Test-Path -LiteralPath $cacheHelper -PathType Leaf)) { throw 'Presenter cache helper is missing.' }
. $cacheHelper
Write-JA21BootStage 'presenter-cache-check-begin'
$presenter = Import-JA21Presenter -Code $code -References $refs -CacheRoot (Join-Path $PortableRoot 'cache\presenter')
if ($CompileOnly) {
    Write-JA21BootStage 'compile-only-complete' ($(if ($presenter.CacheHit) { 'cache hit' } else { 'cache built' }))
    return
}
Write-JA21BootStage 'presenter-run-begin'
[VBJA21.Program]::Run($Root)
Write-JA21BootStage 'presenter-run-exit'
